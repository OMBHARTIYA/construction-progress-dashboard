from __future__ import annotations

import csv
import random
from collections import Counter, defaultdict
from datetime import date, datetime, time, timedelta
from pathlib import Path


SEED = 20260629
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


STATUSES = [
    ("STS-001", "Not Started", "Planning", 1, 0.00, "FALSE"),
    ("STS-002", "Released", "Planning", 2, 0.10, "FALSE"),
    ("STS-003", "In Production", "Production", 3, 0.30, "FALSE"),
    ("STS-004", "Produced", "Production", 4, 0.50, "FALSE"),
    ("STS-005", "Delivered", "Logistics", 5, 0.70, "FALSE"),
    ("STS-006", "Installed", "Site", 6, 0.90, "FALSE"),
    ("STS-007", "Approved", "Complete", 7, 1.00, "TRUE"),
    ("STS-008", "Blocked", "Exception", 8, 0.00, "FALSE"),
    ("STS-009", "Rework", "Exception", 9, 0.40, "FALSE"),
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fmt_date(value: date | None) -> str:
    return value.isoformat() if value else ""


def fmt_datetime(value: datetime) -> str:
    return value.isoformat(sep=" ")


def random_datetime_on(day: date) -> datetime:
    return datetime.combine(day, time(hour=random.randint(6, 18), minute=random.randint(0, 59), second=random.randint(0, 59)))


def weighted_choice(values: list[str], weights: list[int]) -> str:
    return random.choices(values, weights=weights, k=1)[0]


def build_projects() -> list[dict[str, object]]:
    projects = [
        {
            "ProjectID": "PRJ-001",
            "ProjectName": "Riverside Tower",
            "ClientName": "Representative Client One",
            "Country": "United Kingdom",
            "City": "Asterford",
            "ProjectType": "Residential High-Rise",
            "StartDate": "2025-01-13",
            "PlannedEndDate": "2027-10-29",
            "ProjectManager": "Representative User 01",
            "ProjectStatus": "Execution",
        },
        {
            "ProjectID": "PRJ-002",
            "ProjectName": "Northline Campus",
            "ClientName": "Representative Client Two",
            "Country": "Germany",
            "City": "Lindenhafen",
            "ProjectType": "Mixed-Use Campus",
            "StartDate": "2025-03-03",
            "PlannedEndDate": "2027-12-17",
            "ProjectManager": "Representative User 02",
            "ProjectStatus": "Execution",
        },
        {
            "ProjectID": "PRJ-003",
            "ProjectName": "Harbor Point",
            "ClientName": "Representative Client Three",
            "Country": "Netherlands",
            "City": "Westhaven",
            "ProjectType": "Commercial Waterfront",
            "StartDate": "2025-05-19",
            "PlannedEndDate": "2028-02-25",
            "ProjectManager": "Representative User 03",
            "ProjectStatus": "Mobilization",
        },
    ]
    return projects


def build_statuses() -> list[dict[str, object]]:
    return [
        {
            "StatusID": status_id,
            "StatusName": status_name,
            "StatusGroup": status_group,
            "StatusOrder": status_order,
            "ProgressWeight": f"{progress_weight:.2f}",
            "IsFinalStatus": is_final,
        }
        for status_id, status_name, status_group, status_order, progress_weight, is_final in STATUSES
    ]


def build_disciplines() -> list[dict[str, object]]:
    raw = [
        ("DSC-001", "Structural", "Core Build"),
        ("DSC-002", "Architectural", "Finishes"),
        ("DSC-003", "Mechanical", "MEP"),
        ("DSC-004", "Electrical", "MEP"),
        ("DSC-005", "Plumbing", "MEP"),
        ("DSC-006", "Fire Protection", "Safety"),
        ("DSC-007", "Facade", "Envelope"),
        ("DSC-008", "Interior Fit-Out", "Finishes"),
    ]
    return [
        {
            "DisciplineID": discipline_id,
            "DisciplineName": discipline_name,
            "DisciplineGroup": discipline_group,
        }
        for discipline_id, discipline_name, discipline_group in raw
    ]


def build_contractors() -> list[dict[str, object]]:
    cities = ["Asterford", "Lindenhafen", "Westhaven", "Northbridge", "Elmstead", "Brookfield"]
    countries = ["United Kingdom", "Germany", "Netherlands"]
    contractor_types = ["General", "Specialist", "Logistics", "Installation", "Quality"]
    rows = []
    for index in range(1, 9):
        rows.append(
            {
                "ContractorID": f"CTR-{index:03d}",
                "ContractorName": f"Representative Contractor {chr(64 + index)}",
                "ContractorType": contractor_types[(index - 1) % len(contractor_types)],
                "Country": countries[(index - 1) % len(countries)],
                "City": cities[(index - 1) % len(cities)],
            }
        )
    return rows


def build_buildings_levels_zones(projects: list[dict[str, object]]):
    building_templates = {
        "PRJ-001": [("B1", "Tower A", "Residential"), ("B2", "Tower B", "Residential"), ("B3", "Podium", "Mixed Use")],
        "PRJ-002": [("B1", "North Block", "Office"), ("B2", "Central Block", "Laboratory"), ("B3", "South Block", "Office")],
        "PRJ-003": [("B1", "Pier East", "Commercial"), ("B2", "Pier West", "Commercial")],
    }
    level_counts = {
        "PRJ-001": [9, 9, 6],
        "PRJ-002": [8, 8, 7],
        "PRJ-003": [7, 7],
    }
    buildings = []
    levels = []
    zones = []

    for project in projects:
        project_id = project["ProjectID"]
        for building_index, (short_name, building_name, building_type) in enumerate(building_templates[project_id], start=1):
            building_id = f"BLD-{project_id[-3:]}-{building_index:02d}"
            total_floors = level_counts[project_id][building_index - 1]
            buildings.append(
                {
                    "BuildingID": building_id,
                    "ProjectID": project_id,
                    "BuildingName": building_name,
                    "BuildingType": building_type,
                    "TotalFloors": total_floors,
                }
            )

            for level_number in range(1, total_floors + 1):
                level_id = f"LVL-{project_id[-3:]}-{building_index:02d}-{level_number:02d}"
                levels.append(
                    {
                        "LevelID": level_id,
                        "BuildingID": building_id,
                        "LevelName": f"Level {level_number:02d}",
                        "LevelNumber": level_number,
                        "Elevation": round((level_number - 1) * 3.6, 1),
                    }
                )

                zone_count = 3 if (building_index + level_number) % 2 == 0 else 2
                for zone_number in range(1, zone_count + 1):
                    zone_id = f"ZON-{project_id[-3:]}-{building_index:02d}-{level_number:02d}-{zone_number:02d}"
                    area = random.randint(180, 540)
                    zones.append(
                        {
                            "ZoneID": zone_id,
                            "LevelID": level_id,
                            "ZoneName": f"Zone {zone_number:02d}",
                            "AreaM2": area,
                        }
                    )

    return buildings, levels, zones


def build_units(projects, buildings, levels, zones):
    levels_by_building = defaultdict(list)
    zones_by_level = defaultdict(list)
    building_to_project = {}

    for building in buildings:
        building_to_project[building["BuildingID"]] = building["ProjectID"]
    for level in levels:
        levels_by_building[level["BuildingID"]].append(level)
    for zone in zones:
        zones_by_level[zone["LevelID"]].append(zone)

    unit_categories = ["Apartment", "Room Package", "Service Module", "Facade Panel", "Plant Item", "Utility Rack"]
    unit_types = ["Type A", "Type B", "Type C", "Type D"]
    qty_uoms = ["EA", "SET", "M2"]
    status_ids = [row[0] for row in STATUSES]
    status_weights = [10, 9, 18, 14, 13, 12, 10, 7, 7]

    units = []
    unit_index = 1

    for building in buildings:
        project_id = building["ProjectID"]
        building_id = building["BuildingID"]
        for level in levels_by_building[building_id]:
            for zone in zones_by_level[level["LevelID"]]:
                unit_count = random.randint(35, 50)
                for zone_unit_index in range(1, unit_count + 1):
                    planned_start = date.fromisoformat(next(p["StartDate"] for p in projects if p["ProjectID"] == project_id)) + timedelta(days=random.randint(10, 540))
                    planned_finish = planned_start + timedelta(days=random.randint(12, 120))
                    current_status = weighted_choice(status_ids, status_weights)
                    category = random.choice(unit_categories)
                    units.append(
                        {
                            "UnitID": f"UNT-{unit_index:05d}",
                            "ProjectID": project_id,
                            "BuildingID": building_id,
                            "LevelID": level["LevelID"],
                            "ZoneID": zone["ZoneID"],
                            "UnitCode": f"{building_id[-2:]}-{level['LevelNumber']:02d}-{zone['ZoneName'].split()[-1]}-{zone_unit_index:03d}",
                            "UnitName": f"{category} {zone_unit_index:03d}",
                            "UnitCategory": category,
                            "UnitType": random.choice(unit_types),
                            "PlannedQuantity": random.randint(1, 12) if category != "Facade Panel" else random.randint(4, 20),
                            "QuantityUOM": random.choice(qty_uoms),
                            "PlannedStartDate": fmt_date(planned_start),
                            "PlannedFinishDate": fmt_date(planned_finish),
                            "CurrentStatusID": current_status,
                            "IsCritical": "TRUE" if random.random() < 0.16 else "FALSE",
                        }
                    )
                    unit_index += 1

    return units


def build_status_history(units, projects, disciplines, contractors):
    project_start = {project["ProjectID"]: date.fromisoformat(project["StartDate"]) for project in projects}
    discipline_ids = [row["DisciplineID"] for row in disciplines]
    contractor_ids = [row["ContractorID"] for row in contractors]
    progression = ["STS-001", "STS-002", "STS-003", "STS-004", "STS-005", "STS-006", "STS-007"]
    status_history = []
    event_index = 1

    for unit in units:
        current_status = unit["CurrentStatusID"]
        if current_status in progression:
            max_step = progression.index(current_status)
            sequence = progression[: max_step + 1]
        elif current_status == "STS-008":
            step = random.randint(1, 5)
            sequence = progression[:step] + ["STS-008"]
        else:
            step = random.randint(2, 5)
            sequence = progression[:step] + ["STS-009", progression[min(step, len(progression) - 1)]]

        event_day = max(project_start[unit["ProjectID"]], date.fromisoformat(unit["PlannedStartDate"]) - timedelta(days=random.randint(0, 20)))
        prev_status = ""
        prev_date = event_day
        for seq_index, status_id in enumerate(sequence):
            if seq_index == 0:
                event_day = event_day + timedelta(days=random.randint(0, 10))
                days_prev = 0
            else:
                jump = random.randint(3, 28)
                event_day = event_day + timedelta(days=jump)
                days_prev = (event_day - prev_date).days
            event_dt = random_datetime_on(event_day)
            status_history.append(
                {
                    "StatusEventID": f"EVT-{event_index:06d}",
                    "UnitID": unit["UnitID"],
                    "ProjectID": unit["ProjectID"],
                    "StatusID": status_id,
                    "DisciplineID": random.choice(discipline_ids),
                    "ContractorID": random.choice(contractor_ids),
                    "EventDate": fmt_date(event_day),
                    "EventDateTime": fmt_datetime(event_dt),
                    "PreviousStatusID": prev_status,
                    "DaysInPreviousStatus": days_prev,
                    "UpdatedBy": f"Representative User {random.randint(1, 18):02d}",
                    "SourceSystem": "Synthetic Progress Tracker",
                    "Comment": random.choice(
                        [
                            "Synthetic update generated for portfolio reporting.",
                            "Planned workflow transition for portfolio dataset.",
                            "Representative progress event created from scripted scenario.",
                            "Synthetic site update for dashboard testing.",
                        ]
                    ),
                    "IsLatestStatus": "FALSE",
                }
            )
            prev_status = status_id
            prev_date = event_day
            event_index += 1

    latest_event_by_unit = {}
    for row in status_history:
        latest_event_by_unit[row["UnitID"]] = row["StatusEventID"]
    for row in status_history:
        if latest_event_by_unit[row["UnitID"]] == row["StatusEventID"]:
            row["IsLatestStatus"] = "TRUE"

    return status_history


def build_unit_plan(units):
    planned_statuses = ["STS-002", "STS-004", "STS-005", "STS-006", "STS-007"]
    offsets = {
        "STS-002": -5,
        "STS-004": 20,
        "STS-005": 35,
        "STS-006": 60,
        "STS-007": 85,
    }
    rows = []
    plan_index = 1
    for unit in units:
        planned_start = date.fromisoformat(unit["PlannedStartDate"])
        for status_id in planned_statuses:
            planned_date = planned_start + timedelta(days=offsets[status_id] + random.randint(-7, 10))
            rows.append(
                {
                    "PlanID": f"PLN-{plan_index:06d}",
                    "UnitID": unit["UnitID"],
                    "ProjectID": unit["ProjectID"],
                    "PlannedStatusID": status_id,
                    "PlannedDate": fmt_date(planned_date),
                    "PlannedQuantity": unit["PlannedQuantity"],
                    "BaselineVersion": random.choice(["BL-01", "BL-02"]),
                    "PlanMonth": planned_date.strftime("%Y-%m"),
                }
            )
            plan_index += 1
    return rows


def build_quality_issues(units, contractors):
    contractor_ids = [row["ContractorID"] for row in contractors]
    issue_types = ["Dimensional", "Surface Finish", "Missing Component", "Documentation", "Alignment", "Damage"]
    severities = ["Low", "Medium", "High", "Critical"]
    statuses = ["Open", "In Review", "Closed"]
    rows = []
    issue_index = 1
    selected_units = random.sample(units, 1100)
    for unit in selected_units:
        issue_date = date.fromisoformat(unit["PlannedStartDate"]) + timedelta(days=random.randint(0, 140))
        issue_status = weighted_choice(statuses, [35, 20, 45])
        if issue_status == "Closed":
            closed_date = issue_date + timedelta(days=random.randint(2, 35))
            days_open = (closed_date - issue_date).days
        else:
            closed_date = None
            days_open = (date(2026, 6, 29) - issue_date).days
        rows.append(
            {
                "IssueID": f"ISS-{issue_index:06d}",
                "UnitID": unit["UnitID"],
                "ProjectID": unit["ProjectID"],
                "IssueDate": fmt_date(issue_date),
                "IssueType": random.choice(issue_types),
                "Severity": weighted_choice(severities, [30, 35, 25, 10]),
                "IssueStatus": issue_status,
                "ClosedDate": fmt_date(closed_date),
                "ResponsibleContractorID": random.choice(contractor_ids),
                "DaysOpen": days_open,
            }
        )
        issue_index += 1
    return rows


def build_deliveries(units, contractors):
    contractor_ids = [row["ContractorID"] for row in contractors]
    rows = []
    delivery_index = 1
    selected_units = random.sample(units, 1900)
    for unit in selected_units:
        planned = date.fromisoformat(unit["PlannedStartDate"]) - timedelta(days=random.randint(15, 60))
        delay = random.randint(-4, 18)
        actual = planned + timedelta(days=max(delay, 0)) if random.random() < 0.82 else None
        status = "Planned"
        delay_days = 0
        if actual:
            delay_days = (actual - planned).days
            if delay_days > 0:
                status = "Delayed"
            else:
                status = "Delivered"
        rows.append(
            {
                "DeliveryID": f"DLV-{delivery_index:06d}",
                "UnitID": unit["UnitID"],
                "ProjectID": unit["ProjectID"],
                "ContractorID": random.choice(contractor_ids),
                "PlannedDeliveryDate": fmt_date(planned),
                "ActualDeliveryDate": fmt_date(actual),
                "DeliveryStatus": status,
                "QuantityDelivered": unit["PlannedQuantity"],
                "TransportBatch": f"TB-{planned.strftime('%y%m')}-{random.randint(1, 45):03d}",
                "DelayDays": delay_days,
            }
        )
        delivery_index += 1
    return rows


def validate_data(units, projects, buildings, levels, zones, statuses, contractors, facts):
    project_ids = {row["ProjectID"] for row in projects}
    building_ids = {row["BuildingID"] for row in buildings}
    level_ids = {row["LevelID"] for row in levels}
    zone_ids = {row["ZoneID"] for row in zones}
    unit_ids = {row["UnitID"] for row in units}
    status_ids = {row["StatusID"] for row in statuses}
    contractor_ids = {row["ContractorID"] for row in contractors}

    for unit in units:
        assert unit["ProjectID"] in project_ids
        assert unit["BuildingID"] in building_ids
        assert unit["LevelID"] in level_ids
        assert unit["ZoneID"] in zone_ids
        assert unit["CurrentStatusID"] in status_ids

    for row in facts["fact_unit_status_history"]:
        assert row["UnitID"] in unit_ids
        assert row["ProjectID"] in project_ids
        assert row["StatusID"] in status_ids
        assert row["ContractorID"] in contractor_ids
        if row["PreviousStatusID"]:
            assert row["PreviousStatusID"] in status_ids

    for row in facts["fact_unit_plan"]:
        assert row["UnitID"] in unit_ids
        assert row["ProjectID"] in project_ids
        assert row["PlannedStatusID"] in status_ids

    for row in facts["fact_quality_issues"]:
        assert row["UnitID"] in unit_ids
        assert row["ProjectID"] in project_ids
        assert row["ResponsibleContractorID"] in contractor_ids

    for row in facts["fact_deliveries"]:
        assert row["UnitID"] in unit_ids
        assert row["ProjectID"] in project_ids
        assert row["ContractorID"] in contractor_ids

    latest_count = Counter()
    for row in facts["fact_unit_status_history"]:
        if row["IsLatestStatus"] == "TRUE":
            latest_count[row["UnitID"]] += 1
    assert all(count == 1 for count in latest_count.values())
    assert len(latest_count) == len(units)


def main() -> None:
    projects = build_projects()
    statuses = build_statuses()
    disciplines = build_disciplines()
    contractors = build_contractors()
    buildings, levels, zones = build_buildings_levels_zones(projects)
    units = build_units(projects, buildings, levels, zones)
    status_history = build_status_history(units, projects, disciplines, contractors)
    unit_plan = build_unit_plan(units)
    quality_issues = build_quality_issues(units, contractors)
    deliveries = build_deliveries(units, contractors)

    facts = {
        "fact_unit_status_history": status_history,
        "fact_unit_plan": unit_plan,
        "fact_quality_issues": quality_issues,
        "fact_deliveries": deliveries,
    }
    validate_data(units, projects, buildings, levels, zones, statuses, contractors, facts)

    datasets = {
        "dim_project.csv": (
            ["ProjectID", "ProjectName", "ClientName", "Country", "City", "ProjectType", "StartDate", "PlannedEndDate", "ProjectManager", "ProjectStatus"],
            projects,
        ),
        "dim_building.csv": (
            ["BuildingID", "ProjectID", "BuildingName", "BuildingType", "TotalFloors"],
            buildings,
        ),
        "dim_level.csv": (
            ["LevelID", "BuildingID", "LevelName", "LevelNumber", "Elevation"],
            levels,
        ),
        "dim_zone.csv": (
            ["ZoneID", "LevelID", "ZoneName", "AreaM2"],
            zones,
        ),
        "dim_unit.csv": (
            [
                "UnitID",
                "ProjectID",
                "BuildingID",
                "LevelID",
                "ZoneID",
                "UnitCode",
                "UnitName",
                "UnitCategory",
                "UnitType",
                "PlannedQuantity",
                "QuantityUOM",
                "PlannedStartDate",
                "PlannedFinishDate",
                "CurrentStatusID",
                "IsCritical",
            ],
            units,
        ),
        "dim_status.csv": (
            ["StatusID", "StatusName", "StatusGroup", "StatusOrder", "ProgressWeight", "IsFinalStatus"],
            statuses,
        ),
        "dim_discipline.csv": (
            ["DisciplineID", "DisciplineName", "DisciplineGroup"],
            disciplines,
        ),
        "dim_contractor.csv": (
            ["ContractorID", "ContractorName", "ContractorType", "Country", "City"],
            contractors,
        ),
        "fact_unit_status_history.csv": (
            [
                "StatusEventID",
                "UnitID",
                "ProjectID",
                "StatusID",
                "DisciplineID",
                "ContractorID",
                "EventDate",
                "EventDateTime",
                "PreviousStatusID",
                "DaysInPreviousStatus",
                "UpdatedBy",
                "SourceSystem",
                "Comment",
                "IsLatestStatus",
            ],
            status_history,
        ),
        "fact_unit_plan.csv": (
            ["PlanID", "UnitID", "ProjectID", "PlannedStatusID", "PlannedDate", "PlannedQuantity", "BaselineVersion", "PlanMonth"],
            unit_plan,
        ),
        "fact_quality_issues.csv": (
            ["IssueID", "UnitID", "ProjectID", "IssueDate", "IssueType", "Severity", "IssueStatus", "ClosedDate", "ResponsibleContractorID", "DaysOpen"],
            quality_issues,
        ),
        "fact_deliveries.csv": (
            ["DeliveryID", "UnitID", "ProjectID", "ContractorID", "PlannedDeliveryDate", "ActualDeliveryDate", "DeliveryStatus", "QuantityDelivered", "TransportBatch", "DelayDays"],
            deliveries,
        ),
    }

    for filename, (fieldnames, rows) in datasets.items():
        write_csv(DATA_DIR / filename, fieldnames, rows)

    print("Synthetic construction progress dataset generated successfully.")
    print(f"Seed: {SEED}")
    for filename, (_, rows) in datasets.items():
        print(f"{filename}: {len(rows)} rows")


if __name__ == "__main__":
    main()
