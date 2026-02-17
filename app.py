import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Gelişim Günlüğü", page_icon="📈", layout="wide")

# --- STİL ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTextArea textarea { border-radius: 10px; }
    .stTextInput input { border-radius: 10px; }
    .habit-box { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ SİSTEMİ ---
if 'history' not in st.session_state:
    st.session_state.history = []

if 'habits' not in st.session_state:
    st.session_state.habits = ["📚 Kitap Okuma", "💪 Spor", "💧 Su İçmek"]

if 'bad_habits' not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Gereksiz Sosyal Medya"]

# --- ANA BAŞLIK ---
st.title("📈 Kişisel Gelişim ve Alışkanlık Günlüğü")
st.write(f"📅 **{datetime.now().strftime('%d %B %Y, %A')}**")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("✅ Kazanmak İstediğim Alışkanlıklar")
    good_results = {}
    for h in st.session_state.habits:
        good_results[h] = st.checkbox(h, key=f"good_{h}")

    st.write("---")
    st.subheader("🚫 Bırakmak İstediğim Alışkanlıklar")
    st.info("Bu kutucukları işaretlemediysen başarılısın demektir!")
    bad_results = {}
    for bh in st.session_state.bad_habits:
        bad_results[bh] = st.checkbox(f"Bugün bunu yaptım: {bh}", key=f"bad_{bh}")

with col2:
    st.subheader("📝 Günlük Notlar & Değerlendirme")
    
    st.write("**🌟 Bugün memnun olduğum 3 şey:**")
    m1 = st.text_input("1.", key="m1", placeholder="Örn: Erken uyandım")
    m2 = st.text_input("2.", key="m2")
    m3 = st.text_input("3.", key="m3")
    
    st.write("**💡 Daha iyi yapabileceğim 3 şey:**")
    d1 = st.text_input("1.", key="d1", placeholder="Örn: Tatlı yemeseydim iyiydi")
    d2 = st.text_input("2.", key="d2")
    d3 = st.text_input("3.", key="d3")
    
    extra_note = st.text_area("🗒️ Ekstra Notlar", placeholder="Bugün nasıl geçti?")

# --- KAYDETME ---
st.write("---")
if st.button("🚀 GÜNÜ SİSTEME KAYDET", use_container_width=True):
    entry = {
        "tarih": datetime.now().strftime("%Y-%m-%d"),
        "iyi_aliskanliklar": sum(good_results.values()),
        "kotu_aliskanliklar": sum(bad_results.values()),
        "notlar": extra_note,
        "memnuniyet": [m1, m2, m3],
        "gelisim": [d1, d2, d3]
    }
    st.session_state.history.append(entry)
    st.balloons()
    st.success("Harika! Günlük verilerin kaydedildi.")

# --- GEÇMİŞ VE AYARLAR ---
st.divider()
tab1, tab2 = st.tabs(["📊 Geçmiş Kayıtlar", "⚙️ Alışkanlık Yönetimi"])

with tab1:
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            with st.expander(f"📅 Kayıt: {item['tarih']}"):
                c_a, c_b = st.columns(2)
                with c_a:
                    st.write(f"✅ Kazanılan: {item['iyi_aliskanliklar']}/{len(st.session_state.habits)}")
                    st.write(f"🚫 Kaçınılan Kötü Alışkanlıklar: {len(st.session_state.bad_habits) - item['kotu_aliskanliklar']}")
                with c_b:
                    st.write("**🌟 Memnuniyet:** " + ", ".join([x for x in item['memnuniyet'] if x]))
                    st





