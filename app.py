import streamlit as st
from navigation import render_sidebar
from page import Home, Dashboard, Dataset, BMI, Kecukupan_Gizi

#bar style chrome
st.set_page_config(page_title="Klasifikasi Gizi Balita", page_icon="🤱🏻", layout="centered")

#sidebar & halaman yang dipilih
selected_page = render_sidebar()

#routing berdasarkan pilihan di sidebar
if selected_page == "Home":
    Home.main()
elif selected_page == "Dashboard":
    Dashboard.main()
elif selected_page == "Dataset":
    Dataset.main()
elif selected_page == "BB & TB Ideal":
    BMI.main()
elif selected_page == "Rekomendasi Gizi":
    Kecukupan_Gizi.main()