import streamlit as st
#from streamlit import bootstrap
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#st.title('QC_Dashboard')
st.set_page_config(page_title="Price Comparison",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_csv(r"C:\Users\pratik.mudholkar\OneDrive - Drilling Info\Desktop\Open Insights Index\Tasks\7 Oct-2021\Pratik QC code\QC Oct-2021.csv", index_col=None) #, sheet_name="QC File", index_col=None)

df = df.dropna()

with st.sidebar.form(key ='Form1'):
    no_of_months = st.number_input("No of Months", 6)    
    threshold_lower = st.number_input("Threshold (Lower) in %", 10)    
    threshold_upper = st.number_input("Threshold (Upper)) in %", 20)
    submitted1 = st.form_submit_button(label='Submit')



st.sidebar.header("Filters:")

index = st.sidebar.multiselect(
    "Select the index:",
    options=df["Index Category_y_x"].unique(),
    default=df["Index Category_y_x"].unique()
)

subcategory = st.sidebar.multiselect(
    "Select the Sub Category:",
    options=df["Sub Category_y_x"].unique(),
    default=df["Sub Category_y_x"].unique()
)

region = st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region_y_x"].unique(),
    default=df["Region_y_x"].unique()
)

df_selection = df.query(
    "`Index Category_y_x` == @index & `Sub Category_y_x` == @subcategory & Region_y_x == @region")

st.title(":bar_chart: Price Comparison")
st.markdown("---")



df_selection['Plow_x'] = df_selection['Plow_x'].astype(float)
df_selection['Plow_y'] = df_selection['Plow_y'].astype(float)
df_selection['Index_x'] = df_selection['Index_x'].astype(float)
df_selection['Index_y'] = df_selection['Index_y'].astype(float)
df_selection['Phigh_x'] = df_selection['Plow_x'].astype(float)
df_selection['Phigh_y'] = df_selection['Phigh_y'].astype(float)
no_significant_change = df_selection[df_selection['Result'] == 'No significant change'].index.tolist()
df_selection = df_selection.groupby('Date_y_x', as_index=False).sum()

year = df_selection["Date_y_x"].apply(str).str.split("-", n=1, expand=True)
month = df_selection["Date_y_x"]
#print(month)

fig1 = go.Figure()

if len(no_significant_change):
    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Plow_x'],
        name="Average of Plow_x - No significant change"
    ))

    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Plow_y'],
        name="Average of Plow_y - No significant change"
    ))

    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Index_x'],
        name="Average of Index_x - No significant change"
    ))

    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Index_y'],
        name="Average of Index_y - No significant change"
    ))

    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Phigh_x'],
        name="Average of Phigh_x - No significant change"
    ))

    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Phigh_y'],
        name="Average of Phigh_y - No significant change"
    ))
else:
    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Index_x'],
        name="Average of Index_x - Significant change"
    ))
    fig1.add_trace(go.Scatter(
        x=df_selection['Date_y_x'],
        y=df_selection['Index_y'],
        name="Average of Index_y - Significant change"
    ))

fig1.update_layout(title="Price Comparison",
                xaxis_title="Datemonth",
                yaxis_title="Average prices (in $MM)",
                legend_title="",
                font=dict(
                    family="Times New Roman",
                    size=14,
                    color="RebeccaPurple"
                )
                )

fig1.update_layout(
    autosize=False,
    width=1000,
    height=600,)

st.plotly_chart(fig1)
#real_script = 'QC_Dashboard.py'
#bootstrap.run(real_script, f'run.py {real_script}', [], {})