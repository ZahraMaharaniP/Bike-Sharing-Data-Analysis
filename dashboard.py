import streamlit as st
import pandas as pd
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

# Sidebar for navigation
st.sidebar.header("Select Analysis Type")
analysis_type = st.sidebar.selectbox("Choose a view", 
                                     ["Bike Rental Based on Weather and Season", 
                                      "Bike Rental Based on Holidays and Weekdays", 
                                      "Bike Rental Over Time"])

# Halaman 1: Rata-rata berdasarkan Musim dan Cuaca
if analysis_type == "Bike Rental Based on Weather and Season":
    st.subheader("Average of Bike Rental by Season & Weather")

    # Filter the dataframe based on date input
    st.sidebar.header("Filter Data by Date Range")
    min_date = pd.to_datetime(day_df['dteday']).min()
    max_date = pd.to_datetime(day_df['dteday']).max()

    start_date, end_date = st.sidebar.date_input(
        "Select Date Range", [min_date, max_date],
        min_value=min_date, max_value=max_date
    )

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
    st.write("**Average of Bike Rentals by Season**")
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), constrained_layout=True)
    sns.barplot(x=season_avg_day.index, y=season_avg_day.values, palette=['lightpink', 'pink'], ax=axes[0])
    axes[0].set_xlabel('Season')
    axes[0].set_ylabel('Average Rentals')
    axes[0].set_title('Average Rentals per Season (day.csv)')

    sns.barplot(x=season_avg_hour.index, y=season_avg_hour.values, palette=['lightpink', 'pink'], ax=axes[1])
    axes[1].set_xlabel('Season')
    axes[1].set_ylabel('Average Rentals')
    axes[1].set_title('Average Rentals per Season (hour.csv)')
    st.pyplot(fig)

    # Visualisasi Rata-rata Peminjaman Sepeda per Kondisi Cuaca
    st.write("**Average of Bike Rentals by Weather**")
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), constrained_layout=True)
    sns.barplot(x=weather_avg_day.index, y=weather_avg_day.values, palette=['lightpink', 'pink'], ax=axes[0])
    axes[0].set_xlabel('Weather Condition')
    axes[0].set_ylabel('Average Rentals')
    axes[0].set_title('Average Rentals per Weather Condition (day.csv)')

    sns.barplot(x=weather_avg_hour.index, y=weather_avg_hour.values, palette=['lightpink', 'pink'], ax=axes[1])
    axes[1].set_xlabel('Weather Condition')
    axes[1].set_ylabel('Average Rentals')
    axes[1].set_title('Average Rentals per Weather Condition (hour.csv)')
    st.pyplot(fig)

# Halaman 2: Rata-rata berdasarkan hari kerja dan hari libur
elif analysis_type == "Bike Rental Based on Holidays and Weekdays":
    st.subheader("Average of Bike Rental by Days")
    weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
    holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()

    weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
    holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg_day, holiday_avg_day], palette=['lightpink', 'pink'], ax=axes[0])
    axes[0].set_xlabel('Days')
    axes[0].set_ylabel('Average Rentals')
    axes[0].set_title('Average Rentals (day.csv)')

    sns.barplot(x=['Weekday', 'Holiday'], y=[weekday_avg_hour, holiday_avg_hour], palette=['lightpink', 'pink'], ax=axes[1])
    axes[1].set_xlabel('Days')
    axes[1].set_ylabel('Average Rentals')
    axes[1].set_title('Average Rentals (hour.csv)')
    st.pyplot(fig)

# Halaman 3: Grafik jumlah peminjaman sepeda per waktu
elif analysis_type == "Bike Rental Over Time":
    st.subheader("Bike Rental Over Time")
    def plot_daily_rentals(day_df):
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='dteday', y='cnt', data=day_df, color='pink')
        plt.grid(True)
        plt.title('Bike Rentals per Day', fontsize=16, pad=20)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Rentals', fontsize=12)
        plt.xticks(rotation=45)
        st.pyplot(plt)
    
    plot_daily_rentals(day_df)


# Fungsi utama untuk menjalankan Streamlit
if __name__ == "__main__":
    pass

