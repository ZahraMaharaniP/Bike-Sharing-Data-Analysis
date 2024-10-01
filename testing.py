# Mengimpor packages / library
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

#memuat tabel untuk file csv day
day_df = pd.read_csv("day.csv")
day_df.head()

#memuat tabel untuk file csv hour
hour_df = pd.read_csv("hour.csv")
hour_df.head()