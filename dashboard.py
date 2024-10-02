
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
# Buat figure dan axes
season_avg_day = avg_rentals_by_season(filtered_day_df)
season_avg_hour = avg_rentals_by_season(hour_df)

st.subheader("Average of Bike Rental by Season Condition")
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

# Grafik pertama: Data harian (day.csv)
sns.barplot(x=season_avg_day.index, y=season_avg_day.values, ax=axes[0], palette=['lightpink', 'pink'])
axes[0].set_xlabel('Season')
axes[0].set_ylabel('Average Total of Bike Rental')
axes[0].set_title('day.csv')

# Grafik kedua: Data per jam (hour.csv)
sns.barplot(x=season_avg_hour.index, y=season_avg_hour.values, ax=axes[1], palette=['lightpink', 'pink'])
axes[1].set_xlabel('Season')
axes[1].set_ylabel('Average Total of Bike Rental')
axes[1].set_title('hour.csv')

plt.tight_layout()
st.pyplot(fig)

# Section: Average Rentals by Weather
st.subheader("Average of Bike Rental by Weather Condition")
wcol1, col2 = st.columns(2)
# Graph for day.csv
weather_avg_day = avg_rentals_by_weather(filtered_day_df)
fig, ax = plt.subplots(figsize=(4, 6))
sns.barplot(x=weather_avg_day.index, y=weather_avg_day.values, ax=ax, palette=['lightpink', 'pink'])
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Total of Bike Rental')
ax.set_title('day.csv')
with col1:
    st.pyplot(fig)
# Graph for hour.csv
weather_avg_hour = avg_rentals_by_weather(filtered_hour_df)
fig, ax = plt.subplots(figsize=(4, 6))
sns.barplot(x=weather_avg_hour.index, y=weather_avg_hour.values, ax=ax, palette=['lightpink', 'pink'])
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Total of Bike Rental')
ax.set_title('hour.csv')
with col2:
    st.pyplot(fig)

# Section: Rentals on Holidays vs Workdays
weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()
# Hitung rata-rata peminjaman untuk data per jam
weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()
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

# Section: Date with Most Rentals
st.subheader("Date of The Most Bike Rental")
max_day = max_rentals_day(filtered_day_df)
st.write(f"**Date of The Most Bike Rental: {max_day}**")
plt.figure(figsize=(10, 5))  # Ukuran gambar sedikit lebih kecil
plt.rcParams['font.size'] = 12  # Ukuran font sedikit lebih kecil

# Buat line plot dengan warna pink dan grid
sns.lineplot(x='dteday', y='cnt', data=day_df, color='pink')
plt.grid(True)

# Tambahkan judul dan label dengan ukuran font yang lebih besar
plt.title('Total Bike Rental per Day', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Loan Total', fontsize=12)
plt.xticks(rotation=45)

# Atur posisi judul agar lebih terpusat
plt.title('Amount of Bike Rentals per Day', fontsize=16, pad=20)
plt.show()

if __name__ == "__main__":
    pass
