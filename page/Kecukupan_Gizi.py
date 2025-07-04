import streamlit as st
from PIL import Image

kecukupan_gizi = Image.open("assets/kecukupan_gizi.png")
kandungan_nutrisi = Image.open("assets/kandungan_nutrisi.png")
kecukupan_gizi_url = "https://stunting.go.id/kemenkes-permenkes-no-28-tahun-2019-angka-kecukupan-gizi-yang-dianjurkan/"
rekomendasi_makanan = "https://repository.binawan.ac.id/3526/"

def main():
    st.title("🚼 Angka Kecukupan Gizi Balita")
    st.subheader("Tabel Angka Kecukupan Gizi Balita")
    st.markdown("Angka Kecukupan Energi, Protein, Lemak, Karbohidrat, Serat, dan Air yang dianjurkan (per orang per hari).")
    st.image(kecukupan_gizi, caption="Tabel Angka Kecukupan Gizi Balita")
    st.caption("Pemenuhan kebutuhan gizi bayi 0-5 bulan bersumber dari pemberian ASI Eksklusif.")

    st.divider()
    
    st.subheader("Tabel Kandungan Nutrisi Pada Makanan")
    st.markdown("Tabel berikut menunjukkan kandungan nutrisi pada berbagai jenis makanan yang umum dikonsumsi oleh balita.")
    st.image(kandungan_nutrisi, caption="Tabel Kandungan Nutrisi Pada Makanan")

    st.divider()
    st.markdown("Sumber Rujukan:")
    st.markdown(f"Rujukan mengenai Angka Kecukupan Gizi yang Dianjurkan dapat diakses melalui [Permenkes No 28 Tahun 2019]({kecukupan_gizi_url}).") 
    st.markdown(f"Rujukan mengenai Kandungan Nutrisi Makanan dan Rekomendasi Makanan untuk balita, dapat diakses melalui [Panduan Gizi Optimal Mengurangi Stunting]({rekomendasi_makanan}).")

    # --- Footer ---
    st.markdown("---")
    st.markdown(
        "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
        unsafe_allow_html=True
    )