
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# הגדרת הפונט העברי (Arial)
font_path = "Arial.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(layout="wide")

# טוען את הדאטה
df_clean = pd.read_csv("data_arnona.csv")

# שמות העמודות
cluster_col = 'אשכול'
city_col = 'שם הרשות'
income_columns = [
    'הכנסות מהמדינה לנפש',
    'ארנונה למגורים והכנסות עצמיות לנפש',
    'ארנונה לא למגורים לנפש'
]

# כותרת ראשית
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")

# תפריט נפתח לבחירת רשות
selected_city = st.selectbox("בחרו רשות", sorted(df_clean[city_col].dropna().unique()))

# מחשב ממוצעים לפי אשכול
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# מוסיף את נתוני הרשות הנבחרת
selected_row = df_clean[df_clean[city_col] == selected_city]
if not selected_row.empty:
    selected_cluster = selected_row.iloc[0][cluster_col]
    city_data = selected_row[income_columns].iloc[0].values
    city_bar = pd.DataFrame([city_data], columns=income_columns)
    city_bar[cluster_col] = selected_cluster + 0.2  # מקדם כדי לא לכסות את העמודה הקיימת
    city_bar['label'] = f"(הרשות) {selected_city}"

# תרשים
fig, ax = plt.subplots(figsize=(10, 6))
bottom = np.zeros(len(grouped))

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# עמודות ראשיות לפי אשכול
for idx, column in enumerate(income_columns):
    ax.bar(grouped[cluster_col], grouped[column], bottom=bottom, label=column, color=colors[idx])
    bottom += grouped[column]

# עמודת הרשות הנבחרת
if not selected_row.empty:
    bottom_city = np.zeros(1)
    for idx, column in enumerate(income_columns):
        ax.bar(
            city_bar[cluster_col],
            city_bar[column],
            bottom=bottom_city,
            label=f"{column} ({city_bar['label'].iloc[0]})" if idx == 0 else "",
            color=colors[idx],
            alpha=0.3,
            edgecolor='black',
            linewidth=1
        )
        bottom_city += city_bar[column].values

# סגנון
ax.set_xlabel("אשכול חברתי-כלכלי", fontsize=12)
ax.set_ylabel('ש"ח לנפש', fontsize=12)
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות שנבחרה", fontsize=14)
ax.legend()
st.pyplot(fig)
