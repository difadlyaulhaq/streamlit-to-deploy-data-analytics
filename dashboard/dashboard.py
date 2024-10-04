# -*- coding: utf-8 -*-
"""dashboard.py

# Proyek Analisis Data: Bike Sharing
- **Nama:** Difa Dlyaul Haq
- **Email:** difadlyaulhaq2@gmail.com
- **ID Dicoding:** Difa Dlyaul Haq
"""

# Import libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df_day = pd.read_csv('data/day.csv')

# Preprocessing: clean the data
df_day['temp2'] = df_day['temp'] * 47 - 8
df_day['atemp2'] = df_day['atemp'] * 66 - 16
df_day['hum2'] = df_day['hum'] * 100
df_day['windspeed2'] = df_day['windspeed'] * 67

# Map season and month
season_map = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
df_day['season'] = df_day['season'].map(season_map)

mnth_string = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
}
df_day['mnth'] = df_day['mnth'].map(mnth_string)

# Binning temperature, humidity, and windspeed
temps2_bin = np.linspace(df_day["temp2"].min(), df_day["temp2"].max(), 4)
temps2_labels = ["cold", "mild", "hot"]
df_day["temp2_bin"] = pd.cut(df_day["temp2"], bins=temps2_bin, labels=temps2_labels)

hum2_bin = np.linspace(df_day["hum2"].min(), df_day["hum2"].max(), 4)
hum2_labels = ["low", "medium", "high"]
df_day["hum2_binned"] = pd.cut(df_day["hum2"], bins=hum2_bin, labels=hum2_labels)

windspeed2_bins = np.linspace(df_day["windspeed2"].min(), df_day["windspeed2"].max(), 4)
windspeed2_labels = ["calm", "breezy", "windy"]
df_day["windspeed2_binned"] = pd.cut(df_day["windspeed2"], bins=windspeed2_bins, labels=windspeed2_labels)

# Sidebar for filtering
st.sidebar.header("Filter Data")
season_selected = st.sidebar.multiselect(
    "Select Seasons",
    options=df_day['season'].unique(),
    default=df_day['season'].unique()
)

# Filter data based on user selection
df_filtered = df_day[df_day['season'].isin(season_selected)]

# Title and Introduction
st.title('Bike Sharing Analysis')
st.markdown("This dashboard analyzes bike-sharing trends across different seasons and weather conditions.")

# Visualization 1: Bike rentals based on temperature
st.subheader("Bike Rentals Based on Temperature")
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_filtered, x='temp2', y='cnt', ax=ax1)
ax1.set_title('Jumlah Penyewaan Sepeda Berdasarkan Suhu')
ax1.set_xlabel('Suhu (temp2)')
ax1.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig1)

# Visualization 2: Bike rentals by month
st.subheader("Bike Rentals by Month")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_filtered, x='mnth', y='casual', marker='o', color='red', label='Casual', ax=ax2)
sns.lineplot(data=df_filtered, x='mnth', y='registered', marker='o', color='blue', label='Registered', ax=ax2)
ax2.set_title('Jumlah Penyewaan Sepeda Berdasarkan Bulan')
ax2.set_xlabel('Bulan')
ax2.set_ylabel('Jumlah Penyewaan')
ax2.legend()
st.pyplot(fig2)

# Visualization 3: Bike rentals by season
st.subheader("Bike Rentals by Season")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(data=df_filtered, x='season', y='cnt', ax=ax3)
ax3.set_title('Jumlah Penyewaan Sepeda Berdasarkan Musim')
ax3.set_xlabel('Musim')
ax3.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig3)

# Conclusion
st.markdown('''**Conclusion:**
- The highest number of users is recorded in hot weather.
- Both user groups peak in the summer months, particularly in June and July.
''')
