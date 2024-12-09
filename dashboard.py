import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st

# Load the data
day_df = pd.read_csv('day_df.csv')  # Menampilkan data dari file
st.title("Dasbor Penyewaan Sepeda")

# Menampilakan data
st.subheader("Data Penyewaan Sepeda")
st.table(day_df.head(20))

# Memberikan Select Box untuk memilih musim
st.subheader("Eksplorasi Interaktif")
season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
season_filter = st.selectbox(
    "Pilih Musim untuk Ditampilkan:",
    options=[-1] + list(season_mapping.keys()),  # Add -1 for "Semua"
    format_func=lambda x: "Semua" if x == -1 else season_mapping[x]
)
if season_filter != -1:
    filtered_df = day_df[day_df['season'] == season_filter]
else:
    filtered_df = day_df

# Menampilkan data yang sudah difilter
st.write(f"Menampilkan data untuk musim: {'Semua' if season_filter == -1 else season_mapping[season_filter]}")
st.dataframe(filtered_df)

# Menampilkan distribusi jumlah penyewaan sepeda berdasarkan kondisi cuaca
st.subheader("Distribusi Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
weather_mapping = {1: "Cerah", 2: "Berawan", 3: "Hujan/Bersalju", 4: "Badai"}
selected_weather = st.multiselect(
    "Pilih Kondisi Cuaca (dapat memilih lebih dari satu):",
    options=day_df['weathersit'].unique(),
    default=day_df['weathersit'].unique(),
    format_func=lambda x: weather_mapping[x]
)
weather_filtered_df = filtered_df[filtered_df['weathersit'].isin(selected_weather)]

fig, ax = plt.subplots(figsize=(15, 6))
sns.boxplot(x='weathersit', y='cnt', data=weather_filtered_df, ax=ax)
plt.title('Distribusi Jumlah Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca [weathersit]')
plt.ylabel('Jumlah Penyewaan [cnt]')
plt.xticks(
    ticks=range(1, 5),
    labels=[weather_mapping[i] for i in range(1, 5)],
    rotation=0
)
st.pyplot(fig)

# Pengaruh musim terhadap jumlah penyewaan sepeda
st.subheader("Pengaruh Musim terhadap Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(15, 7))
sns.boxplot(x='season', y='cnt', data=filtered_df, ax=ax)
plt.title('Pengaruh Musim terhadap Jumlah Penyewaan Sepeda')
plt.ylabel('Jumlah Sewa [cnt]')
plt.xlabel('Kondisi Musim [season]')
plt.xticks(ticks=range(1, 5), labels=[season_mapping[i] for i in range(1, 5)], rotation=0)
st.pyplot(fig)

st.subheader("Rata-rata Suhu Tiap Musim")
suhuMean= day_df.groupby('season')['temp'].mean().reset_index()
suhuMean.columns = ['Season', 'Average Temperature']

plt.figure(figsize=(14, 6))
sns.barplot(x='Season', y='Average Temperature', data=suhuMean)
plt.title('Rata-rata suhu tiap musim')
plt.ylabel('Suhu rata-rata(_x 41 untuk mencari suhu asli)')
plt.xlabel('Musim')
plt.xticks(ticks=[0, 1, 2, 3], labels=['Semi', 'Panas', 'Gugur', 'Dingin'])
plt.show()

# Additional Analysis: Custom threshold for rentals
st.subheader("Jumlah Penyewaan Melebihi Ambang Batas")
rental_threshold = st.slider(
    "Tentukan Ambang Batas Jumlah Penyewaan:",
    min_value=int(day_df['cnt'].min()),
    max_value=int(day_df['cnt'].max()),
    value=int(day_df['cnt'].mean())
)
high_rental_df = filtered_df[filtered_df['cnt'] > rental_threshold]

st.write(f"Jumlah data di atas ambang batas ({rental_threshold}): {len(high_rental_df)}")
st.dataframe(high_rental_df)