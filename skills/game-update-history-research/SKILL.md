---
name: game-update-history-research
description: Analyze mobile/game version update histories from CSV, app-store logs, patch notes, or public announcements. Use when Codex needs to research games' update cadence, mainline level releases, progression-system evolution, mid/late-game content direction, activities/seasons/social systems, and produce a decision-ready HTML report with public-source validation rather than keyword-only classification. Also use for Chinese requests about 游戏版本日志、主线关卡更新频率、养成系统演进、公开资料核验、竞品更新历史调研、HTML 报告.
---

# Game Update History Research

## Overview

Use this skill to turn game version logs plus public evidence into a product-strategy report. The core task is not to list patch notes; it is to classify what each update changed, validate important system meanings, and explain each product's update pattern and implications for RPG-like live-ops planning.

For the detailed brief, taxonomy, and report skeleton, read `references/report-brief.md` when building the final analysis or when classification is ambiguous.

## Workflow

1. **Clarify the research brief.** Identify the products, source log files, cutoff date, market/platform, whether comparison is desired, and special questions. If the user provides a complete brief, proceed without asking.

2. **Inventory and clean the logs.** Parse dates, versions, raw notes, duplicate rows, mainline level/chapter additions, gameplay additions, progression-related items, activities/seasons, social/co-op/guild/cross-server systems, economy/trade/market systems, QoL, and uncertain items. Preserve raw evidence rows for audit.

3. **Define classification before counting.** Do not treat every "new" item as a new system. Classify updates as independent progression line, old-line deepening, old-system content expansion, activity/season/gameplay, social/co-op/organization layer, economy/trade layer, display/collection/QoL, or special mechanism. If a mechanism does not fit, create a specific category and explain it.

4. **Validate system meaning with public sources.** Browse public sources for every important or ambiguous system before making a product-strategy claim. Prefer official announcements, official community posts, app-store update logs, and official sites. Use guides/databases only to explain mechanics; do not let them alone support a core conclusion. Use player discussion only as a lead or caveat. State when a claim is inferred.

5. **Analyze each product separately first.** For each game, report mainline update frequency and batch size, lifecycle stages, progression-system evolution, mid/late-game direction, activity/season/social/economy roles, adjustment philosophy, and notable uncertainty. Do not force a comparison unless the user requests it.

6. **Synthesize RPG-like implications.** Convert product observations into planning guidance: what should stay on a regular cadence, what can become seasonal, when to open a new line, when to deepen an old line, and what mechanisms reduce complexity or extend system life.

7. **Build the HTML report.** Include an executive summary, quick directory, data/method notes, charts, taxonomy table, per-product sections, special-topic sections for unusual mechanisms, recommendations, sources, and caveats. Use readable UI: clear headings, compact cards, tables with "Notes"/"Remarks" rather than over-academic labels, clickable sources, and lifecycle-aligned timelines.

8. **Validate before handoff.** Check that charts do not imply false time alignment, sources are linked, tables are readable, and important claims have evidence. Refresh or regenerate the report after edits.

## Quality Rules

- Do not classify by keywords alone.
- Do not count gallery, codex, preview, quick switch, display, or collection shells as progression unless they have stats, levels, resources, output, or combat impact.
- Do not treat affixes/traits/entries as standalone systems until the parent system is identified.
- Treat skins/costumes as progression only when they have stats, stars, skills, affixes, resources, or combat effects.
- Treat seasons, guilds, auctions, trading, housing, UGC, server politics, spectator features, and creator systems as open-ended mechanisms; analyze their product role instead of forcing them into progression or activity buckets.
- Products with different launch dates should use each product's lifecycle timeline, not a shared natural-year axis.
- Report uncertainty explicitly when public evidence is weak or non-official.

## Resource Use

- Read `references/report-brief.md` for the reusable prompt template, classification taxonomy, source reliability rubric, and HTML report outline.
- Use spreadsheet/data-analysis tooling for CSV parsing and chart-ready summaries.
- Use public web browsing for source validation whenever the user asks for research, current public evidence, or cited claims.
