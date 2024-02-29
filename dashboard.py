import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Bike Sharing",
                   page_icon="🚲",
                   layout="wide")


@st.cache_data
def get_data_c():
    day_df = pd.read_csv("https://raw.githubusercontent.com/0bry/data-project/main/day.csv")
    return day_df

day_df = get_data_c()
st.sidebar.header("Gunakan: ")
weather = st.sidebar.multiselect(
    "Select the weather: ",
    options=day_df["weathersit"],
    default=day_df["weathersit"].unique()
)

year = st.sidebar.multiselect(
    "Select the year: ",
    options=day_df["yr"],
    default=day_df["yr"].unique()
)

month = st.sidebar.multiselect(
    "Select the month: ",
    options=day_df["mnth"],
    default=day_df["mnth"].unique()
)

weekday = st.sidebar.multiselect(
    "Select the week: ",
    options=day_df["weekday"],
    default=day_df["weekday"].unique()
)

df_sel = day_df.query(
    "weathersit == @weather & yr == @year & mnth == @month & weekday == @weekday"
)

st.title("🚲 Bike Sharing Dashboard")
st.markdown("##")

total_pemakai = int(df_sel["cnt"].sum())
average_pemakai = round(df_sel["cnt"].mean(), 1)
total_hari = int(df_sel["instant"].max())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Pengguna: ")
    st.subheader(f"{total_pemakai:,} Orang telah menggunakan sepeda")
with middle_column:
    st.subheader("Rata-rata Pengguna: ")
    st.subheader(f"{average_pemakai} Orang telah menggunakan sepeda")
with right_column:
    st.subheader("Dengan total ")
    st.subheader(f"{total_hari} Hari melayani")

st.markdown("---")

p_re = df_sel["registered"].sum()/df_sel["cnt"].sum()*100
p_ca = df_sel["casual"].sum()/df_sel["cnt"].sum()*100

rc_p = pd.DataFrame({
    "Type": ["Registered", "Casual"],
    "Percentage": [p_re, p_ca]
})

fig_user_ty = px.bar(
    rc_p,
    x="Type",
    y="Percentage",
    orientation="v",
    title="Percentage Tipe Pengguna",
    template="plotly_white",
)

working_day_total = df_sel[df_sel["workingday"] == 1]["cnt"].sum()/df_sel["workingday"].sum()
holiday_total = df_sel[df_sel["holiday"] == 1]["cnt"].sum()/df_sel["holiday"].sum()

wh_p = pd.DataFrame({
    "Type": ["Working Day", "Holiday"],
    "Percentage": [working_day_total, holiday_total]
})

fig_wh = px.bar(
    wh_p,
    x="Percentage",
    y="Type",
    orientation="h",
    title="Jumlah Pengguna Pada Workingday & Holiday",
    template="plotly_white",
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_user_ty, use_container_width=True)
right_column.plotly_chart(fig_wh, use_container_width=True)

st.markdown("---")
st.subheader("Tracker Jumlah Pengguna per Bulan")

fig_time_series = px.line(
    df_sel,
    x='dteday',
    y='cnt',
    title='Jumlah Pengguna per Bulan',
    labels={'cnt': 'Jumlah Pengguna', 'dteday': 'Tanggal'},
    template='plotly_white'
)

st.plotly_chart(fig_time_series, use_container_width=True)