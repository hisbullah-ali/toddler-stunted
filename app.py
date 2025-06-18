# streamlit_app.py
import streamlit as st
import pandas as pd
import joblib

# --- Load model dan encoder ---
model_stunting = joblib.load("cb_classifier_model_stunting.pkl")
model_wasting = joblib.load("cb_classifier_model_wasting.pkl")
label_encoder_stunting = joblib.load("stunting_label_encoder_gender.pkl")
label_encoder_wasting = joblib.load("wasting_label_encoder_gender.pkl")

# --- Judul dan Deskripsi Aplikasi ---
st.set_page_config(page_title="Prediksi Gizi Balita", page_icon="🧒", layout="centered")
#st.image("logo.png", width=80)  # Ganti dengan nama file logomu jika ada
st.title("📊 Prediksi Status Gizi Balita")
st.markdown(
    """
    Aplikasi ini memprediksi status gizi balita berdasarkan **jenis kelamin**, **umur (bulan)**, **tinggi badan**, dan **berat badan** 
    menggunakan model **CatBoost Classifier**.
    """
)

# --- Input Data ---
st.header("🧒 Masukkan Data Balita")

col1, col2, col3 = st.columns(2)
with col1:
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["laki-laki", "perempuan"])
    umur = st.number_input("Umur (bulan)", min_value=0, max_value=60, step=1)

with col2:
    tinggi_badan = st.number_input("Tinggi Badan (cm)", min_value=30.0, max_value=150.0, step=0.1)

with col3:
    berat_badan = st.number_input("Berat Badan (kg)", min_value=2.0, max_value=50.0, step=0.1)

# --- Tombol Prediksi ---
st.markdown("### 🔍 Hasil Prediksi")
if st.button("Prediksi Status Gizi"):

    # Encode jenis kelamin
    jenis_kelamin_encoded = 1 if jenis_kelamin == 'laki-laki' else 0

    # Buat dataframe input
    df_input = pd.DataFrame([{
        "Umur (bulan)": umur,
        "Jenis Kelamin": jenis_kelamin_encoded,
        "Tinggi Badan (cm)": tinggi_badan,
        "Berat Badan (kg)": berat_badan
    }])

    # Prediksi
    with st.spinner("Memproses prediksi..."):
        prediction = model.predict(df_input)[0]
        prediction_label = label_encoder.inverse_transform([prediction])[0] \
            if prediction in label_encoder.transform(label_encoder.classes_) else prediction

    # Output dengan warna berbeda
    # Output dinamis berdasarkan status gizi
    label = prediction_label.lower()

    if label in ["tinggi", "tall"]:
        st.info(f"📈 Status Gizi Balita: **{prediction_label}** – Pertumbuhan di atas rata-rata")
    elif label in ["normal", "normal"]:
        st.success(f"✅ Status Gizi Balita: **{prediction_label}** – Pertumbuhan sesuai usia")
    elif label in ["stunted", "pendek"]:
        st.warning(f"⚠️ Status Gizi Balita: **{prediction_label}** – Perlu perhatian, balita mengalami stunting")
    elif label in ["severely stunted", "sangat pendek"]:
        st.error(f"❌ Status Gizi Balita: **{prediction_label}** – Kondisi serius, segera konsultasi ke tenaga medis")
    else:
        st.write(f"ℹ️ Status Gizi Balita: **{prediction_label}**")


# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
    unsafe_allow_html=True
)
