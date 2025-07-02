
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


# בניית ערכי y
bottom_vals = np.zeros(len(x_labels))
bar_positions = np.arange(len(x_labels))

fig, ax = plt.subplots(figsize=(10, 6))

for i, col in enumerate(income_columns):
    values = grouped[col].tolist()
    values.insert(insert_index, 0)  # מקום לעמודת הרשות
    ax.bar(bar_positions, values, bottom=bottom_vals,
           width=0.6, color=colors[i], label=labels[i])
    bottom_vals += values

# הוספת אחוזים לעמודות של האשכולות
totals = grouped[income_columns].sum(axis=1)
for i, col in enumerate(income_columns):
    cumulative = np.zeros(len(grouped))
    for j in range(i):
        cumulative += grouped[income_columns[j]]
    for idx, val in enumerate(grouped[col]):
        percent = val / totals[idx] * 100
        ax.text(x_positions[idx], cumulative[idx] + val / 2, f"{percent:.0f}%", ha='center', va='center', fontsize=8, color='white')


# ציור עמודת הרשות בצבעים מודגשים
highlight_colors = ["#2c6b99", "#cc6c00", "#2a9232"]
overlay_bottom = 0
for i, col in enumerate(income_columns):
    val = selected_row[col].values[0]
    ax.bar(bar_positions[insert_index], val, bottom=overlay_bottom,
           width=0.6, color=highlight_colors[i], edgecolor='black', linewidth=1.5)
    overlay_bottom += val

# הוספת אחוזים לעמודת הרשות
selected_total = selected_row[income_columns].sum(axis=1).values[0]
overlay_bottom = 0
for i, col in enumerate(income_columns):
    val = selected_row[col].values[0]
    percent = val / selected_total * 100
    ax.text(bar_positions[insert_index], overlay_bottom + val / 2, f"{percent:.0f}%", ha='center', va='center', fontsize=8, color='white')
    overlay_bottom += val


# יצירת תוויות לציר X כולל הרשות
x_labels = clusters.tolist()
selected_label = f"{selected_city} – אשכול {int(selected_cluster)}"[::-1]
x_labels.insert(insert_index, selected_label)

# עדכון התוויות על הציר
ax.set_xticks(bar_positions)  # תואם לאורך x_labels
ax.set_xticklabels(x_labels, rotation=45, ha='right')



ax.set_xlabel("אשכול חברתי-כלכלי"[::-1], fontsize=12)
ax.set_ylabel('ש"ח לנפש'[::-1], fontsize=12)
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת"[::-1], fontsize=14)
ax.legend()

st.pyplot(fig)




