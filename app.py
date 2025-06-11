import streamlit as st
import pandas as pd
import plotly.express as px
from copy import deepcopy

# Mock Data (Expanded with full breakdowns for all metrics)
mock_raw_data = {
  "2023": {
    "Brand A": {
      "Core": {
        "USA": {
          "metrics": { "Power": 80, "Meaningful": 70, "Difference": 60, "Salience": 75 },
          "breakdowns": {
            "Power": {
              "AMUD KPIs": { "Affinity": 20, "Meet Needs": 25, "Unique": 15, "Dynamic": 10, "Top of mind": 10 },
              "Age Group KPIs": { "18-24": 18, "24-35": 22, "35-55": 25, "55+": 15 },
              "Gender KPIs": { "Male": 40, "Female": 40 },
              "Region KPIs": { "Region A": 20, "Region B": 30, "Region C": 30 }
            },
            "Meaningful": {
              "components": { "Affinity": 18, "Meet Needs": 22, "Unique": 12, "Dynamic": 8 },
              "AMUD KPIs (M)": { "Affinity (M)": 18, "Meet Needs (M)": 22, "Unique (M)": 12, "Dynamic (M)": 8, "Top of mind (M)": 10 },
              "Age Group KPIs (M)": { "18-24": 15, "24-35": 20, "35-55": 22, "55+": 13 },
              "Gender KPIs (M)": { "Male": 35, "Female": 35 },
              "Region KPIs (M)": { "Region A": 18, "Region B": 28, "Region C": 24 }
            },
            "Difference": {
              "components": { "Affinity": 15, "Meet Needs": 20, "Unique": 10, "Dynamic": 7 },
              "AMUD KPIs (D)": { "Affinity (D)": 15, "Meet Needs (D)": 20, "Unique (D)": 10, "Dynamic (D)": 7, "Top of mind (D)": 8 },
              "Age Group KPIs (D)": { "18-24": 12, "24-35": 18, "35-55": 20, "55+": 10 },
              "Gender KPIs (D)": { "Male": 30, "Female": 30 },
              "Region KPIs (D)": { "Region A": 15, "Region B": 25, "Region C": 20 }
            },
            "Salience": {
              "components": { "Top of Mind": 10, "Awareness": 65 },
              "AMUD KPIs (S)": { "Affinity (S)": 19, "Meet Needs (S)": 23, "Unique (S)": 14, "Dynamic (S)": 9, "Top of mind (S)": 10 },
              "Age Group KPIs (S)": { "18-24": 16, "24-35": 21, "35-55": 24, "55+": 14 },
              "Gender KPIs (S)": { "Male": 37, "Female": 38 },
              "Region KPIs (S)": { "Region A": 19, "Region B": 29, "Region C": 27 }
            }
          }
        },
      }
    }
  },
  "2024": {
    "Brand A": {
      "Core": {
        "USA": {
          "metrics": { "Power": 85, "Meaningful": 72, "Difference": 65, "Salience": 78 },
          "breakdowns": {
            "Power": {
              "AMUD KPIs": { "Affinity": 22, "Meet Needs": 27, "Unique": 16, "Dynamic": 10, "Top of mind": 10 },
              "Age Group KPIs": { "18-24": 20, "24-35": 24, "35-55": 26, "55+": 15 },
              "Gender KPIs": { "Male": 42, "Female": 43 },
              "Region KPIs": { "Region A": 22, "Region B": 31, "Region C": 32 }
            },
            "Meaningful": {
              "components": { "Affinity": 20, "Meet Needs": 24, "Unique": 13, "Dynamic": 7 },
              "AMUD KPIs (M)": { "Affinity (M)": 20, "Meet Needs (M)": 24, "Unique (M)": 13, "Dynamic (M)": 7, "Top of mind (M)": 8 },
              "Age Group KPIs (M)": { "18-24": 17, "24-35": 22, "35-55": 23, "55+": 10 },
              "Gender KPIs (M)": { "Male": 36, "Female": 36 },
              "Region KPIs (M)": { "Region A": 20, "Region B": 30, "Region C": 22 }
            },
            "Difference": {
              "components": { "Affinity": 17, "Meet Needs": 22, "Unique": 11, "Dynamic": 6 },
              "AMUD KPIs (D)": { "Affinity (D)": 17, "Meet Needs (D)": 22, "Unique (D)": 11, "Dynamic (D)": 6, "Top of mind (D)": 9 },
              "Age Group KPIs (D)": { "18-24": 14, "24-35": 20, "35-55": 21, "55+": 10 },
              "Gender KPIs (D)": { "Male": 32, "Female": 33 },
              "Region KPIs (D)": { "Region A": 17, "Region B": 27, "Region C": 21 }
            },
            "Salience": {
              "components": { "Top of Mind": 9, "Awareness": 69 },
              "AMUD KPIs (S)": { "Affinity (S)": 21, "Meet Needs (S)": 25, "Unique (S)": 15, "Dynamic (S)": 8, "Top of mind (S)": 9 },
              "Age Group KPIs (S)": { "18-24": 18, "24-35": 23, "35-55": 25, "55+": 12 },
              "Gender KPIs (S)": { "Male": 38, "Female": 40 },
              "Region KPIs (S)": { "Region A": 21, "Region B": 31, "Region C": 26 }
            }
          }
        },
      }
    }
  }
}

