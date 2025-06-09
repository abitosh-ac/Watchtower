import streamlit as st

import plotly.graph_objects as go

import pandas as pd

 

st.set_page_config(layout="wide")

 

# Dropdowns

st.title("Overall")

col1, col2, col3, col4, col5 = st.columns(5)

 

with col1:

    period = st.selectbox("Period", ["2024", "2023"])

with col2:

    metric = st.selectbox("Metric", ["Power", "Meaning", "Difference", "Salience"])

with col3:

    brand = st.selectbox("Brand", ["Brand A", "Brand B", "Brand C"])

with col4:

    price_segment = st.selectbox("Price Segment", ["Core", "Premium"])

with col5:

    country = st.selectbox("Country", ["USA", "Brazil", "Germany", "India", "Japan"])

 

# Show warning for unavailable data

if period == "2024" and metric != "Power":

    st.warning(f"Data for {metric} in {period} is not yet available.")

 

# Power values based on period

data = {

    "2024": {

        "start_power": 11.9,

        "end_power": 11.4,

        "values1": [-0.19, 0.01, -0.32],

        "values2": [-0.1, -0.05, 0.05, -0.1, -0.16],

        "gender_values": [-0.2, -0.3],

        "region_values": [-0.2, -0.1, -0.2],

        "age_values": [-0.1, -0.15, -0.2, -0.05],

        "meaning_gender": [8, 10],

        "difference_gender": [12, 13],

        "salience_gender": [14, 16],

        "meaning_age": [5, 6, 4, 3],

        "difference_age": [7, 8, 6, 5],

        "salience_age": [9, 10, 8, 6],

        "meaning_region": [6, 5, 7],

        "difference_region": [8, 7, 9],

        "salience_region": [10, 9, 8],

    },

    "2023": {

        "start_power": 11.5,

        "end_power": 11.9,

        "values1": [0.15, 0.05, 0.2],

        "values2": [0.1, 0.05, 0.1, 0.05, 0.05],

        "gender_values": [0.2, 0.2],

        "region_values": [0.15, 0.1, 0.15],

        "age_values": [0.1, 0.1, 0.1, 0.1],

        "meaning_gender": [6, 5],

        "difference_gender": [7, 8],

        "salience_gender": [9, 10],

        "meaning_age": [5, 6, 4, 3],

        "difference_age": [6, 7, 5, 4],

        "salience_age": [7, 8, 6, 5],

        "meaning_region": [4, 3, 2],

        "difference_region": [5, 4, 3],

        "salience_region": [6, 5, 4],

    }

}

 

current_data = data[period]

 

start_power = current_data["start_power"]

end_power = current_data["end_power"]

values1 = current_data["values1"]

values2 = current_data["values2"]

gender_values = current_data["gender_values"]

region_values = current_data["region_values"]

age_values = current_data["age_values"]

meaning_gender = current_data["meaning_gender"]

difference_gender = current_data["difference_gender"]

salience_gender = current_data["salience_gender"]

meaning_age = current_data["meaning_age"]

difference_age = current_data["difference_age"]

salience_age = current_data["salience_age"]

meaning_region = current_data["meaning_region"]

difference_region = current_data["difference_region"]

salience_region = current_data["salience_region"]

 

# Helper to make waterfall chart

def waterfall_chart(title, categories, changes, start=start_power, end=end_power):

    return go.Figure(

        go.Waterfall(

            name=title,

            orientation="v",

            measure=["absolute"] + ["relative"] * len(changes) + ["absolute"],

            x=["{} {}".format(metric, int(period)-1)] + categories + ["{} {}".format(metric, period)],

            textposition="outside",

            y=[start] + changes + [end],

            connector={"line": {"color": "rgb(63, 63, 63)"}}

        )

    ).update_layout(title=title, showlegend=False, height=400, margin=dict(t=50, l=20, r=20))

 

if metric == "Power":

    chart1 = waterfall_chart("Power by Meaningful, Difference, Salience", ["Meaningful", "Difference", "Salience"], values1)

    chart2 = waterfall_chart("Power by Affinity, Meet Needs, Unique, Dynamic, Top of mind", ["Affinity", "Meet Needs", "Unique", "Dynamic", "Top of mind"], values2)

    chart3 = waterfall_chart("Power by Age Group", ["18-24", "24-35", "35-55", "55+"], age_values)

    chart4 = waterfall_chart("Power by Gender", ["Male", "Female"], gender_values)

    chart5 = waterfall_chart("Power by Region", ["Region A", "Region B", "Region C"], region_values)

 

    st.plotly_chart(chart1, use_container_width=True)

    st.plotly_chart(chart2, use_container_width=True)

    st.plotly_chart(chart3, use_container_width=True)

    st.plotly_chart(chart4, use_container_width=True)

    st.plotly_chart(chart5, use_container_width=True)

 

elif period == "2023":

    if metric == "Meaning":

        chart3 = waterfall_chart("Meaning by Age Group", ["18-24", "24-35", "35-55", "55+"], meaning_age, 150, 168)

        chart4 = waterfall_chart("Meaning by Gender", ["Male", "Female"], meaning_gender, 150, 168)

        chart5 = waterfall_chart("Meaning by Region", ["Region A", "Region B", "Region C"], meaning_region, 150, 168)

    elif metric == "Difference":

        chart3 = waterfall_chart("Difference by Age Group", ["18-24", "24-35", "35-55", "55+"], difference_age, 150, 168)

        chart4 = waterfall_chart("Difference by Gender", ["Male", "Female"], difference_gender, 150, 168)

        chart5 = waterfall_chart("Difference by Region", ["Region A", "Region B", "Region C"], difference_region, 150, 168)

    elif metric == "Salience":

        chart3 = waterfall_chart("Salience by Age Group", ["18-24", "24-35", "35-55", "55+"], salience_age, 150, 168)

        chart4 = waterfall_chart("Salience by Gender", ["Male", "Female"], salience_gender, 150, 168)

        chart5 = waterfall_chart("Salience by Region", ["Region A", "Region B", "Region C"], salience_region, 150, 168)

 

    st.plotly_chart(chart3, use_container_width=True)

    age_table = pd.DataFrame({

        f"{metric} {int(period) - 1}": [150] * len(current_data[f"{metric.lower()}_age"]),

        f"{metric} {period}": [150 + delta for delta in current_data[f"{metric.lower()}_age"]]

    }, index=["18-24", "24-35", "35-55", "55+"])

    st.table(age_table)

 

    st.plotly_chart(chart4, use_container_width=True)

    gender_table = pd.DataFrame({

        f"{metric} {int(period) - 1}": [150, 150],

        f"{metric} {period}": [150 + delta for delta in current_data[f"{metric.lower()}_gender"]]

    }, index=["Male", "Female"])

    st.table(gender_table)

 

    st.plotly_chart(chart5, use_container_width=True)

    region_table = pd.DataFrame({

        f"{metric} {int(period) - 1}": [150] * len(current_data[f"{metric.lower()}_region"]),

        f"{metric} {period}": [150 + delta for delta in current_data[f"{metric.lower()}_region"]]

    }, index=["Region A", "Region B", "Region C"])

    st.table(region_table)