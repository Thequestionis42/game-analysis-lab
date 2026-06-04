# Game Update History Research Brief

## Reusable User Brief

```text
I want to analyze the version update history of Product A and Product B.

Inputs:
- Product A version log file:
- Product B version log file:
- Cutoff date:
- Market/platform:
- Optional special questions:

Goals:
1. Analyze each product's mainline level/chapter update frequency and per-update volume.
2. Analyze progression-system evolution:
   - independent new progression lines;
   - deepening of existing progression lines;
   - content expansion within existing systems;
   - display, gallery, management, convenience, or QoL features;
   - unusual mechanisms that need separate explanation.
3. Analyze mid/late-game update direction:
   - first open-endedly identify all important new or strengthened systems, mechanics, gameplay modes, operating frameworks, and economy/social structures;
   - then infer what product role each serves;
   - do not assume late-game direction must be mainline, activity, season, social, guild, co-op, or numeric progression;
   - analyze special mechanisms such as auctions, trading markets, housing, UGC, guild tech, server politics, seasonal economy, leaderboards, spectator features, creator tools, return-user systems, complexity reduction, resource conversion, or monetization carriers according to evidence.
4. Validate system meanings with public sources before citing or classifying important systems. Do not rely on version-log keywords alone.
5. Do not force comparison. First summarize each product's own pattern, then abstract implications for RPG-like products.

Output:
Build an HTML report with executive summary, quick directory, data/method scope, mainline cadence charts, progression taxonomy, per-product patterns, special-topic sections, RPG-like recommendations, sources, and caveats.
```

## Classification Taxonomy

| Category | Use when | Common evidence |
|---|---|---|
| Independent progression line | The system has its own entry, resources, slots, levels/stars/quality/affixes/reforge, and combat/stat/long-term impact. | Pet, vehicle, mercenary, mecha, gene, card deck, code system. |
| Existing-line deepening | The update adds depth to an existing parent system. | Awakening, forging, resonance, overload, fusion, reroll, affix pool, season wash, higher rarity. |
| Existing-system content expansion | The update adds items inside an old structure without changing the growth structure. | New equipment, new pet, new card, new mecha, new boss, new chapter batch. |
| Activity/season/gameplay | The update adds or changes a play mode, event, season, challenge, ranking, or map rule. | Seasonal map, boss raid, rotating mode, trial, ranking event. |
| Social/co-op/organization layer | The update creates or strengthens player organization, cooperation, support, guilds, alliances, cross-server competition, chat, gifting, intimacy, or role assignments. | Guild battle, alliance expedition, co-op roles, support army, cross-server ranking. |
| Economy/trade/market layer | The update changes resource circulation, player exchange, auction, marketplace, bidding, taxes, production, or server economy. | Auction house, trading, guild auction, seasonal market, production buildings. |
| Display/collection/QoL | The update improves visibility, management, preview, reset, loadouts, gallery, collection display, one-click actions, or resource return. | Gallery, exhibition hall, preview, quick switch, reset, rollback, dismantle, auto-fill. |
| Special mechanism | The update does not fit the above categories or represents a new product direction. | Housing, UGC, spectator mode, creator ecosystem, server politics, live-stream hooks. |

## Source Reliability Rubric

Use this order unless the user gives a stronger source:

1. Official announcement, official site, official community/TapTap post, App Store or app-market update log.
2. Official-adjacent platform posts or verified publisher/developer pages.
3. Guide sites and databases, only for mechanic interpretation.
4. Player discussions, only as leads or supporting color.

Before using a source, evaluate:

- Is it official or clearly tied to the game/operator?
- Does it describe the current system or a historical version?
- Does it state mechanics directly, or is it player inference?
- Does it support classification, or only naming?
- Is the claim important enough to need a second source?

Phrase uncertainty explicitly:

- "The official log names this as..."
- "Public guides describe the mechanic as..."
- "This is an inference from..."
- "Evidence is insufficient to classify it as..."

## Analysis Questions

For each product:

- What is the mainline cadence by median interval, average interval, count, and batch volume?
- Does mainline remain a fixed live-ops heartbeat, or become intermittent?
- Which progression systems were opened early, and which were deepened later?
- Which late-game additions are truly new systems versus higher layers on old systems?
- What non-progression mechanisms appeared later, and what player behavior do they change?
- How do activities/seasons/social/economy systems give existing progression a use case?
- What mechanisms reduce complexity, recover resources, improve targeting, or extend system life?
- Which claims are verified, inferred, or uncertain?

## HTML Report Outline

1. Title and metadata
2. Executive Summary
3. Quick directory
4. Data scope and classification method
5. Mainline cadence and volume
6. Progression taxonomy
7. Product A pattern
8. Product B pattern
9. Special-topic sections for unusual mechanisms or user questions
10. RPG-like implications and planning recommendations
11. Sources and caveats

UI guidance:

- Use lifecycle stages when launch dates differ; avoid shared calendar-year timelines that imply false alignment.
- Use "Notes" or "Remarks" for interpretation columns.
- Keep tables scannable: short headers, first-column emphasis, tags, and zebra rows.
- Put source links near the supported claim or in a source section.
- Keep report conclusions actionable, not a patch-note dump.
