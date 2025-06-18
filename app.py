# streamlit_app.py
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# --- Load model dan encoder ---
model_stunting = joblib.load("model/cb_classifier_model_stunting.pkl")
model_wasting = joblib.load("model/cb_classifier_model_wasting.pkl")
label_encoder_stunting = joblib.load("model/stunting_label_encoder_gender.pkl")
label_encoder_wasting = joblib.load("model/wasting_label_encoder_gender.pkl")

# --- Konfigurasi halaman ---
st.set_page_config(page_title="Klasifikasi Gizi Balita", page_icon="🤱🏻", layout="centered")
st.title("🔎 Klasifikasi Status Gizi Balita")
st.markdown(
    """
    Aplikasi ini mengklasifikasikan status gizi balita berdasarkan **jenis kelamin**, **umur (bulan)**, **tinggi badan**, dan **berat badan** 
    menggunakan model **CatBoost Classifier**.
    """
)

# --- Input Data ---
st.header("🧒 Masukkan Data Balita")
col1, col2, col3 = st.columns(3)
with col1:
    jenis_kelamin = st.selectbox("Jenis Kelamin", ["laki-laki", "perempuan"])
    umur = st.number_input("Umur (bulan)", min_value=0, max_value=60, step=1)

with col2:
    tinggi_badan = st.number_input("Tinggi Badan (cm)", min_value=0.0, max_value=150.0, step=0.1)

with col3:
    berat_badan = st.number_input("Berat Badan (kg)", min_value=0.0, max_value=50.0, step=0.1)

