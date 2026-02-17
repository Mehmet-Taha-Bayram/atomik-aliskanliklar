import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Gelişim Günlüğü v3", page_icon="📈", layout="wide")

# 2. Veri Yapısını Başlatma (Hata Payı Bırakmayan Güvenli Başlatma)
if 'history' not in st.session_state:
    st.session_state.history = []
if 'habits' not in st.session_state:
    st.session_state.habits = ["📚 Kitap Okuma", "💪 Spor", "💧 Su İçmek"]
if 'bad_habits' not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Sosyal Medya (Gereksiz)"]

# 3. Başlık
st.title("📈 Kişisel Gelişim ve Alışkanlık Günlüğü")
st.write(f"📅 **Bugün:** {datetime.now().strftime('%d %B %Y')}")

# 4. Ana Arayüz (İki Sütun)
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("✅ Alışkanlık Takibi")
    st.markdown("---")
    good_results = {}
    for h in st.session_state.habits:
        good_results[h] = st.checkbox(h, key=f"g_{h}")

    st.subheader("🚫 Bırakmak İstediğim Şeyler")
    st.caption("Eğer bugün bunları yapmadıysan boş bırak.")
    bad_results = {}
    for bh in st.session_state.bad_habits:
        bad_results[bh] = st.checkbox(f"Bugün yaptım: {bh}", key=f"b_{bh}")

with col2:
    st.subheader("📝 Günlük Değerlendirme")
    st.markdown("---")
    
    st.write("**🌟 Bugün memnun olduğum 3 şey:**")
    m1 = st.text_input("1. Memnuniyet", label_visibility="collapsed", key="m1")
    m2 = st.text_input("2. Memnuniyet", label_visibility="collapsed", key="m2")
    m3 = st.text_input("3. Memnuniyet", label_visibility="collapsed", key="m3")
    
    st.write("**💡 Daha iyi yapabileceğim 3 şey:**")
    d1 = st.text_input("1. Gelişim", label_visibility="collapsed", key="d1")
    d2 = st.text_input("2. Gelişim", label_visibility="collapsed", key="d2")
    d3 = st.text_input("3. Gelişim", label_visibility="collapsed", key="d3")
    
    extra_note = st.text_area("🗒️ Günlük Ek Notlar", placeholder="Bugün zihnim nasıldı?")

# 5. Kayıt Mekanizması
st.markdown("---")
if st.button("🚀 GÜNÜ SİSTEME KAYDET", use_container_width=True):
    yeni_kayit = {
        "tarih": datetime.now().strftime("%d/%m/%Y"),
        "iyi_skor": sum(good_results.values()),
        "kotu_skor": sum(bad_results.values()),
        "memnuniyet": [m1, m2, m3],
        "gelisim": [d1, d2, d3],
        "notlar": extra_note
    }
    st.session_state.history.append(yeni_kayit)
    st.balloons()
    st.success("Harika! Günlük verilerin başarıyla arşive eklendi.")

# 6. Alt Bölüm (Geçmiş ve Ayarlar)
st.divider()
tab1, tab2 = st.tabs(["📊 Geçmiş Kayıtlar", "⚙️ Alışkanlık Listesini Düzenle"])

with tab1:
    if len(st.session_state.history) > 0:
        for entry in reversed(st.session_state.history):
            with st.expander(f"📅 Kayıt: {entry['tarih']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"✅ İyi Alışkanlıklar: **{entry['iyi_skor']}**")
                    st.write(f"🚫 Kötü Alışkanlıklar (Yapılan): **{entry['kotu_skor']}**")
                with c2:
                    st.write("**🌟 Memnuniyet:** " + ", ".join(filter(None, entry['memnuniyet'])))
                    st.write("**💡 Gelişim:** " + ", ".join(filter(None, entry['gelisim'])))
                if entry['notlar']:
                    st.info(f"**Not:** {entry['notlar']}")
    else:
        st.info("Henüz kaydedilmiş bir gün bulunmuyor.")

with tab2:
    c_a, c_b = st.columns(2)
    with c_a:
        yeni_iyi = st.text_input("Yeni Alışkanlık Ekle:")
        if st.button("Listeye Ekle (İyi)"):
            if yeni_iyi:
                st.session_state.habits.append(yeni_iyi)
                st.rerun()
    with c_b:
        yeni_kotu = st.text_input("Yeni Kötü Alışkanlık (Bırakılacak):")
        if st.button("Listeye Ekle (Kötü)"):
            if yeni_kotu:
                st.session_state.bad_habits.append(yeni_kotu)
                st.rerun()
