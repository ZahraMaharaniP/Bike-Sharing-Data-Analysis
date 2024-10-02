# Streamlit and additional packages
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
day_df = pd.read_csv("data/day.csv")
hour_df = pd.read_csv("data/hour.csv")

# Set up the dashboard layout
st.title("Bike Rental Dashboard")

# Calculate average rentals by season and weather
season_avg_day = day_df.groupby('season')['cnt'].mean()
season_avg_hour = hour_df.groupby('season')['cnt'].mean()

weather_avg_day = day_df.groupby('weathersit')['cnt'].mean()
weather_avg_hour = hour_df.groupby('weathersit')['cnt'].mean()

# Visualize average rentals by season
st.subheader("Rata-rata Peminjaman Sepeda per Musim")
col1, col2 = st.columns(2)  # Creating two side-by-side columns
with col1:
    st.write("Rata-rata peminjaman sepeda berdasarkan day.csv")
    fig1, ax1 = plt.subplots()
    sns.barplot(x=season_avg_day.index, y=season_avg_day.values, ax=ax1)
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax1.set_title('Rata-rata Peminjaman Sepeda per Musim (day.csv)')
    st.pyplot(fig1, key="fig1")

with col2:
    st.write("Rata-rata peminjaman sepeda berdasarkan hour.csv")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=season_avg_hour.index, y=season_avg_hour.values, ax=ax2, palette=['lightpink', 'pink'])
    ax2.set_xlabel('Musim')
    ax2.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax2.set_title('Rata-rata Peminjaman Sepeda per Musim (hour.csv)')
    st.pyplot(fig2, key="fig2")

# Visualize average rentals by weather
st.subheader("Rata-rata Peminjaman Sepeda per Kondisi Cuaca")
col3, col4 = st.columns(2)
with col3:
    st.write("Rata-rata peminjaman sepeda berdasarkan day.csv")
    fig3, ax3 = plt.subplots()
    sns.barplot(x=weather_avg_day.index, y=weather_avg_day.values, ax=ax3)
    ax3.set_xlabel('Kondisi Cuaca')
    ax3.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax3.set_title('Rata-rata Peminjaman Sepeda per Kondisi Cuaca (day.csv)')
    st.pyplot(fig3, key="fig3")

with col4:
    st.write("Rata-rata peminjaman sepeda berdasarkan hour.csv")
    fig4, ax4 = plt.subplots()
    sns.barplot(x=weather_avg_hour.index, y=weather_avg_hour.values, ax=ax4)
    ax4.set_xlabel('Kondisi Cuaca')
    ax4.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax4.set_title('Rata-rata Peminjaman Sepeda per Kondisi Cuaca (hour.csv)')
    st.pyplot(fig4, key="fig4")

# Calculate and display rentals on holidays vs workdays
weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()
weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

st.subheader("Perbandingan Peminjaman pada Hari Kerja dan Libur")
col5, col6 = st.columns(2)
with col5:
    st.write("Rata-rata peminjaman sepeda pada day.csv")
    fig5, ax5 = plt.subplots()
    sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg_day, holiday_avg_day], palette=['lightpink', 'pink'], ax=ax5)
    ax5.set_xlabel('Jenis Hari')
    ax5.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax5.set_title('Rata-rata Peminjaman (day.csv)')
    st.pyplot(fig5, key="fig5")

with col6:
    st.write("Rata-rata peminjaman sepeda pada hour.csv")
    fig6, ax6 = plt.subplots()
    sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg_hour, holiday_avg_hour], ax=ax6)
    ax6.set_xlabel('Jenis Hari')
    ax6.set_ylabel('Rata-rata Jumlah Peminjaman')
    ax6.set_title('Rata-rata Peminjaman (hour.csv)')
    st.pyplot(fig6, key="fig6")

# Find the busiest day
busiest_day_day = day_df['dteday'].loc[day_df['cnt'].idxmax()]
busiest_day_hour = hour_df['dteday'].loc[hour_df['cnt'].idxmax()]

st.subheader("Hari dengan Peminjaman Sepeda Terbanyak")
st.write(f"Hari tersibuk dalam day.csv: {busiest_day_day}")
st.write(f"Hari tersibuk dalam hour.csv: {busiest_day_hour}")



if __name__ == "__main__":
    pass
