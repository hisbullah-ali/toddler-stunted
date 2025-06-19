# streamlit_app.py
import streamlit as st
from navigation import render_sidebar
from page import Home, Dashboard, Dataset

# Sidebar & halaman yang dipilih
selected_page = render_sidebar()

# Routing berdasarkan pilihan di sidebar
if selected_page == "Home":
    Home.main()
elif selected_page == "Dashboard":
    Dashboard.main()
elif selected_page == "Dataset":
    Dataset.main()
