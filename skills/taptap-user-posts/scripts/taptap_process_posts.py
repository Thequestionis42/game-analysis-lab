import argparse
import csv
import html
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Asia/Shanghai")


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def clean_text(value: str) -> str:
    if not value:
        return ""
    value = value.replace("\r\n", "\n").replace("\r", "\n").replace("\u2028", "\n")
    value = re.sub(r"[ \t]+\n", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def clean_bbcode(value: str) -> str:
    if not value:
        return ""
    value = re.sub(r"\[img\].*?\[/img\]", "", value, flags=re.I | re.S)
    value = re.sub(r"\[(?:/)?(?:b|i|u|url|size|color)[^\]]*\]", "", value, flags=re.I)
    value = re.sub(r"\[[^\]]+\]", "", value)
    return clean_text(value)


def local_dt(ts):
    if not ts:
        return ""
    return datetime.fromtimestamp(int(ts), tz=timezone.utc).astimezone(TZ)


def parse_title_update_date(title: str, published: datetime):
    match = re.search(r"(\d{1,2})月(\d{1,2})日", title or "")
    if not match or not published:
        return ""
    month, day = int(match.group(1)), int(match.group(2))
    year = published.year
    if published.month == 12 and month == 1:
        year += 1
    elif published.month == 1 and month == 12:
        year -= 1
    try:
        return datetime(year, month, day, tzinfo=TZ).date().isoformat()
    except ValueError:
        return ""


def classify(title: str, text: str, labels: list[str]) -> str:
    joined = f"{title}\n{text}"
    if re.search(r"\d{1,2}月\d{1,2}日更新公告|更新公告", title):
        return "正式更新公告"
    if re.search(r"维护公告|维护结束|停服|闪断|服务器.*互通|数据互通|社交互通|跨服|延时开服|延长|开服公告", joined):
        return "维护/服务器"
    if re.search(r"已知问题|异常问题|异常|修复|补发|补偿|解决办法", joined):
        return "问题/修复/补偿"
    if re.search(r"活动|预览|计划|礼包|周边|测试|招募|返利|福利|小贴士|抽奖|征集|赛事", joined):
        return "活动/运营"
    if any(label in ("游戏公告", "官方") for label in labels):
        return "其他公告"
    return "其他"


def maintenance_mode(text: str) -> str:
    if "不停服" in text:
        return "不停服更新"
    if "停服维护" in text or "维护期间" in text or "无法进入游戏" in text:
        return "停服维护"
    if "闪断" in text:
        return "闪断维护"
    if "维护" in text:
        return "维护"
    return ""


def extract_time_window(text: str) -> str:
    patterns = [
        r"预计在(.{0,28}?\d{1,2}:\d{2}\s*[-—至~]\s*\d{1,2}:\d{2})",
        r"(\d{1,2}月\d{1,2}日\d{1,2}:\d{2}\s*[-—至~]\s*\d{1,2}:\d{2})",
        r"(\d{1,2}:\d{2}\s*[-—至~]\s*\d{1,2}:\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return clean_text(match.group(1))
    return ""


SECTION_PATTERNS = {
    "新增": re.compile(r"新增|全新|上线"),
    "优化": re.compile(r"优化|调整|改善"),
    "修复": re.compile(r"修复|异常|问题"),
    "活动": re.compile(r"活动|任务|奖励|礼包|签到|大卖场|宝藏湖|纸杯蛋糕|忆战回环|塔莎"),
    "系统/玩法": re.compile(r"玩法|系统|服务器|社交互通|数据互通|跨服|旅团|秘境|职业|技能|麦乐兽|骑兽|时装|坐骑"),
}


def extract_highlights(text: str, limit: int = 10) -> list[str]:
    lines = []
    for raw in clean_text(text).split("\n"):
        line = raw.strip(" \t-•　")
        line = re.sub(r"^\d+[\.、]\s*", "", line)
        if not line or len(line) <= 4:
            continue
        is_heading = bool(re.match(r"^【[^】]{2,20}】$", line)) or line in {"新增内容", "优化内容", "异常修复", "修复内容", "调整内容"}
        is_item = bool(re.match(r"^【[^】]+】", line)) or any(p.search(line) for p in SECTION_PATTERNS.values())
        if is_heading or is_item:
            lines.append(re.sub(r"\s+", " ", line))
    deduped = []
    seen = set()
    for line in lines:
        if line not in seen:
            deduped.append(line)
            seen.add(line)
        if len(deduped) >= limit:
            break
    return deduped


def section_tags(text: str) -> str:
    tags = [name for name, pattern in SECTION_PATTERNS.items() if pattern.search(text)]
    return "、".join(tags)


def load_details(details_dir: Path):
    details = {}
    if not details_dir.exists():
        return details
    for path in details_dir.glob("*.json"):
        payload = load_json(path)
        moment = payload.get("data", {}).get("moment")
        if moment:
            details[moment["id_str"]] = moment
    return details


def load_topic_details(topic_details_dir: Path):
    by_moment_id = {}
    by_topic_id = {}
    if not topic_details_dir.exists():
        return by_moment_id, by_topic_id
    for path in topic_details_dir.glob("*.json"):
        payload = load_json(path)
        data = payload.get("data", {})
        moment = data.get("moment") or {}
        topic = data.get("topic") or {}
        first_post = data.get("first_post") or {}
        contents = first_post.get("contents") or {}
        full_text = clean_bbcode(contents.get("raw_text") or "") or clean_bbcode(contents.get("text") or "")
        if not full_text:
            continue
        moment_id = moment.get("id_str")
        topic_id = topic.get("id_str") or topic.get("id")
        if moment_id:
            by_moment_id[moment_id] = full_text
        if topic_id:
            by_topic_id[topic_id] = full_text
    return by_moment_id, by_topic_id


def get_moment(item, details):
    moment = item["moment"]
    return details.get(moment["id_str"], moment)


def topic_full_text(topic_obj, moment_id, topic_text_by_moment, topic_text_by_topic):
    if moment_id and moment_id in topic_text_by_moment:
        return topic_text_by_moment[moment_id]
    topic_id = (topic_obj or {}).get("id_str") or (topic_obj or {}).get("id")
    if topic_id and topic_id in topic_text_by_topic:
        return topic_text_by_topic[topic_id]
    return ""


def normalize_item(item, details, topic_text_by_moment, topic_text_by_topic):
    moment = get_moment(item, details)
    source_moment = item["moment"]
    topic = moment.get("topic") or {}
    reposted = moment.get("reposted_moment") or {}
    reposted_topic = reposted.get("topic") or {}
    sharing = moment.get("sharing") or {}
    stat = moment.get("stat") or {}
    author = (moment.get("author") or {}).get("user") or (moment.get("author") or {}).get("app") or {}
    labels = [label.get("name", "") for label in moment.get("labels", []) if label.get("name")]

    title = clean_text(topic.get("title") or sharing.get("title") or reposted_topic.get("title") or "")
    summary = topic_full_text(topic, moment["id_str"], topic_text_by_moment, topic_text_by_topic)
    if not summary:
        summary = clean_text(topic.get("summary") or "")
    referenced_title = clean_text(reposted_topic.get("title") or "")
    referenced_moment_id = (reposted or {}).get("id_str") or ""
    referenced_summary = topic_full_text(reposted_topic, referenced_moment_id, topic_text_by_moment, topic_text_by_topic)
    if not referenced_summary:
        referenced_summary = clean_text(reposted_topic.get("summary") or "")
    if not summary:
        summary = clean_text(sharing.get("description") or "")
    if summary == "来自冒险家公会的图文" and referenced_summary:
        summary = referenced_summary
    full_text_parts = [title, summary]
    if referenced_title and referenced_title != title:
        full_text_parts.append(referenced_title)
    if referenced_summary and referenced_summary != summary:
        full_text_parts.append(referenced_summary)
    full_text = clean_text("\n".join(part for part in full_text_parts if part))

    published = local_dt(moment.get("publish_time") or moment.get("created_time"))
    url = sharing.get("url") or f"https://www.taptap.cn/moment/{moment['id_str']}"
    category = classify(title, full_text, labels)
    highlights = extract_highlights(full_text)

    source_type = "topic" if topic else ("repost" if reposted_topic else "moment")
    return {
        "moment_id": moment["id_str"],
        "source_moment_id": source_moment["id_str"],
        "source_type": source_type,
        "published_at": published.strftime("%Y-%m-%d %H:%M:%S") if published else "",
        "published_date": published.date().isoformat() if published else "",
        "update_date_in_title": parse_title_update_date(title, published) if published else "",
        "title": title,
        "category": category,
        "labels": "、".join(labels),
        "maintenance_mode": maintenance_mode(full_text),
        "maintenance_window": extract_time_window(full_text),
        "has_compensation": "是" if ("补偿" in full_text or "补发" in full_text) else "",
        "content_tags": section_tags(full_text),
        "highlights": " | ".join(highlights),
        "summary": summary,
        "referenced_title": referenced_title,
        "url": url,
        "pv_total": stat.get("pv_total", ""),
        "ups": stat.get("ups", ""),
        "comments": stat.get("comments", ""),
        "favorites": stat.get("favorites", ""),
        "reposts": stat.get("reposts", ""),
        "author_name": author.get("name") or author.get("title") or "",
    }


FIELDS = [
    "moment_id",
    "source_moment_id",
    "source_type",
    "published_at",
    "published_date",
    "update_date_in_title",
    "title",
    "category",
    "labels",
    "maintenance_mode",
    "maintenance_window",
    "has_compensation",
    "content_tags",
    "highlights",
    "summary",
    "referenced_title",
    "url",
    "pv_total",
    "ups",
    "comments",
    "favorites",
    "reposts",
    "author_name",
]


def write_csv(path: Path, rows: list[dict]):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def html_table_rows(rows: list[dict]) -> str:
    out = []
    for row in rows:
        summary = html.escape(row["summary"])
        highlights = html.escape(row["highlights"])
        out.append(
            "<tr>"
            f"<td>{html.escape(row['published_date'])}</td>"
            f"<td>{html.escape(row['update_date_in_title'])}</td>"
            f"<td><a href=\"{html.escape(row['url'])}\" target=\"_blank\" rel=\"noreferrer\">{html.escape(row['title'])}</a></td>"
            f"<td>{html.escape(row['maintenance_mode'])}</td>"
            f"<td>{html.escape(row['content_tags'])}</td>"
            f"<td>{html.escape(row['has_compensation'])}</td>"
            f"<td><details><summary>{highlights[:160] or '查看摘要'}</summary><pre>{summary}</pre></details></td>"
            "</tr>"
        )
    return "\n".join(out)


def build_html(rows, update_rows, related_rows, user_id: str, source_note: str):
    category_counts = Counter(row["category"] for row in rows)
    year_counts = Counter(row["published_date"][:4] for row in update_rows if row["published_date"])
    tag_counts = Counter()
    for row in update_rows:
        for tag in row["content_tags"].split("、"):
            if tag:
                tag_counts[tag] += 1

    dated = [row["published_date"] for row in rows if row["published_date"]]
    oldest = min(dated) if dated else ""
    newest = max(dated) if dated else ""
    now = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %Z")

    cards = [
        ("全部帖子", len(rows)),
        ("正式更新公告", len(update_rows)),
        ("更新相关时间线", len(related_rows)),
        ("覆盖区间", f"{oldest} 至 {newest}"),
    ]
    card_html = "\n".join(f"<div class=\"card\"><div class=\"metric\">{html.escape(str(v))}</div><div>{html.escape(k)}</div></div>" for k, v in cards)
    cat_html = "\n".join(f"<li><strong>{html.escape(k)}</strong>：{v}</li>" for k, v in category_counts.most_common())
    year_html = "\n".join(f"<li><strong>{html.escape(k)}</strong>：{v} 条正式更新公告</li>" for k, v in sorted(year_counts.items(), reverse=True))
    tag_html = "\n".join(f"<li><strong>{html.escape(k)}</strong>：{v}</li>" for k, v in tag_counts.most_common())

    recent_updates = sorted(update_rows, key=lambda r: (r["published_at"], r["moment_id"]), reverse=True)
    related_sorted = sorted(related_rows, key=lambda r: (r["published_at"], r["moment_id"]), reverse=True)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TapTap 用户 {html.escape(user_id)} 更新日志整理</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; background: #f6f7f8; color: #1f2933; }}
    header {{ background: #ffffff; border-bottom: 1px solid #d9dee3; padding: 28px 36px; }}
    main {{ max-width: 1240px; margin: 0 auto; padding: 24px 28px 48px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    h2 {{ margin-top: 30px; font-size: 20px; }}
    p {{ line-height: 1.65; }}
    a {{ color: #087b75; text-decoration: none; }}
    .subtle {{ color: #667085; }}
    .cards {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 18px; }}
    .card {{ background: #fff; border: 1px solid #d9dee3; border-radius: 8px; padding: 16px; }}
    .metric {{ font-size: 24px; font-weight: 700; margin-bottom: 4px; }}
    .grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }}
    .panel {{ background: #fff; border: 1px solid #d9dee3; border-radius: 8px; padding: 16px; }}
    ul {{ margin: 8px 0 0 18px; padding: 0; line-height: 1.8; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d9dee3; }}
    th, td {{ border-bottom: 1px solid #e5e8eb; padding: 10px 12px; vertical-align: top; text-align: left; font-size: 13px; }}
    th {{ background: #edf2f2; position: sticky; top: 0; z-index: 1; }}
    tr:hover td {{ background: #fbfcfc; }}
    pre {{ white-space: pre-wrap; font-family: inherit; line-height: 1.55; margin: 10px 0 0; max-width: 680px; }}
    details summary {{ cursor: pointer; color: #40515f; }}
    .table-wrap {{ max-height: 760px; overflow: auto; border-radius: 8px; }}
    @media (max-width: 900px) {{ .cards, .grid {{ grid-template-columns: 1fr; }} main {{ padding: 18px; }} header {{ padding: 22px 18px; }} }}
  </style>
</head>
<body>
  <header>
    <h1>TapTap 用户 {html.escape(user_id)} 更新日志整理</h1>
    <p class="subtle">来源：<a href="https://www.taptap.cn/user/{html.escape(user_id)}" target="_blank" rel="noreferrer">TapTap 用户 {html.escape(user_id)}</a>；抓取时间：{html.escape(now)}。{html.escape(source_note)}</p>
    <div class="cards">{card_html}</div>
  </header>
  <main>
    <section class="grid">
      <div class="panel"><h2>分类统计</h2><ul>{cat_html}</ul></div>
      <div class="panel"><h2>年度更新公告</h2><ul>{year_html}</ul></div>
      <div class="panel"><h2>正式更新内容标签</h2><ul>{tag_html}</ul></div>
    </section>
    <section>
      <h2>正式更新公告时间线</h2>
      <p class="subtle">筛选规则：标题包含“更新公告”或“X月X日更新公告”。表中“标题日期”为标题中提到的维护/更新时间。</p>
      <div class="table-wrap"><table><thead><tr><th>发布日</th><th>标题日期</th><th>标题</th><th>维护方式</th><th>内容标签</th><th>补偿/补发</th><th>摘要</th></tr></thead><tbody>{html_table_rows(recent_updates)}</tbody></table></div>
    </section>
    <section>
      <h2>更新相关公告时间线</h2>
      <p class="subtle">包括正式更新公告、维护/服务器互通、问题修复/补偿、活动运营公告。</p>
      <div class="table-wrap"><table><thead><tr><th>发布日</th><th>标题日期</th><th>标题</th><th>维护方式</th><th>内容标签</th><th>补偿/补发</th><th>摘要</th></tr></thead><tbody>{html_table_rows(related_sorted)}</tbody></table></div>
    </section>
  </main>
</body>
</html>
"""


def process(raw_path: Path, details_dir: Path, topic_details_dir: Path, out_dir: Path, user_id: str, prefix: str, source_note: str):
    payload = load_json(raw_path)
    details = load_details(details_dir)
    topic_text_by_moment, topic_text_by_topic = load_topic_details(topic_details_dir)
    rows = [normalize_item(item, details, topic_text_by_moment, topic_text_by_topic) for item in payload["items"]]
    rows.sort(key=lambda r: (r["published_at"], r["moment_id"]), reverse=True)
    update_rows = [row for row in rows if row["category"] == "正式更新公告"]
    related_rows = [row for row in rows if row["category"] in {"正式更新公告", "维护/服务器", "问题/修复/补偿", "活动/运营"}]

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / f"{prefix}_all_posts.csv", rows)
    write_csv(out_dir / f"{prefix}_update_announcements.csv", update_rows)
    write_csv(out_dir / f"{prefix}_update_related_timeline.csv", related_rows)
    (out_dir / f"{prefix}_update_log_report.html").write_text(
        build_html(rows, update_rows, related_rows, user_id, source_note),
        encoding="utf-8",
    )

    dated = [row["published_date"] for row in rows if row["published_date"]]
    summary = {
        "source": f"https://www.taptap.cn/user/{user_id}",
        "fetched_count": len(rows),
        "unique_moment_count": len({row["moment_id"] for row in rows}),
        "date_range": [min(dated), max(dated)] if dated else [],
        "category_counts": dict(Counter(row["category"] for row in rows)),
        "outputs": {
            "all_posts_csv": f"{prefix}_all_posts.csv",
            "update_announcements_csv": f"{prefix}_update_announcements.csv",
            "update_related_timeline_csv": f"{prefix}_update_related_timeline.csv",
            "html_report": f"{prefix}_update_log_report.html",
        },
        "topic_detail_count": len(topic_text_by_topic),
    }
    (out_dir / f"{prefix}_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main():
    parser = argparse.ArgumentParser(description="Process TapTap user feed JSON into update-log CSV/HTML outputs.")
    parser.add_argument("--raw", required=True, type=Path, help="Path to combined user_feed_all_raw.json.")
    parser.add_argument("--details-dir", required=True, type=Path, help="Directory containing optional moment detail JSON files.")
    parser.add_argument("--topic-details-dir", required=True, type=Path, help="Directory containing optional topic detail JSON files.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output directory.")
    parser.add_argument("--user-id", required=True, help="TapTap user id.")
    parser.add_argument("--prefix", default=None, help="Output file prefix. Defaults to taptap_<user_id>.")
    parser.add_argument("--source-note", default="数据来自 TapTap 页面暴露的公开 Web API。", help="Note shown in the HTML report.")
    args = parser.parse_args()

    prefix = args.prefix or f"taptap_{args.user_id}"
    summary = process(args.raw, args.details_dir, args.topic_details_dir, args.out_dir, args.user_id, prefix, args.source_note)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
