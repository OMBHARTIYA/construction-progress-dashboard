from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DATA = ROOT / "data"
DOCS = ROOT / "docs"

STATUS_COLORS = {
    "Prepared": "#b35bb6",
    "Assembled": "#65a34a",
    "Glazed": "#4db8c8",
    "Packed": "#8170b4",
    "Produced": "#df7430",
    "In Stock": "#4d86bf",
    "Out Stock": "#be3d40",
    "Delivered": "#f2c500",
    "Installed": "#33b36f",
    "Accepted": "#1685f2",
}

ISSUE_COLORS = {
    "Current": "#e85b00",
    "Solved": "#00a98f",
}


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pct(value: int, total: int) -> str:
    return f"{(value / total * 100):.1f}%" if total else "0.0%"


def rect(x: int, y: int, width: int, height: int, fill: str, stroke: str = "#d7d7d7", radius: int = 8) -> str:
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def text(x: int, y: int, value: str, cls: str = "body", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'


def status_tiles(x: int, y: int, rows: list[dict[str, object]], total: int, show_pct: bool) -> str:
    parts = []
    tile_w = 52
    tile_gap = 4
    for index, row in enumerate(rows):
        sx = x + index * (tile_w + tile_gap)
        status = str(row["Status"])
        count = int(row["Units"])
        parts.append(rect(sx, y, tile_w, 76, STATUS_COLORS[status], "#6f6f6f", 2))
        parts.append(f'<rect x="{sx + 5}" y="{y + 8}" width="{tile_w - 10}" height="26" rx="5" fill="#ffffff" opacity="0.18"/>')
        parts.append(text(sx + tile_w / 2, y + 28, status, "tile-label", "middle"))
        parts.append(text(sx + tile_w / 2, y + 49, f"{count:,}", "tile-value", "middle"))
        if show_pct:
            parts.append(text(sx + tile_w / 2, y + 68, pct(count, total), "tile-pct", "middle"))
    return "\n".join(parts)


def model_preview(x: int, y: int, installed_color: str = "#33b36f", issue_color: str | None = None) -> str:
    parts = [rect(x, y, 462, 470, "#eef5f7", "#ff6a2d", 6)]
    parts.append(text(x + 16, y + 28, "3D model preview", "panel-title"))
    tower_x = x + 170
    tower_y = y + 72
    cell = 10
    rows = 28
    cols = 18
    for row in range(rows):
        row_width = cols - max(0, row - 20) // 2
        offset = max(0, row - 20) * 4
        for col in range(row_width):
            sx = tower_x + col * cell + offset
            sy = tower_y + row * cell
            color = "#f7f7f7"
            if 11 <= row <= 16 and col in {2, 3, 5, 8, 9, 13, 14}:
                color = issue_color or installed_color
            if row >= 21 and col in {1, 2, 3, 7, 8, 12, 13, 14}:
                color = installed_color
            parts.append(f'<rect x="{sx}" y="{sy}" width="{cell}" height="{cell}" fill="{color}" stroke="#4b4b4b" stroke-width="0.45"/>')
    parts.append(f'<polygon points="{tower_x + 20},{tower_y + 285} {tower_x + 210},{tower_y + 250} {tower_x + 210},{tower_y + 300} {tower_x + 20},{tower_y + 335}" fill="#e8e8e8" opacity="0.55"/>')
    parts.append(text(x + 354, y + 444, "Local model layer", "small"))
    return "\n".join(parts)


def build_progress_svg(status_rows: list[dict[str, object]], current_rows: list[dict[str, object]], total_units: int) -> str:
    kpis = [
        ("Total Units", f"{total_units:,}"),
        ("Units In Progress", "3,420"),
        ("Units Installed", "1,586"),
        ("Not Started", "18,940"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">',
        STYLE,
        rect(0, 0, 1280, 720, "#f7f7f7", "#f7f7f7", 0),
        rect(18, 18, 84, 34, "#ffffff", "#ff3030", 10),
        text(60, 41, "DEMO", "brand", "middle"),
        rect(116, 18, 316, 34, "#ffffff", "#ff3030", 10),
        text(274, 41, "FACADE PROGRESS OVERVIEW", "title-red", "middle"),
    ]
    for index, (label, value) in enumerate(kpis):
        x = 512 + index * 128
        parts.append(rect(x, 18, 116, 34, "#ffffff", "#ff3030", 10))
        parts.append(text(x + 58, 34, label, "kpi-label", "middle"))
        parts.append(text(x + 58, 50, value, "kpi-value", "middle"))
    parts.extend(
        [
            rect(22, 70, 98, 54, "#ffffff", "#2a2a2a", 6),
            text(71, 103, "CLEAR", "filter-label", "middle"),
        ]
    )
    for index, label in enumerate(["Date", "Stage", "BOM Number", "Block ID", "Level", "Elevation", "Unit Name"]):
        x = 132 + index * 144
        parts.append(rect(x, 70, 134, 54, "#ffffff", "#2a2a2a", 6))
        parts.append(text(x + 12, 92, label, "filter-label"))
        parts.append(text(x + 12, 114, "All", "muted"))
    parts.extend(
        [
            rect(22, 140, 588, 126, "#eeeeee", "#ff3030", 5),
            text(34, 165, "Unit Status Distribution", "panel-title"),
            status_tiles(48, 186, status_rows, total_units, True),
            rect(22, 278, 588, 126, "#eeeeee", "#ff3030", 5),
            text(34, 303, "Current Units Status", "panel-title"),
            status_tiles(48, 324, current_rows, sum(int(row["Units"]) for row in current_rows), False),
            rect(22, 416, 588, 266, "#eeeeee", "#ff3030", 5),
            text(34, 441, "Detailed Data Summary", "panel-title"),
            table_preview(40, 462),
            model_preview(622, 140),
            "</svg>",
        ]
    )
    return "\n".join(parts)


def table_preview(x: int, y: int) -> str:
    headers = ["DateTime", "BOM", "Block", "Unit", "Level", "Elevation", "Status"]
    rows = [
        ["09-Apr-26", "A12-P01", "B-18", "U52", "18", "East", "Installed"],
        ["09-Apr-26", "A12-P01", "B-18", "U53", "18", "East", "Installed"],
        ["09-Apr-26", "A12-P02", "B-19", "U10", "19", "North", "Delivered"],
        ["09-Apr-26", "A12-P02", "B-19", "U11", "19", "North", "In Stock"],
        ["09-Apr-26", "A12-P03", "B-20", "U02", "20", "West", "Produced"],
        ["09-Apr-26", "A12-P03", "B-20", "U03", "20", "West", "Glazed"],
    ]
    parts = [rect(x, y, 548, 192, "#dcdcdc", "#7a7a7a", 0)]
    col_w = [86, 74, 62, 62, 58, 86, 94]
    cx = x
    for width, header in zip(col_w, headers):
        parts.append(f'<rect x="{cx}" y="{y}" width="{width}" height="28" fill="#8c8c8c" stroke="#5d5d5d"/>')
        parts.append(text(cx + 6, y + 20, header, "table-head"))
        cx += width
    for row_index, row in enumerate(rows):
        cx = x
        ry = y + 28 + row_index * 26
        for width, value in zip(col_w, row):
            parts.append(f'<rect x="{cx}" y="{ry}" width="{width}" height="26" fill="#eeeeee" stroke="#999999"/>')
            parts.append(text(cx + 6, ry + 18, value, "table-cell"))
            cx += width
    return "\n".join(parts)


def build_issue_svg(status_rows: list[dict[str, object]], total_units: int) -> str:
    issue_categories = [
        ("Warehouse - material defects", 14, "#c83a3a"),
        ("Warehouse - quantities", 48, "#63a8d6"),
        ("CNC Department", 70, "#eee9d6"),
        ("Technical Department", 161, "#ffd43b"),
        ("Production Department", 188, "#f4772e"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">',
        STYLE,
        rect(0, 0, 1280, 720, "#f7f7f7", "#f7f7f7", 0),
        rect(18, 18, 84, 34, "#ffffff", "#ff3030", 10),
        text(60, 41, "DEMO", "brand", "middle"),
        rect(116, 18, 316, 34, "#ffffff", "#ff3030", 10),
        text(274, 41, "FACADE ISSUES OVERVIEW", "title-red", "middle"),
        rect(512, 18, 116, 34, "#ffffff", "#ff3030", 10),
        text(570, 34, "Open Issues", "kpi-label", "middle"),
        text(570, 50, "5", "kpi-value", "middle"),
        rect(642, 18, 116, 34, "#ffffff", "#ff3030", 10),
        text(700, 34, "Solved Issues", "kpi-label", "middle"),
        text(700, 50, "481", "kpi-value", "middle"),
        rect(22, 70, 588, 94, "#eeeeee", "#ff3030", 5),
        text(34, 95, "Current Issues Status", "panel-title"),
        text(42, 127, "Current", "body-bold"),
        f'<rect x="120" y="112" width="18" height="18" fill="{ISSUE_COLORS["Current"]}"/>',
        text(146, 127, "5", "body"),
        text(42, 152, "Solved", "body-bold"),
        f'<rect x="120" y="137" width="316" height="18" fill="{ISSUE_COLORS["Solved"]}"/>',
        text(446, 152, "481", "body"),
        rect(22, 176, 588, 116, "#eeeeee", "#ff3030", 5),
        text(34, 201, "Current Units Status", "panel-title"),
        status_tiles(48, 222, status_rows[:7], total_units, False),
        rect(22, 306, 588, 190, "#eeeeee", "#ff3030", 5),
        text(34, 331, "Issue Category", "panel-title"),
    ]
    for index, (label, value, color) in enumerate(issue_categories):
        y = 358 + index * 27
        parts.append(text(42, y + 16, label, "body-bold"))
        parts.append(f'<rect x="230" y="{y}" width="{value * 2}" height="19" fill="{color}" stroke="#333"/>')
        parts.append(text(244 + value * 2, y + 16, str(value), "body"))
    parts.extend(
        [
            rect(22, 510, 588, 166, "#eeeeee", "#ff3030", 5),
            text(34, 535, "Issue Status Timeline", "panel-title"),
            timeline_svg(52, 556),
            model_preview(622, 70, "#33b36f", "#00a98f"),
            "</svg>",
        ]
    )
    return "\n".join(parts)


def timeline_svg(x: int, y: int) -> str:
    solved = [44, 64, 49, 169, 120, 20]
    current = [0, 0, 0, 2, 3, 0]
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]
    parts = []
    for tick in [0, 50, 100, 150, 200]:
        yy = y + 110 - tick / 2
        parts.append(f'<line x1="{x}" y1="{yy}" x2="{x + 500}" y2="{yy}" stroke="#d6d6d6" stroke-dasharray="2 5"/>')
        parts.append(text(x - 8, int(yy + 4), str(tick), "small", "end"))
    points = []
    current_points = []
    for index, value in enumerate(solved):
        px = x + index * 92
        py = y + 110 - value / 2
        points.append(f"{px},{py}")
        parts.append(text(px, int(py - 8), str(value), "small", "middle"))
        parts.append(text(px, y + 132, months[index], "small", "middle"))
    for index, value in enumerate(current):
        px = x + index * 92
        py = y + 110 - value / 2
        current_points.append(f"{px},{py}")
    parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="#00a98f" stroke-width="3"/>')
    parts.append(f'<polyline points="{" ".join(current_points)}" fill="none" stroke="#e85b00" stroke-width="3"/>')
    return "\n".join(parts)


STYLE = """<style>
  .brand { font: 800 17px Arial, sans-serif; fill: #ff2020; }
  .title-red { font: 800 16px Arial, sans-serif; fill: #ff2020; }
  .kpi-label { font: 600 11px Arial, sans-serif; fill: #ff2020; }
  .kpi-value { font: 800 13px Arial, sans-serif; fill: #111; }
  .filter-label { font: 700 13px Arial, sans-serif; fill: #1d1d1d; }
  .muted { font: 400 13px Arial, sans-serif; fill: #777; }
  .panel-title { font: 800 16px Arial, sans-serif; fill: #111; }
  .body { font: 400 13px Arial, sans-serif; fill: #111; }
  .body-bold { font: 700 13px Arial, sans-serif; fill: #111; }
  .small { font: 400 11px Arial, sans-serif; fill: #555; }
  .tile-label { font: 400 8.5px Arial, sans-serif; fill: #1f2730; }
  .tile-value { font: 800 11px Arial, sans-serif; fill: #111; }
  .tile-pct { font: 800 10px Arial, sans-serif; fill: #fff; }
  .table-head { font: 700 12px Arial, sans-serif; fill: #111; }
  .table-cell { font: 400 11px Arial, sans-serif; fill: #333; }
</style>"""


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    DATA.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)

    status_rows = [
        {"Status": "Prepared", "Units": 5040},
        {"Status": "Assembled", "Units": 5008},
        {"Status": "Glazed", "Units": 4996},
        {"Status": "Packed", "Units": 4962},
        {"Status": "Produced", "Units": 5140},
        {"Status": "In Stock", "Units": 1550},
        {"Status": "Out Stock", "Units": 1486},
        {"Status": "Delivered", "Units": 1372},
        {"Status": "Installed", "Units": 1586},
        {"Status": "Accepted", "Units": 1},
    ]
    current_rows = [
        {"Status": "Prepared", "Units": 3},
        {"Status": "Assembled", "Units": 3},
        {"Status": "Glazed", "Units": 6},
        {"Status": "Packed", "Units": 1},
        {"Status": "Produced", "Units": 3480},
        {"Status": "In Stock", "Units": 56},
        {"Status": "Out Stock", "Units": 11},
        {"Status": "Delivered", "Units": 85},
        {"Status": "Installed", "Units": 1586},
    ]
    total_units = 25452

    write_csv(DATA / "facade_status_workflow_summary.csv", status_rows)
    write_csv(DATA / "facade_current_status_snapshot.csv", current_rows)
    (ASSETS / "facade-progress-preview.svg").write_text(build_progress_svg(status_rows, current_rows, total_units), encoding="utf-8")
    (ASSETS / "facade-issues-preview.svg").write_text(build_issue_svg(current_rows, total_units), encoding="utf-8")

    status_counter = Counter({row["Status"]: row["Units"] for row in status_rows})
    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    case_study = [
        "# Facade Progress Dashboard Case Study",
        "",
        f"Generated: {generated_at}",
        "",
        "This is a public, synthetic reconstruction of the kind of facade-progress analytics workflow represented in this repository. It is not a screenshot, export, data extract, or model from any employer system.",
        "",
        "## What The Original Type Of Dashboard Solves",
        "",
        "- Tracks facade units through a multi-step operational workflow.",
        "- Lets users filter by date, stage, BOM/package number, block, level, elevation, unit, and stillage/package.",
        "- Connects tabular progress data with a 3D model-style visual layer.",
        "- Shows current unit status, full status distribution, detailed rows, issue categories, and issue timeline.",
        "- Separates progress reporting from issue reporting while keeping shared filters and model context.",
        "",
        "## Synthetic Status Snapshot",
        "",
        "| Status | Units | Share of Synthetic Total |",
        "| --- | ---: | ---: |",
    ]
    case_study.extend(
        f"| {status} | {count:,} | {pct(count, total_units)} |" for status, count in status_counter.items()
    )
    case_study.extend(
        [
            "",
            "## Public Proof Assets",
            "",
            "- [Synthetic facade progress preview](../assets/facade-progress-preview.svg)",
            "- [Synthetic facade issues preview](../assets/facade-issues-preview.svg)",
            "- `data/facade_status_workflow_summary.csv`",
            "- `data/facade_current_status_snapshot.csv`",
            "",
            "## Confidentiality Boundary",
            "",
            "The public repo intentionally excludes real project names, real model files, real BIM/Revit GUIDs, employer branding, Power BI PBIX files, screenshots, API URLs, credentials, and operational records.",
        ]
    )
    (DOCS / "facade-dashboard-case-study.md").write_text("\n".join(case_study) + "\n", encoding="utf-8")
    print("Wrote synthetic facade dashboard case study assets.")


if __name__ == "__main__":
    main()
