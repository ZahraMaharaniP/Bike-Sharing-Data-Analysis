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
# Menghitung rata-rata peminjaman per musim
season_avg_day = avg_rentals_by_season(filtered_day_df)
season_avg_hour = avg_rentals_by_season(filtered_hour_df)
# Menghitung rata-rata peminjaman per kondisi cuaca
weather_avg_day = avg_rentals_by_weather(filtered_day_df)
weather_avg_hour = avg_rentals_by_weather(filtered_hour_df)

st.subheader("Average of Bike Rental by Season")
# Membuat subplots berdampingan
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), constrained_layout=True)
# Grafik untuk day.csv
sns.barplot(x=season_avg_day.index, y=season_avg_day.values, palette=['lightpink', 'pink'], ax=axes[0])
axes[0].set_xlabel('Musim')
axes[0].set_ylabel('Rata-rata Jumlah Peminjaman')
axes[0].set_title('Rata-rata Peminjaman Sepeda per Musim (day.csv)')

# Grafik untuk hour.csv
sns.barplot(x=season_avg_hour.index, y=season_avg_hour.values, palette=['lightpink', 'pink'], ax=axes[1])
axes[1].set_xlabel('Musim')
axes[1].set_ylabel('Rata-rata Jumlah Peminjaman')
axes[1].set_title('Rata-rata Peminjaman Sepeda per Musim (hour.csv)')

st.pyplot(fig)  # Menampilkan plot di Streamlit

# Visualisasi Rata-rata Peminjaman Sepeda per Kondisi Cuaca
st.subheader("Average of Bike Rental by Season")

# Membuat subplots berdampingan untuk cuaca
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), constrained_layout=True)
# Grafik untuk day.csv
sns.barplot(x=weather_avg_day.index, y=weather_avg_day.values, palette=['lightpink', 'pink'], ax=axes[0])
axes[0].set_xlabel('Kondisi Cuaca')
axes[0].set_ylabel('Rata-rata Jumlah Peminjaman')
axes[0].set_title('Rata-rata Peminjaman Sepeda per Kondisi Cuaca (day.csv)')
# Grafik untuk hour.csv
sns.barplot(x=weather_avg_hour.index, y=weather_avg_hour.values, palette=['lightpink', 'pink'], ax=axes[1])
axes[1].set_xlabel('Kondisi Cuaca')
axes[1].set_ylabel('Rata-rata Jumlah Peminjaman')
axes[1].set_title('Rata-rata Peminjaman Sepeda per Kondisi Cuaca (hour.csv)')

st.pyplot(fig)  # Menampilkan plot di Streamlit

# Menghitung rata-rata peminjaman di hari weekday n weekend
weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()

weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

# Display bar plots with custom colors
# Buat figure dan axes
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
# Grafik pertama: Data harian
sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg_day, holiday_avg_day], palette=['lightpink', 'pink'], ax=axes[0])
axes[0].set_xlabel('Days')
axes[0].set_ylabel('Average Total of Bike Rental')
axes[0].set_title('day.csv')
# Grafik kedua: Data per jam
sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg_hour, holiday_avg_hour], palette=['lightpink', 'pink'], ax=axes[1])
axes[1].set_xlabel('Days')
axes[1].set_ylabel('Average Total of Bike Rental')
axes[1].set_title('hour.csv')

plt.tight_layout()
st.pyplot(fig)

if __name__ == "__main__":
    pass
