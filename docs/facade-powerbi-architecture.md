# Facade Power BI Architecture Pattern

This document describes a public-safe architecture pattern for a facade progress dashboard with model-linked reporting. It is intentionally generic and synthetic.

## Reporting Layers

| Layer | Purpose | Example Public-Safe Tables |
| --- | --- | --- |
| Source extracts | Raw operational records from planning, production, logistics, site updates, and issue logs. | Not included publicly |
| Clean dimensions | Stable lookup tables for projects, blocks, levels, elevations, statuses, contractors, and model elements. | `dim_project`, `dim_building`, `dim_level`, `dim_zone`, `dim_status`, `dim_unit` |
| Facts | Event-style records for status movements, plans, issues, deliveries, and update timestamps. | `fact_unit_status_history`, `fact_unit_plan`, `fact_quality_issues`, `fact_deliveries` |
| Semantic measures | DAX measures for unit counts, latest status, installed units, open issues, solved issues, delayed deliveries, and update labels. | `docs/dax-measures.md` |
| Report pages | Power BI pages for progress overview, block overview, issue overview, and issue details. | `docs/dashboard-pages.md` |

## Model-Linked Reporting Concept

The key reporting idea is to connect each facade unit or package to a model element key.

```text
dim_unit
  UnitID
  ProjectID
  BuildingID
  LevelID
  ZoneID
  ModelElementKey
  UnitName
  ConstructionType

fact_unit_status_history
  StatusEventID
  UnitID
  StatusID
  EventDateTime
  IsLatestStatus

fact_quality_issues
  IssueID
  UnitID
  IssueStatus
  IssueCategory
  CreatedDate
  SolvedDate

dim_status
  StatusID
  StatusName
  ProgressWeight
  ColorHex
```

In Power BI, this supports:

- status cards by workflow step
- current-status cards filtered to the latest unit event
- detailed row tables for auditability
- issue category and issue timeline visuals
- 3D model coloring by status or issue state through a shared model element key

## Dashboard Pages

| Page | Business Question | Typical Visuals |
| --- | --- | --- |
| Progress overview | What is the current progress of all facade units? | KPI cards, status distribution, current status cards, detailed table, 3D model view |
| Block overview | What is happening in a selected block, stage, level, or elevation? | same pattern scoped by filters |
| Issues overview | Where are unresolved issues concentrated? | current vs solved issues, issue category bars, issue timeline, model highlighting |
| Issue details | Which exact units/issues need follow-up? | issue table, image/link placeholders, status and category filters |

## Confidentiality Boundary

This public repo does not include:

- real employer data
- real screenshots
- real project names
- real BIM/Revit/model files
- real GUIDs or internal IDs
- PBIX/PBIP files
- API URLs or credentials
- internal refresh logic

The public assets are synthetic reconstructions designed to demonstrate the same reporting skill set without exposing private work.
