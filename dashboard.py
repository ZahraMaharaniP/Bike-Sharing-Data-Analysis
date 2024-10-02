import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Set Streamlit page configuration
st.set_page_config(page_title="Bike Sharing Data Analysis", layout="wide")

# Set the main title
st.title("Bike Sharing Data Analysis")

# Load the dataset (You will need to adjust the path or upload option)
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')  # Assuming day.csv is uploaded
    hour_df = pd.read_csv('data/hour.csv')  # Assuming hour.csv is uploaded
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Sidebar for filtering
st.sidebar.header("Filter Data")
seasons = st.sidebar.multiselect(
    "Select Seasons", ['Winter', 'Spring', 'Summer', 'Fall'], default=['Winter', 'Spring', 'Summer', 'Fall']
)
weather_conditions = st.sidebar.multiselect(
    "Select Weather Conditions", ['Clear', 'Cloudy, Mist', 'Light Rain', 'Heavy Rain'], 
    default=['Clear', 'Cloudy, Mist']
)

# Filter the data based on selections
if seasons:
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    day_df['season'] = day_df['season'].map(season_mapping)
    day_df = day_df[day_df['season'].isin(seasons)]

if weather_conditions:
    weather_mapping = {
        1: 'Clear',
        2: 'Cloudy, Mist',
        3: 'Light Rain',
        4: 'Heavy Rain'
    }
    day_df['weathersit'] = day_df['weathersit'].map(weather_mapping)
    day_df = day_df[day_df['weathersit'].isin(weather_conditions)]

# Visualizations

# 1. Average Bike Rentals by Season
st.subheader("Average Bike Rentals by Season")
season_avg = day_df.groupby('season')['cnt'].mean()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_avg.index, y=season_avg.values, palette="coolwarm", ax=ax)
ax.set_title('Average Bike Rentals by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

# 2. Average Bike Rentals by Weather
st.subheader("Average Bike Rentals by Weather")
weather_avg = day_df.groupby('weathersit')['cnt'].mean()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=weather_avg.index, y=weather_avg.values, palette="Blues", ax=ax)
ax.set_title('Average Bike Rentals by Weather')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

# 3. Bike Rentals Over Time
fig, ax = plt.subplots(figsize=(10, 5))  # Mengatur ukuran gambar menjadi 10 inci lebar dan 5 inci tinggi
plt.rcParams['font.size'] = 12  # Mengatur ukuran font secara global menjadi 12

# Buat line plot dengan warna pink dan grid
sns.lineplot(x='dteday', y='cnt', data=day_df, ax=ax, color='pink')
ax.grid(True)  # Menampilkan grid pada plot

# Tambahkan judul dan label dengan ukuran font yang lebih besar
ax.set_title('Jumlah Peminjaman Sepeda per Hari', fontsize=16, pad=20)  # Judul dengan ukuran font 16 dan padding 20 poin
ax.set_xlabel('Tanggal', fontsize=12)  # Label sumbu x dengan ukuran font 12
ax.set_ylabel('Jumlah Peminjaman', fontsize=12)  # Label sumbu y dengan ukuran font 12
ax.tick_params(axis='x', rotation=45)  # Memutar label pada sumbu x sebesar 45 derajat agar lebih mudah dibaca

# 4. Bike Rentals by Weekdays and Holidays
st.subheader("Average Bike Rentals: Weekdays vs Holidays")
weekday_avg = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg = day_df[day_df['holiday'] == 1]['cnt'].mean()

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg, holiday_avg], palette="Set2", ax=ax)
ax.set_title('Weekday vs Holiday Rentals')
ax.set_xlabel('Day Type')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

# Fungsi utama untuk menjalankan Streamlit
if __name__ == "__main__":
    pass

