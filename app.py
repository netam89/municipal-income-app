
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

# מיון מחדש לפי אשכול
grouped[cluster_col] = pd.to_numeric(grouped[cluster_col], errors='coerce')
grouped = grouped.sort_values(by=cluster_col)

# יצירת גרף נערם
fig, ax = plt.subplots(figsize=(12, 6))
bar_bottom = [0] * len(grouped)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# ציור עמודות לכל סוג הכנסה
for i, col in enumerate(income_columns):
    for j, (x, y) in enumerate(zip(grouped['אשכול'], grouped[col])):
        is_selected = '(' in x
        ax.bar(
            x,
            y,
            bottom=bar_bottom[j],
            color=colors[i],
            alpha=0.4 if is_selected else 1.0,
            edgecolor='black' if is_selected else 'none',
            linewidth=1,
            label=col if j == 0 else None
        )
        bar_bottom[j] += y

# תצוגת גרף
ax.set_xlabel("אשכול חברתי-כלכלי")
ax.set_ylabel("ש\"ח לנפש")
ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת", loc='right')
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), loc="upper left")
plt.xticks(rotation=0)
st.pyplot(fig)
