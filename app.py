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

# --- YAN MENÜ (ALIŞKANLIK YÖNETİMİ) ---
with st.sidebar:
    st.header("⚙️ Ayarlar")
    yeni_aliskanlik = st.text_input("Yeni Alışkanlık Ekle:")
    if st.button("Ekle"):
        if yeni_aliskanlik and yeni_aliskanlik not in st.session_state.my_habits:
            st.session_state.my_habits.append(yeni_aliskanlik)
            st.rerun()
    
    st.write("---")
    st.write("🗑️ Mevcut Alışkanlıkların:")
    for h in st.session_state.my_habits:
        col_h, col_b = st.columns([3, 1])
        col_h.write(h)
        if col_b.button("Sil", key=f"del_{h}"):
            st.session_state.my_habits.remove(h)
            st.rerun()

# --- ANA SAYFA ---
st.title("🚀 Atomik Gelişim Pro")
st.write(f"📅 Bugün: **{datetime.now().strftime('%d %B %Y')}**")

# Alışkanlık Listesi (Tikleme Alanı)
st.subheader("Bugünkü Görevlerin")
check_list = {}
for habit in st.session_state.my_habits:
    check_list[habit] = st.checkbox(habit, key=f"check_{habit}")

tamamlanan = sum(check_list.values())
toplam = len(st.session_state.my_habits)
oran = tamamlanan / toplam if toplam > 0 else 0

# Kaydetme ve Geri Alma Alanı
col_save, col_undo = st.columns([3, 1])

with col_save:
    if st.button("✅ Günü Kaydet", use_container_width=True):
        yeni_gun_no = len(st.session_state.history) + 1
        onceki_deger = st.session_state.history["Bileşik_Büyüme"].iloc[-1] if yeni_gun_no > 1 else 1.0
        # %1 kuralı: Hepsi tamsa %1 artış
        yeni_deger = onceki_deger * 1.01 if oran == 1.0 else onceki_deger
        
        yeni_veri = pd.DataFrame({
            "Tarih": [datetime.now().strftime("%d/%m")],
            "Gün": [yeni_gun_no],
            "Puan": [int(oran*100)],
            "Bileşik_Büyüme": [yeni_deger]
        })
        st.session_state.history = pd.concat([st.session_state.history, yeni_veri], ignore_index=True)
        if oran == 1.0: st.balloons()

with col_undo:
    if st.button("🔄 Geri Al", help="Son kaydı siler"):
        if not st.session_state.history.empty:
            st.session_state.history = st.session_state.history[:-1]
            st.rerun()

# --- HAFTALIK ÖZET VE GRAFİK ---
if not st.session_state.history.empty:
    st.divider()
    
    # Haftalık Özet Tablosu
    st.subheader("📅 Son Kayıtlar")
    # Tabloyu daha şık gösterelim
    tablo_df = st.session_state.history.tail(7)[["Tarih", "Puan"]].copy()
    tablo_df["Puan"] = tablo_df["Puan"].apply(lambda x: f"%{x}")
    st.dataframe(tablo_df.set_index("Tarih").T, use_container_width=True)

    # Gelişim Grafiği
    st.subheader("📈 Gelişim Grafiği")
    fig = px.area(st.session_state.history, x="Gün", y="Bileşik_Büyüme", 
                  title="Bileşik Büyüme (Hedef: %1)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Henüz veri kaydedilmemiş. İlk gününü tamamla ve 'Günü Kaydet' butonuna bas!")



