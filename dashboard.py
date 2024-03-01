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
st.subheader("Tracker Faktor Cuaca")

#PIECHART
df_sel['weathersit_desc'] = df_sel['weathersit'].map({1: 'Cerah', 2: 'Berkabut', 3: 'Hujan'})
weather_counts = df_sel['weathersit_desc'].value_counts().reset_index()
weather_counts.columns = ['WeathersitDesc', 'Count']
fig_weather_pie = px.pie(
    weather_counts,
    names='WeathersitDesc',
    values='Count',
    title="Persentase Situasi Cuaca",
    color_discrete_sequence=px.colors.sequential.RdBu
)
fig_weather_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_weather_pie, use_container_width=True)

weather_user_counts = df_sel.groupby('weathersit_desc')['cnt'].sum().reset_index()

#BARCHART 1
fig_weather_users = px.bar(
    weather_user_counts,
    x='weathersit_desc',
    y='cnt',
    title="Jumlah Pengguna Tiap Situasi Cuaca",
    labels={'cnt': 'Jumlah Pengguna', 'weathersit_desc': 'Situasi Cuaca'},
    template="plotly_white" 
)

df_sel['weathersit_desc'] = df_sel['weathersit'].map({1: "Cerah", 2: "Berkabut", 3: "Hujan"})
weather_summary = df_sel.groupby('weathersit_desc').agg(
    total_pengguna=pd.NamedAgg(column='cnt', aggfunc='sum'),
    jumlah_hari=pd.NamedAgg(column='dteday', aggfunc='nunique')
).reset_index()
weather_summary['rata_rata_per_hari'] = weather_summary['total_pengguna'] / weather_summary['jumlah_hari']
fig_avg_users_bar = px.bar(
    weather_summary,
    x='weathersit_desc',
    y='rata_rata_per_hari',
    title="Rata-Rata Pengguna per Hari untuk Setiap Situasi Cuaca",
    labels={'rata_rata_per_hari': 'Rata-Rata Pengguna per Hari', 'weathersit_desc': 'Situasi Cuaca'},
    template="plotly_white"
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_weather_users, use_container_width=True)
right_column.plotly_chart(fig_avg_users_bar, use_container_width=True)

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

st.markdown("---")
st.subheader("Tracker Faktor Pendorong Pengguna")

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

total_per_bulan = df_sel.groupby('mnth')['cnt'].sum().reset_index()

bulan_map = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}
total_per_bulan['mnth'] = total_per_bulan['mnth'].map(bulan_map)

total_users_per_month = df_sel.groupby('mnth')['cnt'].sum().reset_index()
bulan_map = {
    1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
    5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
}
total_users_per_month['mnth'] = total_users_per_month['mnth'].map(bulan_map)
fig_total_users_per_month = px.bar(
    total_users_per_month,
    x='cnt',
    y='mnth',
    orientation='h',
    title='Total Pengguna Tiap Bulan',
    labels={'cnt': 'Total Pengguna', 'mnth': 'Bulan'},
    template='plotly_white'
)

total_users_per_weekday = df_sel.groupby('weekday')['cnt'].sum().reset_index()

weekday_map = {
    0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu',
    4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'
}
total_users_per_weekday['weekday'] = total_users_per_weekday['weekday'].map(weekday_map)

fig_total_users_per_weekday = px.bar(
    total_users_per_weekday,
    x='weekday',
    y='cnt',
    title='Total Pengguna Tiap Hari dalam Minggu',
    labels={'cnt': 'Total Pengguna', 'weekday': 'Hari dalam Minggu'},
    template='plotly_white'
)
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_total_users_per_weekday, use_container_width=True)
right_column.plotly_chart(fig_total_users_per_month, use_container_width=True)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_user_ty, use_container_width=True)
right_column.plotly_chart(fig_wh, use_container_width=True)
