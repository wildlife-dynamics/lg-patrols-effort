# LG Patrols Effort Workflow

This guide walks you through loading, configuring, and running the LG Patrols Effort Workflow, which generates a patrol effort analysis report for Lion Guardians rangers in the Amboseli ecosystem sourced from EarthRanger.

---

## What it produces

The workflow produces, for each patrol group:

- A **Patrol Events map** (scatter plot of events, coloured by event type)
- A **Patrol Trajectories map** (tracks in a single fixed colour)
- A **Linear Time Density map** (patrol coverage heat map)
- A **time series bar chart** and **pie chart** of patrol events
- **Summary CSV tables** — per guardian, event type, and monthly breakdown
- A **Word document report** (`.docx`) with a cover page and one section per group
- An **interactive widget dashboard**

---

## Requirements

- Access to an **EarthRanger** instance with a configured data source
- The patrol types and event types you want to analyse (leave blank to include all)

> The two study-area boundaries (Conservancies and Group Ranch Boundaries) are fetched live from EarthRanger — no local files are required. Only the Word report templates and the organisation logo are downloaded automatically from Dropbox.

---

## 1. Load the Workflow

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste this repository's URL into the **Github Link** field, then click **Add Template**:

```
https://github.com/wildlife-dynamics/lg-patrols-effort.git
```

Once added, it appears in the **Workflow Templates** list as **lg-patrols-effort**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

You'll also need an **EarthRanger data source connection** configured beforehand (via **Data Sources** in the runner) — patrol tracks and events are pulled live from EarthRanger, so a connection is required before this workflow can run.

---

## 2. Configure the Workflow

### Workflow Details and Time Range

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes about the run (e.g. date range or patrol group) |

**Time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

All patrol tracks, events, and metrics are computed within this window.

### Groupers

Groupers control how the workflow partitions data for per-group outputs. **Left blank by default** — all data appears in a single combined view. Click **Add** to add a grouper:

| Grouper | Effect |
|---------|--------|
| Patrol Type | One map, metrics, and report section per patrol type |
| Patrol Serial Number | One output per patrol serial |
| Patrol Status | One output per patrol status (e.g. done) |
| Patrol Subject | One output per guardian ranger |

### Connect to EarthRanger

Select the EarthRanger data source configured for this environment from the **Connect to EarthRanger** dropdown. Patrol tracks, patrol events, and the two study-area boundary layers (Conservancies and Group Ranch Boundaries) are all fetched live from this connection — there is no offline/local-file mode for this workflow.

### Patrol and Patrol Event Parameters

| Field | Description |
|-------|-------------|
| Patrol Types | Filter to specific patrol types — defaults to `routine_patrol` only |
| Event Types | Filter to specific event types (leave empty to include all) |
| Include Events Without a Geometry | Check to include events with no point or polygon location — excluded by default |

Expand **Advanced Configurations** to access additional query parameters, including patrol status (defaults to `done` patrols only) and date-range overlap behaviour.

### Basemap Layers

Two stacked ArcGIS tile layers form the background of every map. Pre-filled with sensible defaults, but the URL, opacity, and max zoom of each layer are editable.

| Layer | Default Opacity | Max Zoom |
|-------|------------------|----------|
| ESRI World Hillshade | `1.0` | `20` |
| ESRI World Street Map | `0.15` | `20` |

### Trajectory Segment Filter *(Advanced Configurations)*

These parameters remove GPS noise and biologically unrealistic movements before trajectory analysis. Patrol tracks are always rendered in a single fixed colour — there is no user-selectable colour category for this map.

| Field | Default | Description |
|-------|---------|-------------|
| Minimum Segment Length (m) | `10` | Discard segments shorter than this distance |
| Maximum Segment Length (m) | `100000` | Discard segments longer than this distance |
| Minimum Segment Duration (s) | `10` | Discard segments shorter than this duration |
| Maximum Segment Duration (s) | `21600` | Discard segments longer than this duration (6 hours) |
| Minimum Segment Speed (km/h) | `1` | Discard segments below this average speed |
| Maximum Segment Speed (km/h) | `7` | Discard segments above this average speed |

A daytime filter also restricts patrol fixes to between **06:00 and 19:00** local time, excluding night-time GPS drift.

### Filter Patrol Events *(Advanced Configurations)*

Restricts events to a bounding box, pre-filled by default to the Amboseli ecosystem extent. Clear it to include all events within the time range regardless of location.

### Time Series Bar Chart

| Field | Description |
|-------|-------------|
| Time Interval | The time bucket used to group events on the x-axis (e.g. day, week, month) |

### Linear Time Density Meshgrid *(Advanced Configurations)*

Controls the resolution of the patrol coverage raster. Leave at defaults for most analyses.

---

## 3. Run the Workflow

Once all parameters are configured, click **Submit**. The runner will:

1. Pull patrol tracks and events from EarthRanger for the specified time range.
2. Fetch the Conservancies and Group Ranch Boundaries study-area layers live from EarthRanger.
3. Convert observations to relocations and build trajectory segments.
4. Generate the Patrol Events, Patrol Trajectories, and Linear Time Density maps.
5. Compute per-guardian, event type, and monthly summary tables.
6. Render the time series bar chart and pie chart.
7. Assemble the Word report (cover page + per-group sections) and the dashboard.
8. Save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

### Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`:

| File | Description |
|------|-------------|
| `events.geoparquet` | Patrol events with display names and timezone-converted timestamps |
| `trajectories.geoparquet` | Patrol segments with speed and distance |
| `<group>_events.html` | Interactive patrol events map per group |
| `<group>_patrol_trajectories.html` | Interactive patrol trajectories map per group |
| `<group>_time_density.html` | Interactive linear time density map per group |
| `<group>_events.png` | Screenshot of the patrol events map (2× resolution) |
| `<group>_patrol_trajectories.png` | Screenshot of the patrol trajectories map (2× resolution) |
| `<group>_time_density.png` | Screenshot of the time density map (2× resolution) |
| `<group>_patrols_pie_chart.png` | Screenshot of the event type pie chart (2× resolution) |
| `<group>_patrol_events_time_series_bar_chart.png` | Screenshot of the events time series bar chart (2× resolution) |
| `<group>_guardian_patrol.csv` | Per-guardian patrol effort (patrols, distance, time) |
| `<group>_guardian_events.csv` | Per-guardian event count |
| `<group>_pivot_guardian_events.csv` | Guardian × event type pivot table |
| `<group>_monthly_patrol_efforts.csv` | Monthly patrol effort summary |
| `<group>_event_types.csv` | Per-event-type count |
| `cover_page.docx` | Rendered report cover page |
| `<group>.docx` | Per-grouper report section |
| `overall_report.docx` | Final combined Word report |

> A patrol-type summary is computed internally (`summarized_patrol_types`) but is not currently persisted to a CSV or wired into the report/dashboard.
