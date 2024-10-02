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

# Project Title
st.title("Proyek Analisis Data: Bike Sharing Dataset")
st.write("Nama: Zahra Maharani Putri")
st.write("Email: zhrmhrnputri2001@gmail.com")
st.write("ID Dicoding: zahra_maharani_putri_T8FO")

# Business Questions
st.header("Pertanyaan Bisnis")
st.write("1. What is the average bike sharing data when considering the influence of weather and season?")
st.write("2. What is the pattern of bike sharing data based on weekdays and holidays?")
st.write("3. Which date shows the most bike sharing data?")

# Load the dataset (You will need to adjust the path or upload option)
@st.cache_data
def load_data():
    day_df = pd.read_csv('data/day.csv')  # Assuming day.csv is uploaded
    hour_df = pd.read_csv('data/hour.csv')  # Assuming hour.csv is uploaded
    return day_df, hour_df

# Load the data
day_df, hour_df = load_data()

# Display data samples
st.header("Bike Sharing Data (Day)")
st.write(day_df.head())

st.header("Bike Sharing Data (Hour)")
st.write(hour_df.head())

# Average bike sharing by weather and season
st.subheader("Rata-rata Peminjaman Berdasarkan Cuaca dan Musim")

weekday_avg_day = day_df[day_df['workingday'] == 1]['cnt'].mean()
holiday_avg_day = day_df[day_df['holiday'] == 1]['cnt'].mean()

weekday_avg_hour = hour_df[hour_df['workingday'] == 1]['cnt'].mean()
holiday_avg_hour = hour_df[hour_df['holiday'] == 1]['cnt'].mean()

# Display bar plots with custom colors
fig1, ax1 = plt.subplots()
sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg_day, holiday_avg_day], palette=['lightpink', 'pink'], ax=ax1)
ax1.set_xlabel('Jenis Hari')
ax1.set_ylabel('Rata-rata Jumlah Peminjaman')
ax1.set_title('Perbandingan Peminjaman Sepeda pada Hari Kerja dan Libur (Data Harian)')
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
sns.barplot(x=['Hari Kerja', 'Hari Libur'], y=[weekday_avg_hour, holiday_avg_hour], palette=['lightpink', 'pink'], ax=ax2)
ax2.set_xlabel('Jenis Hari')
ax2.set_ylabel('Rata-rata Jumlah Peminjaman')
ax2.set_title('Perbandingan Peminjaman Sepeda pada Hari Kerja dan Libur (Data Jam)')
st.pyplot(fig2)

# Statistical tests (T-tests)
st.subheader("Uji Statistik (T-Test)")
t_stat_day, p_value_day = stats.ttest_ind(day_df[day_df['workingday'] == 1]['cnt'],
                                          day_df[day_df['holiday'] == 1]['cnt'])
st.write(f"Uji t (Data Harian): t-statistic = {t_stat_day}, p-value = {p_value_day}")

t_stat_hour, p_value_hour = stats.ttest_ind(hour_df[hour_df['workingday'] == 1]['cnt'],
                                            hour_df[hour_df['holiday'] == 1]['cnt'])
st.write(f"Uji t (Data Jam): t-statistic = {t_stat_hour}, p-value = {p_value_hour}")