filter_options = {
  "periods": ["2024", "2023"],
  "metrics": ["Power", "Meaningful", "Difference", "Salience"],
  "brands": ["Brand A", "Brand B", "Brand C"],
  "priceSegments": ["Core", "Premium", "Mainstream"],
  "countries": ["USA", "India", "Japan", "Brazil", "UK"],
}

# Expanded breakdown configuration
breakdown_options_config = {
  "Power": [
    {"value": "AMUD KPIs", "label": "AMUD KPIs"},
    {"value": "Age Group KPIs", "label": "Age Group KPIs"},
    {"value": "Gender KPIs", "label": "Gender KPIs"},
    {"value": "Region KPIs", "label": "Region KPIs"}
  ],
  "Meaningful": [
    {"value": "AMUD KPIs (M)", "label": "AMUD KPIs"},
    {"value": "Age Group KPIs (M)", "label": "Age Group KPIs"},
    {"value": "Gender KPIs (M)", "label": "Gender KPIs"},
    {"value": "Region KPIs (M)", "label": "Region KPIs"}
  ],
  "Difference": [
    {"value": "AMUD KPIs (D)", "label": "AMUD KPIs"},
    {"value": "Age Group KPIs (D)", "label": "Age Group KPIs"},
    {"value": "Gender KPIs (D)", "label": "Gender KPIs"},
    {"value": "Region KPIs (D)", "label": "Region KPIs"}
  ],
  "Salience": [
    {"value": "AMUD KPIs (S)", "label": "AMUD KPIs"},
    {"value": "Age Group KPIs (S)", "label": "Age Group KPIs"},
    {"value": "Gender KPIs (S)", "label": "Gender KPIs"},
    {"value": "Region KPIs (S)", "label": "Region KPIs"}
  ]
}

overview_components_map = {
    "Meaningful": ["Affinity", "Meet Needs", "Unique", "Dynamic"],
    "Difference": ["Affinity", "Meet Needs", "Unique", "Dynamic"],
    "Salience": ["Top of Mind", "Awareness"]
}

metric_colors = {
  "Power": "#3B82F6", "Meaningful": "#10B981", "Difference": "#F59E0B", "Salience": "#EF4444",
  "Affinity": "#60A5FA", "Meet Needs": "#34D399", "Unique": "#FCD34D", "Dynamic": "#F87171", 
  "Top of Mind": "#93C5FD", "Awareness": "#A78BFA",
  "18-24": "#A78BFA", "24-35": "#818CF8", "35-55": "#C084FC", "55+": "#F0ABFC",
  "Male": "#7DD3FC", "Female": "#F472B6",
  "Region A": "#6EE7B7", "Region B": "#93C5FD", "Region C": "#FBCFE8",
  "Default": "#6B7280"
}
# FIX: Iterate over a copy of the items to avoid RuntimeError for changing dict size during iteration.
for suffix_map in [(" (M)", "(Meaningful)"), (" (D)", "(Difference)"), (" (S)", "(Salience)")]:
    for cat_key, cat_val in list(metric_colors.items()):
        if not "(" in cat_key: # Avoid re-processing already suffixed keys
            metric_colors[cat_key + suffix_map[0]] = cat_val

def get_nested_data(data_dict, path_keys):
    temp_data = data_dict
    for key in path_keys:
        if isinstance(temp_data, dict) and key in temp_data:
            temp_data = temp_data[key]
        else:
            return None
    return temp_data

def calculate_yoy(current_val, previous_val):
    if current_val is None or previous_val is None or previous_val == 0:
        return "N/A"
    yoy = ((current_val - previous_val) / previous_val) * 100
    return f"{yoy:.1f}%"

