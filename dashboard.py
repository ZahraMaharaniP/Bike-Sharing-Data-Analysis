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


# Fungsi utama untuk menjalankan Streamlit
if __name__ == "__main__":
    pass

