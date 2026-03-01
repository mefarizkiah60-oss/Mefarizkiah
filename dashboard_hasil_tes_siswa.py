
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Hasil Tes Siswa", layout="wide")
st.title("📊 Dashboard Analisis Hasil Tes 50 Siswa")
st.markdown("Analisis performa siswa berdasarkan 20 butir soal")

# ==============================
# LOAD DATA
# ==============================
df = pd.read_excel("data_simulasi_50_siswa_20_soal.xlsx")

# Hitung skor total tiap siswa
df["Total Skor"] = df.iloc[:, 1:].sum(axis=1)

# ==============================
# KPI UTAMA
# ==============================
rata_rata = df["Total Skor"].mean()
skor_maks = df["Total Skor"].max()
skor_min = df["Total Skor"].min()

col1, col2, col3 = st.columns(3)
col1.metric("📈 Rata-rata Skor", f"{rata_rata:.2f}")
col2.metric("🏆 Skor Tertinggi", skor_maks)
col3.metric("📉 Skor Terendah", skor_min)

st.divider()

# ==============================
# DISTRIBUSI NILAI
# ==============================
st.header("📊 Distribusi Skor Siswa")

fig1, ax1 = plt.subplots()
ax1.hist(df["Total Skor"], bins=10)
ax1.set_xlabel("Total Skor")
ax1.set_ylabel("Jumlah Siswa")
ax1.set_title("Histogram Skor Siswa")
st.pyplot(fig1)

st.divider()

# ==============================
# ANALISIS TINGKAT KESULITAN SOAL
# ==============================
st.header("🧠 Analisis Tingkat Kesulitan Soal")

butir = df.iloc[:, 1:-1]
tingkat_kesulitan = butir.mean().sort_values()

fig2, ax2 = plt.subplots(figsize=(8,4))
ax2.bar(tingkat_kesulitan.index, tingkat_kesulitan.values)
ax2.set_ylabel("Proporsi Jawaban Benar")
ax2.set_title("Tingkat Kesulitan Soal")
ax2.set_xticklabels(tingkat_kesulitan.index, rotation=90)

st.pyplot(fig2)

st.success(f"Soal paling sulit: {tingkat_kesulitan.idxmin()}")
st.success(f"Soal paling mudah: {tingkat_kesulitan.idxmax()}")

st.divider()

# ==============================
# KLASIFIKASI SISWA
# ==============================
st.header("👥 Klasifikasi Performa Siswa")

def kategori(x):
    if x >= rata_rata + 2:
        return "Tinggi"
    elif x >= rata_rata - 2:
        return "Sedang"
    else:
        return "Rendah"

df["Kategori"] = df["Total Skor"].apply(kategori)

kategori_count = df["Kategori"].value_counts()

fig3, ax3 = plt.subplots()
ax3.pie(kategori_count, labels=kategori_count.index, autopct="%1.1f%%")
ax3.set_title("Persentase Kategori Siswa")

st.pyplot(fig3)

st.dataframe(df[["Total Skor", "Kategori"]])

st.success("Dashboard Analisis Selesai ✅")
