# Construction Progress Dashboard Demo

This repository is a public, portfolio-safe Power BI demo built entirely with synthetic data. It does not contain any real company names, client names, API endpoints, BIM identifiers, screenshots, operational records, employer assets, or confidential implementation details.

The project generates a realistic fictional construction-progress dataset as CSV files that can be imported into Power BI Desktop to build a dashboard covering progress tracking, plan vs actual performance, quality issues, and deliveries.

## Portfolio Safety

Everything in this repository is generated from scratch for demonstration purposes.

It does not include:

- Real company or client data
- Real project names or IDs
- Real API URLs or internal paths
- Real BIM or model file references
- Real PBIX, PBIP, screenshots, or production extracts
- Employer-owned source code or confidential structures

## Repository Structure

```text
construction-progress-dashboard-demo/
├── README.md
├── data/
│   ├── dim_project.csv
│   ├── dim_building.csv
│   ├── dim_level.csv
│   ├── dim_zone.csv
│   ├── dim_unit.csv
│   ├── dim_status.csv
│   ├── dim_discipline.csv
│   ├── dim_contractor.csv
│   ├── fact_unit_status_history.csv
│   ├── fact_unit_plan.csv
│   ├── fact_quality_issues.csv
│   └── fact_deliveries.csv
├── docs/
│   ├── data-model.md
│   ├── dashboard-pages.md
│   └── dax-measures.md
└── scripts/
    └── generate_fake_data.py
```

## What It Demonstrates

- Synthetic data generation with deterministic output
- Star-schema modeling for Power BI
- Construction-style operational progress tracking
- Unit status history and latest-status reporting
- Plan vs actual analysis
- Quality issue monitoring
- Delivery and logistics analysis

## Quick Start

Run the generator from the repository root:

```bash
python scripts/generate_fake_data.py
```

The script writes all CSV files into `data/` and prints row counts after generation.

## Recommended Power BI Flow

1. Import all CSV files from `data/`.
2. Create relationships described in [docs/data-model.md](./docs/data-model.md).
3. Add the measures from [docs/dax-measures.md](./docs/dax-measures.md).
4. Build the report pages outlined in [docs/dashboard-pages.md](./docs/dashboard-pages.md).

## Example Reporting Questions

- How many units are complete, installed, blocked, or in rework?
- Which buildings, levels, or zones are lagging the plan?
- Which contractors have the highest issue volume?
- How many deliveries are delayed?
- Where should project teams focus next?

## Regeneration

The generator uses a deterministic seed, so rerunning it reproduces the same dataset structure and values unless the script is intentionally changed.

## License

This project is intended for learning, portfolio use, and experimentation with synthetic data.
