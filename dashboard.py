import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# Sidebar with selectbox for navigation
st.sidebar.header("Bike Rent")
page = st.sidebar.selectbox(
    "Navigate Pages",
    ("Bike Rental based on Season & Weather", "Bike Rental based on Days", "Bike Rentals Over Time")
)

# Page 1: Bike Rental based on Season & Weather
if page == "Bike Rental based on Season & Weather":
    st.subheader("Average of Bike Rental by Season & Weather")

    # Definisikan fungsi untuk menghitung rata-rata peminjaman
    def avg_rentals_by_season(df):
        season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
        df['season'] = df['season'].map(season_mapping)
        return df.groupby('season')['cnt'].mean()

    def avg_rentals_by_weather(df):
        weather_mapping = {
            1: 'Clear',
            2: 'Cloudy, Mist',
            3: 'Light Rain',
            4: 'Heavy Rain'
        }
        df['weathersit'] = df['weathersit'].map(weather_mapping)
        return df.groupby('weathersit')['cnt'].mean()

    # Menghitung rata-rata peminjaman per musim
    season_avg_day = avg_rentals_by_season(day_df)
    season_avg_hour = avg_rentals_by_season(hour_df)  # Data per jam

    # Menghitung rata-rata peminjaman per kondisi cuaca
    weather_avg_day = avg_rentals_by_weather(day_df)
    weather_avg_hour = avg_rentals_by_weather(hour_df)  # Data per jam

    # Visualisasi Rata-rata Peminjaman Sepeda per Musim
    st.write("**Average by Season**")
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), constrained_layout=True)
    sns.barplot(x=season_avg_day.index, y=season_avg_day.values, palette=['lightpink', 'pink'], ax=axes[0])
    axes[0].set_xlabel('Season')
    axes[0].set_ylabel('Average Total of Bike Rental')
    axes[0].set_title('(day.csv)')

    sns.barplot(x=season_avg_hour.index, y=season_avg_hour.values, palette=['lightpink', 'pink'], ax=axes[1])
    axes[1].set_xlabel('Season')
    axes[1].set_ylabel('Average Total of Bike Rental')
    axes[1].set_title('(hour.csv)')

    st.pyplot(fig)  # Menampilkan plot di Streamlit

    # Visualisasi Rata-rata Peminjaman Sepeda per Kondisi Cuaca
    st.write("**Average by Weather**")
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), constrained_layout=True)
    sns.barplot(x=weather_avg_day.index, y=weather_avg_day.values, palette=['lightpink', 'pink'], ax=axes[0])
    axes[0].set_xlabel('Weather')
    axes[0].set_ylabel('Average Total of Bike Renta')
    axes[0].set_title('(day.csv)')

    sns.barplot(x=weather_avg_hour.index, y=weather_avg_hour.values, palette=['lightpink', 'pink'], ax=axes[1])
    axes[1].set_xlabel('Kondisi Cuaca')
    axes[1].set_ylabel('verage Total of Bike Renta')
    axes[1].set_title('(hour.csv)')

    st.pyplot(fig)

# Page 2: Bike Rental based on Days
elif page == "Bike Rental based on Days":
    st.subheader("Average of Bike Rental Based on Days")

    # Menghitung rata-rata peminjaman di hari kerja dan libur
    weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
    holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()

    weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
    holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg_day, holiday_avg_day], palette=['lightpink', 'pink'], ax=axes[0])
    axes[0].set_xlabel('Days')
    axes[0].set_ylabel('Average Total of Bike Rental')
    axes[0].set_title('day.csv')

    sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg_hour, holiday_avg_hour], palette=['lightpink', 'pink'], ax=axes[1])
    axes[1].set_xlabel('Days')
    axes[1].set_ylabel('Average Total of Bike Rental')
    axes[1].set_title('hour.csv')

    plt.tight_layout()
    st.pyplot(fig)

# Page 3: Bike Rentals Over Time
elif page == "Bike Rentals Over Time":
    st.subheader("Bike Rentals Over Time")

    fig, ax = plt.subplots(figsize=(10, 5))  # Set the figure size
    plt.rcParams['font.size'] = 12  # Set the global font size

    # Create line plot
    sns.lineplot(x='dteday', y='cnt', data=day_df, ax=ax, color='pink')
    ax.grid(True)  # Show grid

    # Add title and labels
    ax.set_title('Bike Rental Total per Day', fontsize=16, pad=20)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Rental Total', fontsize=12)

    # Set x-axis major ticks to be every month
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # Major ticks every month
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format to show month and year

    # Rotate x-ticks for better visibility
    ax.tick_params(axis='x', rotation=45)

    # Display the plot
    st.pyplot(fig)

if __name__ == "__main__":
    pass
