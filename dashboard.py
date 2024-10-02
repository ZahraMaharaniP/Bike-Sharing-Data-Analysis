
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

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

# Helper functions for calculating metrics
def avg_rentals_by_season(df):
    return df.groupby('season')['cnt'].mean()

def avg_rentals_by_weather(df):
    return df.groupby('weathersit')['cnt'].mean()

def avg_rentals_by_holiday_workday(df):
    weekday_avg = df[df['workingday'] == 1]['cnt'].mean()
    holiday_avg = df[df['holiday'] == 1]['cnt'].mean()
    return weekday_avg, holiday_avg

def max_rentals_day(df):
    return df[df['cnt'] == df['cnt'].max()]['dteday'].values[0]

# Main Dashboard Layout
st.title("Bike Rentals Dashboard")
st.markdown("### Data Overview")
st.write("Filtered Data", filtered_day_df.head())

# Section: Average Rentals by Season
st.subheader("Rata-rata Peminjaman Sepeda per Musim")
season_avg_day = avg_rentals_by_season(filtered_day_df)
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=season_avg_day.index, y=season_avg_day.values, ax=ax)
ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.set_title('Rata-rata Peminjaman Sepeda per Musim')
st.pyplot(fig)

# Section: Average Rentals by Weather
st.subheader("Rata-rata Peminjaman Sepeda per Kondisi Cuaca")
weather_avg_day = avg_rentals_by_weather(filtered_day_df)
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=weather_avg_day.index, y=weather_avg_day.values, ax=ax)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.set_title('Rata-rata Peminjaman Sepeda per Kondisi Cuaca')
st.pyplot(fig)

# Section: Rentals on Holidays vs Workdays
st.subheader("Perbandingan Peminjaman pada Hari Kerja dan Libur")
weekday_avg, holiday_avg = avg_rentals_by_holiday_workday(filtered_day_df)
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg, holiday_avg], ax=ax)
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.set_title('Perbandingan Peminjaman pada Hari Kerja dan Libur')
st.pyplot(fig)

# Section: Date with Most Rentals
st.subheader("Tanggal dengan Peminjaman Sepeda Terbanyak")
max_day = max_rentals_day(filtered_day_df)
st.write(f"**Tanggal dengan peminjaman sepeda terbanyak: {max_day}**")

if __name__ == "__main__":
    pass
