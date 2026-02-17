import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Sayfa Konfigürasyonu
st.set_page_config(page_title="Gelişim Günlüğü Pro", page_icon="📆", layout="wide")

# 2. Veri Başlatma
if 'history' not in st.session_state:
    st.session_state.history = []
if 'habits' not in st.session_state:
    st.session_state.habits = ["📚 Kitap Okuma", "💪 Spor", "💧 Su İçmek"]
if 'bad_habits' not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Sosyal Medya"]

# --- 3. YAN MENÜ (SIDEBAR - 3 ÇİZGİ MANTIĞI) ---
with st.sidebar:
    st.title("📌 Menü")
    sayfa = st.radio("Gitmek istediğiniz sayfa:", 
                    ["🏠 Bugünün Girişi", "📅 Geçmiş Takvim", "⚙️ Alışkanlık Ayarları"])
    st.divider()
   

# --- SAYFA 1: BUGÜNÜN GİRİŞİ ---
if sayfa == "🏠 Bugünün Girişi":
    st.title("🚀 Bugünün Gelişim Girişi")
    st.write(f"📅 **Tarih:** {datetime.now().strftime('%d %B %Y')}")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.subheader("✅ Alışkanlıklarını İşaretle")
        good_results = {h: st.checkbox(h, key=f"g_{h}") for h in st.session_state.habits}
        
        st.subheader("🚫 Bırakmak İstediğin Şeyler")
        bad_results = {bh: st.checkbox(f"Bugün yaptım: {bh}", key=f"b_{bh}") for bh in st.session_state.bad_habits}

    with col2:
        st.subheader("📝 Günlük Değerlendirme")
        st.write("**🌟 Bugün memnun olduğum 3 şey:**")
        m = [st.text_input(f"{i+1}.", key=f"m{i}") for i in range(3)]
        
        st.write("**💡 Daha iyi yapabileceğim 3 şey:**")
        d = [st.text_input(f"{i+1}.", key=f"d{i}") for i in range(3)]
        
        note = st.text_area("🗒️ Günlük Ek Notlar")

    if st.button("💾 GÜNÜ SİSTEME KAYDET", use_container_width=True):
        kayit = {
            "tarih": datetime.now().strftime("%d/%m/%Y"),
            "iyi": sum(good_results.values()),
            "kotu": sum(bad_results.values()),
            "memnuniyet": m,
            "gelisim": d,
            "notlar": note
        }
        st.session_state.history.append(kayit)
        st.balloons()
        st.success("Veriler kaydedildi! 'Geçmiş Takvim' sayfasından görebilirsin.")

# --- SAYFA 2: GEÇMİŞ TAKVİM & ARŞİV ---
elif sayfa == "📅 Geçmiş Takvim":
    st.title("📅 Kayıt Arşivi")
    
    if len(st.session_state.history) > 0:
        st.write("Aşağıdaki listeden geçmiş günleri inceleyebilirsin:")
        for entry in reversed(st.session_state.history):
            # Pencere pencere (Expander) yapısı
            with st.expander(f"📅 Kayıt Tarihi: {entry['tarih']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"📊 **Başarı:** {entry['iyi']}/{len(st.session_state.habits)} Alışkanlık")
                    st.write(f"⚠️ **Kaçınılamayan:** {entry['kotu']} Kötü Alışkanlık")
                with c2:
                    st.write("**🌟 Memnuniyet:** " + ", ".join(filter(None, entry['memnuniyet'])))
                    st.write("**💡 Gelişim:** " + ", ".join(filter(None, entry['gelisim'])))
                if entry['notlar']:
                    st.info(f"**Not:** {entry['notlar']}")
    else:
        st.warning("Henüz hiç kayıt yapmamışsın. İlk girişini 'Bugünün Girişi' sayfasından yapabilirsin.")

# --- SAYFA 3: AYARLAR ---
elif sayfa == "⚙️ Alışkanlık Ayarları":
    st.title("⚙️ Alışkanlık Yönetimi")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("✅ İyi Alışkanlık Listesi")
        for h in st.session_state.habits:
            st.write(f"- {h}")
        yeni_i = st.text_input("Yeni İyi Alışkanlık:")
        if st.button("Ekle (İyi)"):
            if yeni_i: st.session_state.habits.append(yeni_i); st.rerun()
            
    with c2:
        st.subheader("🚫 Bırakılacak Liste")
        for bh in st.session_state.bad_habits:
            st.write(f"- {bh}")
        yeni_k = st.text_input("Yeni Bırakılacak:")
        if st.button("Ekle (Bırak)"):
            if yeni_k: st.session_state.bad_habits.append(yeni_k); st.rerun()


