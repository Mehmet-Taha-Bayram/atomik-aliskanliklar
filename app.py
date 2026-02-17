import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Ayarları
st.set_page_config(page_title="Gelişim Günlüğü", page_icon="📈", layout="wide")

# --- VERİ SİSTEMİ (HATASIZ BAŞLATMA) ---
if 'history' not in st.session_state:
    st.session_state.history = []

if 'habits' not in st.session_state:
    st.session_state.habits = ["📚 Kitap Okuma", "💪 Spor", "💧 Su İçmek"]

if 'bad_habits' not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Gereksiz Sosyal Medya"]

# --- ANA BAŞLIK ---
st.title("📈 Kişisel Gelişim ve Alışkanlık Günlüğü")
st.write(f"📅 **{datetime.now().strftime('%d %B %Y')}**")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("✅ Kazanmak İstediğim Alışkanlıklar")
    good_results = {}
    for h in st.session_state.habits:
        good_results[h] = st.checkbox(h, key=f"good_{h}")

    st.divider()
    st.subheader("🚫 Bırakmak İstediğim Alışkanlıklar")
    st.info("Bu kutucukları işaretlemediysen başarılısın demektir!")
    bad_results = {}
    for bh in st.session_state.bad_habits:
        bad_results[bh] = st.checkbox(f"Bugün bunu yaptım: {bh}", key=f"bad_{bh}")

with col2:
    st.subheader("📝 Günlük Değerlendirme")
    
    st.write("**🌟 Bugün memnun olduğum 3 şey:**")
    m1 = st.text_input("1.", key="m1")
    m2 = st.text_input("2.", key="m2")
    m3 = st.text_input("3.", key="m3")
    
    st.write("**💡 Daha iyi yapabileceğim 3 şey:**")
    d1 = st.text_input("d1", key="d1", label_visibility="collapsed")
    d2 = st.text_input("d2", key="d2", label_visibility="collapsed")
    d3 = st.text_input("d3", key="d3", label_visibility="collapsed")
    
    extra_note = st.text_area("🗒️ Ekstra Notlar", placeholder="Bugün nasıl geçti?")

# --- KAYDETME BUTONU ---
st.write("---")
if st.button("🚀 GÜNÜ SİSTEME KAYDET", use_container_width=True):
    # Yeni kaydı oluştur
    yeni_kayit = {
        "tarih": datetime.now().strftime("%d/%m/%Y"),
        "iyi": sum(good_results.values()),
        "kotu": sum(bad_results.values()),
        "memnun": [m1, m2, m3],
        "gelisim": [d1, d2, d3],
        "not": extra_note
    }
    st.session_state.history.append(yeni_kayit)
    st.balloons()
    st.success("Veriler başarıyla kaydedildi!")

# --- ALT PANEL (GEÇMİŞ VE AYARLAR) ---
st.divider()
tab1, tab2 = st.tabs(["📊 Geçmiş Kayıtlar", "⚙️ Alışkanlık Yönetimi"])

with tab1:
    if len(st.session_state.history) > 0:
        for entry in reversed(st.session_state.history):
            with st.expander(f"📅 Tarih: {entry['tarih']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"✅ İyi Alışkanlıklar: {entry['iyi']}")
                    st.write(f"🚫 Kötü Alışkanlıklar: {entry['kotu']}")
                with c2:
                    st.write(f"**🌟 Memnuniyet:** {', '.join(filter(None, entry['memnun']))}")
                    st.write(f"**💡 Gelişim:** {', '.join(filter(None, entry['gelisim']))}")
                if entry['not']:
                    st.info(f"**Not:** {entry['not']}")
    else:
        st.write("Henüz bir kayıt yok.")

with tab2:
    c_a, c_b = st.columns(2)
    with c_a:
        yeni_iyi = st.text_input("Yeni İyi Alışkanlık:")
        if st.button("Ekle (İyi)"):
            if yeni_iyi: st.session_state.habits.append(yeni_iyi); st.rerun()
    with c_b:
        yeni_kotu = st.text_input("Yeni K