def initialize_session_state():
    defaults = {
        "selected_period": filter_options["periods"][0],
        "selected_metric": filter_options["metrics"][0],
        "selected_brand": filter_options["brands"][0],
        "selected_price_segment": filter_options["priceSegments"][0],
        "selected_country": filter_options["countries"][0],
        "drilldown_metric_key": None,
        "selected_breakdown_type": "",
        "is_transposed": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

st.set_page_config(layout="wide", page_title="Brand Metrics Dashboard")
st.title("Brand Metrics Dashboard")

# --- Filters at the top of the main page ---
st.markdown("### Filters")
filter_cols = st.columns(5)
with filter_cols[0]:
    st.session_state.selected_period = st.selectbox("Period", filter_options["periods"], key="period_sb")
with filter_cols[1]:
    st.session_state.selected_metric = st.selectbox("Metric (Focus)", filter_options["metrics"], key="metric_sb")
with filter_cols[2]:
    st.session_state.selected_brand = st.selectbox("Brand", filter_options["brands"], key="brand_sb")
with filter_cols[3]:
    st.session_state.selected_price_segment = st.selectbox("Price Segment", filter_options["priceSegments"], key="segment_sb")
with filter_cols[4]:
    st.session_state.selected_country = st.selectbox("Country", filter_options["countries"], key="country_sb")


# --- Main Page View Controller ---
st.markdown("### Chart Controls")
view_control_cols = st.columns(2)

with view_control_cols[0]:
    view_options = ["Overview"] + list(breakdown_options_config.keys())
    current_view_index = 0
    if st.session_state.drilldown_metric_key:
        try:
            current_view_index = view_options.index(st.session_state.drilldown_metric_key)
        except ValueError:
            pass 

    selected_view = st.selectbox("Select Chart View", options=view_options, index=current_view_index)
    if selected_view == "Overview":
        if st.session_state.drilldown_metric_key is not None:
            st.session_state.drilldown_metric_key = None
            st.session_state.selected_breakdown_type = ""
    else:
        if st.session_state.drilldown_metric_key != selected_view:
            st.session_state.drilldown_metric_key = selected_view
            if breakdown_options_config.get(selected_view):
                st.session_state.selected_breakdown_type = breakdown_options_config[selected_view][0]['value']

# 'View By' dropdown appears next to the main view controller when in drilldown mode
with view_control_cols[1]:
    if st.session_state.drilldown_metric_key:
        current_breakdown_options = breakdown_options_config.get(st.session_state.drilldown_metric_key, [])
        valid_breakdown_values = [opt['value'] for opt in current_breakdown_options]
        if st.session_state.selected_breakdown_type not in valid_breakdown_values and valid_breakdown_values:
            st.session_state.selected_breakdown_type = valid_breakdown_values[0]
        current_index = valid_breakdown_values.index(st.session_state.selected_breakdown_type) if st.session_state.selected_breakdown_type in valid_breakdown_values else 0
        if current_breakdown_options:
            st.session_state.selected_breakdown_type = st.selectbox("View By", options=valid_breakdown_values, format_func=lambda x: next((item['label'] for item in current_breakdown_options if item['value'] == x), x), index=current_index, key="view_by_sb")
        else:
            # Render a disabled-like placeholder if no options
            st.text_input("View By", "Not Applicable", disabled=True)


# --- Data Preparation ---
chart_data_for_df = []
table_data_for_df = []
chart_title = ""
base_path = [st.session_state.selected_brand, st.session_state.selected_price_segment, st.session_state.selected_country]
current_year_data_main = get_nested_data(mock_raw_data, [st.session_state.selected_period] + base_path)
previous_period_val = str(int(st.session_state.selected_period) - 1)
previous_year_data_main = get_nested_data(mock_raw_data, [previous_period_val] + base_path) if previous_period_val in mock_raw_data else None

if st.session_state.drilldown_metric_key:
    # --- Drilldown View ---
    drilldown_label = next((item['label'] for item in breakdown_options_config[st.session_state.drilldown_metric_key] if item['value'] == st.session_state.selected_breakdown_type), st.session_state.selected_breakdown_type)
    chart_title = f"{st.session_state.drilldown_metric_key} Breakdown by {drilldown_label}"

    if current_year_data_main and 'breakdowns' in current_year_data_main:
        breakdown_data_current = get_nested_data(current_year_data_main['breakdowns'], [st.session_state.drilldown_metric_key, st.session_state.selected_breakdown_type])
        breakdown_data_previous = None
        if previous_year_data_main and 'breakdowns' in previous_year_data_main:
             breakdown_data_previous = get_nested_data(previous_year_data_main['breakdowns'], [st.session_state.drilldown_metric_key, st.session_state.selected_breakdown_type])

        if breakdown_data_current:
            for key, value in breakdown_data_current.items():
                prev_val = breakdown_data_previous.get(key) if breakdown_data_previous else None
                chart_data_for_df.append({"name": key, "value": value, "fill": metric_colors.get(key, metric_colors["Default"])})
                table_data_for_df.append({"metric": key, "actual": value, "yoy": calculate_yoy(value, prev_val)})
        else:
            st.warning(f"No data for '{drilldown_label}' in '{st.session_state.drilldown_metric_key}' for current selections.")
    else:
        st.warning("Breakdown data not available for current selections.")

else:
    # --- Overview View ---
    chart_title = f"Metrics Overview (Focus: {st.session_state.selected_metric})"
    focus_metric = st.session_state.selected_metric

    if current_year_data_main and previous_year_data_main:
        focus_prev_val = get_nested_data(previous_year_data_main, ['metrics', focus_metric])
        chart_data_for_df.append({"name": f"{focus_metric} {previous_period_val}", "value": focus_prev_val, "originalMetric": focus_metric, "fill": metric_colors.get(focus_metric)})
        table_data_for_df.append({"metric": f"{focus_metric} {previous_period_val}", "actual": focus_prev_val, "yoy": "N/A"})
        
        if focus_metric == "Power":
            for m_key in ["Meaningful", "Difference", "Salience"]:
                curr_val = get_nested_data(current_year_data_main, ['metrics', m_key])
                prev_val = get_nested_data(previous_year_data_main, ['metrics', m_key])
                chart_data_for_df.append({"name": f"{m_key} {st.session_state.selected_period}", "value": curr_val, "originalMetric": m_key, "fill": metric_colors.get(m_key)})
                table_data_for_df.append({"metric": f"{m_key} {st.session_state.selected_period}", "actual": curr_val, "yoy": calculate_yoy(curr_val, prev_val)})
        
        elif focus_metric in overview_components_map:
            components = overview_components_map[focus_metric]
            for component in components:
                curr_val = get_nested_data(current_year_data_main, ['breakdowns', focus_metric, 'components', component])
                prev_val = get_nested_data(previous_year_data_main, ['breakdowns', focus_metric, 'components', component])
                chart_data_for_df.append({"name": component, "value": curr_val, "originalMetric": focus_metric, "fill": metric_colors.get(component, metric_colors["Default"])})
                table_data_for_df.append({"metric": component, "actual": curr_val, "yoy": calculate_yoy(curr_val, prev_val)})

        focus_curr_val = get_nested_data(current_year_data_main, ['metrics', focus_metric])
        chart_data_for_df.append({"name": f"{focus_metric} {st.session_state.selected_period}", "value": focus_curr_val, "originalMetric": focus_metric, "fill": metric_colors.get(focus_metric)})
        table_data_for_df.append({"metric": f"{focus_metric} {st.session_state.selected_period}", "actual": focus_curr_val, "yoy": calculate_yoy(focus_curr_val, focus_prev_val)})

    chart_data_for_df = [item for item in chart_data_for_df if item.get("value") is not None]
    table_data_for_df = [item for item in table_data_for_df if item.get("actual") is not None]

st.markdown("---")
# --- Chart Display ---
st.subheader(chart_title)
if chart_data_for_df:
    df_chart = pd.DataFrame(chart_data_for_df)
    color_map = {row['name']: row['fill'] for _, row in df_chart.iterrows() if 'fill' in row and row['fill']}
    fig = px.bar(df_chart, x='name', y='value', color='name', color_discrete_map=color_map, labels={'value': 'Value', 'name': 'Metric/Category'}, height=450, text_auto=True)
    fig.update_layout(xaxis_title="", yaxis_title="Value", showlegend=False)
    fig.update_xaxes(tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available for the chart with the selected filters. Please adjust your selections or ensure mock data covers this combination.")

# --- Table Display ---
st.markdown("---")
st.subheader("Data Table")
if table_data_for_df:
    df_table = pd.DataFrame(table_data_for_df)
    is_transposed_now = st.checkbox("Transpose Table", value=st.session_state.is_transposed, key="transpose_cb")
    st.session_state.is_transposed = is_transposed_now
    if st.session_state.is_transposed:
        if 'metric' in df_table.columns:
            transposed_df = df_table.set_index('metric').T.astype(str)
            st.dataframe(transposed_df, use_container_width=True)
        else:
            st.dataframe(df_table.T.astype(str), use_container_width=True)
    else:
        st.dataframe(df_table, use_container_width=True)
else:
    st.info("No data available for table display.")

# --- Footer ---
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: grey; font-size: 0.9em;'>Brand Metrics Dashboard &copy; {pd.Timestamp('today').year}</p>", unsafe_allow_html=True)