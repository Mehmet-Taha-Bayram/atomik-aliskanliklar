import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Atomik Gelişim", page_icon="🚀", layout="centered")

# Stil Dokunuşları (Hatalı kısım burasıydı, düzelttim)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stCheckbox { font-size: 18px; padding: 8px; background: white; border-radius: 10px; margin-bottom: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Atomik %1 Gelişim")
st.write(f"📅 Bugün: **{datetime.now().strftime('%d %B %Y')}**")

# Veri Sistemi
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Gün", "Puan", "Bileşik_Büyüme"])

# Alışkanlıklar
st.subheader("Bugünün Küçük Dev Adımları")
h1 = st.checkbox("📚 Kitap (10 Sayfa)")
h2 = st.checkbox("💪 Spor (20 Dakika)")
h3 = st.checkbox("💧 Su (2 Litre)")
h4 = st.checkbox("🧘 Meditasyon/Not")

tamamlanan = sum([h1, h2, h3, h4])
oran = tamamlanan / 4

if st.button("Günü Tamamla ve Kaydet!", use_container_width=True):
    yeni_gun = len(st.session_state.history) + 1
    onceki_deger = st.session_state.history["Bileşik_Büyüme"].iloc[-1] if yeni_gun > 1 else 1.0
    yeni_deger = onceki_deger * 1.01 if oran == 1.0 else onceki_deger
    
    yeni_veri = pd.DataFrame({"Gün": [yeni_gun], "Puan": [oran*100], "Bileşik_Büyüme": [yeni_deger]})
    st.session_state.history = pd.concat([st.session_state.history, yeni_veri], ignore_index=True)
    
    if oran == 1.0:
        st.balloons()
        st.success("MÜKEMMEL! Bugün %1 daha iyisin.")

# İstatistikler
if not st.session_state.history.empty:
    st.divider()
    c1, c2 = st.columns(2)
    c1.metric("Toplam Gün", len(st.session_state.history))
    son_deger = st.session_state.history["Bileşik_Büyüme"].iloc[-1]
    c2.metric("Toplam Gelişim", f"x{son_deger:.2f}")

    st.subheader("📈 Gelişim Yolculuğun")
    fig = px.area(st.session_state.history, x="Gün", y="Bileşik_Büyüme", color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig, use_container_width=True)

