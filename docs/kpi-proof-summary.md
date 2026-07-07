# KPI Proof Summary

Generated: 2026-07-07 13:25 UTC

This file summarizes the synthetic reporting layer generated from the construction-progress dataset. It is intended as portfolio-safe proof of data modeling, KPI definition, and dashboard thinking.

## Headline KPIs

| Metric | Value | Definition |
| --- | ---: | --- |
| Projects | 3 | Synthetic construction projects. |
| Units | 6513 | Generated units/packages tracked in the model. |
| CompletionPercent | 10.2 | Units in final status divided by all units. |
| BlockedUnits | 445 | Units currently in blocked status. |
| ReworkUnits | 443 | Units currently in rework status. |
| OpenIssues | 585 | Quality issues not yet closed. |
| DelayedDeliveries | 1230 | Delivery records with positive delay. |
| DeliveredOrDelayedPercent | 81.9 | Delivery records with an actual delivery event. |

## Project Completion

| Project | Units | Complete Units | Completion % |
| --- | ---: | ---: | ---: |
| Riverside Tower | 2574 | 234 | 9.1 |
| Northline Campus | 2444 | 259 | 10.6 |
| Harbor Point | 1495 | 170 | 11.4 |

## Reviewer Notes

- The numbers come from deterministic synthetic CSV files in `data/`.
- The KPI summary can be regenerated with `python scripts/build_dashboard_preview.py`.
- No employer data, production screenshots, PBIX files, internal IDs, or confidential logic are included.
