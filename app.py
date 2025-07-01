import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Load custom Hebrew font
font_path = "Arial.ttf"
fm.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Arial'

# Load data
df_clean = pd.read_csv("data_arnona.csv")

# Columns for the plot
income_columns = [
    "הכנסות מהמדינה לנפש",
    "ארנונה למגורים והכנסות עצמיות לנפש",
    "ארנונה לא למגורים לנפש"
]

# Map for Hebrew labels
income_labels = {
    "הכנסות מהמדינה לנפש": "הכנסות מהמדינה לנפש",
    "ארנונה למגורים והכנסות עצמיות לנפש": "ארנונה למגורים והכנסות עצמיות לנפש",
    "ארנונה לא למגורים לנפש": "ארנונה לא למגורים לנפש"
}

# Streamlit title and dropdown
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")
selected_city = st.selectbox("בחרי רשות", sorted(df_clean["שם הרשות"].dropna().unique()))

# אשכול column
cluster_col = "אשכול"
df_clean[cluster_col] = pd.to_numeric(df_clean[cluster_col], errors='coerce')

# Grouped data
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# Get selected city values
selected_city_data = df_clean[df_clean["שם הרשות"] == selected_city]
selected_cluster = selected_city_data[cluster_col].values[0]

# Bar chart
fig, ax = plt.subplots(figsize=(10, 6))
bottom = [0] * len(grouped)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
for i, col in enumerate(income_columns):
    ax.bar(
        grouped[cluster_col],
        grouped[col],
        bottom=bottom,
        label=income_labels[col],
        color=colors[i]
    )
    bottom = [x + y for x, y in zip(bottom, grouped[col])]

# Add selected city
if not pd.isna(selected_cluster):
    base_values = selected_city_data[income_columns].values[0]
    bottom_values = [0, base_values[0], base_values[0] + base_values[1]]
    highlight_colors = ['lightblue'] * len(income_columns)
    ax.bar(
        selected_cluster,
        base_values,
        bottom=bottom_values,
        color=highlight_colors,
        edgecolor='black',
        linewidth=1,
        label="_nolegend_"  # לא ייכנס למקרא
    )

# Labels and legend
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת", fontsize=14)
ax.set_xlabel("אשכול חברתי-כלכלי", fontsize=12)
ax.set_ylabel("ש"ח לנפש", fontsize=12)
ax.legend()

st.pyplot(fig)