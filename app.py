import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------------------------------------
# 1️⃣ SAYFA AYARI
# -------------------------------------------------
st.set_page_config(
    page_title="Gelişim Günlüğü Pro",
    page_icon="📆",
    layout="wide"
)

# -------------------------------------------------
# 2️⃣ SESSION STATE BAŞLATMA
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "habits" not in st.session_state:
    st.session_state.habits = ["📚 Kitap Okuma", "💪 Spor", "💧 Su İçmek"]

if "bad_habits" not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Sosyal Medya"]


# -------------------------------------------------
# 3️⃣ SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.title("📌 Menü")
    sayfa = st.radio(
        "Gitmek istediğiniz sayfa:",
        ["🏠 Bugünün Girişi", "📅 Takvim & Arşiv", "⚙️ Ayarlar"]
    )
    st.divider()
    st.info("Menüyü sol üstten daraltıp açabilirsin.")


# =================================================
# 🏠 SAYFA 1 – BUGÜNÜN GİRİŞİ
# =================================================
if sayfa == "🏠 Bugünün Girişi":

    st.title("🚀 Bugünün Gelişim Girişi")
    st.write(f"📅 **Tarih:** {datetime.now().strftime('%d %B %Y')}")

    col1, col2 = st.columns(2, gap="large")

    # --------- SOL TARAF ----------
    with col1:
        st.subheader("✅ Alışkanlık Takibi")

        good_res = {}
        for h in st.session_state.habits:
            good_res[h] = st.checkbox(h, key=f"g_{h}")

        st.subheader("🚫 Kaçınılacaklar")

        bad_res = {}
        for bh in st.session_state.bad_habits:
            bad_res[bh] = st.checkbox(f"Bugün yaptım: {bh}", key=f"b_{bh}")

    # --------- SAĞ TARAF ----------
    with col2:
        st.subheader("📝 Günlük Değerlendirme")

        st.write("**🌟 Bugün memnun olduğum 3 şey:**")
        memnun = [st.text_input(f"{i+1}.", key=f"m{i}") for i in range(3)]

        st.write("**💡 Daha iyi yapabileceğim 3 şey:**")
        gelisim = [st.text_input(f"{i+1}. ", key=f"d{i}") for i in range(3)]

        note = st.text_area("🗒️ Günlük Ek Notlar")

    # --------- KAYDET ----------
    if st.button("💾 GÜNÜ SİSTEME KAYDET", use_container_width=True):

        yeni_kayit = {
            "tarih": datetime.now().strftime("%d/%m/%Y"),
            "iyi": sum(good_res.values()),
            "kotu": sum(bad_res.values()),
            "memnuniyet": [x for x in memnun if x],
            "gelisim": [x for x in gelisim if x],
            "notlar": note
        }

        st.session_state.history.append(yeni_kayit)

        st.success("Kaydedildi ✔")


# =================================================
# 📅 SAYFA 2 – TAKVİM & ARŞİV
# =================================================
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

                if entry["notlar"]:
                    st.info(f"Not: {entry['notlar']}")

    else:
        st.warning("Henüz kayıt yok.")


# =================================================
# ⚙️ SAYFA 3 – AYARLAR
# =================================================
elif sayfa == "⚙️ Ayarlar":

    st.title("⚙️ Alışkanlık Yönetimi")

    col1, col2 = st.columns(2)

    # --------- İYİLER ----------
    with col1:
        st.subheader("✅ İyi Alışkanlıklar")

        for i, h in enumerate(st.session_state.habits):
            c_h, c_btn = st.columns([4,1])
            with c_h:
                st.text(h)
            with c_btn:
                if st.button("❌", key=f"del_good_{i}"):
                    st.session_state.habits.pop(i)
                    st.rerun()

        yeni_iyi = st.text_input("Yeni İyi Ekle:")
        if st.button("Ekle (İyi)"):
            if yeni_iyi.strip() != "":
                st.session_state.habits.append(yeni_iyi.strip())
                st.rerun()

    # --------- KÖTÜLER ----------
    with col2:
        st.subheader("🚫 Kötü Alışkanlıklar")

        for i, bh in enumerate(st.session_state.bad_habits):
            c_bh, c_btn = st.columns([4,1])
            with c_bh:
                st.text(bh)
            with c_btn:
                if st.button("❌", key=f"del_bad_{i}"):
                    st.session_state.bad_habits.pop(i)
                    st.rerun()

        yeni_kotu = st.text_input("Yeni Kötü Ekle:")
        if st.button("Ekle (Kötü)"):
            if yeni_kotu.strip() != "":
                st.session_state.bad_habits.append(yeni_kotu.strip())
                st.rerun()
