

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

# כותרת בעברית בכיוון תקין
st.markdown("<h1 style='direction: rtl;'>השוואת הכנסות לנפש לפי אשכול ורשות מקומית</h1>", unsafe_allow_html=True)

# תווית לבחירת רשות גם כן בכיוון תקין
st.markdown("<p style='direction: rtl;'>בחרי רשות:</p>", unsafe_allow_html=True)
selected_city = st.selectbox("", df_clean[city_col].dropna().unique())



# חישוב ממוצע לפי אשכול
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# ציור הגרף
fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.6
clusters = grouped[cluster_col].astype(str)
x_positions = np.arange(len(clusters))  # מיקומים מספריים לציר X

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
labels = [col[::-1] for col in income_columns]  # להפוך לעברית תקינה
bottom_vals = np.zeros(len(grouped))
for i, col in enumerate(income_columns):
    ax.bar(x_positions, grouped[col], bottom=bottom_vals, color=colors[i], label=labels[i])
    bottom_vals += grouped[col]

# הוספת עמודה שקופה של הרשות הנבחרת
selected_row = df_clean[df_clean[city_col] == selected_city]
# הכנת df_plot כמו בקולאב
df_plot = grouped.copy()
selected_cluster = selected_row[cluster_col].values[0]
selected_vals = selected_row[income_columns].values[0]
selected_label = f"{selected_city} – אשכול {int(selected_cluster)}"

insert_index = grouped[cluster_col].tolist().index(selected_cluster) + 1
x_labels = grouped[cluster_col].astype(str).tolist()
selected_label = f"{selected_city} – אשכול {int(selected_cluster)}"[::-1]
x_labels.insert(insert_index, selected_label)

# ציור כל העמודות כולל עמודת הרשות והוספת אחוזים
selected_total = selected_row[income_columns].sum(axis=1).values[0]
bar_positions = np.arange(len(clusters) + 1)  # +1 לרשות
x_labels = clusters.tolist()
selected_label = f"{selected_city} – אשכול {int(selected_cluster)}"[::-1]
x_labels.insert(insert_index, selected_label)

fig, ax = plt.subplots(figsize=(10, 6))
bottom_vals = np.zeros(len(bar_positions))

# ציור עמודות האשכולות והרשות
for i, col in enumerate(income_columns):
    values = grouped[col].tolist()
    values.insert(insert_index, selected_vals[i])  # להכניס ערך הרשות הנבחרת

    bars = ax.bar(
        bar_positions,
        values,
        bottom=bottom_vals,
        width=0.6,
        color=colors[i],
        label=labels[i]
    )

    # הוספת אחוזים
    for j, val in enumerate(values):
        if j == insert_index:
            total = selected_total
        else:
            grouped_index = j if j < insert_index else j - 1
            total = sum([grouped[c].iloc[grouped_index] for c in income_columns])

        percent = val / total * 100 if total > 0 else 0
        y_pos = bottom_vals[j] + val / 2
        va = 'center'

        if val / total < 0.15:
            y_pos = bottom_vals[j] + val + 100
            va = 'bottom'

        ax.text(
            bar_positions[j],
            y_pos,
            f"{percent:.0f}%",
            ha='center',
            va=va,
            fontsize=8,
            color='white' if va == 'center' else 'black'
        )

    bottom_vals += values


# ציור מחדש של עמודת הרשות עם גבול שחור בלבד (ללא צבע חדש)
overlay_bottom = 0
for i, col in enumerate(income_columns):
    val = selected_vals[i]
    ax.bar(
        bar_positions[insert_index], val, bottom=overlay_bottom,
        width=0.6, color=colors[i], edgecolor='black', linewidth=1.5
    )
    overlay_bottom += val



ax.set_xlabel("אשכול חברתי-כלכלי"[::-1], fontsize=12)
ax.set_ylabel('ש"ח לנפש'[::-1], fontsize=12)
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת"[::-1], fontsize=14)
ax.legend()

fig.tight_layout()
st.pyplot(fig)







