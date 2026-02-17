import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Solo Leveling: Atomic Progress", page_icon="🗡️", layout="centered")

# --- SOLO LEVELING STİLİ ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stCheckbox { background: #1a1c23; border: 1px solid #4a90e2; border-radius: 5px; padding: 10px; }
    .level-box { border: 2px solid #4a90e2; padding: 20px; border-radius: 15px; text-align: center; background: linear-gradient(45deg, #12141d, #1a1c23); }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SİSTEMİ ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Tarih", "Gün", "XP", "Bileşik_Büyüme"])

if 'my_habits' not in st.session_state:
    st.session_state.my_habits = ["📚 Günlük Okuma", "💪 Antrenman", "💧 Hidrasyon"]

# --- OYUN MANTIĞI (LEVEL & RANK) ---
total_xp = st.session_state.history["XP"].sum() if not st.session_state.history.empty else 0
level = int((total_xp / 100) ** 0.5) + 1
rank = "E-Rank"
if level > 5: rank = "D-Rank"
if level > 10: rank = "C-Rank"
if level > 20: rank = "B-Rank"
if level > 40: rank = "A-Rank"
if level > 80: rank = "S-Rank"

# --- ÜST PANEL (STATÜ) ---
st.title("🗡️ SYSTEM: DAILY QUEST")
st.markdown(f"""
<div class="level-box">
    <h2 style='color: #4a90e2;'>{rank} Avcı: Taha</h2>
    <p style='font-size: 24px;'><b>LEVEL: {level}</b></p>
    <p>Toplam Tecrübe (XP): {total_xp:.0f}</p>
</div>
""", unsafe_allow_html=True)

# --- GÜNLÜK GÖREVLER ---
st.subheader("📝 Günlük Görev Listesi")
check_list = {}
for habit in st.session_state.my_habits:
    check_list[habit] = st.checkbox(habit, key=f"quest_{habit}")

tamamlanan = sum(check_list.values())
toplam = len(st.session_state.my_habits)
gunluk_basari_orani = tamamlanan / toplam if toplam > 0 else 0

# --- BUTONLAR ---
col_save, col_undo, col_export = st.columns([2, 1, 1])

with col_save:
    if st.button("⚔️ GÖREVİ TAMAMLA", use_container_width=True):
        yeni_gun_no = len(st.session_state.history) + 1
        onceki_buyume = st.session_state.history["Bileşik_Büyüme"].iloc[-1] if yeni_gun_no > 1 else 1.0
        
        # XP Hesaplama: Her tamamlanan görev 10 XP, hepsi biterse +50 bonus
        kazanilan_xp = (tamamlanan * 10) + (50 if gunluk_basari_orani == 1.0 else 0)
        yeni_buyume = onceki_buyume * 1.01 if gunluk_basari_orani == 1.0 else onceki_buyume
        
        yeni_veri = pd.DataFrame({
            "Tarih": [datetime.now().strftime("%Y-%m-%d")],
            "Gün": [yeni_gun_no],
            "XP": [kazanilan_xp],
            "Bileşik_Büyüme": [yeni_buyume]
        })
        st.session_state.history = pd.concat([st.session_state.history, yeni_veri], ignore_index=True)
        if gunluk_basari_orani == 1.0:
            st.toast("SEVİYE ATLANDI! (Veya XP Kazanıldı)", icon='🔥')

with col_undo:
    if st.button("🔄 GERİ AL"):
        if not st.session_state.history.empty:
            st.session_state.history = st.session_state.history[:-1]
            st.rerun()

with col_export:
    # Verileri yedeklemek için CSV olarak indir
    if not st.session_state.history.empty:
        csv = st.session_state.history.to_csv(index=False).encode('utf-8')
        st.download_button("💾 YEDEKLE", data=csv, file_name="solo_leveling_data.csv", mime="text/csv")

# --- TAKVİM VE ANALİZ ---
if not st.session_state.history.empty:
    st.divider()
    
    # Isı Haritası Mantığında Haftalık Tablo
    st.subheader("📅 Görev Geçmişi")
    hist_view = st.session_state.history.tail(7).copy()
    st.dataframe(hist_view.set_index("Tarih")[["XP"]].T, use_container_width=True)

    # Gelişim Grafiği
    st.subheader("📈 Güç Artışı (Bileşik Etki)")
    fig = px.line(st.session_state.history, x="Tarih", y="Bileşik_Büyüme", 
                  template="plotly_dark", line_shape="spline")
    fig.update_traces(line_color='#4a90e2')
    st.plotly_chart(fig, use_container_width=True)

# --- AYARLAR (SOL MENÜ) ---
with st.sidebar:
    st.header("⚙️ SİSTEM AYARLARI")
    yeni = st.text_input("Yeni Görev Ekle:")
    if st.button("Sisteme Kaydet"):
        if yeni:
            st.session_state.my_habits.append(yeni)
            st.rerun()
    
    st.write("---")
    st.write("🗑️ Görev Sil:")
    for h in st.session_state.my_habits:
        if st.button(f"Sil: {h}"):
            st.session_state.my_habits.remove(h)
            st.rerun()




