import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------------------------
# SAYFA AYARI
# -------------------------------------------------
st.set_page_config(
    page_title="Atomik Gelişim Paneli",
    page_icon="📊",
    layout="wide"
)

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

    st.title("🚀 Günlük Giriş")
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
        yuzde = 0
        if toplam > 0:
            yuzde = round((sum(good_res.values()) / toplam) * 100, 1)

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

        st.rerun()

# =================================================
# TAKVİM & ANALİZ
# =================================================
elif sayfa == "📅 Takvim & Analiz":

    st.title("📊 Performans Analizi")

    if len(st.session_state.history) == 0:
        st.warning("Henüz veri yok.")
    else:
        df = pd.DataFrame(st.session_state.history)
        df["tarih"] = pd.to_datetime(df["tarih"], format="%d/%m/%Y")
        df = df.sort_values("tarih")

        ortalama = round(df["yuzde"].mean(), 1)
        en_iyi = df.loc[df["yuzde"].idxmax()]
        en_kotu = df.loc[df["yuzde"].idxmin()]

        streak = 0
        for val in reversed(df["yuzde"].tolist()):
            if val >= 50:
                streak += 1
            else:
                break

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Genel Ortalama", f"%{ortalama}")
        c2.metric("En İyi Gün", f"%{en_iyi['yuzde']}")
        c3.metric("En Kötü Gün", f"%{en_kotu['yuzde']}")
        c4.metric("🔥 Streak (50%+)", f"{streak} gün")

        st.divider()

        st.subheader("📋 Kayıt Tablosu")
        st.dataframe(df[["tarih", "yuzde"]], use_container_width=True)

        son_hafta = df[df["tarih"] >= (df["tarih"].max() - timedelta(days=6))]

        st.subheader("📈 Son 7 Günlük Grafik")
        st.line_chart(
            son_hafta.set_index("tarih")["yuzde"],
            use_container_width=True
        )

        st.subheader("📊 Ortalama Çizgili Grafik")
        chart_df = df.set_index("tarih")[["yuzde"]]
        chart_df["ortalama"] = ortalama
        st.line_chart(chart_df, use_container_width=True)

        st.divider()

        st.subheader("🟩 Performans Yoğunluk Tablosu")

        heatmap_df = df.copy()
        heatmap_df["gün"] = heatmap_df["tarih"].dt.strftime("%d %b")
        heatmap_df = heatmap_df[["gün", "yuzde"]]
        st.dataframe(heatmap_df, use_container_width=True)

        st.divider()

        st.subheader("✏️ Kayıt Düzenle / Sil")

        for idx, entry in list(enumerate(st.session_state.history))[::-1]:

            with st.expander(f"{entry['tarih']} - %{entry['yuzde']}"):

                st.write("🌟 Memnun Olduklarım:")
                for m in entry.get("memnun", []):
                    if m:
                        st.write("-", m)

                st.write("🚀 Gelişim Alanlarım:")
                for g in entry.get("gelisim", []):
                    if g:
                        st.write("-", g)

                st.divider()

                yeni_yuzde = st.number_input(
                    "Başarı Yüzdesi",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(entry["yuzde"]),
                    key=f"edit_{idx}"
                )

                col_s, col_d = st.columns(2)

                with col_s:
                    if st.button("Güncelle", key=f"save_{idx}"):
                        st.session_state.history[idx]["yuzde"] = yeni_yuzde
                        st.success("Güncellendi.")
                        st.rerun()

                with col_d:
                    if st.button("Sil", key=f"del_{idx}"):
                        st.session_state.history.pop(idx)
                        st.warning("Silindi.")
                        st.rerun()

# =================================================
# AYARLAR
# =================================================
elif sayfa == "⚙️ Ayarlar":

    st.title("⚙️ Alışkanlık Yönetimi")

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
