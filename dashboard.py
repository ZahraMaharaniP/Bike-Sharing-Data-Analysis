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
    ["Bike Rental Based Weather and Season", "Bike Rental Based Holidays and Weekdays", "Bike Rental Over Time"]
)

@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')  # Assuming day.csv is uploaded
    hour_df = pd.read_csv('data/hour.csv')  # Assuming hour.csv is uploaded
    return day_df, hour_df

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

