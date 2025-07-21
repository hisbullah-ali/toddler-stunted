# streamlit_app.py
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

def main():

    # --- Inisialisasi Session State ---
    def reset_all_inputs():
        st.session_state["prediksi_selesai"] = False
        st.session_state["Jenis Kelamin"] = "laki-laki"
        st.session_state["Umur (bulan)"] = 0
        st.session_state["Tinggi Badan (cm)"] = 0.0
        st.session_state["Berat Badan (kg)"] = 0.0
        st.rerun()

    if "prediksi_selesai" not in st.session_state:
        reset_all_inputs()

    # --- Judul dan Penjelasan ---
    st.title("🔎 Klasifikasi Status Gizi Balita")
    st.markdown(
        """
        Aplikasi ini mengklasifikasikan status gizi balita berdasarkan **jenis kelamin**, **umur (bulan)**, **tinggi badan**, dan **berat badan** 
        menggunakan model **CatBoost Classifier**.
        """
    )
    st.header("👶 Masukkan Data Balita")

    # --- Input Form ---
    col1, col2 = st.columns(2)
    with col1:
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["laki-laki", "perempuan"], key="jenis_kelamin")
        tinggi_badan = st.number_input("Tinggi Badan (cm)", min_value=0.0, max_value=150.0, step=0.1, key="tinggi")
    with col2:
        umur = st.number_input("Umur (bulan)", min_value=0, max_value=60, step=1, key="umur")
        berat_badan = st.number_input("Berat Badan (kg)", min_value=0.0, max_value=50.0, step=0.1, key="berat")

    # --- Tombol ---
    col_pred, col_reset = st.columns([1, 1])
    with col_pred:
        if st.button("🔍 Prediksi Status Gizi"):
            st.session_state["prediksi_selesai"] = True
    with col_reset:
        if st.button("🔄 Reset"):
            reset_all_inputs()

    # --- Prediksi ---
    if st.session_state["prediksi_selesai"]:

        # Load model dan encoder
        model_stunting = joblib.load("model/cb_classifier_model_stunting.pkl")
        model_wasting = joblib.load("model/cb_classifier_model_wasting.pkl")
        label_encoder_stunting = joblib.load("model/stunting_label_encoder_gender.pkl")
        label_encoder_wasting = joblib.load("model/wasting_label_encoder_gender.pkl")

        jenis_kelamin_encoded = 1 if jenis_kelamin == 'laki-laki' else 0
        df_input = pd.DataFrame([{
            "Umur (bulan)": umur,
            "Jenis Kelamin": jenis_kelamin_encoded,
            "Tinggi Badan (cm)": tinggi_badan,
            "Berat Badan (kg)": berat_badan
        }])

        with st.spinner("Memproses prediksi..."):
            pred_stunting = model_stunting.predict(df_input)[0]
            label_stunting = label_encoder_stunting.inverse_transform([pred_stunting])[0]
            pred_wasting = model_wasting.predict(df_input)[0]
            label_wasting = label_encoder_wasting.inverse_transform([pred_wasting])[0]

        # --- Output ---
        st.subheader("📌 Hasil Prediksi Status Gizi Balita:")
        label_s = label_stunting.lower()
        label_w = label_wasting.lower()

        """
        # STUNTING
        st.markdown("#### 📏 Prediksi Status **Stunting**")
        if label_s == "tinggi":
            st.info(f"📈 {label_stunting} -- Pertumbuhan tinggi di atas rata-rata")
        elif label_s == "normal":
            st.success(f"✅ {label_stunting} -- Pertumbuhan sesuai usia")
        elif label_s == "stunted":
            st.warning(f"⚠️ {label_stunting} -- Waspada, kemungkinan stunting ringan")
        elif label_s == "severely stunted":
            st.error(f"❌ {label_stunting} -- Kondisi serius, segera konsultasi ke tenaga medis")
        else:
            st.write(f"ℹ️ {label_stunting}")

        # WASTING
        st.markdown("#### ⚖️ Prediksi Status **Wasting**")
        if label_w == "overweight":
            st.info(f"📈 {label_wasting} -- Berat badan di atas rata-rata")
        elif label_w == "normal":
            st.success(f"✅ {label_wasting} -- Berat badan sesuai")
        elif label_w == "underweight":
            st.warning(f"⚠️ {label_wasting} -- Waspada, kemungkinan kekurangan energi")
        elif label_w == "severely underweight":
            st.error(f"❌ {label_wasting} -- Kondisi sangat kurus, butuh penanganan medis")
        else:
            st.write(f"ℹ️ {label_wasting}")

        st.markdown("---")
        """


        if label_s == "normal" and label_w == "normal":
            st.success("Anak Anda memiliki status gizi **normal** dari sisi tinggi badan dan berat badan.")
            st.markdown("""
            - Pertumbuhan dan berat badan balita sesuai standar WHO.
            - Tidak ada indikasi kekurangan gizi dari aspek tinggi maupun berat badan.
            """)

        elif label_s == "normal" and label_w == "severely underweight":
            st.error("Anak Anda memiliki **tinggi badan normal**, namun **berat badan sangat kurang**.")
            st.markdown("""
            - Tinggi badan sesuai standar, namun berat badan sangat rendah.
            - Waspadai kemungkinan kekurangan energi kronis.
            - Segera konsultasikan ke tenaga medis untuk penanganan lebih lanjut.
            """)

        elif label_s == "normal" and label_w == "underweight":
            st.warning("Anak Anda memiliki **tinggi badan normal**, namun **berat badan kurang**.")
            st.markdown("""
            - Tinggi badan sesuai usia, namun berat badan agak rendah.
            - Perlu perhatian terhadap asupan gizi harian.
            """)

        elif label_s == "normal" and label_w == "overweight":
            st.warning("Anak Anda memiliki **tinggi badan normal**, namun **kelebihan berat badan**.")
            st.markdown("""
            - Tinggi badan sesuai, tetapi berat badan melebihi standar.
            - Jaga pola makan dan aktivitas fisik agar tidak berkembang menjadi obesitas.
            """)

        elif label_s == "severely stunted" and label_w == "normal":
            st.error("Anak Anda mengalami **stunting berat** dengan **berat badan normal**.")
            st.markdown("""
            - Tinggi badan sangat kurang untuk usianya, meskipun berat badan sesuai.
            - Kondisi ini tetap membutuhkan intervensi karena keterlambatan pertumbuhan.
            """)

        elif label_s == "severely stunted" and label_w == "severely underweight":
            st.error("Anak Anda mengalami **stunting berat** dan **berat badan sangat kurang**.")
            st.markdown("""
            - Ini adalah kondisi serius, menunjukkan kekurangan gizi kronis dan akut.
            - Segera konsultasikan ke dokter atau puskesmas terdekat.
            """)

        elif label_s == "severely stunted" and label_w == "underweight":
            st.error("Anak Anda mengalami **stunting berat** dan **berat badan kurang**.")
            st.markdown("""
            - Tinggi badan dan berat badan di bawah standar WHO.
            - Diperlukan pemantauan dan intervensi gizi segera.
            """)

        elif label_s == "severely stunted" and label_w == "overweight":
            st.error("Anak Anda mengalami **stunting berat** namun **kelebihan berat badan**.")
            st.markdown("""
            - Tinggi badan kurang, tapi berat badan berlebih.
            - Perlu pemeriksaan lanjutan karena bisa jadi ada gangguan metabolisme.
            """)

        elif label_s == "stunted" and label_w == "normal":
            st.warning("Anak Anda mengalami **stunting ringan** dengan **berat badan normal**.")
            st.markdown("""
            - Balita tergolong pendek untuk usianya, namun berat badan sesuai.
            - Pantau terus pertumbuhannya dan pastikan asupan gizinya cukup.
            """)

        elif label_s == "stunted" and label_w == "severely underweight":
            st.error("Anak Anda mengalami **stunting ringan** dan **berat badan sangat kurang**.")
            st.markdown("""
            - Ini adalah tanda kekurangan gizi yang cukup serius.
            - Segera konsultasikan ke petugas kesehatan.
            """)

        elif label_s == "stunted" and label_w == "underweight":
            st.warning("Anak Anda mengalami **stunting ringan** dan **berat badan kurang**.")
            st.markdown("""
            - Anak memiliki kekurangan pertumbuhan di kedua aspek.
            - Perlu perhatian terhadap asupan nutrisi dan lingkungan sehat.
            """)

        elif label_s == "stunted" and label_w == "overweight":
            st.warning("Anak Anda mengalami **stunting ringan** namun **kelebihan berat badan**.")
            st.markdown("""
            - Tinggi badan rendah, namun berat badan berlebih.
            - Perlu evaluasi karena mungkin terjadi disproporsi pertumbuhan.
            """)

        elif label_s == "tinggi" and label_w == "normal":
            st.info("Anak Anda memiliki **tinggi badan di atas rata-rata** dan **berat badan normal**.")
            st.markdown("""
            - Pertumbuhan sangat baik, melebihi rata-rata tinggi anak seusianya.
            - Berat badan pun sesuai, menandakan status gizi baik.
            """)

        elif label_s == "tinggi" and label_w == "underweight":
            st.warning("Anak Anda memiliki **tinggi badan di atas rata-rata**, namun **berat badan kurang**.")
            st.markdown("""
            - Pertumbuhan tinggi bagus, namun berat badannya tidak sebanding.
            - Perlu perbaikan asupan gizi agar pertumbuhan tetap seimbang.
            """)

        elif label_s == "tinggi" and label_w == "severely underweight":
            st.error("Anak Anda memiliki **tinggi badan di atas rata-rata**, namun **berat badan sangat kurang**.")
            st.markdown("""
            - Walaupun tinggi badannya bagus, berat badan sangat rendah bisa membahayakan kesehatan.
            - Perlu intervensi medis segera untuk memperbaiki keseimbangan gizi.
            """)

        elif label_s == "tinggi" and label_w == "overweight":
            st.info("Anak Anda memiliki **tinggi badan di atas rata-rata** dan **kelebihan berat badan**.")
            st.markdown("""
            - Pertumbuhan tubuh sangat cepat, baik tinggi maupun berat.
            - Tetap pantau asupan makanan dan aktivitas agar tetap sehat dan seimbang.
            """)
        
        st.markdown("---")

        """
        # Edukasi
        st.markdown("### 📚 Penjelasan Status Gizi")
        st.markdown("#### 🧬 **Stunting**")
        if label_s == "tinggi":
            st.markdown("- Pertumbuhan sangat baik. Balita memiliki tinggi badan di atas rata-rata untuk usianya.")
        elif label_s == "normal":
            st.markdown("- Pertumbuhan sesuai standar WHO. Tidak ada indikasi kekurangan gizi dari aspek tinggi badan.")
        elif label_s == "stunted":
            st.markdown("- Balita tergolong pendek untuk usianya. Ini dapat menjadi indikasi awal stunting.")
        elif label_s == "severely stunted":
            st.markdown("- Tinggi badan sangat kurang untuk usianya. Stunting berat membutuhkan perhatian medis.")

        st.markdown("#### 🍽️ **Wasting**")
        if label_w == "overweight":
            st.markdown("- Berat badan berlebih untuk tinggi dan usia. Perlu dikontrol agar tidak obesitas.")
        elif label_w == "normal":
            st.markdown("- Berat badan sesuai untuk tinggi badan. Kondisi gizi baik.")
        elif label_w == "underweight":
            st.markdown("- Berat badan rendah untuk tinggi dan usia. Waspadai kemungkinan kekurangan energi.")
        elif label_w == "severely underweight":
            st.markdown("- Kondisi sangat kurus. Segera konsultasikan ke petugas kesehatan.")
        """
        
        # Rekomendasi
        st.markdown("### 🩺 Rekomendasi Umum")
        st.markdown("""
        - Pantau pertumbuhan balita secara rutin menggunakan buku KIA atau aplikasi kesehatan digital.
        - Pastikan balita mendapat **asupan gizi seimbang**, termasuk **protein**, **karbohidrat**, dan **vitamin**.
        - Berikan imunisasi dan ASI eksklusif (jika masih usia bayi).
        - Jika hasil prediksi menunjukkan stunting atau wasting, segera **konsultasikan ke posyandu atau puskesmas terdekat**.
        """)

    # Footer
    st.markdown("---")
    st.markdown(
        "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
        unsafe_allow_html=True
    )
