import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')

# Set Streamlit page configuration
st.set_page_config(page_title="Bike Sharing Data Analysis", layout="wide")

# Set the main title
st.title("Bike Sharing Data Analysis")
# Menambahkan logo perusahaan di sidebar utama
st.sidebar.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

# Menambahkan pilihan page
page = st.sidebar.selectbox(
    "Pilih Page",
    ["Information: Bike Rental Based Weather and Season", "Information: Bike Rental Based Holidays and Weekdays", "Bike Rental Over Time"]
)

# Filter berdasarkan page
if page == "Information: Bike Rental Based Weather and Season":
    # Tambahkan filter untuk musim dan cuaca di sini
    season = st.sidebar.selectbox("Pilih Musim", ["Spring", "Summer", "Autumn", "Winter"])
    weather = st.sidebar.selectbox("Pilih Cuaca", ["Clear", "Cloudy", "Light rain", "Heavy rain"])

    # Filter data berdasarkan musim dan cuaca
    filtered_data = all_df[(all_df['season'] == season) & (all_df['weather'] == weather)]

elif page == "Information: Bike Rental Based Holidays and Weekdays":
    # Tambahkan filter untuk hari libur dan hari kerja di sini
    holiday = st.sidebar.radio("Pilih Hari", ["Holiday", "Weekday"])

    # Filter data berdasarkan hari libur atau hari kerja
    filtered_data = all_df[all_df['holiday'] == holiday]

else:
    # Filter berdasarkan rentang waktu
    min_date = all_df["order_date"].min()
    max_date = all_df["order_date"].max()

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    filtered_data   
 = all_df[(all_df['order_date'] >= start_date) & (all_df['order_date'] <= end_date)]
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
st.subheader("Bike Rentals Over Time")
fig, ax = plt.subplots(figsize=(10, 5))  # Set the figure size
plt.rcParams['font.size'] = 12  # Set the global font size

# Create line plot
sns.lineplot(x='dteday', y='cnt', data=day_df, ax=ax, color='pink')
ax.grid(True)  # Show grid

# Add title and labels
ax.set_title('Jumlah Peminjaman Sepeda per Hari', fontsize=16, pad=20)
ax.set_xlabel('Tanggal', fontsize=12)
ax.set_ylabel('Jumlah Peminjaman', fontsize=12)

# Set x-axis major ticks to be every month
ax.xaxis.set_major_locator(mdates.MonthLocator())  # Major ticks every month
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format to show month and year

# Rotate x-ticks for better visibility
ax.tick_params(axis='x', rotation=45)

# Display the plot
st.pyplot(fig)

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

