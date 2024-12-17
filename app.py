import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Fuel and CO2 Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

@st.cache_data
def get_data():
    df = pd.read_csv('ship_fuel_efficiency.csv')
    return df

df = get_data()


# --- sidebar ---
st.sidebar.header("Filter Here:")
ship_type = st.sidebar.multiselect(
    "Select the Ship Type:",
    options=df["ship_type"].unique(),
    default=df["ship_type"].unique()
)

fuel_type = st.sidebar.multiselect(
    "Select the Fuel Type:",
    options=df["fuel_type"].unique(),
    default=df["fuel_type"].unique()
)

weather_conditions = st.sidebar.multiselect(
    "Select the Weather Conditions:",
    options=df["weather_conditions"].unique(),
    default=df["weather_conditions"].unique()
)


# query to store selected options
df_selection = df.query(
    "ship_type == @ship_type & fuel_type == @fuel_type & weather_conditions == @weather_conditions"
)

# st.dataframe(df_selection)


# --- main page ---
st.title("Fuel Consumption and CO₂ Emissions Dashboard")
st.markdown("This dashboard provides an overview of fuel consumption and CO₂ emissions of various ship types operating in Nigerian waterways over one year. By exploring the efficiency and environmental impact of these vessels, we can provide actionable insights for optimizing maritime operations and reducing emissions.")
st.markdown("##")

# Top Figures
total_fuel = int(df_selection["fuel_consumption"].sum())
total_co2 = int(df_selection["CO2_emissions"].sum())
average_ee = round(df_selection["engine_efficiency"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Fuel Consumption:")
    st.subheader(f"{total_fuel:,}L")
with middle_column:
    st.subheader("Total Carbon Emissions:")
    st.subheader(f"{total_co2:,}kg")
with right_column:
    st.subheader("Average Ship Engine Efficiency:")
    st.subheader(f"{average_ee}%")

st.markdown("---")


# --- charts and tables ---
# average fuel consumption per month bar
fuel_per_month = df_selection.groupby(by=["month"], sort=False)[["fuel_consumption"]].mean()
fuel_per_month_bar = px.bar(
    fuel_per_month,
    x=fuel_per_month.index,
    y="fuel_consumption",
    orientation="v",
    title="<b>Average Fuel Consumption (L) over each Month</b>",
    color_discrete_sequence=["#0083B8"] * len(fuel_per_month),
    template="plotly_white"
)


# average co2 emission per month bar
co2_per_month = df_selection.groupby(by=["month"], sort=False)[["CO2_emissions"]].mean()
co2_per_month_bar = px.bar(
    co2_per_month,
    x="CO2_emissions",
    y=co2_per_month.index,
    orientation="h",
    title="<b>Average CO2 Emissions (kg) over each Month</b>",
    color_discrete_sequence=["#0083B8"] * len(co2_per_month),
    template="plotly_white"
)


# table
import plotly.graph_objects as go 

ee_per_month = df_selection.groupby(by=["month"], sort=False)[["engine_efficiency"]].mean()
all_per_month_table = go.Figure(
    data=[go.Table( 
    header=dict(values=['Month', 'Average Fuel Consumption (L)', 'Average CO2 Emissions (kg)', 'Average Engine Efficiency (%)']), 
    cells=dict(values=[df_selection["month"].unique(), 
                       round(fuel_per_month),
                       round(co2_per_month),
                       round(ee_per_month)])
) 
]) 


# co2 over fuel scatter
co2_per_fuel_scatter = px.scatter(
    df_selection,
    x="fuel_consumption",
    y="CO2_emissions",
    title="<b>CO2 Emissions (kg) over Fuel Consumption (L)</b>",
    color_discrete_sequence=["#0083B8"] * len(co2_per_month),
    template="plotly_white"
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fuel_per_month_bar, use_container_width=True)
right_column.plotly_chart(all_per_month_table, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(co2_per_month_bar, use_container_width=True)
right_column.plotly_chart(co2_per_fuel_scatter, use_container_width=True)


# --- hide st style ---
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
