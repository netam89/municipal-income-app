import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st
import numpy as np
import os

# Load custom font if available
font_path = "./arial.ttf"
if os.path.exists(font_path):
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()

# Load the data
df_clean = pd.read_csv("data_arnona.csv")

# Column definitions
income_columns = [
    "הכנסות מהמדינה לנפש",
    "ארנונה למגורים והכנסות עצמיות לנפש",
    "ארנונה לא למגורים לנפש"
]
cluster_col = "אשכול"
city_col = "שם הרשות"

# Title
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית"[::-1])

# City selector
selected_city = st.selectbox("בחרי רשות"[::-1], df_clean[city_col].dropna().unique())

# Group data by cluster and calculate mean
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# Extract selected city values
selected_row = df_clean[df_clean[city_col] == selected_city]
if not selected_row.empty:
    selected_cluster = selected_row[cluster_col].values[0]
    selected_vals = selected_row[income_columns].values[0]

    # Insert the selected city as a separate bar
    new_row = {cluster_col: selected_cluster}
    for col in income_columns:
        new_row[col] = selected_row[col].values[0]
    new_row_df = pd.DataFrame([new_row])
    new_row_df[cluster_col] = "★"  # Mark it visually
    grouped[cluster_col] = grouped[cluster_col].astype(str)
    grouped = pd.concat([grouped, new_row_df], ignore_index=True)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.6
bottom_vals = np.zeros(len(grouped))

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
labels = [col[::-1] for col in income_columns]  # reverse Hebrew labels

for i, col in enumerate(income_columns):
    ax.bar(grouped[cluster_col], grouped[col], bottom=bottom_vals, color=colors[i], label=labels[i])
    bottom_vals += grouped[col]

# Add selected city overlay
if not selected_row.empty:
    overlay_vals = selected_row[income_columns].values[0]
    bottom = [0, overlay_vals[0], overlay_vals[0] + overlay_vals[1]]
    ax.bar(
        "★",
        overlay_vals,
        bottom=bottom,
        color="#aec7e8",
        edgecolor="black",
        linewidth=1,
        label="_nolegend_"
    )

ax.set_xlabel("אשכול חברתי-כלכלי"[::-1], fontsize=12)
ax.set_ylabel('ש"ח לנפש', fontsize=12)
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת"[::-1], fontsize=14)
ax.legend()

st.pyplot(fig)