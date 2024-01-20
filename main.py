import streamlit as st
import pandas as pd


# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("data/player_passing_data.csv")
    return data


# Clean data
def clean_data(data):
    data['Player'] = data['Player'].str.replace('*', '')
    return data


# Filter data for QBs
def filter_data(data):
    return data[data["Pos"] == "QB"]


data = load_data()
data = filter_data(data)
data = clean_data(data)

# Sidebar for user input
st.title("NFL QB 2023 Comparison App")
st.sidebar.header("User Input Features")

# Allow user to select multiple QBs
selected_qbs = st.sidebar.multiselect("Select QBs", data["Player"].unique())

# Allow user to select stats for benchmark
selected_stats = st.sidebar.multiselect("Select Stats for Benchmark", ["Player"] + list(data.columns))

# Display selected QBs stats
if selected_qbs and selected_stats:
    selected_data = data[data["Player"].isin(selected_qbs)]

    # Include "Player" in the benchmark data
    benchmark_data = selected_data[["Player"] + selected_stats]

    st.header("Display Player Stats of Selected QBs")
    st.write(
        "Data Dimension: " + str(selected_data.shape[0]) + " rows and " + str(selected_data.shape[1]) + " columns.")
    st.dataframe(selected_data)

    # Display benchmark stats in a bar chart
    st.header("Benchmark Stats Comparison")
    st.line_chart(benchmark_data.set_index("Player"))  # Set "Player" as the index for the chart
