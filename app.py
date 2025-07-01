
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# קריאת הדאטה
df_clean = pd.read_csv("data_arnona.csv")

# כותרת
st.title("השוואת הכנסות לנפש לפי אשכול ורשות מקומית")

# תפריט בחירת רשות
selected_city = st.selectbox("בחרי רשות", df_clean['שם הרשות'].unique())

# שמות עמודות קיימות בפועל בקובץ
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

# נתוני רשות נבחרת
selected_row = df_clean[df_clean['שם הרשות'] == selected_city].copy()

if not selected_row.empty:
    selected_group = selected_row.iloc[0][cluster_col]

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.35
    x = grouped[cluster_col]
    x_pos = range(len(x))

    for i, col in enumerate(income_columns):
        ax.bar([p + i * bar_width for p in x_pos],
               grouped[col],
               bar_width,
               label=col[::-1])

    selected_vals = selected_row[income_columns].values[0]
    ax.bar([x_pos[int(selected_group) - 1] + i * bar_width for i in range(len(income_columns))],
           selected_vals,
           bar_width,
           label=f"{selected_city} (השוואה)",
           edgecolor='black',
           linewidth=2,
           alpha=0.7)

    ax.set_xlabel("אשכול חברתי-כלכלי"[::-1])
    ax.set_ylabel('ש"ח לנפש'[::-1])
    ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת"[::-1])
    ax.set_xticks([p + bar_width for p in x_pos])
    ax.set_xticklabels([str(int(val)) for val in grouped[cluster_col]])
    ax.legend(loc='best')

    st.pyplot(fig)
else:
    st.error("לא נמצאה רשות מתאימה.")
