"""
Interactive demographic change visualization for Swedish kommuner
Shows working age (18-67) population by background
"""
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Swedish Demographic Change Explorer",
    page_icon="🇸🇪",
    layout="wide"
)

# Get the directory where this script is located
APP_DIR = Path(__file__).parent

# Load data
@st.cache_data
def load_data():
    """Load processed demographic data and geodata"""
    df = pd.read_csv(APP_DIR / "processed_demographics.csv")
    gdf = gpd.read_file(APP_DIR / "swedish_municipalities.geojson")

    # Merge on kommun name
    gdf['kom_namn'] = gdf['kom_namn'].str.strip()
    df['kommun'] = df['kommun'].str.strip()

    merged = gdf.merge(df, left_on='kom_namn', right_on='kommun', how='left')

    return df, gdf, merged

df, gdf, merged_gdf = load_data()

# Language translations
TRANSLATIONS = {
    "en": {
        "title": "🇸🇪 Swedish Demographic Change Explorer",
        "settings": "Settings",
        "language": "Language",
        "view_type": "View Type",
        "snapshot": "Current Snapshot (2024)",
        "change": "Change Over Time (2014-2024)",
        "born_overseas": "Born overseas",
        "both_parents_overseas": "Both parents born overseas (born in Sweden)",
        "one_parent_overseas": "One parent born overseas (born in Sweden)",
        "both_parents_sweden": "Both parents born in Sweden",
        "show_aggregated": "Show aggregated view",
        "aggregated_categories": "**Aggregated categories:**",
        "select_categories": "Select categories to combine",
        "select_category": "Select demographic category",
        "error_select_one": "Please select at least one category",
        "foreign_background": "Foreign background",
        "change_metric": "Change metric",
        "percentage_points": "Percentage points",
        "relative_change": "Relative percent change",
        "percentage_of_pop": "Percentage of Working Age Population (2024)",
        "change_pp": "Change in Percentage Points (2024-2014)",
        "relative_change_title": "Relative Change (2024-2014)",
        "percentage": "Percentage (%)",
        "percent_change": "Percent Change (%)",
        "key_stats": "Key Statistics",
        "population_2024": "2024 Population",
        "population_2014": "2014 Population",
        "absolute_change": "Absolute Change",
        "relative_change_stat": "Relative Change",
        "of_working_age": "of working age",
        "top_bottom": "Top & Bottom Kommuner",
        "top_10": "Top 10 Kommuner",
        "bottom_10": "Bottom 10 Kommuner",
        "kommun": "Kommun",
        "change_label": "Change",
        "data_source": "**Data Source:** Statistics Sweden (SCB) - TAB4824",
        "working_age_def": "**Working Age Definition:** 18-67 years",
        "time_period": "**Time Period:** 2014-2024",
        "license_text": "This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).",
        "total_2024": "Total 2024",
        "total_2014": "Total 2014"
    },
    "sv": {
        "title": "🇸🇪 Demografisk förändring i Sverige",
        "settings": "Inställningar",
        "language": "Språk",
        "view_type": "Visningstyp",
        "snapshot": "Nuläge (2024)",
        "change": "Förändring över tid (2014-2024)",
        "born_overseas": "Födda utomlands",
        "both_parents_overseas": "Båda föräldrarna födda utomlands (födda i Sverige)",
        "one_parent_overseas": "En förälder född utomlands (födda i Sverige)",
        "both_parents_sweden": "Båda föräldrarna födda i Sverige",
        "show_aggregated": "Visa aggregerad vy",
        "aggregated_categories": "**Aggregerade kategorier:**",
        "select_categories": "Välj kategorier att kombinera",
        "select_category": "Välj demografisk kategori",
        "error_select_one": "Välj minst en kategori",
        "foreign_background": "Utländsk bakgrund",
        "change_metric": "Förändringsenhet",
        "percentage_points": "Procentenheter",
        "relative_change": "Relativ procentuell förändring",
        "percentage_of_pop": "Andel av befolkningen i arbetsför ålder (2024)",
        "change_pp": "Förändring i procentenheter (2024-2014)",
        "relative_change_title": "Relativ förändring (2024-2014)",
        "percentage": "Procent (%)",
        "percent_change": "Procentuell förändring (%)",
        "key_stats": "Nyckelstatistik",
        "population_2024": "Befolkning 2024",
        "population_2014": "Befolkning 2014",
        "absolute_change": "Absolut förändring",
        "relative_change_stat": "Relativ förändring",
        "of_working_age": "av arbetsför ålder",
        "top_bottom": "Högsta & lägsta kommuner",
        "top_10": "Topp 10 kommuner",
        "bottom_10": "Botten 10 kommuner",
        "kommun": "Kommun",
        "change_label": "Förändring",
        "data_source": "**Datakälla:** Statistiska centralbyrån (SCB) - TAB4824",
        "working_age_def": "**Definition av arbetsför ålder:** 18-67 år",
        "time_period": "**Tidsperiod:** 2014-2024",
        "license_text": "Detta verk är licensierat under en [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).",
        "total_2024": "Totalt 2024",
        "total_2014": "Totalt 2014"
    }
}

