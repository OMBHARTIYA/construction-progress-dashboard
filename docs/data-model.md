# Data Model

This case study uses a star-schema-friendly structure centered on a synthetic construction unit. A unit represents a progress-tracked item such as a module, room package, panel, equipment set, or installation package.

## Dimension Tables

- `dim_project.csv`: project-level metadata such as project name, location, manager, and status
- `dim_building.csv`: buildings linked to projects
- `dim_level.csv`: levels linked to buildings
- `dim_zone.csv`: zones linked to levels
- `dim_unit.csv`: the main reporting grain for tracked work items
- `dim_status.csv`: status definitions and progress weights
- `dim_discipline.csv`: disciplines such as structural, mechanical, electrical, and finishes
- `dim_contractor.csv`: synthetic contractors tied to activities and issues

## Fact Tables

- `fact_unit_status_history.csv`: status events over time for each unit, including the latest event flag
- `fact_unit_plan.csv`: planned milestone dates by unit and status
- `fact_quality_issues.csv`: quality observations tied to units and contractors
- `fact_deliveries.csv`: planned and actual deliveries with delay metrics

## Relationship Overview

```text
dim_project[ProjectID] 1 -> * dim_building[ProjectID]
dim_building[BuildingID] 1 -> * dim_level[BuildingID]
dim_level[LevelID] 1 -> * dim_zone[LevelID]

dim_project[ProjectID] 1 -> * dim_unit[ProjectID]
dim_building[BuildingID] 1 -> * dim_unit[BuildingID]
dim_level[LevelID] 1 -> * dim_unit[LevelID]
dim_zone[ZoneID] 1 -> * dim_unit[ZoneID]
dim_status[StatusID] 1 -> * dim_unit[CurrentStatusID]

dim_unit[UnitID] 1 -> * fact_unit_status_history[UnitID]
dim_project[ProjectID] 1 -> * fact_unit_status_history[ProjectID]
dim_status[StatusID] 1 -> * fact_unit_status_history[StatusID]
dim_status[StatusID] 1 -> * fact_unit_status_history[PreviousStatusID]
dim_discipline[DisciplineID] 1 -> * fact_unit_status_history[DisciplineID]
dim_contractor[ContractorID] 1 -> * fact_unit_status_history[ContractorID]

dim_unit[UnitID] 1 -> * fact_unit_plan[UnitID]
dim_project[ProjectID] 1 -> * fact_unit_plan[ProjectID]
dim_status[StatusID] 1 -> * fact_unit_plan[PlannedStatusID]

dim_unit[UnitID] 1 -> * fact_quality_issues[UnitID]
dim_project[ProjectID] 1 -> * fact_quality_issues[ProjectID]
dim_contractor[ContractorID] 1 -> * fact_quality_issues[ResponsibleContractorID]

dim_unit[UnitID] 1 -> * fact_deliveries[UnitID]
dim_project[ProjectID] 1 -> * fact_deliveries[ProjectID]
dim_contractor[ContractorID] 1 -> * fact_deliveries[ContractorID]
```

## Modeling Notes

- `dim_unit` is the core analytical dimension because most business questions roll up from unit-level progress.
- `fact_unit_status_history` supports status-over-time analysis and should usually be filtered to `IsLatestStatus = TRUE` for current snapshots.
- `dim_status` includes `ProgressWeight`, which can be used to calculate weighted completion metrics.
- `fact_unit_plan` can support month-by-month plan tracking or planned milestone comparisons.
- `fact_quality_issues` and `fact_deliveries` provide operational side views often used on supporting dashboard pages.
