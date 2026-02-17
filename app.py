import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Atomik %1", layout="centered")

st.title("🚀 Atomik 1% Gelişim")

# Veri Saklama (Mobil uygulama için basit bir simülasyon)
if 'gecmis_veri' not in st.session_state:
    st.session_state.gecmis_veri = pd.DataFrame(columns=["Gün", "İlerleme"])

# Sol Menü: Hedef Ayarı
st.sidebar.header("🎯 Hedef Ayarı")
hedef_gun = st.sidebar.number_input("Yıl Hedefi (Gün)", 1, 365, 365)

# Ana Ekran: Alışkanlıklar
st.subheader("Bugünün Küçük Adımları")
col1, col2 = st.columns(2)

with col1:
    h1 = st.checkbox("📚 Kitap Okuma")
    h2 = st.checkbox("💪 Spor Yapma")
with col2:
    h3 = st.checkbox("💧 Su İçme")
    h4 = st.checkbox("✍️ Günlük Not")

# Değerlendirme ve Not Alanı
gunluk_not = st.text_area("Bugün neyi daha iyi yapabilirdin?", placeholder="Sistemdeki pürüzleri yaz...")

# Hesaplama Mantığı
basari = sum([h1, h2, h3, h4]) / 4

if st.button("Günü Kaydet"):
    yeni_gun = len(st.session_state.gecmis_veri) + 1
    # %1 Bileşik büyüme formülü
    deger = (1.01) ** yeni_gun if basari == 1.0 else (st.session_state.gecmis_veri["İlerleme"].iloc[-1] if yeni_gun > 1 else 1.0)
    
    yeni_satir = pd.DataFrame({"Gün": [yeni_gun], "İlerleme": [deger]})
    st.session_state.gecmis_veri = pd.concat([st.session_state.gecmis_veri, yeni_satir], ignore_index=True)
    st.balloons()

# Grafik: Yıl Bazlı İlerleme
if not st.session_state.gecmis_veri.empty:
    st.write("### 📈 Gelişim Çizgin")
    fig = px.line(st.session_state.gecmis_veri, x="Gün", y="İlerleme", title="37 Kat Büyüme Yolculuğu")
    st.plotly_chart(fig)