# Language selector in sidebar
language = st.sidebar.radio("Language / Språk", ["English", "Svenska"], horizontal=True)
lang = "en" if language == "English" else "sv"
t = TRANSLATIONS[lang]

# Title
st.title(t["title"])

# Sidebar controls
st.sidebar.header(t["settings"])

# View type
view_type_options = [t["snapshot"], t["change"]]
view_type = st.sidebar.radio(
    t["view_type"],
    view_type_options
)

# Category selection - map translated labels to internal keys
category_options_display = {
    t["born_overseas"]: "born_overseas",
    t["both_parents_overseas"]: "both_parents_overseas",
    t["one_parent_overseas"]: "one_parent_overseas",
    t["both_parents_sweden"]: "both_parents_sweden"
}

# Aggregation option
show_aggregated = st.sidebar.checkbox(t["show_aggregated"], value=False)

if show_aggregated:
    st.sidebar.markdown(t["aggregated_categories"])
    selected_categories = st.sidebar.multiselect(
        t["select_categories"],
        options=list(category_options_display.keys()),
        default=[t["born_overseas"], t["both_parents_overseas"], t["one_parent_overseas"]]
    )

    if not selected_categories:
        st.error(t["error_select_one"])
        st.stop()

    category_label = t["foreign_background"] if len(selected_categories) > 1 else selected_categories[0]
else:
    selected_category = st.sidebar.selectbox(
        t["select_category"],
        options=list(category_options_display.keys())
    )
    category_label = selected_category

# For change view, select metric type
if view_type == t["change"]:
    change_metric_options = [t["percentage_points"], t["relative_change"]]
    change_metric = st.sidebar.radio(
        t["change_metric"],
        change_metric_options
    )

# Prepare map data
map_data = merged_gdf.copy()

if view_type == t["snapshot"]:
    # Calculate the value to display
    if show_aggregated:
        # Sum up selected categories
        cols_to_sum = [f"count_2024_{category_options_display[cat]}" for cat in selected_categories]
        map_data['display_value'] = map_data[cols_to_sum].sum(axis=1)
        # Calculate percentage
        map_data['display_percentage'] = (map_data['display_value'] / map_data['total_2024'] * 100).round(2)
        map_column = 'display_percentage'
    else:
        # Single category percentage
        map_column = f"pct_2024_{category_options_display[selected_category]}"

    title_text = f"{category_label} - {t['percentage_of_pop']}"
    colorbar_title = t["percentage"]
    color_scale = "Blues"
    # Fixed range for snapshot: 0-100%
    color_range = [0, 100]

else:  # Change view
    if show_aggregated:
        # Calculate change for combined categories
        if change_metric == t["percentage_points"]:
            # Sum up percentage point changes
            cols_2014 = [f"pct_2014_{category_options_display[cat]}" for cat in selected_categories]
            cols_2024 = [f"pct_2024_{category_options_display[cat]}" for cat in selected_categories]

            pct_2014 = map_data[cols_2014].sum(axis=1)
            pct_2024 = map_data[cols_2024].sum(axis=1)
            map_data['display_value'] = pct_2024 - pct_2014
        else:  # Relative change
            # Sum absolute counts then calculate relative change
            count_cols_2014 = [f"count_2014_{category_options_display[cat]}" for cat in selected_categories]
            count_cols_2024 = [f"count_2024_{category_options_display[cat]}" for cat in selected_categories]

            count_2014 = map_data[count_cols_2014].sum(axis=1)
            count_2024 = map_data[count_cols_2024].sum(axis=1)
            map_data['display_value'] = ((count_2024 - count_2014) / count_2014.replace(0, 1) * 100).round(2)

        map_column = 'display_value'
    else:
        # Single category
        if change_metric == t["percentage_points"]:
            # Calculate percentage point change
            pct_2014 = map_data[f"pct_2014_{category_options_display[selected_category]}"]
            pct_2024 = map_data[f"pct_2024_{category_options_display[selected_category]}"]
            map_data['display_value'] = pct_2024 - pct_2014
        else:  # Relative change
            map_column = f"change_relative_{category_options_display[selected_category]}"
            map_data['display_value'] = map_data[map_column]

        map_column = 'display_value'

    if change_metric == t["percentage_points"]:
        title_text = f"{category_label} - {t['change_pp']}"
        colorbar_title = t["percentage_points"]
        # Fixed range for percentage point change: -20 to +20
        color_range = [-20, 20]
    else:
        title_text = f"{category_label} - {t['relative_change_title']}"
        colorbar_title = t["percent_change"]
        # Fixed range for relative change: -50% to +200%
        color_range = [-50, 200]

    # Use diverging color scale for change
    color_scale = "RdBu_r"

