import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from collections import Counter

# -------------------------------------------------
# SAYFA AYARI
# -------------------------------------------------
st.set_page_config(
    page_title="Atomik Gelişim Paneli",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# PREMIUM CSS TASARIM
# -------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
    color:white;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    padding:15px;
    border-radius:15px;
    backdrop-filter: blur(8px);
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "habits" not in st.session_state:
    st.session_state.habits = ["📚 Kitap", "💪 Spor", "💧 Su"]

if "bad_habits" not in st.session_state:
    st.session_state.bad_habits = ["🚬 Sigara", "📱 Sosyal Medya"]

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:
    st.title("📌 Menü")
    sayfa = st.radio(
        "Sayfa Seç",
        ["🏠 Bugünün Girişi", "📅 Takvim & Analiz", "⚙️ Ayarlar"]
    )

# =================================================
# BUGÜNÜN GİRİŞİ
# =================================================
if sayfa == "🏠 Bugünün Girişi":

    st.markdown("<h1 style='text-align:center;'>🚀 Günlük Giriş</h1>", unsafe_allow_html=True)

    bugun_str = datetime.now().strftime("%d/%m/%Y")
    st.write(f"Tarih: {bugun_str}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ İyi Alışkanlıklar")
        good_res = {}
        for h in st.session_state.habits:
            good_res[h] = st.checkbox(h, key=f"g_{h}")

        st.subheader("🚫 Kötü Alışkanlıklar")
        bad_res = {}
        for bh in st.session_state.bad_habits:
            bad_res[bh] = st.checkbox(f"Yaptım: {bh}", key=f"b_{bh}")

    with col2:
        st.subheader("📝 Günlük Not")
        note = st.text_area("Not")

        st.subheader("🌟 Memnun Olduğum 3 Şey")
        memnun1 = st.text_input("1.", key="m1")
        memnun2 = st.text_input("2.", key="m2")
        memnun3 = st.text_input("3.", key="m3")

        st.subheader("🚀 Daha İyi Yapabileceğim 3 Şey")
        gelisim1 = st.text_input("1..", key="g1")
        gelisim2 = st.text_input("2..", key="g2")
        gelisim3 = st.text_input("3..", key="g3")

    if st.button("💾 Kaydet", use_container_width=True):

        toplam = len(st.session_state.habits)
        yuzde = round((sum(good_res.values()) / toplam) * 100, 1) if toplam > 0 else 0

        mevcut_index = next(
            (i for i, x in enumerate(st.session_state.history) if x["tarih"] == bugun_str),
            None
        )

        yeni = {
            "tarih": bugun_str,
            "iyi": sum(good_res.values()),
            "kotu": sum(bad_res.values()),
            "yuzde": yuzde,
            "notlar": note,
            "memnun": [memnun1, memnun2, memnun3],
            "gelisim": [gelisim1, gelisim2, gelisim3]
        }

        if mevcut_index is not None:
            st.session_state.history[mevcut_index] = yeni
            st.info("Bugünkü kayıt güncellendi.")
        else:
            st.session_state.history.append(yeni)
            st.success("Yeni kayıt oluşturuldu.")

        st.progress(yuzde / 100)

        st.rerun()

# =================================================
# TAKVİM & ANALİZ
# =================================================
elif sayfa == "📅 Takvim & Analiz":

    st.markdown("<h1 style='text-align:center;'>📊 Performans Analizi</h1>", unsafe_allow_html=True)

    if len(st.session_state.history) == 0:
        st.warning("Henüz veri yok.")
    else:
        df = pd.DataFrame(st.session_state.history)
        df["tarih"] = pd.to_datetime(df["tarih"], format="%d/%m/%Y")
        df = df.sort_values("tarih")

        ortalama = round(df["yuzde"].mean(), 1)
        en_iyi = df.loc[df["yuzde"].idxmax()]
        en_kotu = df.loc[df["yuzde"].idxmin()]

        # Trend hesaplama
        x = np.arange(len(df))
        slope = np.polyfit(x, df["yuzde"], 1)[0]

        streak = 0
        for val in reversed(df["yuzde"].tolist()):
            if val >= 50:
                streak += 1
            else:
                break

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Genel Ortalama", f"%{ortalama}")
        c2.metric("En İyi Gün", f"%{en_iyi['yuzde']}")
        c3.metric("Trend Eğimi", f"{round(slope,2)}")
        c4.metric("🔥 Streak", f"{streak} gün")

        st.divider()

        # Plotly Grafik
        fig = px.line(df, x="tarih", y="yuzde", markers=True)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Radar Chart
        toplam_iyi = df["iyi"].sum()
        toplam_kotu = df["kotu"].sum()

        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=[toplam_iyi, toplam_kotu],
            theta=["İyi", "Kötü"],
            fill='toself'
        ))
        radar.update_layout(polar=dict(radialaxis=dict(visible=True)))
        st.plotly_chart(radar, use_container_width=True)

        # Haftalık Heatmap
        df["hafta_gun"] = df["tarih"].dt.day_name()
        pivot = df.pivot_table(index="hafta_gun", values="yuzde", aggfunc="mean")
        heat = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale="Viridis")
        st.plotly_chart(heat, use_container_width=True)

        # Motivasyon üretimi
        if slope > 0:
            st.success("Yukarı yönlü trenddesin. Momentum sende.")
        elif slope < 0:
            st.warning("Düşüş var. Küçük alışkanlık reseti zamanı.")
        else:
            st.info("Stabil gidiyorsun. Disiplin korunuyor.")

# =================================================
# AYARLAR
# =================================================
elif sayfa == "⚙️ Ayarlar":

    st.markdown("<h1 style='text-align:center;'>⚙️ Alışkanlık Yönetimi</h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ İyi Alışkanlıklar")
        for i, h in enumerate(st.session_state.habits):
            c1, c2 = st.columns([4,1])
            with c1:
                st.write(h)
            with c2:
                if st.button("❌", key=f"del_good_{i}"):
                    st.session_state.habits.pop(i)
                    st.rerun()

        yeni = st.text_input("Yeni İyi")
        if st.button("Ekle İyi"):
            if yeni.strip():
                st.session_state.habits.append(yeni.strip())
                st.rerun()

    with col2:
        st.subheader("🚫 Kötü Alışkanlıklar")
        for i, bh in enumerate(st.session_state.bad_habits):
            c1, c2 = st.columns([4,1])
            with c1:
                st.write(bh)
            with c2:
                if st.button("❌", key=f"del_bad_{i}"):
                    st.session_state.bad_habits.pop(i)
                    st.rerun()

        yeni2 = st.text_input("Yeni Kötü")
        if st.button("Ekle Kötü"):
            if yeni2.strip():
                st.session_state.bad_habits.append(yeni2.strip())
                st.rerun()
