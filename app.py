
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

# הגדרות גופן ותמיכה בעברית
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False

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
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()
grouped['אשכול'] = grouped[cluster_col].astype(str)

# יוצרים DataFrame חדש עבור הרשות הנבחרת
selected_row = df_clean[df_clean['שם הרשות'] == selected_city]
if not selected_row.empty:
    selected_group = int(selected_row.iloc[0][cluster_col])
    selected_vals = selected_row[income_columns].values[0]
    selected_dict = {
        cluster_col: selected_group,
        'אשכול': f"{selected_group} ({selected_city})"
    }
    for col in income_columns:
        selected_dict[col] = selected_row.iloc[0][col]
    grouped = pd.concat([grouped, pd.DataFrame([selected_dict])], ignore_index=True)

# יצירת גרף נערם
fig, ax = plt.subplots(figsize=(12, 6))
bar_bottom = [0] * len(grouped)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# ציור עמודות לכל סוג הכנסה
for i, col in enumerate(income_columns):
    bars = ax.bar(
        grouped['אשכול'],
        grouped[col],
        label=col,
        bottom=bar_bottom,
        color=colors[i],
        alpha=[0.4 if '(' in x else 1.0 for x in grouped['אשכול']],
        edgecolor=['black' if '(' in x else 'none' for x in grouped['אשכול']],
        linewidth=1
    )
    bar_bottom = [a + b for a, b in zip(bar_bottom, grouped[col])]

# תצוגת גרף
ax.set_xlabel("אשכול חברתי-כלכלי")
ax.set_ylabel("ש"ח לנפש")
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת", loc='right')
ax.legend(loc="upper left")
plt.xticks(rotation=0)
st.pyplot(fig)
