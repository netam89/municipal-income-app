
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# הגדרת גופן תומך בעברית
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False

# קריאת הנתונים
df_clean = pd.read_csv("data_arnona.csv")

# שמות עמודות
cluster_col = 'אשכול'
city_col = 'שם הרשות'
income_columns = [
    'הכנסות מהמדינה לנפש',
    'ארנונה למגורים והכנסות עצמיות לנפש',
    'ארנונה לא למגורים לנפש'
]

# אפליקציית סטרימליט
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")

# תפריט בחירה
selected_city = st.selectbox("בחרי רשות", df_clean[city_col].dropna().unique())

# חישוב ממוצעים לפי אשכול
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# הוספת נתוני הרשות הנבחרת
selected_row = df_clean[df_clean[city_col] == selected_city]
if not selected_row.empty:
    selected_cluster = selected_row[cluster_col].values[0]
    selected_data = selected_row[income_columns].values[0]
    insert_index = grouped[grouped[cluster_col] == selected_cluster].index[0] + 0.1
    grouped.loc[insert_index] = [selected_cluster] + list(selected_data)
    grouped = grouped.sort_index().reset_index(drop=True)
    is_selected = [False] * len(grouped)
    is_selected[insert_index] = True
else:
    is_selected = [False] * len(grouped)

# תרשים
fig, ax = plt.subplots(figsize=(10, 6))

bottom = [0] * len(grouped)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
labels = [
    'הכנסות מהמדינה לנפש',
    'ארנונה למגורים והכנסות עצמיות לנפש',
    'ארנונה לא למגורים לנפש'
]

for idx, column in enumerate(income_columns):
    values = grouped[column]
    bar_colors = [colors[idx] if not sel else 'lightblue' for sel in is_selected]
    ax.bar(grouped[cluster_col], values, bottom=bottom, color=bar_colors, label=labels[idx], edgecolor='black', linewidth=0.5)
    bottom = [i + j for i, j in zip(bottom, values)]

# עיצוב
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת", fontsize=14)
ax.set_xlabel("אשכול חברתי-כלכלי", fontsize=12)
ax.set_ylabel("ש"ח לנפש", fontsize=12)
ax.legend()
st.pyplot(fig)
