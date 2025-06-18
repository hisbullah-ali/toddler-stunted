import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------- Styling -------------------
st.markdown("""
    <style>
        .main { background-color: #eaf6ff; }
        .sidebar .sidebar-content { background-color: #ffe6e6; }
        h1, h2, h3 { color: #003366; }
    </style>
""", unsafe_allow_html=True)

# ------------------- Judul -------------------
st.markdown("# 📊 Dashboard Status Gizi Balita")
st.markdown("Silakan pilih status gizi yang ingin divisualisasikan: **Stunting** atau **Wasting**.")

# ------------------- Load Dataset -------------------
df_stunting = pd.read_csv("dataset/stunting.csv")
df_wasting = pd.read_csv("dataset/wasting.csv")

# ------------------- Warna Status Gizi -------------------
colors_stunting = {
    'stunted': 'red',
    'severely stunted': 'purple',
    'tinggi': 'green',
    'normal': 'blue'
}

colors_wasting = {
    'underweight': 'orange',
    'severely underweight': 'red',
    'overweight': 'yellow',
    'normal': 'green'
}

# ------------------- Pilihan Status Gizi -------------------
pilihan = st.selectbox("Pilih Status Gizi:", ["Stunting", "Wasting"])

st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        cursor: pointer !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------- Fungsi Tampilkan Grafik -------------------
def tampilkan_grafik_stunting(df):
    df_used = df.sample(n=1000, random_state=42) if len(df) > 1000 else df

    with st.spinner("📊 Memuat grafik stunting..."):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(
            data=df_used,
            x='Umur (bulan)',
            y='Tinggi Badan (cm)',
            hue='Status Gizi',
            palette=colors_stunting,
            ax=ax,
            legend=False
        )
        ax.set_title('Umur (bulan) vs Tinggi Badan (cm) - Stunting')
        ax.set_xlabel('Umur (bulan)')
        ax.set_ylabel('Tinggi Badan (cm)')
        st.pyplot(fig)

        st.markdown("""
        Grafik ini menampilkan hubungan antara **umur balita (bulan)** dan **tinggi badan (cm)**.  
        Setiap titik mewakili satu anak, dan warna menunjukkan kategori status gizi menurut WHO:
        - 🔵 **Normal**: Tinggi badan sesuai standar
        - 🟢 **Tinggi**: Tinggi badan di atas rata-rata
        - 🔴 **Stunted**: Tinggi badan di bawah standar
        - 🟣 **Severely Stunted**: Tinggi badan jauh di bawah standar
        """)

        st.divider()

    with st.spinner("📈 Memuat pie chart..."):
        male_counts = df[df['Jenis Kelamin'] == 'laki-laki']['Status Gizi'].value_counts()
        female_counts = df[df['Jenis Kelamin'] == 'perempuan']['Status Gizi'].value_counts()
        data = [male_counts, female_counts]
        titles = ['Laki-laki', 'Perempuan']

        fig2, axes = plt.subplots(1, 2, figsize=(8, 4))
        for i in range(2):
            pie_colors = [colors_stunting[label] for label in data[i].index]
            axes[i].pie(
                data[i],
                labels=data[i].index,
                autopct='%1.1f%%',
                startangle=90,
                explode=[0.05] * len(data[i]),
                wedgeprops={'edgecolor': 'black', 'linewidth': 1},
                colors=pie_colors
            )
            axes[i].set_title(titles[i])

        fig2.suptitle("Distribusi Status Gizi Stunting Berdasarkan Jenis Kelamin", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig2)

        st.markdown("""
        Diagram lingkaran ini menunjukkan **proporsi status gizi** pada anak laki-laki dan perempuan.  
        Setiap warna mewakili kategori status gizi yang sama seperti pada grafik scatter.  
        Dengan ini, kita bisa melihat apakah ada perbedaan distribusi status gizi antara laki-laki dan perempuan.
        """)


def tampilkan_grafik_wasting(df):
    df_used = df.sample(n=1000, random_state=42) if len(df) > 1000 else df

    with st.spinner("📊 Memuat grafik wasting..."):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(
            data=df_used,
            x='Umur (bulan)',
            y='Berat Badan (kg)',
            hue='Status Gizi',
            palette=colors_wasting,
            ax=ax,
            legend=False
        )
        ax.set_title('Umur (bulan) vs Berat Badan (kg) - Wasting')
        ax.set_xlabel('Umur (bulan)')
        ax.set_ylabel('Berat Badan (kg)')
        st.pyplot(fig)

        st.markdown("""
        Grafik ini menampilkan hubungan antara **umur balita (bulan)** dan **berat badan (kg)**.  
        Setiap titik mewakili satu anak, dan warna menunjukkan status gizi berdasarkan berat badan menurut WHO:
        - 🟢 **Normal**: Berat badan sesuai standar
        - 🟠 **Underweight**: Berat badan di bawah standar
        - 🔴 **Severely Underweight**: Berat badan jauh di bawah standar
        - 🟡 **Overweight**: Berat badan di atas rata-rata
        """)

        st.divider()

    with st.spinner("📈 Memuat pie chart..."):
        male_counts = df[df['Jenis Kelamin'] == 'laki-laki']['Status Gizi'].value_counts()
        female_counts = df[df['Jenis Kelamin'] == 'perempuan']['Status Gizi'].value_counts()
        data = [male_counts, female_counts]
        titles = ['Laki-laki', 'Perempuan']

        fig2, axes = plt.subplots(1, 2, figsize=(8, 4))
        for i in range(2):
            pie_colors = [colors_wasting[label] for label in data[i].index]
            axes[i].pie(
                data[i],
                labels=data[i].index,
                autopct='%1.1f%%',
                startangle=90,
                explode=[0.05] * len(data[i]),
                wedgeprops={'edgecolor': 'black', 'linewidth': 1},
                colors=pie_colors
            )
            axes[i].set_title(titles[i])

        fig2.suptitle("Distribusi Status Gizi Wasting Berdasarkan Jenis Kelamin", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig2)

        st.markdown("""
        Diagram ini memperlihatkan **proporsi status gizi** berdasarkan berat badan untuk anak laki-laki dan perempuan.  
        Tujuannya untuk melihat apakah ada kecenderungan perbedaan status gizi antar jenis kelamin dalam hal berat badan.
        """)


# ------------------- Tampilkan Sesuai Pilihan -------------------
if pilihan == "Stunting":
    tampilkan_grafik_stunting(df_stunting)
else:
    tampilkan_grafik_wasting(df_wasting)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<center><small>© 2025 Said Ali Nuryudha Hisbullah • Informatika UIN Jakarta</small></center>",
    unsafe_allow_html=True
)