---
name: taptap-user-posts
description: Export and analyze public TapTap user posts with full topic text. Use when Codex needs to scrape a TapTap user page by user ID, fetch all public posts, recover full topic bodies beyond truncated summaries, produce all-post CSVs, update-announcement timelines, HTML update-log reports, or investigate Chinese game/community update histories from TapTap users.
---

# TapTap User Posts

Use this skill to export public TapTap user posts and build update-log datasets.

## Standard Interface

Run the bundled PowerShell CLI from the current workspace:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill_dir>\scripts\taptap_export_user_posts.ps1" -UserId <TapTapUserId>
```

Recommended explicit output:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill_dir>\scripts\taptap_export_user_posts.ps1" -UserId <TapTapUserId> -OutDir "<workspace>\outputs\taptap_<TapTapUserId>"
```

The script defaults to `outputs\taptap_<UserId>` under the current working directory.

## What The Script Does

1. Page through `/webapiv2/feed/v7/by-user?user_id=<UserId>&limit=10&__times=0`.
2. Save raw feed pages and combined `user_feed_all_raw.json`.
3. Fetch `/webapiv2/moment/v3/detail?id=<moment_id>` for moments.
4. Fetch `/webapiv2/topic/v1/detail?id=<topic_id>` for each topic.
5. Prefer `data.first_post.contents.raw_text` from topic detail because feed and moment summaries are often truncated.
6. Export CSV and HTML files.

## Outputs

The output directory contains:

- `raw\user_feed_all_raw.json`
- `raw\user_feed_pages\page_*.json`
- `raw\moment_details\*.json`
- `raw\topic_details\*.json`
- `taptap_<UserId>_all_posts.csv`
- `taptap_<UserId>_update_announcements.csv`
- `taptap_<UserId>_update_related_timeline.csv`
- `taptap_<UserId>_update_log_report.html`
- `taptap_<UserId>_summary.json`

## Reprocessing Existing Raw Data

Use this when raw and details already exist and only classification/report logic changed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill_dir>\scripts\taptap_export_user_posts.ps1" -UserId <TapTapUserId> -OutDir "<workspace>\outputs\taptap_<TapTapUserId>" -SkipFetch -SkipDetails -SkipTopicDetails
```

Use this when feed raw exists but full topic bodies must be fetched or refreshed:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<skill_dir>\scripts\taptap_export_user_posts.ps1" -UserId <TapTapUserId> -OutDir "<workspace>\outputs\taptap_<TapTapUserId>" -SkipFetch -SkipDetails
```

## Validation

After export, verify:

- `summary.json` has the expected `fetched_count`.
- `raw\topic_details` count is close to the number of topic posts.
- A long known update notice has `summary` length greater than 200 characters.
- CSV opens with UTF-8/BOM encoding in Excel or PowerShell `Import-Csv -Encoding UTF8`.

For update-log analysis, use `taptap_<UserId>_update_announcements.csv` for formal update notices and `taptap_<UserId>_update_related_timeline.csv` for formal updates plus maintenance, server, issue, compensation, and activity posts.

## Caveats

- Only public content available through TapTap Web APIs can be exported.
- Some user IDs may return zero posts even if the profile exists.
- TapTap API paths or `X-UA` rules may change; inspect the current web app JS for replacement endpoints if requests fail.
- Network access may require escalation in restricted Codex sandboxes.
