from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pct(numerator: float, denominator: float) -> float:
    return round((numerator / denominator * 100), 1) if denominator else 0.0


def svg_card(x: int, y: int, title: str, value: str, subtitle: str, fill: str) -> str:
    return f"""
    <rect x="{x}" y="{y}" width="230" height="112" rx="10" fill="{fill}" stroke="#d8e5e5"/>
    <text x="{x + 18}" y="{y + 34}" class="label">{escape(title)}</text>
    <text x="{x + 18}" y="{y + 72}" class="metric">{escape(value)}</text>
    <text x="{x + 18}" y="{y + 96}" class="small">{escape(subtitle)}</text>
    """


def svg_bar(x: int, y: int, width: int, label: str, value: float, fill: str) -> str:
    bar_width = max(4, int(width * value / 100))
    return f"""
    <text x="{x}" y="{y - 7}" class="small">{escape(label)} {value:.1f}%</text>
    <rect x="{x}" y="{y}" width="{width}" height="16" rx="4" fill="#edf3f3"/>
    <rect x="{x}" y="{y}" width="{bar_width}" height="16" rx="4" fill="{fill}"/>
    """


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)

    projects = read_csv("dim_project.csv")
    units = read_csv("dim_unit.csv")
    statuses = {row["StatusID"]: row for row in read_csv("dim_status.csv")}
    issues = read_csv("fact_quality_issues.csv")
    deliveries = read_csv("fact_deliveries.csv")

    total_units = len(units)
    status_counts = Counter(unit["CurrentStatusID"] for unit in units)
    final_status_ids = {sid for sid, row in statuses.items() if row["IsFinalStatus"] == "TRUE"}
    complete_units = sum(count for sid, count in status_counts.items() if sid in final_status_ids)
    blocked_units = status_counts.get("STS-008", 0)
    rework_units = status_counts.get("STS-009", 0)
    open_issues = sum(1 for row in issues if row["IssueStatus"] != "Closed")
    delayed_deliveries = sum(1 for row in deliveries if row["DeliveryStatus"] == "Delayed")
    delivered_or_delayed = sum(1 for row in deliveries if row["DeliveryStatus"] in {"Delivered", "Delayed"})

    project_unit_counts = Counter(unit["ProjectID"] for unit in units)
    project_complete = defaultdict(int)
    for unit in units:
        if unit["CurrentStatusID"] in final_status_ids:
            project_complete[unit["ProjectID"]] += 1

    project_rows = []
    for project in projects:
        project_id = project["ProjectID"]
        unit_count = project_unit_counts[project_id]
        project_rows.append(
            {
                "ProjectID": project_id,
                "ProjectName": project["ProjectName"],
                "Units": unit_count,
                "CompleteUnits": project_complete[project_id],
                "CompletionPercent": pct(project_complete[project_id], unit_count),
            }
        )

    kpis = [
        {"Metric": "Projects", "Value": len(projects), "Definition": "Synthetic construction projects."},
        {"Metric": "Units", "Value": total_units, "Definition": "Generated units/packages tracked in the model."},
        {"Metric": "CompletionPercent", "Value": pct(complete_units, total_units), "Definition": "Units in final status divided by all units."},
        {"Metric": "BlockedUnits", "Value": blocked_units, "Definition": "Units currently in blocked status."},
        {"Metric": "ReworkUnits", "Value": rework_units, "Definition": "Units currently in rework status."},
        {"Metric": "OpenIssues", "Value": open_issues, "Definition": "Quality issues not yet closed."},
        {"Metric": "DelayedDeliveries", "Value": delayed_deliveries, "Definition": "Delivery records with positive delay."},
        {"Metric": "DeliveredOrDelayedPercent", "Value": pct(delivered_or_delayed, len(deliveries)), "Definition": "Delivery records with an actual delivery event."},
    ]
    write_csv(DATA / "reporting_kpis.csv", kpis)

    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    markdown = [
        "# KPI Proof Summary",
        "",
        f"Generated: {generated_at}",
        "",
        "This file summarizes the synthetic reporting layer generated from the construction-progress dataset. It is intended as portfolio-safe proof of data modeling, KPI definition, and dashboard thinking.",
        "",
        "## Headline KPIs",
        "",
        "| Metric | Value | Definition |",
        "| --- | ---: | --- |",
    ]
    markdown.extend(f"| {row['Metric']} | {row['Value']} | {row['Definition']} |" for row in kpis)
    markdown.extend(
        [
            "",
            "## Project Completion",
            "",
            "| Project | Units | Complete Units | Completion % |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    markdown.extend(
        f"| {row['ProjectName']} | {row['Units']} | {row['CompleteUnits']} | {row['CompletionPercent']} |"
        for row in project_rows
    )
    markdown.extend(
        [
            "",
            "## Reviewer Notes",
            "",
            "- The numbers come from deterministic synthetic CSV files in `data/`.",
            "- The KPI summary can be regenerated with `python scripts/build_dashboard_preview.py`.",
            "- No employer data, production screenshots, PBIX files, internal IDs, or confidential logic are included.",
        ]
    )
    (DOCS / "kpi-proof-summary.md").write_text("\n".join(markdown) + "\n", encoding="utf-8")

    colors = ["#00756f", "#d83a34", "#f2a52b"]
    bars = []
    for index, row in enumerate(project_rows):
        bars.append(svg_bar(70, 390 + index * 58, 500, row["ProjectName"], float(row["CompletionPercent"]), colors[index % len(colors)]))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620">
  <style>
    .title {{ font: 700 34px Arial, sans-serif; fill: #12202a; }}
    .subtitle {{ font: 400 16px Arial, sans-serif; fill: #5b6a72; }}
    .label {{ font: 700 15px Arial, sans-serif; fill: #25333b; }}
    .metric {{ font: 800 32px Arial, sans-serif; fill: #12202a; }}
    .small {{ font: 400 13px Arial, sans-serif; fill: #5b6a72; }}
  </style>
  <rect width="1000" height="620" fill="#fbfcfc"/>
  <rect x="38" y="34" width="924" height="552" rx="18" fill="#ffffff" stroke="#dce6e6"/>
  <text x="70" y="92" class="title">Construction Progress Dashboard Preview</text>
  <text x="70" y="124" class="subtitle">Synthetic Power BI-ready data model: progress, quality, delivery, and exception tracking.</text>
  {svg_card(70, 170, "Tracked Units", f"{total_units:,}", "Synthetic unit/package records", "#e3f4f1")}
  {svg_card(305, 170, "Completion", f"{pct(complete_units, total_units):.1f}%", "Units in final status", "#fff5dd")}
  {svg_card(540, 170, "Open Issues", f"{open_issues:,}", "Quality actions not closed", "#fff0f1")}
  {svg_card(775, 170, "Delayed Deliveries", f"{delayed_deliveries:,}", "Positive delivery delay", "#f2eefc")}
  <text x="70" y="342" class="label">Completion by project</text>
  {''.join(bars)}
  <text x="70" y="575" class="small">Generated from deterministic synthetic CSV data. Safe for public portfolio review.</text>
</svg>
"""
    (ASSETS / "dashboard-preview.svg").write_text(svg, encoding="utf-8")

    print("Wrote data/reporting_kpis.csv")
    print("Wrote docs/kpi-proof-summary.md")
    print("Wrote assets/dashboard-preview.svg")


if __name__ == "__main__":
    main()
