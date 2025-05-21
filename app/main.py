import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


# Title and description
st.title("Solar Energy Analysis Dashboard")
st.markdown("Visualize solar energy metrics (GHI, DNI, DHI) across Benin, Sierra Leone, and Togo.")

@st.cache_data
def load_data():
    def read_and_optimize(path, country_name):
        df = pd.read_csv(path, low_memory=False)
        df["country"] = country_name

        # Downcast numerical columns to reduce memory usage
        for col in df.select_dtypes(include=["float64"]).columns:
            df[col] = pd.to_numeric(df[col], downcast="float")
        for col in df.select_dtypes(include=["int64"]).columns:
            df[col] = pd.to_numeric(df[col], downcast="integer")
        return df

    benin = read_and_optimize("../data/benin_clean.csv", "Benin")
    togo = read_and_optimize("../data/togo_clean.csv", "Togo")
    sierraleone = read_and_optimize("../data/sierraleone-bumbuna.csv", "Sierra Leone")

    return pd.concat([benin, togo, sierraleone], ignore_index=True)

# Load the full optimized dataset
df_all = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filters")
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=df_all["country"].unique(),
    default=list(df_all["country"].unique())
)

selected_metric = st.sidebar.selectbox("Select Metric", ["GHI", "DNI", "DHI"])

# --- Filtered Data ---
filtered_df = df_all[df_all["country"].isin(selected_countries)]

# --- Boxplot ---
st.title("Solar Radiation Comparison Dashboard")
st.subheader(f"{selected_metric} Distribution by Country")

fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x="country", y=selected_metric, data=filtered_df, ax=ax)
st.pyplot(fig)

