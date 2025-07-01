
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import ipywidgets as widgets
from IPython.display import display, clear_output
import numpy as np

# פונט עברית ללא אזהרות
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['axes.unicode_minus'] = False

# תפריט
city_dropdown = widgets.Dropdown(
    options=sorted(df_clean['שם הרשות'].dropna().unique()),
    description='בחר רשות:',
    value='חיפה'
)
display(city_dropdown)

# ציור הגרף
def draw_chart_matplotlib(selected_city):
    income_columns = [
        'הכנסות מהמדינה לנפש',
        'ארנונה למגורים והכנסות עצמיות לנפש',
        'ארנונה לא למגורים לנפש'
    ]

    df_clean['אשכול'] = pd.to_numeric(
        df_clean['אשכול מדד חברתי כלכלי (משנת 2019, מ-1 עד 10, 1 הנמוך ביותר)'],
        errors='coerce'
    )

    grouped = df_clean.groupby('אשכול')[income_columns].mean()

    selected_row = df_clean[df_clean['שם הרשות'] == selected_city]
    if selected_row.empty:
        print(f"שגיאה: לא נמצאה רשות בשם {selected_city}")
        return

    selected_group = selected_row['אשכול'].values[0]
    selected_vals = selected_row[income_columns].values[0]

    # הפיכת שמות האשכולות (ציר X)
    grouped.index = [f"אשכול {int(i)}"[::-1] for i in grouped.index]
    selected_city_label = f"{selected_city} – אשכול {int(selected_group)}"[::-1]

    # הוספת הרשות לשלב הבא
    df_plot = grouped.copy()
    insert_index = list(df_plot.index).index(f"אשכול {int(selected_group)}"[::-1]) + 1
    x_labels = list(df_plot.index)
    x_labels.insert(insert_index, selected_city_label)

    # הפיכת שמות העמודות
    columns_rtl = [col[::-1] for col in income_columns]
    df_plot.columns = columns_rtl

    # ציור
    clear_output(wait=True)
    display(city_dropdown)

    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.6
    bar_positions = np.arange(len(x_labels))

    # ציור כל האשכולות
    bottoms = np.zeros(len(x_labels))
    for i, col in enumerate(columns_rtl):
        values = df_plot[col].tolist()
        values.insert(insert_index, 0)  # אפס בעמודת הרשות — נצייר אותה בנפרד
        ax.bar(bar_positions, values, bottom=bottoms, label=col, width=bar_width,
               color=['skyblue', 'lightgreen', 'salmon'][i])
        bottoms += np.array(values)

    # ציור עמודת הרשות בצבע שונה
    highlight_colors = ['dodgerblue', 'forestgreen', 'indianred']
    bottom = 0
    for i, val in enumerate(selected_vals):
        ax.bar(bar_positions[insert_index], val, bottom=bottom, width=bar_width,
               color=highlight_colors[i])
        bottom += val

    ax.set_title("התפלגות הכנסות לנפש לפי אשכול ורשות נבחרת"[::-1])
    ax.set_xlabel("אשכול / רשות"[::-1])
    ax.set_ylabel('ש"ח לנפש'[::-1])
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.show()

# חיבור תפריט
def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        draw_chart_matplotlib(change['new'])

city_dropdown.observe(on_change)
draw_chart_matplotlib(city_dropdown.value)



