# Power BI Visualization Build Instructions

This is the manual, in-Desktop follow-up to the PBIP repair done on 2026-08-17
(see `docs/handoff/claude-review.md`, "Fourth Follow-Up"). The project now
**opens** correctly, but all three report pages are intentionally empty — no
`visual.json` containers exist yet, because those can only be created inside
Power BI Desktop itself (they aren't hand-editable text the way TMDL/JSON
elsewhere in this repo is). This document is the checklist for building the
real visuals per page.

Each page's original design intent lives in two places if you want to
cross-check anything below: `powerbi/<page-folder>/report-spec.yml` (the
source-of-truth spec) and
`powerbi/NSU BI Modernization Demo/New/NSU BI Modernization Demo New/report-visual-specs/`
(a generated reference derived from it — not loaded by Power BI, just notes).

## Before you start

1. Open `NSU BI Modernization Demo.pbip` (or `NSU BI Modernization Demo.Report/definition.pbir` directly) in Power BI Desktop.
2. It should now load without the "Required artifact is missing" error. If you still see a "Values aren't shown due to possible data privacy issues" or a stale-credential prompt, that's unrelated to the fix — approve it, or ignore it if it's just about the `ProjectRoot`/`LakehouseName` parameters.
3. **Refresh the semantic model** (Home ribbon → Refresh) before doing anything else, so you're placing visuals against real data, not an empty cache. All three fact tables (`FactEnrollment`, `RecruitmentFunnel`, `CensusEnrollment`) and all dimension/governance tables load from the CSVs under `seeds/` via the `ProjectRoot` parameter — confirm that parameter (Transform data → Manage Parameters) still points at this repo's root on your machine (it was set to `C:\Users\maxbrooks\Documents\GitHub\nsu-modernization-demo` during the repair).
4. Relationships are already wired: `FactEnrollment`, `RecruitmentFunnel`, and `CensusEnrollment` each relate to `dim_school`, `dim_program`, and `dim_term` on `school_id`/`program_id`/`term_id`. You do not need to add anything to the model to build the visuals below — just place them.

---

## Page 1 — Executive Enrollment & Admissions

Page object name: `30b3c1f79a90c2cbf9c7`. Source spec: `powerbi/executive-enrollment-admissions/report-spec.yml`.

### Slicers (place across the top of the page)

| Field | Type |
|---|---|
| `dim_term[term_name]` | Slicer, multi-select |
| `dim_school[school_name]` | Slicer, multi-select |
| `dim_program[program_name]` | Slicer, multi-select |

### KPI cards (row of 4, left to right)

| Visual | Field | Title |
|---|---|---|
| Card | `RecruitmentFunnel[Applications]` | Applications |
| Card | `RecruitmentFunnel[Admits]` | Admits |
| Card | `RecruitmentFunnel[Deposits]` | Deposits |
| Card | `FactEnrollment[Enrolled]` | Enrolled |

These are all pre-built certified measures — just drag the measure onto a Card visual, no aggregation to configure.

### Funnel

The source spec lists this visual as `type: funnel, metric: yield` — a single ratio doesn't make a real funnel shape, so build it as the actual 3-stage recruitment funnel it represents, with Yield called out separately since it's a rate, not a stage:

1. Insert a **Funnel** visual.
2. Drag **Values**: `RecruitmentFunnel[Applications]`, then `RecruitmentFunnel[Admits]`, then `RecruitmentFunnel[Deposits]` — in that order, so the funnel narrows top to bottom.
3. Title it "Recruitment Funnel".
4. Add a small **Card** beneath/beside it bound to `RecruitmentFunnel[Yield]`, titled "Yield (Deposits ÷ Admits)", so the ratio is still visible without distorting the funnel's bar-length scale.

### Column chart

1. Insert a **Clustered column chart**.
2. **X-axis**: `dim_school[school_name]`.
3. **Y-axis / Values**: `FactEnrollment[Enrolled]`.
4. Title: "Enrolled by School".

---

## Page 2 — Institutional Data Trust

Page object name: `7d0b4c17e6cc4c4f9e7a`. Source spec: `powerbi/institutional-data-trust/report-spec.yml`. Underlying table: `certification_catalog` (3 rows — one per certified data product: `fact_enrollment`, `recruitment_funnel`, `census_enrollment`) and `quality_test_evidence` (47 rows, one per dbt test).

### Slicers

| Field | Type |
|---|---|
| `certification_catalog[product]` | Slicer, multi-select |
| `certification_catalog[status]` | Slicer, multi-select |

### Cards

- **Certification Status card**: drag `certification_catalog[status]` onto a Card visual, then in the field well click the dropdown on the field and set summarization to **First** (not Count/Count Distinct) — all 3 rows currently share the value `Certified`, so First cleanly displays it as text. Title: "Certification Status".
- **Release Gate card**: there is **no `release_gate` field in the semantic model** — an earlier generated draft of this page referenced one that was never real (see `docs/handoff/claude-review.md`, item 6 of the Fourth Follow-Up). Per the original spec (`report-spec.yml`: `label: Release gate, value: Enabled`) this is a static label, not data-bound. Use a **Text Box** visual (Insert → Text box), not a Card, reading "Release Gate: Enabled". Do not add a `release_gate` column to the model to make a Card work — that would be a semantic-model change outside this document's authority.

