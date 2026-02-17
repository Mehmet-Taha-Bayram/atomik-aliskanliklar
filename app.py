import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Gelişim Günlüğü Pro", page_icon="📆", layout="wide")

# 2. Veri Yapısını Sabitleme
if 'history' not in st.session_state or isinstance(st.session_state.history, pd.DataFrame):
    st.session_state.history = []
if 'habits' not in st.session_state:
    st.session_state.habits = ["📚 Kitap Okuma", "💪 Spor", "💧 Su İçmek"]
if 'bad_habits' not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Sosyal Medya"]

# --- 3. YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("📌 Menü")
    sayfa = st.radio("Gitmek istediğiniz sayfa:", 
                    ["🏠 Bugünün Girişi", "📅 Takvim & Arşiv", "⚙️ Ayarlar"])
    st.divider()
    st.info("Sol üstteki (>) işaretinden menüyü yönetebilirsin.")

# --- SAYFA 1: BUGÜNÜN GİRİŞİ ---
if sayfa == "🏠 Bugünün Girişi":
    st.title("🚀 Bugünün Gelişim Girişi")
    st.write(f"📅 **Tarih:** {datetime.now().strftime('%d %B %Y')}")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("✅ Alışkanlık Takibi")
        good_res = {h: st.checkbox(h, key=f"g_{h}") for h in st.session_state.habits}
        
        st.subheader("🚫 Kaçınılacaklar")
        bad_res = {bh: st.checkbox(f"Bugün yaptım: {bh}", key=f"b_{bh}") for bh in st.session_state.bad_habits}

    with col2:
        st.subheader("📝 Günlük Değerlendirme")
        st.write("**🌟 Bugün memnun olduğum 3 şey:**")
        m = [st.text_input(f"{i+1}.", key=f"m{i}") for i in range(3)]
        
        st.write("**💡 Daha iyi yapabileceğim 3 şey:**")
        d = [st.text_input(f"{i+1}. ", key=f"d{i}") for i in range(3)]
        
        note = st.text
