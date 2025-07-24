import streamlit as st

#halaman sidebar
def render_sidebar():
    st.sidebar.title("Navigasi Gizi Balita")
    selected_page = st.sidebar.radio(
        "Pilih halaman",
        ["Home", "Dashboard", "Dataset", "BB & TB Ideal", "Rekomendasi Gizi"],
        index=0
    )
    #sidebar info
    st.sidebar.markdown("---")
    st.sidebar.info("Aplikasi ini untuk mengklasifikasikan **status gizi balita** berdasarkan data tinggi badan, berat badan, umur, dan jenis kelamin.")

    return selected_page