### Tables

| Visual | Fields | Title |
|---|---|---|
| Table | `certification_catalog[product]`, `[model]`, `[version]`, `[owner]`, `[steward]`, `[status]`, `[last_reviewed]` | Certified Products |
| Table | `quality_test_evidence[test_name]`, `[result]`, `[evidence]` | Quality Test Evidence |

---

## Page 3 — Data Lineage & Certification

Page object name: `8e5c2a6d9f1b4c7e8a3d`. Source spec: `powerbi/data-lineage-certification/report-spec.yml`. Underlying tables: `lineage_summary` (3 rows) and `certification_catalog`.

### Slicers

| Field | Type |
|---|---|
| `certification_catalog[product]` | Slicer, multi-select |
| `lineage_summary[consumers]` | Slicer, multi-select — note this column holds combined multi-value strings (e.g. `"Executive Enrollment and Admissions reporting; downstream enrollment analysis"`) rather than one consumer per row, so it filters on the whole combined string, not individual consumers. Splitting that out would be a model change; left as-is. |
| `certification_catalog[status]` | Slicer, multi-select |

### Lineage flow diagram

There is no native Power BI visual for an arbitrary process-flow diagram, and this is a fixed, non-data-bound label sequence (`Source → Transformation → Certified Model → Semantic Definition → Report`) — build it with shapes, not a data visual:

1. Insert → Shapes → Rectangle, five times, arranged left to right, labeled: **Source**, **Transformation**, **Certified Model**, **Semantic Definition**, **Report**.
2. Insert → Shapes → Arrow (or Line), four times, connecting each rectangle to the next.
3. Group the 9 shapes (select all → right-click → Group) so they move together, and title the group area "Source → Transformation → Certified Model → Semantic Definition → Report".

If you'd rather not hand-place shapes, an equivalent free AppSource visual (e.g. a Sankey or process-flow custom visual) can be substituted, but isn't required — the shape approach exactly matches the original spec's `type: flow` intent with zero external dependencies.

### Tables

| Visual | Fields | Title |
|---|---|---|
| Table | `lineage_summary[product]`, `[source_entities]`, `[model]`, `[semantic_definitions]`, `[consumers]` | Certified Product Lineage |
| Table | `certification_catalog[product]`, `[owner]`, `[steward]`, `[version]`, `[status]`, `[approval_decision]` | Certification Release Details |

Note: `approval_decision` is the real column name. An earlier draft of `powerbi/data-lineage-certification/report-spec.yml` said `approval` — that was a stale spec typo, already corrected in this repo (see Fourth Follow-Up, item 5).

---

## After building: save, then re-check

1. Save the project (**Ctrl+S**) — this is what actually generates the real `visual.json` files under each page's `visuals/` folder. Until you save, nothing above is written to disk.
2. Re-open the `.pbip` once (close and reopen Desktop) to confirm it still loads cleanly with the new visuals — this catches anything Desktop silently auto-corrected on save.
3. Spot-check that each page's slicers actually filter its visuals (e.g., picking one school on Page 1 should move the KPI cards and column chart).

---

## Can I save the `.pbip` over the existing `.pbix`?

Short answer: **yes, but not by copying/overwriting the file directly** — the two formats aren't interchangeable on disk (`.pbix` is a single zipped binary container; `.pbip` is a folder of text files). The conversion has to go through Power BI Desktop:

1. Open the `.pbip` in Power BI Desktop (after building the visuals above).
2. **File → Save As**.
3. Choose **Power BI files (\*.pbix)** as the save-as type.
4. Save it to
   `powerbi/NSU BI Modernization Demo/New/NSU BI Modernization Demo New/NSU BI Modernization Demo.pbix`
   — the same path as the existing `.pbix` — and confirm the overwrite prompt.

This is directly confirmed by Microsoft's own PBIP documentation (`learn.microsoft.com/power-bi/developer/projects/projects-overview`, FAQ section): *"If I convert a PBIX to a PBIP, can I convert it back to PBIX? Answer: Yes... using Power BI Desktop's Save As"* — and separately, *"Can I convert PBIX into PBIP and vice-versa **programmatically**? Answer: No."* So there's no script or file-copy shortcut; it has to be a manual Save As inside Desktop, but doing that is fully supported and the result is a normal, working `.pbix`.

One caveat: the `.pbix` currently checked into this repo predates the repair done on 2026-08-17 and was generated from the same broken source, so it's likely just as non-functional as the old `.pbip` was — don't treat it as a working fallback. Once you've rebuilt the visuals and re-saved as `.pbix` per the steps above, that new file is the one to keep; the old one can be replaced.
