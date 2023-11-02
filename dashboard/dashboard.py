import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Konfigurasi
st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide", page_icon="🌏", page_title="Analisis Kualitas Udara")

# Memuat data
@st.cache_data
def muat_data():
    return pd.read_csv("main_data.csv")

data = muat_data()
polutan = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

def random_figsize():
    # Mengacak ukuran visualisasi
    return (random.randint(8, 15), random.randint(5, 10))

def random_palette():
    # Mengacak palet warna
    palettes = ['pastel', 'muted', 'bright', 'dark', 'colorblind']
    return random.choice(palettes)

def saringan_samping():
    st.sidebar.header("Penyaringan")
    tahun_mulai, tahun_akhir = st.sidebar.slider("Pilih rentang tahun", min(data["year"]), max(data["year"]),
                                                (min(data["year"]), max(data["year"])))
    stasiun = st.sidebar.multiselect("Pilih stasiun", data['station'].unique(), default=data['station'].unique())
    polutan_terpilih = st.sidebar.selectbox("Pilih polutan:", polutan)

    return tahun_mulai, tahun_akhir, stasiun, polutan_terpilih

def dasbor_utama(tahun_mulai, tahun_akhir, stasiun, polutan_terpilih):
    data_terfilter = data[(data["year"] >= tahun_mulai) & (data["year"] <= tahun_akhir) & (data['station'].isin(stasiun))]

    if len(data_terfilter) == 0:
        st.write("Tidak ada data yang tersedia untuk penyaringan yang dipilih.")
        return

    st.title("Analisis Kualitas Udara")
    st.write("""
    Analisis data kualitas udara berdasarkan berbagai metrik. Gunakan panel samping untuk memilih penyaringan dan jelajahi hubungan antara polutan, faktor meteorologi, dan waktu.
    """)

    col1, col2 = st.columns(2)

    with col1:
        # Visualisasi Peta Korelasi
        kondisi_cuaca = ['TEMP', 'PRES', 'DEWP']
        data_korelasi = data_terfilter[polutan + kondisi_cuaca].corr()
        plt.figure(figsize=random_figsize())
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(data_korelasi, annot=True, cmap=cmap, center=0)
        st.pyplot()

    with col2:
        # Visualisasi Histogram untuk Polutan Terpilih
        plt.figure(figsize=random_figsize())
        sns.histplot(data_terfilter[polutan_terpilih], kde=True, palette=random_palette())
        plt.title(f"Distribusi dari {polutan_terpilih}")
        st.pyplot()

    col3, col4 = st.columns(2)

    with col3:
        # Visualisasi Boxplot untuk Polutan Terpilih
        plt.figure(figsize=random_figsize())
        sns.boxplot(y=data_terfilter[polutan_terpilih], palette=random_palette())
        plt.title(f"Boxplot dari {polutan_terpilih}")
        st.pyplot()

        # Visualisasi Variasi Harian
        plt.figure(figsize=random_figsize())
        data_harian = data_terfilter.groupby("hour")[polutan].mean()
        sns.lineplot(data=data_harian, palette=random_palette())
        plt.title("Rata-rata kadar polutan per jam")
        plt.ylabel("Konsentrasi Polutan")
        st.pyplot()

    with col4:
        # Visualisasi Variasi Musiman
        plt.figure(figsize=random_figsize())
        data_bulanan = data_terfilter.groupby("month")[polutan].mean()
        sns.lineplot(data=data_bulanan, palette=random_palette())
        plt.title("Rata-rata kadar polutan per bulan")
        plt.ylabel("Konsentrasi Polutan")
        st.pyplot()

        # Visualisasi Dampak dari Stasiun Pengukuran
        data_stasiun = data_terfilter.groupby("station")[polutan].mean()
        data_stasiun.sort_values(by=polutan_terpilih, ascending=False, inplace=True)
        plt.figure(figsize=random_figsize())
        sns.barplot(x=data_stasiun.index, y=data_stasiun[polutan_terpilih], palette=random_palette())
        plt.title(f"Rata-rata kadar {polutan_terpilih} per stasiun")
        st.pyplot()

    col5, col6 = st.columns(2)

    with col5:
        # Visualisasi Dampak Hujan pada Kualitas Udara
        plt.figure(figsize=random_figsize())
        color = sns.color_palette(random_palette())[0]
        sns.scatterplot(data=data_terfilter, x="RAIN", y=polutan_terpilih, color=color)
        plt.title(f"Dampak Hujan terhadap {polutan_terpilih}")
        st.pyplot()

    with col6:
        wind_directions = {
            'N': 0, 'NNE': 1/8 * np.pi, 'NE': 1/4 * np.pi, 'ENE': 3/8 * np.pi, 'E': 1/2 * np.pi,
            'ESE': 5/8 * np.pi, 'SE': 3/4 * np.pi, 'SSE': 7/8 * np.pi, 'S': np.pi, 'SSW': 9/8 * np.pi,
            'SW': 5/4 * np.pi, 'WSW': 11/8 * np.pi, 'W': 3/2 * np.pi, 'WNW': 13/8 * np.pi, 'NW': 7/4 * np.pi,
            'NNW': 15/8 * np.pi
        }
        filtered_copy = data_terfilter.copy()
        filtered_copy["wind_radians"] = filtered_copy["wd"].map(wind_directions)
        plt.figure(figsize=random_figsize())
        ax = plt.subplot(111, projection='polar')
        color = sns.color_palette(random_palette())[0]
        ax.scatter(filtered_copy["wind_radians"], filtered_copy[polutan_terpilih], color=color)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        plt.title(f"Impact of Wind Direction on {polutan_terpilih}")
        st.pyplot()

# Eksekusi Utama
tahun_mulai, tahun_akhir, stasiun, polutan_terpilih = saringan_samping()
dasbor_utama(tahun_mulai, tahun_akhir, stasiun, polutan_terpilih)
