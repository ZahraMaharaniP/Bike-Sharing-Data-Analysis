import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set Streamlit page configuration
st.set_page_config(page_title="Bike Sharing Data Analysis", layout="centered")

# Load the dataset (You will need to adjust the path or upload option)
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')  # Assuming day.csv is uploaded
    hour_df = pd.read_csv('data/hour.csv')  # Assuming hour.csv is uploaded
    return day_df, hour_df

# Load the data
day_df, hour_df = load_data()

# Sidebar for date range filtering
st.sidebar.header("Filter Data by Date Range")
min_date = pd.to_datetime(day_df['dteday']).min()
max_date = pd.to_datetime(day_df['dteday']).max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range", [min_date, max_date],
    min_value=min_date, max_value=max_date
)

# Filter the dataframe based on date input
filtered_day_df = day_df[
    (pd.to_datetime(day_df['dteday']) >= pd.to_datetime(start_date)) &
    (pd.to_datetime(day_df['dteday']) <= pd.to_datetime(end_date))
]

# Display data samples
st.header("Bike Sharing Data (Day)")
st.write(day_df.head())

st.header("Bike Sharing Data (Hour)")
st.write(hour_df.head())

# Average bike sharing by weather and season
st.subheader("Rata-rata Peminjaman Berdasarkan Cuaca dan Musim")

weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()

weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

# Display bar plots with custom colors
# Buat figure dan axes
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
# Grafik pertama: Data harian
sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg_day, holiday_avg_day], palette=['lightpink', 'pink'], ax=axes[0])
axes[0].set_xlabel('Jenis Hari')
axes[0].set_ylabel('Rata-rata Jumlah Peminjaman')
axes[0].set_title('Perbandingan Peminjaman Sepeda pada Hari Kerja dan Libur (Data Harian)')

# Grafik kedua: Data per jam
sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg_hour, holiday_avg_hour], palette=['lightpink', 'pink'], ax=axes[1])
axes[1].set_xlabel('Jenis Hari')
axes[1].set_ylabel('Rata-rata Jumlah Peminjaman')
axes[1].set_title('Perbandingan Peminjaman Sepeda pada Hari Kerja dan Libur (Data Jam)')

plt.tight_layout()
st.pyplot(fig)

# Statistical tests (T-tests)
st.subheader("Uji Statistik (T-Test)")
t_stat_day, p_value_day = stats.ttest_ind(day_df[day_df['workingday'] == 1]['cnt'],
                                          day_df[day_df['holiday'] == 1]['cnt'])
st.write(f"Uji t (Data Harian): t-statistic = {t_stat_day}, p-value = {p_value_day}")

t_stat_hour, p_value_hour = stats.ttest_ind(hour_df[hour_df['workingday'] == 1]['cnt'],
                                            hour_df[hour_df['holiday'] == 1]['cnt'])
st.write(f"Uji t (Data Jam): t-statistic = {t_stat_hour}, p-value = {p_value_hour}")