# Create the map
fig = px.choropleth_mapbox(
    map_data,
    geojson=json.loads(map_data.to_json()),
    locations=map_data.index,
    color=map_column,
    hover_name='kom_namn',
    hover_data={
        map_column: ':.2f',
        'total_2024': ':,',
        'total_2014': ':,'
    },
    color_continuous_scale=color_scale,
    range_color=color_range,
    mapbox_style="carto-positron",
    center={"lat": 62.5, "lon": 16},
    zoom=3.5,
    opacity=0.7,
    labels={
        map_column: colorbar_title,
        'total_2024': t["total_2024"],
        'total_2014': t["total_2014"]
    }
)

fig.update_layout(
    title=title_text,
    height=700,
    margin={"r":0,"t":40,"l":0,"b":0}
)

# Display map
st.plotly_chart(fig, use_container_width=True)

# Statistics section
st.header(t["key_stats"])

col1, col2, col3, col4 = st.columns(4)

if show_aggregated:
    # Calculate aggregated stats
    selected_cat_keys = [category_options_display[cat] for cat in selected_categories]

    # 2024 totals
    count_2024_cols = [f"count_2024_{cat}" for cat in selected_cat_keys]
    total_selected_2024 = df[count_2024_cols].sum().sum()

    # 2014 totals
    count_2014_cols = [f"count_2014_{cat}" for cat in selected_cat_keys]
    total_selected_2014 = df[count_2014_cols].sum().sum()

else:
    cat_key = category_options_display[selected_category]
    total_selected_2024 = df[f"count_2024_{cat_key}"].sum()
    total_selected_2014 = df[f"count_2014_{cat_key}"].sum()

total_all_2024 = df['total_2024'].sum()
total_all_2014 = df['total_2014'].sum()

pct_of_total_2024 = (total_selected_2024 / total_all_2024 * 100)
pct_of_total_2014 = (total_selected_2014 / total_all_2014 * 100)

with col1:
    st.metric(
        t["population_2024"],
        f"{total_selected_2024:,.0f}",
        f"{pct_of_total_2024:.1f}% {t['of_working_age']}"
    )

with col2:
    st.metric(
        t["population_2014"],
        f"{total_selected_2014:,.0f}",
        f"{pct_of_total_2014:.1f}% {t['of_working_age']}"
    )

with col3:
    change_abs = total_selected_2024 - total_selected_2014
    st.metric(
        t["absolute_change"],
        f"{change_abs:+,.0f}"
    )

with col4:
    change_rel = ((total_selected_2024 - total_selected_2014) / total_selected_2014 * 100)
    st.metric(
        t["relative_change_stat"],
        f"{change_rel:+.1f}%"
    )

# Top/Bottom kommuner
st.header(t["top_bottom"])

col_left, col_right = st.columns(2)

with col_left:
    st.subheader(t["top_10"])
    if view_type == t["snapshot"]:
        top_df = map_data.nlargest(10, map_column)[['kom_namn', map_column]].copy()
        top_df.columns = [t["kommun"], f'{category_label} (%)']
    else:
        top_df = map_data.nlargest(10, map_column)[['kom_namn', map_column]].copy()
        top_df.columns = [t["kommun"], f'{t["change_label"]} ({colorbar_title})']

    st.dataframe(top_df.reset_index(drop=True), use_container_width=True)

with col_right:
    st.subheader(t["bottom_10"])
    if view_type == t["snapshot"]:
        bottom_df = map_data.nsmallest(10, map_column)[['kom_namn', map_column]].copy()
        bottom_df.columns = [t["kommun"], f'{category_label} (%)']
    else:
        bottom_df = map_data.nsmallest(10, map_column)[['kom_namn', map_column]].copy()
        bottom_df.columns = [t["kommun"], f'{t["change_label"]} ({colorbar_title})']

    st.dataframe(bottom_df.reset_index(drop=True), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"""
{t["data_source"]}
{t["working_age_def"]}
{t["time_period"]}

[![CC BY-NC-SA 4.0](https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
{t["license_text"]}
""")
