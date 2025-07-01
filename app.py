
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st
import numpy as np
import os

# טעינת פונט מותאם במידה וקיים
font_path = "./Arial Hebrew Regular.ttf"
if os.path.exists(font_path):
    from matplotlib import font_manager as fm
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = prop.get_name()

# קריאת הנתונים
df_clean = pd.read_csv("data_arnona.csv")

# הגדרת עמודות
income_columns = [
    "הכנסות מהמדינה לנפש",
    "ארנונה למגורים והכנסות עצמיות לנפש",
    "ארנונה לא למגורים לנפש"
]
cluster_col = "אשכול"
city_col = "שם הרשות"

# כותרת ראשית
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")

# תפריט לבחירת רשות (הטקסט בלבד הפוך, לא הערכים)
selected_city = st.selectbox("בחרי רשות", df_clean[city_col].dropna().unique())

# חישוב ממוצע לפי אשכול
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# ציור הגרף
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.6
clusters = grouped[cluster_col].astype(str)

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
labels = [col[::-1] for col in income_columns]  # להפוך לעברית תקינה
bottom_vals = np.zeros(len(grouped))

for i, col in enumerate(income_columns):
    ax.bar(clusters, grouped[col], bottom=bottom_vals, color=colors[i], label=labels[i])
    bottom_vals += grouped[col]

# הוספת עמודה שקופה של הרשות הנבחרת
selected_row = df_clean[df_clean[city_col] == selected_city]
if not selected_row.empty:
    selected_cluster = selected_row[cluster_col].values[0]
    overlay_vals = selected_row[income_columns].values[0]
    cluster_index = grouped[cluster_col].tolist().index(selected_cluster)

  overlay_bottom = 0
  for i, col in enumerate(income_columns):
      ax.bar(
        x_pos,
        overlay_vals[i],
        bottom=overlay_bottom,
        width=0.4,
        color=colors[i],
        alpha=0.4,
        linewidth=0.5,
        edgecolor='black',
        label="_nolegend_"
    )
    overlay_bottom += overlay_vals[i]

ax.set_xlabel("אשכול חברתי-כלכלי"[::-1], fontsize=12)
ax.set_ylabel('ש"ח לנפש'[::-1], fontsize=12)
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת"[::-1], fontsize=14)
ax.legend()

st.pyplot(fig)




