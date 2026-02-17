import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Atomik Gelişim Pro", page_icon="🎯", layout="centered")

# --- VERİ SİSTEMİ BAŞLATMA ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Tarih", "Gün", "Puan", "Bileşik_Büyüme"])

if 'my_habits' not in st.session_state:
    st.session_state.my_habits = ["📚 Kitap Okumak", "💪 Spor Yapmak", "💧 Su İçmek"]

# --- YAN MENÜ (AYARLAR) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    yeni_aliskanlik = st.text_input("Yeni Alışkanlık Ekle:")
    if st.button("Ekle"):
        if yeni_aliskanlik and yeni_aliskanlik not in st.session_state.my_habits:
            st.session_state.my_habits.append(yeni_aliskanlik)
            st.rerun()
    
    st.write("---")
    st.write("🗑️ Alışkanlık Sil:")
    for h in st.session_state.my_habits:
        if st.button(f"Sil: {h}", key=h):
            st.session_state.my_habits.remove(h)
            st.rerun()

# --- ANA SAYFA ---
st.title("🚀 Atomik Gelişim Pro")
st.write(f"📅 Bugün: **{datetime.now().strftime('%d %B %Y')}**")

# Alışkanlık Seçimi
st.subheader("Bugünkü Görevlerin")
check_list = {}
for habit in st.session_state.my_habits:
    check_list[habit] = st.checkbox(habit)

tamamlanan = sum(check_list.values())
toplam = len(st.session_state.my_habits)
oran = tamamlanan / toplam if toplam > 0 else 0

# Kaydetme ve Geri Alma Butonları
col_save, col_undo = st.columns([3, 1])

with col_save:
    if st.button("✅ Günü Kaydet", use_container_width=True):
        yeni_gun_no = len(st.session_state.history) + 1
        onceki_deger = st.session_state.history["Bileşik_Büyüme"].iloc[-1] if yeni_gun_no > 1 else 1.0
        # %1 kuralı: Hepsi tamsa %1 artış
        yeni_deger = onceki_deger * 1.01 if oran == 1.0 else onceki_deger
        
        yeni_veri = pd.DataFrame({
            "T
            "


