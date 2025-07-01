
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# הגדרות תצוגה לעברית
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# טעינת הנתונים
df_clean = pd.read_csv("data_arnona.csv")

# שם עמודת האשכול
cluster_col = 'אשכול'

# עמודות הכנסה לנפש
income_columns = [
    'הכנסות מהמדינה לנפש',
    'ארנונה למגורים והכנסות עצמיות לנפש',
    'ארנונה לא למגורים לנפש'
]

# כותרות ידידותיות לעמודות
nice_names = {
    'הכנסות מהמדינה לנפש': 'שפל הנידרמה חוסנכה',
    'ארנונה למגורים והכנסות עצמיות לנפש': 'שפל תימצע חוסנכה וירגומל הנוריא',
    'ארנונה לא למגורים לנפש': 'שפל וירגומל אל הנוריא'
}

# ממשק Streamlit
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")
selected_city = st.selectbox("בחרי רשות", df_clean['שם הרשות'].dropna().unique())

# עיבוד הנתונים
df_clean[cluster_col] = pd.to_numeric(df_clean[cluster_col], errors='coerce')
grouped = df_clean.groupby(cluster_col)[income_columns].mean().reset_index()

# נתוני הרשות הנבחרת
selected_row = df_clean[df_clean['שם הרשות'] == selected_city]
if not selected_row.empty:
    selected_group = selected_row.iloc[0][cluster_col]
    selected_vals = selected_row[income_columns].iloc[0]

    # הוספת נתוני הרשות לטבלה
    selected_df = pd.DataFrame({cluster_col: [selected_group], **{col: [val] for col, val in zip(income_columns, selected_vals)}})
    grouped = pd.concat([grouped, selected_df], ignore_index=True)

# ציור גרף
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.8
bottom_vals = [0] * len(grouped)

# סידור לפי אשכול
grouped = grouped.sort_values(by=cluster_col)

# עמודות רגילות
for col in income_columns:
    vals = grouped[col]
    label = nice_names.get(col, col)
    ax.bar(grouped[cluster_col], vals, label=label, bottom=bottom_vals)
    bottom_vals = [i + j for i, j in zip(bottom_vals, vals)]

# סימון הרשות הנבחרת
if not selected_row.empty:
    highlight_vals = selected_vals.values
    ax.bar(
        [selected_group],
        highlight_vals,
        bottom=[0]*len(highlight_vals),
        width=bar_width * 0.75,
        color='lightblue',
        edgecolor='black',
        label=f'{selected_city} (הושרה)'
    )

# עיצוב הגרף
ax.set_xlabel("אשכול חברתי-כלכלי")
ax.set_ylabel('ש"ח לנפש')
ax.set_title("התפלגות תושרו לנפש לפי שפל חוסנכה תוגלפתה")
ax.legend()

st.pyplot(fig)
