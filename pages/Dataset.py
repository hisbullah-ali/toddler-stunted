import streamlit as st
import pandas as pd

df_stunting = pd.read_csv("dataset/stunting.csv")
df_wasting = pd.read_csv("dataset/wasting.csv")

st.title("🗂️ Dataset Status Gizi Balita")
st.subheader("Dataset Stunting pada Balita:")
st.markdown("""
**Penjelasan Dataset:**

Dataset di bawah ini merupakan data yang digunakan untuk klasifikasi status gizi balita **(stunting)**. Dataset ini terdiri dari beberapa kolom utama, yaitu:

- **Umur (bulan)**: Usia balita dalam satuan bulan.
- **Jenis Kelamin**: Jenis kelamin balita, biasanya terdiri dari 'laki-laki' dan 'perempuan'.
- **Tinggi Badan (cm)**: Tinggi badan balita dalam satuan sentimeter (cm).
- **Status Gizi**: Label atau target klasifikasi yang menunjukkan status gizi balita, seperti *severely stunted*, *stunted*, *normal*, atau *tinggi* (tall).

Data ini akan digunakan untuk melatih model machine learning dalam memprediksi status gizi balita berdasarkan umur, jenis kelamin, dan tinggi badan.
""")

st.dataframe(df_stunting)
st.divider()

st.subheader("Dataset Wasting pada Balita:")
st.markdown("""
**Penjelasan Dataset:**

Dataset berikut ini merupakan data yang digunakan untuk klasifikasi status gizi balita berdasarkan **berat badan (wasting)**. Dataset ini terdiri dari beberapa kolom utama, yaitu:

- **Umur (bulan)**: Usia balita dalam satuan bulan.
- **Jenis Kelamin**: Jenis kelamin balita, seperti 'laki-laki' atau 'perempuan'.
- **Berat Badan (kg)**: Berat badan balita dalam satuan kilogram (kg).
- **Status Gizi**: Label atau target klasifikasi yang menunjukkan status gizi balita, seperti *severely underweight*, *underweight*, *normal*, atau *overweight*.

Data ini digunakan untuk melatih model machine learning dalam memprediksi status gizi balita berdasarkan umur, jenis kelamin, dan berat badan.
""")

st.dataframe(df_wasting)


# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
    unsafe_allow_html=True
)