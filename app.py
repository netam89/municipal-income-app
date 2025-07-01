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
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")

# City selector
selected_city = st.selectbox("בחרי רשות", df_clean[city_col].dropna().unique())

# Group data by cluster and calculate mean
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.6
clusters = grouped[cluster_col].astype(str)

# צבעים וערכים
colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
labels = income_columns
bottom_vals = np.zeros(len(grouped))

for i, col in enumerate(income_columns):
    ax.bar(clusters, grouped[col], bottom=bottom_vals, color=colors[i], label=labels[i])
    bottom_vals += grouped[col]

# הוספת העמודה של הרשות הנבחרת על גבי האשכול המתאים
selected_row = df_clean[df_clean[city_col] == selected_city]
if not selected_row.empty:
    selected_cluster = selected_row[cluster_col].values[0]
    overlay_vals = selected_row[income_columns].values[0]
    cluster_index = grouped[cluster_col].tolist().index(selected_cluster)

    overlay_bottom = 0
    for i, col in enumerate(income_columns):
        ax.bar(
            clusters[cluster_index],
            overlay_vals[i],
            bottom=overlay_bottom,
            color=colors[i],
            alpha=0.4,
            linewidth=0.5,
            edgecolor='black',
            label="_nolegend_"
        )
        overlay_bottom += overlay_vals[i]

ax.set_xlabel("אשכול חברתי-כלכלי", fontsize=12)
ax.set_ylabel('ש"ח לנפש', fontsize=12)
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת", fontsize=14)
ax.legend()

st.pyplot(fig)