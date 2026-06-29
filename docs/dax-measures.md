# DAX Measures

```DAX
Total Units =
COUNTROWS ( dim_unit )

Completed Units =
CALCULATE (
    DISTINCTCOUNT ( dim_unit[UnitID] ),
    dim_status[StatusName] = "Approved"
)

Installed Units =
CALCULATE (
    DISTINCTCOUNT ( dim_unit[UnitID] ),
    dim_status[StatusName] = "Installed"
)

Blocked Units =
CALCULATE (
    DISTINCTCOUNT ( dim_unit[UnitID] ),
    dim_status[StatusName] = "Blocked"
)

Completion % =
DIVIDE ( [Completed Units], [Total Units] )

Average Progress % =
AVERAGEX (
    VALUES ( dim_unit[UnitID] ),
    RELATED ( dim_status[ProgressWeight] )
)

Planned Units =
DISTINCTCOUNT ( fact_unit_plan[UnitID] )

Actual Updated Units =
CALCULATE (
    DISTINCTCOUNT ( fact_unit_status_history[UnitID] ),
    fact_unit_status_history[IsLatestStatus] = TRUE ()
)

Plan Variance =
[Actual Updated Units] - [Planned Units]

Open Issues =
CALCULATE (
    COUNTROWS ( fact_quality_issues ),
    ISBLANK ( fact_quality_issues[ClosedDate] )
)

Delayed Deliveries =
CALCULATE (
    COUNTROWS ( fact_deliveries ),
    fact_deliveries[DelayDays] > 0
)
```

## Usage Notes

- Use `fact_unit_status_history[IsLatestStatus] = TRUE()` for current-state visuals.
- Format percentage measures such as `Completion %` and `Average Progress %` as percentages.
- If you build a dedicated current-status bridge table in Power BI, these measures can be adapted to reference that model instead.
