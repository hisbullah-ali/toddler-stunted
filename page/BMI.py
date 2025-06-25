import streamlit as st
import pandas as pd

bb_tb_ideal_male = pd.read_csv("dataset/bb_tb_ideal_male.csv")
bb_tb_ideal_female = pd.read_csv("dataset/bb_tb_ideal_female.csv")

def main():
    st.title("⚧️ BB & TB Ideal Balita")
    st.subheader("🧑 BB&TB Ideal pada Balita Laki - laki :")
    st.markdown("Berikut ini adalah tabel berat badan dan tinggi badan anak laki-laki dari usia 0 bulan sampai dengan 5 tahun.")

    st.dataframe(bb_tb_ideal_male)
    st.caption("Tabel di atas menunjukkan berat badan dan tinggi badan ideal untuk balita laki-laki berdasarkan usia dalam bulan. Data ini dapat digunakan sebagai referensi untuk memantau pertumbuhan anak.")
    st.divider()

    st.subheader("👩 BB&TB Ideal pada Balita Perempuan :")
    st.markdown("Berikut ini adalah tabel berat badan dan tinggi badan anak laki-laki dari usia 0 bulan sampai dengan 5 tahun.")

    st.dataframe(bb_tb_ideal_female)
    st.caption("Tabel di atas menunjukkan berat badan dan tinggi badan ideal untuk balita perempuan berdasarkan usia dalam bulan. Data ini dapat digunakan sebagai referensi untuk memantau pertumbuhan anak.")


    # --- Footer ---
    st.markdown("---")
    st.markdown(
        "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
        unsafe_allow_html=True
    )