# --- Prediksi ---
st.markdown("### 🔍 Hasil Prediksi")
if st.button("Prediksi Status Gizi"):

    # Encode jenis kelamin untuk kedua model
    #encoded_gender_stunting = label_encoder_stunting.transform([jenis_kelamin])[0]
    #encoded_gender_wasting = label_encoder_wasting.transform([jenis_kelamin])[0]
    jenis_kelamin_encoded = 1 if jenis_kelamin == 'laki-laki' else 0

    # Buat dataframe input (asumsi fitur sama)
    df_input = pd.DataFrame([{
        "Umur (bulan)": umur,
        "Jenis Kelamin": jenis_kelamin_encoded,
        "Tinggi Badan (cm)": tinggi_badan,
        "Berat Badan (kg)": berat_badan
    }])

    with st.spinner("Memproses prediksi..."):

        # Prediksi stunting
        pred_stunting = model_stunting.predict(df_input)[0]
        label_stunting = label_encoder_stunting.inverse_transform([pred_stunting])[0]

        # Prediksi wasting
        df_input["Jenis Kelamin"] = jenis_kelamin_encoded
        pred_wasting = model_wasting.predict(df_input)[0]
        label_wasting = label_encoder_wasting.inverse_transform([pred_wasting])[0]

    # --- Output ---
    st.subheader("📌 Hasil Prediksi Status Gizi Balita:")

    label_s = label_stunting.lower()
    label_w = label_wasting.lower()

    # STUNTING
    st.markdown("#### 📏 Prediksi Status **Stunting**")
    if label_s in ["tinggi", "tall"]:
        st.info(f"📈 {label_stunting} – Pertumbuhan tinggi di atas rata-rata")
    elif label_s == "normal":
        st.success(f"✅ {label_stunting} – Pertumbuhan sesuai usia")
    elif label_s in ["pendek", "stunted"]:
        st.warning(f"⚠️ {label_stunting} – Waspada, kemungkinan stunting ringan")
    elif label_s in ["sangat pendek", "severely stunted"]:
        st.error(f"❌ {label_stunting} – Kondisi serius, segera konsultasi ke tenaga medis")
    else:
        st.write(f"ℹ️ {label_stunting}")

    # WASTING
    st.markdown("#### ⚖️ Prediksi Status **Wasting**")
    if label_w in ["gemuk", "overweight"]:
        st.info(f"📈 {label_wasting} – Berat badan di atas rata-rata")
    elif label_w == "normal":
        st.success(f"✅ {label_wasting} – Berat badan sesuai")
    elif label_w in ["kurus", "underweight"]:
        st.warning(f"⚠️ {label_wasting} – Waspada, kemungkinan kekurangan energi")
    elif label_w in ["sangat kurus", "severely underweight"]:
        st.error(f"❌ {label_wasting} – Kondisi sangat kurus, butuh penanganan medis")
    else:
        st.write(f"ℹ️ {label_wasting}")

    # --- Visualisasi Grafik Batang ---
    st.markdown("### 📉 Visualisasi Status Gizi")

    fig, ax = plt.subplots(figsize=(6, 3))
    statuses = ['Stunting', 'Wasting']
    predictions = [label_stunting, label_wasting]
    colors = ['skyblue', 'lightgreen']

    ax.bar(statuses, [1, 1], color=colors, edgecolor='black')
    for i, label in enumerate(predictions):
        ax.text(i, 1.05, label, ha='center', fontsize=12, fontweight='bold')

    ax.set_ylim(0, 1.3)
    ax.axis('off')
    st.pyplot(fig)

    # --- Penjelasan Edukatif ---
    st.markdown("### 📚 Penjelasan Status Gizi")

    st.markdown("#### 🧬 **Stunting**")
    if label_s in ["tinggi", "tall"]:
        st.markdown("- Pertumbuhan sangat baik. Balita memiliki tinggi badan di atas rata-rata untuk usianya.")
    elif label_s == "normal":
        st.markdown("- Pertumbuhan sesuai standar WHO. Tidak ada indikasi kekurangan gizi dari aspek tinggi badan.")
    elif label_s in ["pendek", "stunted"]:
        st.markdown("- Balita tergolong pendek untuk usianya. Ini dapat menjadi indikasi awal stunting.")
    elif label_s in ["sangat pendek", "severely stunted"]:
        st.markdown("- Tinggi badan sangat kurang untuk usianya. Stunting berat membutuhkan perhatian medis.")

    st.markdown("#### 🍽️ **Wasting**")
    if label_w in ["gemuk", "overweight"]:
        st.markdown("- Berat badan berlebih untuk tinggi dan usia. Perlu dikontrol agar tidak obesitas.")
    elif label_w == "normal":
        st.markdown("- Berat badan sesuai untuk tinggi badan. Kondisi gizi baik.")
    elif label_w in ["kurus", "underweight"]:
        st.markdown("- Berat badan rendah untuk tinggi dan usia. Waspadai kemungkinan kekurangan energi.")
    elif label_w in ["sangat kurus", "severely underweight"]:
        st.markdown("- Kondisi sangat kurus. Segera konsultasikan ke petugas kesehatan.")

    # --- Rekomendasi ---
    st.markdown("### 🩺 Rekomendasi Umum")
    st.markdown("""
    - Pantau pertumbuhan balita secara rutin menggunakan buku KIA atau aplikasi kesehatan digital.
    - Pastikan balita mendapat **asupan gizi seimbang**, termasuk **protein**, **karbohidrat**, dan **vitamin**.
    - Berikan imunisasi dan ASI eksklusif (jika masih usia bayi).
    - Jika hasil prediksi menunjukkan stunting atau wasting, segera **konsultasikan ke posyandu atau puskesmas terdekat**.
    """)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
    unsafe_allow_html=True
)

def make_sidebar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4280/4280638.png", width=60)
        st.markdown("### 📁 Navigasi")
        
        st.page_link("pages/Dashboard.py", label="Dashboard Status Gizi", icon="📝")
        st.page_link("pages/Dataset.py", label="Dataset Terkait", icon="👤")
        #st.page_link("pages/ltkm-institusi.py", label="LTKM Institusi", icon="🏢")
        #st.page_link("pages/screening.py", label="Screening", icon="🩺")
        #st.page_link("pages/search-kyc.py", label="Search KYC", icon="🔍")
        #st.page_link("pages/search-transaction.py", label="Search Transaction", icon="💳")

        st.write("---")
        if st.button("🔄 Reset Aplikasi"):
            st.rerun()
