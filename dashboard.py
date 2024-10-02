import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')

# Set Streamlit page configuration
st.set_page_config(page_title="Bike Sharing Data Analysis", layout="centered")

# Set the main title
st.title("Bike Sharing Data Analysis")

# Load the dataset (You will need to adjust the path or upload option)
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')  # Assuming day.csv is uploaded
    hour_df = pd.read_csv('data/hour.csv')  # Assuming hour.csv is uploaded
    return day_df, hour_df

# Definisikan fungsi untuk menghitung rata-rata peminjaman
def avg_rentals_by_season(df):
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    df['season'] = df['season'].map(season_mapping)
    return df.groupby('season')['cnt'].mean()

def avg_rentals_by_weather(df):
    # Menghitung rata-rata peminjaman per kondisi cuaca
    weather_mapping = {
        1: 'Clear',
        2: 'Cloudy, Mist',
        3: 'Light Rain',
        4: 'Heavy Rain'
    }
    
    df['weathersit'] = df['weathersit'].map(weather_mapping)
    return df.groupby('weathersit')['cnt'].mean()

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
season_avg_hour = avg_rentals_by_season(hour_df)

# Menghitung rata-rata peminjaman per kondisi cuaca
weather_avg_day = avg_rentals_by_weather(filtered_day_df)
weather_avg_hour = avg_rentals_by_weather(hour_df)

# Visualisasi Rata-rata Peminjaman Sepeda per Musim
st.subheader("Average of Bike Rental by Season & Weather")
st.write("**Average by Season**")

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

st.pyplot(fig)

# Visualisasi Rata-rata Peminjaman Sepeda per Kondisi Cuaca
st.write("**Average by Weather**")
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

st.pyplot(fig)

# Menghitung rata-rata peminjaman di hari weekday dan weekend
weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()
weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

# Rata-rata peminjaman berdasarkan hari
st.subheader("Average of Bike Rental by Days")
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


st.subheader("Total Bike Rental per Day")
# Atur ukuran gambar dan font
plt.figure(figsize=(10, 5))  # Mengatur ukuran gambar menjadi 10 inci lebar dan 5 inci tinggi
plt.rcParams['font.size'] = 12  # Mengatur ukuran font secara global menjadi 12

# Buat line plot dengan warna pink dan grid
sns.lineplot(x='dteday', y='cnt', data=day_df, color='pink')
plt.grid(True)  # Menampilkan grid pada plot

# Tambahkan judul dan label dengan ukuran font yang lebih besar
plt.title('Jumlah Peminjaman Sepeda per Hari', fontsize=16)  # Judul dengan ukuran font 16
plt.xlabel('Tanggal', fontsize=12)  # Label sumbu x dengan ukuran font 12
plt.ylabel('Jumlah Peminjaman', fontsize=12)  # Label sumbu y dengan ukuran font 12
plt.xticks(rotation=45)  # Memutar label pada sumbu x sebesar 45 derajat agar lebih mudah dibaca

# Atur posisi judul agar lebih terpusat
plt.title('Jumlah Peminjaman Sepeda per Hari', fontsize=16, pad=20)  # Menambahkan padding 20 poin untuk memindahkan judul ke bawah

# Tampilkan legend (jika diperlukan)
# plt.legend()

# Simpan gambar dengan resolusi tinggi
plt.savefig('sepeda.png', dpi=300)  # Menyimpan gambar dengan nama 'sepeda.png' dan resolusi 300 dpi

st.pyplot(plt)  # Menampilkan plot

# Fungsi utama untuk menjalankan Streamlit
if __name__ == "__main__":
    pass

