"""
Generate the LG Patrols Effort Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: lg_patrols_effort_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from datetime import date

OUTPUT_FILE = "lg_patrols_effort_technical_guide.pdf"

# ── Colour palette (same as STE Mapbook) ─────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=24, leading=30, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=12, leading=16, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=14, leading=18, textColor=GREEN_DARK,
                  spaceBefore=16, spaceAfter=5, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=11, leading=15, textColor=GREEN_MID,
                  spaceBefore=10, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=9.5, leading=13, textColor=SLATE,
                  spaceBefore=7, spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=5, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=13, textColor=SLATE,
                  spaceAfter=2, leftIndent=14, firstLineIndent=-10)
CELL     = _style("Cell", fontSize=8.5, leading=12, textColor=SLATE,
                  spaceAfter=0, spaceBefore=0)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)

def p(text, style=BODY):       return Paragraph(text, style)
def h1(text):                  return Paragraph(text, H1)
def h2(text):                  return Paragraph(text, H2)
def h3(text):                  return Paragraph(text, H3)
def sp(n=6):                   return Spacer(1, n)
def bullet(text):              return Paragraph(f"• {text}", BULLET)
def note(text):                return Paragraph(f"<b>Note:</b> {text}", NOTE)
def c(text):                   return Paragraph(text, CELL)   # table cell paragraph


def make_table(data, col_widths):
    """Build a table where every cell value is already a Paragraph (use c())."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  GREEN_DARK),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",       (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",       (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",           (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",         (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",    (0, 0), (-1, -1), 6),
        ("RIGHTPADDING",   (0, 0), (-1, -1), 6),
        ("TOPPADDING",     (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


# ── Page template ─────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK)
    canvas.rect(0, 0, w, 22, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(1.5*cm, 7, "LG Patrols Effort — Technical Guide")
    canvas.drawRightString(w - 1.5*cm, 7, f"Page {doc.page}")
    canvas.setFillColor(AMBER)
    canvas.rect(0, h - 4, w, 4, fill=1, stroke=0)
    canvas.restoreState()


# ── Build story ───────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="LG Patrols Effort — Technical Guide",
        author="Ecoscope",
    )

    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    story += [
        sp(60),
        p("Lion Guardians Patrols Effort", TITLE),
        p("Technical Guide", SUBTITLE),
        sp(8),
        hr(),
        p("Patrol Effort Analysis — Methodology &amp; Calculation Reference", META),
        p(f"Version 1.0  ·  Generated {date.today().strftime('%B %d, %Y')}", META),
        hr(),
        PageBreak(),
    ]

    # ── 1. Overview ───────────────────────────────────────────────────────────
    story += [
        h1("1. Overview"), hr(),
        p(
            "The <b>LG Patrols Effort</b> workflow analyses ranger patrol activity "
            "in the Amboseli ecosystem for the <b>Lion Guardians</b> programme. "
            "It ingests patrol tracks and patrol events from <b>EarthRanger</b>, "
            "computes patrol effort maps and summary statistics per guardian and patrol "
            "type, and delivers an interactive dashboard plus a print-ready Word report."
        ),
        p(
            "The workflow produces three maps per group (Patrol Events, Patrol "
            "Trajectories, Linear Time Density), five scalar metrics, two charts "
            "(bar chart and pie chart), and six summary CSV tables."
        ),
        note(
            "All per-group outputs are produced by iterating over a user-chosen "
            "grouper: patrol type, patrol serial number, or patrol subject."
        ),
    ]

    # ── 2. Dependencies ───────────────────────────────────────────────────────
    story += [
        sp(4), h1("2. Dependencies &amp; Prerequisites"), hr(),

        h2("2.1 EarthRanger Connection"),
        p(
            "All patrol data is fetched from an <b>EarthRanger</b> instance via "
            "<code>set_er_connection</code>. The workflow uses "
            "<code>set_patrols_and_patrol_events_params</code> to configure the query, "
            "then calls <code>get_patrols_from_combined_params</code> and "
            "<code>get_patrol_observations_from_patrols_df_and_combined_params</code> "
            "to retrieve patrol tracks, and "
            "<code>unpack_events_from_patrols_df_and_combined_params</code> for events. "
            "The sub-page size is 200 records; patrols are not filtered to overlap the "
            "date range only."
        ),

        sp(4), h2("2.2 Groupers"),
        p("Four grouper fields are available via <code>set_groupers</code> (default: none, a single combined view):"),
        make_table(
            [
                [c("Grouper field"),          c("Source column"),                    c("Typical use")],
                [c("patrol_type"),            c("extra__patrol_type__value"),        c("One output per patrol type")],
                [c("patrol_serial_number"),   c("extra__patrol_serial_number"),      c("One output per patrol serial")],
                [c("patrol_status"),          c("extra__patrol_status"),             c("One output per patrol status")],
                [c("patrol_subject"),         c("extra__patrol_subject"),            c("One output per guardian ranger")],
            ],
            [3.8*cm, 5.5*cm, 6.7*cm],
        ),

        sp(6), h2("2.3 Study Area Layers"),
        p(
            "Unlike some sibling Lion Guardians workflows, the study-area boundaries here are "
            "<b>not</b> downloaded from Dropbox — they are fetched live from the connected "
            "<b>EarthRanger</b> instance via <code>get_spatial_features</code>, querying two "
            "feature types:"
        ),
        make_table(
            [
                [c("Feature type"),           c("Style"),                                    c("Purpose")],
                [c("Conservancies"),          c("Fill #8fbc8b, 75% opacity, 1.75 px stroke"), c("Conservancy boundary polygons")],
                [c("Group Ranch Boundaries"), c("Unfilled, black 1.25 px stroke outline"),     c("Community ranch boundary polygons")],
            ],
            [4.5*cm, 6.5*cm, 5*cm],
        ),
        sp(4),
        p(
            "There is no Dropbox-downloaded boundary file and no separate conflict-hotspot "
            "layer in this workflow — only the org logo and the two Word templates below "
            "come from Dropbox."
        ),

        sp(4), h2("2.4 Word Document Templates &amp; Logo"),
        make_table(
            [
                [c("File"),                             c("Purpose")],
                [c("patrol_guardians_cover_page.docx"), c("Report cover page template — period, preparer")],
                [c("custom_patrol_template.docx"),      c("Per-grouper section template — maps, charts, and summary tables")],
                [c("lion-guardians.png"),               c("Organisation logo, embedded on the cover page")],
            ],
            [6.5*cm, 10*cm],
        ),

        sp(6), h2("2.5 Base Map Tile Layers"),
        make_table(
            [
                [c("Layer"),                  c("Opacity"), c("Max zoom")],
                [c("ArcGIS World Hillshade"),  c("100 %"),   c("20")],
                [c("ArcGIS World Street Map"), c("15 %"),    c("20")],
            ],
            [10*cm, 2.5*cm, 4*cm],
        ),
        sp(4),
        p(
            "The hillshade provides full-opacity terrain context. "
            "The street map is overlaid at 15 % to show roads and settlement names "
            "without obscuring terrain or patrol data."
        ),
    ]

    # ── 3. Data Ingestion ─────────────────────────────────────────────────────
    story += [
        sp(4), h1("3. Data Ingestion Pipeline"), hr(),

        h2("3.1 Patrol Observations → Relocations → Trajectories"),
        p(
            "<code>process_relocations</code> converts raw patrol observations to a "
            "standardised GeoDataFrame. Retained columns include patrol identifiers "
            "(<code>patrol_id</code>, <code>patrol_start_time</code>, "
            "<code>patrol_end_time</code>, <code>patrol_serial_number</code>, "
            "<code>patrol_subject</code>), fix quality (<code>junk_status</code>), "
            "and point geometry. Three null-island coordinate pairs are filtered out:"
        ),
        bullet("(180.0, 90.0) — boundary sentinel"),
        bullet("(0.0, 0.0) — null-island artefact"),
        bullet("(1.0, 1.0) — common default / test value"),
        p(
            "A daytime filter (<code>filter_daytime_patrols</code>) is applied before "
            "trajectory construction, retaining only fixes between 06:00 and 19:00 local "
            "time to exclude night-time GPS drift. "
            "<code>relocations_to_trajectory</code> then connects consecutive fixes "
            "per patrol into LineString segments, adding <code>dist_meters</code>, "
            "<code>speed_kmhr</code>, <code>segment_start</code>, and "
            "<code>segment_end</code>. The following segment filter is applied:"
        ),
        make_table(
            [
                [c("Filter parameter"),       c("Default"), c("Description")],
                [c("min_length_meters"),       c("10"),      c("Discard segments shorter than 10 m")],
                [c("max_length_meters"),       c("100 000"), c("Discard segments longer than 100 km")],
                [c("min_time_secs"),           c("10"),      c("Discard segments shorter than 10 s")],
                [c("max_time_secs"),           c("21 600"),  c("Discard segments longer than 6 hours")],
                [c("min_speed_kmhr"),          c("1"),       c("Discard segments below 1 km/h average speed")],
                [c("max_speed_kmhr"),          c("7"),       c("Discard segments above 7 km/h average speed")],
            ],
            [4.5*cm, 2*cm, 10*cm],
        ),
        sp(4),
        p("Trajectories are persisted as <code>trajectories.geoparquet</code>."),

        sp(4), h2("3.2 Patrol Events"),
        p(
            "<code>unpack_events_from_patrols_df_and_combined_params</code> extracts "
            "associated events for each patrol. "
            "<code>get_event_type_display_names_from_events</code> enriches the events "
            "GeoDataFrame with human-readable event type names "
            "(<code>append_category_names: duplicates</code>). "
            "Events are converted to the user timezone and persisted as "
            "<code>events.geoparquet</code>."
        ),

        sp(4), h2("3.3 Temporal Index &amp; Column Renaming"),
        p(
            "<code>add_temporal_index</code> keys the trajectory GeoDataFrame to "
            "<code>extra__patrol_start_time</code>, grouped by the configured groupers, "
            "enabling per-group iteration. Four columns are then renamed via "
            "<code>map_columns</code> (<code>raise_if_not_found: true</code>):"
        ),
        make_table(
            [
                [c("Original column"),             c("Renamed to")],
                [c("extra__patrol_type__value"),   c("patrol_type")],
                [c("extra__patrol_serial_number"), c("patrol_serial_number")],
                [c("extra__patrol_status"),        c("patrol_status")],
                [c("extra__patrol_subject"),       c("patrol_subject")],
            ],
            [7.5*cm, 9*cm],
        ),
        sp(4),
        p(
            "The renamed GeoDataFrame is split into per-group partitions by "
            "<code>split_groups</code>. All downstream map and metric tasks iterate "
            "over these partitions via <code>mapvalues</code>."
        ),

        sp(4), h2("3.4 Trajectory Colour &amp; Event Colormap"),
        p(
            "Patrol trajectories are <b>not</b> coloured by a user-selectable field — every "
            "track segment on the Trajectories map uses a single fixed colour "
            "(<code>#008b8b</code>, dark cyan), reflected in the map legend as a static "
            "&ldquo;Foot patrols&rdquo; entry. Patrol events, by contrast, "
            "<b>are</b> colour-mapped: <code>apply_color_map</code> maps "
            "<code>event_type</code> to the <b>Accent</b> colormap, writing the result to "
            "<code>event_type_colormap</code>, which drives both the Patrol Events map and "
            "the bar/pie charts."
        ),
    ]

    # ── 4. Static Map Layers ──────────────────────────────────────────────────
    story += [
        sp(4), h1("4. Static Map Layers"), hr(),
        p(
            "Two static layers, fetched live from EarthRanger (see &sect;2.3), are built "
            "once and composited onto every group-level map to provide spatial context."
        ),

        h2("4.1 Layer Styles"),
        make_table(
            [
                [c("Layer"),                  c("Colour"),          c("Opacity"), c("Filled"), c("Notes")],
                [c("Conservancies"),          c("#8fbc8b (dark sea green)"), c("75 %"), c("Yes"),
                 c("Stroke width 1.75 px, same colour as fill")],
                [c("Group Ranch Boundaries"), c("Black outline"),   c("0 % fill"), c("No"),
                 c("Outline only, stroke width 1.25 px")],
            ],
            [4*cm, 4.5*cm, 2*cm, 1.8*cm, 4.2*cm],
        ),
    ]

    # ── 5. Map Outputs ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("5. Map Outputs — Methodology"), hr(),

        h2("5.1 Patrol Events Map"),
        p(
            "<code>create_scatterplot_layer</code> renders each patrol event as a point "
            "marker, coloured by <code>event_type_colormap</code> (Accent colormap). "
            "Point radius is 2.5 px at 75 % opacity with stroked, black outlines. "
            "Before rendering, geometric outliers are removed via "
            "<code>exclude_geom_outliers</code> (z-threshold: 3) and null geometries "
            "are dropped. The event layer is combined with the two study-area static "
            "layers (&sect;4.1). The map is auto-zoomed to the event extent and persisted "
            "as HTML (suffix: <code>events</code>), then converted to PNG at 2× scale "
            "with a 40 s tile-load wait."
        ),

        sp(4), h2("5.2 Patrol Trajectories Map"),
        p(
            "<code>create_path_layer</code> renders patrol track segments with a fixed "
            "style (not driven by any colormap):"
        ),
        make_table(
            [
                [c("Property"),     c("Value")],
                [c("Colour"),       c("#008b8b, dark cyan (fixed for all patrols)")],
                [c("Width"),        c("2.25 px, min 2 px, max 8 px (screen-space pixels)")],
                [c("Cap / Join"),   c("Rounded")],
                [c("Opacity"),      c("45 %")],
            ],
            [4.5*cm, 12*cm],
        ),
        sp(4),
        p(
            "The path layer is combined with the two study-area static layers and "
            "auto-zoomed to the trajectory extent. The map is persisted as HTML "
            "(suffix: <code>patrol_trajectories</code>) and, like the other maps, "
            "converted to PNG at 2× scale with a 40 s tile-load wait — PNG generation "
            "is active for this map, not disabled."
        ),

        sp(4), h2("5.3 Linear Time Density Map"),
        p(
            "<code>create_meshgrid</code> builds a raster grid over the full patrol "
            "trajectory extent. <code>calculate_linear_time_density</code> then computes "
            "the time-weighted density of patrol coverage. Parameters:"
        ),
        make_table(
            [
                [c("Parameter"),    c("Value"),                         c("Meaning")],
                [c("percentiles"),  c("50, 60, 70, 80, 90, 100"),       c("Contour probability thresholds extracted as polygons")],
                [c("intersecting_only"), c("false"),                    c("Meshgrid covers the full AOI extent")],
            ],
            [3.5*cm, 4.5*cm, 8.5*cm],
        ),
        sp(4),
        p(
            "NaN-percentile rows are dropped and the result is sorted ascending. "
            "Contour polygons are coloured with the <b>RdYlGn</b> diverging colormap "
            "(innermost 50th percentile = red, outermost 100th = green) at 45 % opacity. "
            "The map is persisted as HTML (suffix: <code>time_density</code>) and "
            "converted to PNG at 2× scale with a 40 s tile-load wait."
        ),
    ]

    # ── 6. Summary Metrics ────────────────────────────────────────────────────
    story += [
        sp(4), h1("6. Summary Metrics"), hr(),

        h2("6.1 Per-Guardian Statistics"),
        p(
            "<code>summarize_df</code> aggregates trajectory data grouped by "
            "<code>patrol_subject</code>:"
        ),
        make_table(
            [
                [c("Output column"),    c("Source column"),      c("Aggregator"), c("Output unit")],
                [c("no_of_patrols"),    c("extra__patrol_id"),   c("nunique"),    c("count")],
                [c("total_distance"),   c("dist_meters"),        c("sum"),        c("km")],
                [c("total_time"),       c("timespan_seconds"),   c("sum"),        c("h")],
            ],
            [4*cm, 4*cm, 3*cm, 5.5*cm],
        ),
        sp(4),
        p(
            "A separate summary counts the number of events per guardian "
            "(<code>id nunique</code>). Results are persisted as CSVs. "
            "A pivot table is also generated — events pivoted by "
            "<code>event_type_display</code> — to show each guardian's event breakdown."
        ),

        sp(4), h2("6.2 Patrol Type Summary"),
        p(
            "The same three aggregations (no_of_patrols, total_distance, total_time) "
            "are also computed grouped by <code>patrol_type</code> "
            "(<code>summarized_patrol_types</code>)."
        ),
        note(
            "This table is computed by the workflow but its output is never persisted "
            "or wired into the dashboard or Word report — it is currently dead code in "
            "<code>spec.yaml</code>."
        ),

        sp(4), h2("6.3 Event Type Summary"),
        p(
            "Events are summarised by <code>event_type_display</code> using "
            "<code>id nunique</code>, giving a count of distinct events per type "
            "across the analysis period."
        ),

        sp(4), h2("6.4 Monthly Summary"),
        p(
            "<code>decompose_datetime</code> extracts <code>month_name</code> from "
            "<code>extra__patrol_start_time</code> (prefixed <code>time_</code>). Patrol "
            "effort is then summarised by <code>time_month_name</code> (no_of_patrols, "
            "total_distance, total_time) to reveal seasonal patrol patterns."
        ),

        sp(4), h2("6.5 Scalar Dashboard Widgets"),
        p(
            "Five scalar metrics are computed per group from the trajectory data and "
            "displayed as single-value widgets (1 decimal place):"
        ),
        make_table(
            [
                [c("Widget title"),    c("Source column"),     c("Aggregator"), c("Unit")],
                [c("Total Patrols"),   c("extra__patrol_id"),  c("nunique"),    c("count")],
                [c("Total Time"),      c("timespan_seconds"),  c("sum"),        c("h")],
                [c("Total Distance"),  c("dist_meters"),       c("sum"),        c("km")],
                [c("Average Speed"),   c("speed_kmhr"),        c("mean"),       c("km/h")],
                [c("Max Speed"),       c("speed_kmhr"),        c("max"),        c("km/h")],
            ],
            [4*cm, 4*cm, 3*cm, 5.5*cm],
        ),
    ]

    # ── 7. Charts ─────────────────────────────────────────────────────────────
    story += [
        sp(4), h1("7. Event Charts"), hr(),

        h2("7.1 Time Series Bar Chart"),
        p(
            "<code>draw_time_series_bar_chart</code> plots patrol event counts over time. "
            "X-axis: <code>time</code> (event timestamp); Y-axis: <code>event_type_display</code>; "
            "aggregation: <code>count</code>; category colour: <code>event_type_colormap</code> "
            "(Accent colormap). The chart is persisted as HTML "
            "(suffix: <code>patrol_events_time_series_bar_chart</code>) and converted to PNG."
        ),

        sp(4), h2("7.2 Pie Chart"),
        p(
            "<code>draw_pie_chart</code> shows the proportional breakdown of events by "
            "<code>event_type_display</code>, using <code>event_type_colormap</code> for "
            "slice colours and displaying raw counts as text labels. "
            "The chart is persisted as HTML (suffix: <code>patrols_pie_chart</code>) "
            "and converted to PNG."
        ),
    ]

    # ── 8. Word Report ────────────────────────────────────────────────────────
    story += [
        sp(4), h1("8. Word Report (.docx)"), hr(),

        h2("8.1 Cover Page"),
        p(
            "<code>prepare_cover_metadata</code> builds the cover context (org logo, "
            "report period, <i>Ecoscope</i> as preparer, generation timestamp). "
            "<code>create_context_page</code> renders it into "
            "<code>cover_page.docx</code> using the <code>patrol_guardians_cover_page.docx</code> "
            "template."
        ),

        sp(4), h2("8.2 Per-Grouper Sections"),
        p(
            "<code>create_guardians_context</code> assembles a context dict per group "
            "containing maps (events map, trajectories map, time density map), charts "
            "(pie chart, bar chart), and CSV data (monthly efforts, guardian event pivot, "
            "guardian events, guardian patrol stats, event type efforts). "
            "<code>render_docx_page</code> (from "
            "<code>ecoscope_workflows_ext_lion_guardians</code>) renders each section "
            "from the <code>custom_patrol_template.docx</code> template. "
            "Image boxes: <b>9.779 × 16.4592 cm</b> (&asymp; 3.85 × 6.48 in). "
            "<code>strict_images: true</code> catches missing PNGs before rendering."
        ),

        sp(4), h2("8.3 Document Merge"),
        p(
            "<code>merge_docx_documents</code> concatenates the cover page "
            "(<code>cover_page.docx</code>) and all per-grouper sections, ordered by "
            "name, into a single Word file: <code>overall_report.docx</code>."
        ),
    ]

    # ── 9. Interactive Dashboard ───────────────────────────────────────────────
    story += [
        sp(4), h1("9. Interactive Dashboard"), hr(),
        p(
            "<code>gather_dashboard</code> assembles the patrol dashboard from "
            "ten widget groups:"
        ),
        make_table(
            [
                [c("Widget"),              c("Type"),          c("Source task")],
                [c("Total Distance"),      c("Single value"),  c("total_patrol_dist → patrol_dist_grouped_widget")],
                [c("Average Speed"),       c("Single value"),  c("avg_speed → avg_speed_grouped_widget")],
                [c("Max Speed"),           c("Single value"),  c("max_speed → max_speed_grouped_widget")],
                [c("Total Patrols"),       c("Single value"),  c("total_patrols → total_patrols_grouped_sv_widget")],
                [c("Total Time"),          c("Single value"),  c("total_patrol_time → patrol_time_grouped_widget")],
                [c("Patrol Events Map"),   c("Map"),           c("draw_events → events_grouped_map_widget")],
                [c("Trajectories Map"),    c("Map"),           c("trajs_ecomap → trajs_grouped_map_widget")],
                [c("Events Bar Chart"),    c("Plot"),          c("patrol_events_bar_chart → grouped_bar_plot_widget_merge")],
                [c("Events Pie Chart"),    c("Plot"),          c("patrol_events_pie_chart → patrol_events_pie_widget_grouped")],
                [c("Time Density Map"),    c("Map"),           c("td_ecomap → td_grouped_map_widget")],
            ],
            [4.5*cm, 2.8*cm, 9.2*cm],
        ),
        sp(4),
        note(
            "Widget tasks use <code>skipif: [never]</code> so the dashboard always "
            "assembles, even when some groups have no data."
        ),
    ]

    # ── 10. Output Files ──────────────────────────────────────────────────────
    story += [
        sp(4), h1("10. Output Files"), hr(),
        p(
            "All files are written to <code>$ECOSCOPE_WORKFLOWS_RESULTS</code>."
        ),
        make_table(
            [
                [c("File / pattern"),                       c("Format"),     c("Content")],
                [c("events.geoparquet"),                    c("GeoParquet"), c("Patrol events with display names and timezone-converted timestamps")],
                [c("trajectories.geoparquet"),              c("GeoParquet"), c("Patrol segments with speed_kmhr, dist_meters")],
                [c("<group>_events.html"),                  c("HTML"),       c("Interactive patrol events map")],
                [c("<group>_patrol_trajectories.html"),     c("HTML"),       c("Interactive patrol trajectories map")],
                [c("<group>_time_density.html"),            c("HTML"),       c("Interactive linear time density map")],
                [c("<group>_events.png"),                   c("PNG"),        c("2× screenshot of patrol events map")],
                [c("<group>_time_density.png"),             c("PNG"),        c("2× screenshot of time density map")],
                [c("<group>_patrols_pie_chart.png"),        c("PNG"),        c("2× screenshot of event type pie chart")],
                [c("<group>_patrol_events_time_series_bar_chart.png"), c("PNG"), c("2× screenshot of events time series bar chart")],
                [c("<group>_guardian_patrol.csv"),          c("CSV"),        c("Per-guardian patrol effort (patrols, distance, time)")],
                [c("<group>_guardian_events.csv"),          c("CSV"),        c("Per-guardian event count")],
                [c("<group>_pivot_guardian_events.csv"),    c("CSV"),        c("Guardian × event type pivot table")],
                [c("<group>_event_types.csv"),              c("CSV"),        c("Per-event-type count")],
                [c("<group>_monthly_patrol_efforts.csv"),   c("CSV"),        c("Monthly patrol effort summary")],
                [c("cover_page.docx"),                      c("Word"),       c("Rendered report cover page")],
                [c("<group>.docx"),                         c("Word"),       c("Per-grouper report section")],
                [c("overall_report.docx"),                  c("Word"),       c("Final combined Word report")],
            ],
            [5.5*cm, 2.5*cm, 8.5*cm],
        ),
    ]

    # ── 11. Workflow Execution Logic ──────────────────────────────────────────
    story += [
        sp(4), h1("11. Workflow Execution Logic"), hr(),

        h2("11.1 Skip Conditions"),
        p(
            "Two default skip conditions apply to every task "
            "(<code>task-instance-defaults</code>):"
        ),
        bullet(
            "<b>any_is_empty_df</b> — skips the task (and all dependants) when "
            "any input DataFrame is empty, handling patrol types or periods with no "
            "data gracefully."
        ),
        bullet(
            "<b>any_dependency_skipped</b> — propagates skips downstream automatically."
        ),
        p(
            "Widget and map-widget tasks override this with "
            "<code>skipif: [never]</code> to ensure the dashboard always assembles."
        ),

        sp(4), h2("11.2 Data Flow Summary"),
        make_table(
            [
                [c("Stage"),              c("Tasks")],
                [c("Setup"),              c("ER connection, time range, timezone, groupers, base maps")],
                [c("Study area"),         c("Conservancies + Group Ranch Boundaries fetched live from EarthRanger")],
                [c("Downloads"),          c("2 Word templates + org logo from Dropbox")],
                [c("Patrol ingest"),      c("Params → prefetch → observations → events → rename → convert TZ")],
                [c("Trajectories"),       c("Relocations → trajectories → temporal index → rename → split groups")],
                [c("Events branch"),      c("Filter → temporal index → colormap → rename → outlier removal → scatter layer → map → HTML → PNG → widget")],
                [c("Trajectories branch"), c("Speed format → rename → colormap → path layer → map → HTML → widget")],
                [c("Time density branch"), c("Meshgrid → LTD → drop NaN → sort → colormap → GeoJSON layer → map → HTML → PNG → widget")],
                [c("Metrics branch"),     c("5 scalar widgets; 5 CSV summaries (guardian patrol, guardian events, event type, monthly, pivot)")],
                [c("Charts branch"),      c("Time series bar chart + pie chart → HTML → PNG → widgets")],
                [c("Report assembly"),    c("Cover page + per-group sections → merge docx")],
                [c("Dashboard"),          c("gather_dashboard combines all 10 widgets")],
            ],
            [4.5*cm, 12*cm],
        ),
    ]

    # ── 12. Software Versions ─────────────────────────────────────────────────
    story += [
        sp(4), h1("12. Software Versions"), hr(),
        make_table(
            [
                [c("Package"),                               c("Version"),                 c("Role")],
                [c("ecoscope-platform"),                     c(">=2.15.0, &lt;2.16.0"),     c("Consolidated core task library and workflow engine")],
                [c("ecoscope-workflows-ext-custom"),         c("0.1.0rc14.*"),              c("Utility tasks (maps, layers, column mapping)")],
                [c("ecoscope-workflows-ext-ste"),            c("0.0.0rc1.*"),               c("Spatial operations tasks (EarthRanger features, view state)")],
                [c("ecoscope-workflows-ext-lion-guardians"), c("0.0.0rc1.*"),               c("Lion Guardians domain tasks (daytime filter, Word rendering)")],
                [c("pydeck"),                                c("0.9.2"),                    c("Deck.gl map rendering")],
                [c("opentelemetry-sdk"),                     c(">=1.20.0, &lt;2.0.0"),      c("Observability/tracing")],
            ],
            [6*cm, 4*cm, 6.5*cm],
        ),
        sp(4),
        p(
            "This workflow has migrated to the consolidated <code>ecoscope-platform</code> "
            "package scheme. Packages are distributed via the "
            "<code>repo.prefix.dev</code> conda channels and pinned to compatible "
            "version ranges. The runtime environment is managed by <b>pixi</b>."
        ),
    ]

    # ── Build ─────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF written → {OUTPUT_FILE}")


if __name__ == "__main__":
    build()
