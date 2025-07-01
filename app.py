
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# קריאת הדאטה
df_clean = pd.read_csv("data_arnona.csv")

# כותרת
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")

# תפריט בחירת רשות
selected_city = st.selectbox("בחרי רשות", df_clean['שם הרשות'].unique())

# שמות עמודות
income_columns = [
    'הכנסות מהמדינה לנפש',
    'ארנונה למגורים והכנסות עצמיות לנפש',
    'ארנונה לא למגורים לנפש'
]
cluster_col = 'אשכול מדד חברתי כלכלי (משנת 2019, מ-1 עד 10, 1 הנמוך ביותר)'

# המרת אשכול למספר
df_clean[cluster_col] = pd.to_numeric(df_clean[cluster_col], errors='coerce')

# ממוצעים לפי אשכול
grouped = df_clean.groupby(cluster_col)[income_columns].mean()

# יצירת גרף נערם
fig, ax = plt.subplots(figsize=(10, 6))
bar_bottom = [0] * len(grouped)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # צבעים קבועים

for i, col in enumerate(income_columns):
    ax.bar(grouped.index.astype(str),
           grouped[col],
           label=col,
           bottom=bar_bottom,
           color=colors[i])
    bar_bottom = [a + b for a, b in zip(bar_bottom, grouped[col])]

# הוספת רשות נבחרת (עם אותו צבע, שקוף יותר)
selected_row = df_clean[df_clean['שם הרשות'] == selected_city]
if not selected_row.empty:
    selected_group = int(selected_row.iloc[0][cluster_col])
    selected_vals = selected_row[income_columns].values[0]
    selected_bottom = 0
    for i, val in enumerate(selected_vals):
        ax.bar(str(selected_group),
               val,
               bottom=selected_bottom,
               color=colors[i],
               alpha=0.4,
               edgecolor='black',
               linewidth=1,
               label=f"(הרשות) {selected_city}" if i == 0 else "")
        selected_bottom += val

# תצוגת גרף
ax.set_xlabel("אשכול חברתי-כלכלי")
ax.set_ylabel("ש\"ח לנפש")
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת")
ax.legend(loc="upper right")
st.pyplot(fig)
