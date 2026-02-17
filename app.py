import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Gelişim Günlüğü Pro", page_icon="📆", layout="wide")

# 2. Veri Yapısını Sabitleme (Hata Almamak İçin Şart)
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
        
        note = st.text_area("🗒️ Günlük Ek Notlar", placeholder="Zihnin bugün nasıldı?")

    if st.button("💾 GÜNÜ SİSTEME KAYDET", use_container_width=True):
        yeni_kayit = {
            "tarih": datetime.now().strftime("%d/%m/%Y"),
            "iyi": sum(good_res.values()),
            "kotu": sum(bad_res.values()),
            "memnuniyet": [x for x in m if x],
            "gelisim": [x for x in d if x],
            "notlar": note
        }
        st.session_state.history.append(yeni_kayit)
        st.balloons()
        st.success("Kaydedildi! Geçmiş Takvim sayfasına bakabilirsin.")

# --- SAYFA 2: TAKVİM & ARŞİV ---
elif sayfa == "📅 Takvim & Arşiv":
    st.title("📅 Geçmiş Günlerin Değerlendirmesi")
    
    if len(st.session_state.history) > 0:
        for entry in reversed(st.session_state.history):
            with st.expander(f"📅 Tarih: {entry['tarih']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"📊 **Başarı:** {entry['iyi']}/{len(st.session_state.habits)}")
                    st.write(f"⚠️ **Yapılan Kötü:** {entry['kotu']}")
                with c2:
                    st.write("**🌟 Memnuniyet:** " + ", ".join(entry['memnuniyet']))
                    st.write("**💡 Gelişim:** " + ", ".join(entry['gelisim']))
                if entry['notlar']:
                    st.info(f"**Not:** {entry['notlar']}")
    else:
        st.warning("Henüz kayıt bulunamadı.")

# --- SAYFA 3: AYARLAR ---
elif sayfa == "⚙️ Ayarlar":
    st.title("⚙️ Alışkanlık Yönetimi")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("✅ İyi Listesi")
        for h in st.session_state.habits: st.text(f"- {h}")
        y_i = st.text_input("Yeni İyi Ekle:")
        if st.button("Ekle (İyi)"):
            if y_i: st.session_state.habits.append(y_i); st.rerun()
    with c2:
        st.subheader("🚫 Kötü Listesi")
        for bh in st.session_state.bad_habits: st.text(f"- {bh}")
        y_k = st.text_input("Yeni Kötü Ekle:")
        if st.button("Ekle (Kötü)"):
            if y_k: st.session_state.bad_habits.append(y_k); st.rerun()
