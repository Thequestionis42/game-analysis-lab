# HTML 报告结构范例：单产品 RPG-like 长线版本策略分析

> 用途：这是 HTML 交付结构和信息密度范例。执行 Skill 时，在生成 HTML 前必须阅读本文件。
>
> 必须模仿：章节顺序、组件类型、图表位置、表格字段、结论密度、证据标注方式。
>
> 禁止照搬：示例产品名、示例系统名、示例日期、示例结论。

---

## 0. 范例边界

本范例不是完整报告，不提供真实产品结论。它只说明最终 HTML 应该如何组织，避免输出结构在不同任务中漂移。

HTML 报告必须先给判断，再给证据；先解释产品，再统计版本；先拆严格主线，再看阶段包；先给总览矩阵，再给系统明细。

---

## 1. 页面骨架

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《产品名称》长线版本策略分析</title>
  <style>
    :root {
      --ink:#202124;
      --muted:#5f6368;
      --line:#ddd8cc;
      --paper:#f7f5ef;
      --panel:#ffffff;
      --accent:#27445f;
      --wash:#eef4f8;
    }
    * { box-sizing:border-box; }
    body {
      margin:0;
      background:linear-gradient(180deg,#eef1f1 0,var(--paper) 320px),var(--paper);
      color:var(--ink);
      font:16px/1.72 "Microsoft YaHei","PingFang SC",Arial,sans-serif;
    }
    .page { max-width:1160px; margin:0 auto; padding:38px 28px 82px; }
    header, section.summary {
      background:rgba(255,255,255,.84);
      border:1px solid var(--line);
      border-radius:8px;
      padding:24px;
    }
    h1 { margin:0 0 12px; font-size:34px; line-height:1.25; letter-spacing:0; }
    h2 { margin:42px 0 16px; padding-top:18px; border-top:1px solid var(--line); font-size:24px; }
    .subtle { color:var(--muted); }
    .toc { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin:18px 0 24px; }
    .toc a { display:block; padding:10px 12px; border:1px solid var(--line); border-radius:8px; background:#fff; color:#26323b; text-decoration:none; font-weight:700; }
    .metrics { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:12px; }
    .metric-card { background:#fff; border:1px solid var(--line); border-radius:8px; padding:16px; }
    .metric-label { color:var(--muted); font-size:13px; font-weight:700; }
    .metric-value { font-size:30px; font-weight:800; color:#253746; }
    .table-scroll, .lifecycle-scroll { overflow-x:auto; margin:16px 0 24px; }
    table { width:100%; border-collapse:separate; border-spacing:0; background:#fff; border:1px solid var(--line); border-radius:8px; overflow:hidden; }
    th, td { padding:12px 13px; border-bottom:1px solid #e5e1d6; border-right:1px solid #e5e1d6; vertical-align:top; }
    th { background:#ebe8df; text-align:left; font-weight:800; }
    .tag { display:inline-block; border-radius:999px; padding:2px 8px; font-size:12px; font-weight:700; color:#fff; margin-right:4px; }
    .tag-new { background:#6f8f5f; }
    .tag-deep { background:#5b7c99; }
    .tag-content { background:#d9825b; }
    .tag-qol { background:#777; }
    .callout { border-left:4px solid var(--accent); padding:12px 16px; background:var(--wash); border-radius:0 8px 8px 0; }
    .lifecycle-grid {
      min-width:860px;
      display:grid;
      grid-template-columns:130px repeat(var(--phase-count),minmax(170px,1fr));
      gap:10px 12px;
    }
    .phase-head { background:#343a3f; color:#fff; border-radius:6px; padding:12px 14px; }
    .phase-head span { display:block; color:#d8dde1; font-size:12px; }
    .system-label { font-weight:800; align-self:center; color:#232b31; }
    .phase-cell { background:#eef4f8; border:1px solid #d8e1e7; border-radius:6px; padding:13px 14px; min-height:86px; }
    @media (max-width:860px) {
      .toc, .metrics { grid-template-columns:1fr; }
      .page { padding:28px 16px 56px; }
      h1 { font-size:26px; }
    }
  </style>
</head>
<body>
  <main class="page">
    <!-- 正文按本文件第 2 节顺序组织 -->
  </main>
</body>
</html>
```

---

## 2. 正文章节顺序

HTML 正文必须保持以下顺序。可以根据资料多少调整篇幅，但不要改顺序。

1. Executive Summary
2. 快速目录
3. 数据范围、来源说明和方法口径
4. 产品定位与核心玩法结构分析
5. 严格主线扩容频率与单次体量
6. 阶段版本包频率与内容构成
7. 主线在不同生命周期阶段承担的作用
8. 养成系统分类口径
9. 养成系统演进
10. 中后期机制扫描矩阵
11. 中后期重点机制专题分析
12. 商业化辅助轴分析
13. 产品策略判断卡
14. RPG-like 产品策略启发
15. 关键限制与不确定性
16. 附录 A-K

---

## 3. Executive Summary 范式

Executive Summary 使用 4-6 条判断卡。每条必须是“结论 + 证据摘要 + 含义”，不要写泛泛描述。

```html
<section class="summary" id="summary">
  <h2>Executive Summary</h2>
  <ul class="summary-list">
    <li><strong>这是一款低压力自动推进 + 职业 Build 验证的 RPG-like 产品。</strong>官方资料显示其核心循环由自动主线、角色成长、多人挑战和组织协作构成。因此版本历史不能只按“新增活动”阅读。</li>
    <li><strong>严格主线不是每次大版本的唯一主体。</strong>主线扩容需要和转职、挑战内容、养成线、活动和商业化承载拆开统计。</li>
    <li><strong>中后期目标感主要来自旧线深化和阶段包组合。</strong>若资料显示新增独立线减少，应进一步观察旧系统是否通过品质、词条、融合、继承、重置等方式延长消耗。</li>
  </ul>
</section>
```

---

## 4. 数据范围与方法口径范式

必须写清资料边界和分类口径。

```html
<section id="method">
  <h2>数据范围、来源说明和方法口径</h2>
  <p>本报告分析《产品名称》从 YYYY-MM-DD 到 YYYY-MM-DD 的版本公告、官方动态和应用商店更新日志。公开资料优先级为官方公告、官网、TapTap 官方动态、应用商店更新日志；攻略站仅用于解释机制，玩家讨论仅作为辅助线索。</p>
  <p>本报告在分析前读取了产品理解校准范例，仅用于校准分析结构和证据口径，未将范例产品结论直接套用到目标产品。</p>
  <div class="callout"><strong>口径：</strong>严格主线扩容只纳入明确属于主线的章节、关卡、地图、区域、剧情篇章或主线 Boss；转职、秘境、团本、活动、养成、排行榜、商业化和 QoL 进入阶段版本包，不计入严格主线。</div>
</section>
```

---

## 5. 主线频率模块范式

主线章节必须同时提供指标卡、明细表和一句产品判断。

```html
<section id="mainline">
  <h2>严格主线扩容频率与单次体量</h2>
  <div class="metrics">
    <div class="metric-card"><div class="metric-label">主线扩容次数</div><div class="metric-value">N</div><div class="metric-note">仅统计严格主线</div></div>
    <div class="metric-card"><div class="metric-label">中位间隔</div><div class="metric-value">N 天</div><div class="metric-note">优先使用生效日期</div></div>
    <div class="metric-card"><div class="metric-label">单次典型体量</div><div class="metric-value">N</div><div class="metric-note">章节/关卡/地图</div></div>
    <div class="metric-card"><div class="metric-label">最长空窗</div><div class="metric-value">N 天</div><div class="metric-note">资料不足需标注</div></div>
  </div>
  <p><strong>判断：</strong>主线供给更接近“月度稳定 / 季度批量 / 大版本绑定 / 前高后低 / 低频底盘 / 资料不足”中的哪一种，并说明依据。</p>
  <div class="table-scroll">
    <table>
      <thead><tr><th>生效日期</th><th>公告日期</th><th>新增类型</th><th>新增批量</th><th>距上次</th><th>证据等级</th><th>来源</th></tr></thead>
      <tbody>
        <tr><td>YYYY-MM-DD</td><td>YYYY-MM-DD</td><td>新章节</td><td>N 章</td><td>N 天</td><td>A</td><td>官方公告</td></tr>
      </tbody>
    </table>
  </div>
</section>
```

---

## 6. 系统生命周期演进分期图范式

这是“养成系统演进”章节中的核心可视组件。它必须是 HTML 文本矩阵，而不是单独图片。

```html
<section id="progression-lifecycle-map">
  <h2>养成系统生命周期演进分期</h2>
  <p class="subtle">按产品生命周期分期读取，不同阶段代表同一产品的长期演进，不是简单年份罗列。</p>
  <div class="lifecycle-scroll">
    <div class="lifecycle-grid" style="--phase-count:4">
      <div class="axis-label"></div>
      <div class="phase-head"><strong>阶段一</strong><span>基础线铺设</span></div>
      <div class="phase-head"><strong>阶段二</strong><span>旧线深化</span></div>
      <div class="phase-head"><strong>阶段三</strong><span>深层消耗</span></div>
      <div class="phase-head"><strong>阶段四</strong><span>生态治理</span></div>

      <div class="system-label">装备线</div>
      <div class="phase-cell">新增装备入口、品质或基础掉落。<br><span class="tag tag-new">独立线</span></div>
      <div class="phase-cell">新增词条、觉醒、融合或装配层。<br><span class="tag tag-deep">旧线深化</span></div>
      <div class="phase-cell">引入高阶材料、继承、置换或回收。<br><span class="tag tag-deep">深层消耗</span></div>
      <div class="phase-cell">通过减负和资源迁移降低换线成本。<br><span class="tag tag-qol">QoL</span></div>

      <div class="system-label">宠物线</div>
      <div class="phase-cell">新增宠物入口和基础培养。</div>
      <div class="phase-cell">新增品质、助战槽或觉醒。</div>
      <div class="phase-cell">新增高阶宠物、融合或羁绊。</div>
      <div class="phase-cell">加入重置、继承或回收机制。</div>
    </div>
  </div>
  <div class="callout">
    <strong>规律总结：</strong>先说明横向开线是否集中在早期，再说明后期是否转向旧线深化、内容扩充、减负和资源迁移。
  </div>
</section>
```

---

## 7. 阶段版本包模块范式

阶段包不要输出一个不可复算的总分。使用结构矩阵。

```html
<section id="stage-package">
  <h2>阶段版本包频率与内容构成</h2>
  <p><strong>判断：</strong>阶段版本包是否以转职、等级上限、挑战内容、新养成线、旧线深化、活动、社交竞争或商业化承载为核心。</p>
  <div class="table-scroll">
    <table>
      <thead><tr><th>生效日期</th><th>阶段版本</th><th>主线扩容</th><th>挑战内容</th><th>新养成线</th><th>旧线深化</th><th>活动/赛季</th><th>QoL</th><th>商业化</th><th>版本作用</th></tr></thead>
      <tbody>
        <tr><td>YYYY-MM-DD</td><td>阶段名</td><td>有/无</td><td>内容摘要</td><td>系统名</td><td>深化点</td><td>活动名</td><td>减负点</td><td>商店/礼包/凭证</td><td>承接中后期目标感</td></tr>
      </tbody>
    </table>
  </div>
</section>
```

---

## 8. 中后期机制专题范式

每个专题按同一字段写，避免散文化。

```html
<section id="late-game">
  <h2>中后期重点机制专题分析</h2>
  <div class="table-scroll">
    <table>
      <thead><tr><th>机制方向</th><th>状态</th><th>首次关键节点</th><th>新增或强化内容</th><th>玩家行为变化</th><th>承接阶段</th><th>与养成/经济/社交/内容消耗关系</th><th>证据等级</th></tr></thead>
      <tbody>
        <tr><td>赛季化</td><td>已发现</td><td>YYYY-MM</td><td>周期规则、赛季成长、排名奖励</td><td>从日常刷资源转向周期冲榜和组织协作</td><td>中后期</td><td>重组旧养成目标，制造阶段性消耗</td><td>A/B</td></tr>
      </tbody>
    </table>
  </div>
</section>
```

---

## 9. 附录范式

附录必须支持正文复核。不要只列来源链接。

```html
<section id="appendix">
  <h2>附录</h2>
  <h3>附录 A：原始公告节点表</h3>
  <h3>附录 B：严格主线扩容明细</h3>
  <h3>附录 C：阶段版本包明细</h3>
  <h3>附录 D：系统分类明细</h3>
  <h3>附录 E：中后期机制扫描明细</h3>
  <h3>附录 F：商业化承载明细</h3>
  <h3>附录 G：公告日期与生效日期对照</h3>
  <h3>附录 H：来源链接和证据等级</h3>
  <h3>附录 I：推断说明</h3>
  <h3>附录 J：资料缺口与异常节点</h3>
  <h3>附录 K：统计公式</h3>
</section>
```

---

## 10. 结构稳定性检查

生成 HTML 前检查：

- 是否保持 15 个正文章节；
- 是否包含附录 A-K；
- Executive Summary 是否是结论卡，而不是目录复述；
- 主线频率是否有指标卡、明细表和模式判断；
- 养成演进是否包含“系统生命周期演进分期图”；
- 中后期专题是否用统一字段回答“新增了什么、改变了什么行为、承接什么阶段、与养成/经济/社交/内容消耗是什么关系”；
- 所有图表是否能由附录明细复核；
- 是否误加产品 B 或跨产品比较章节。
