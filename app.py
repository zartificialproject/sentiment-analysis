import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd

# Inisialisasi session_state untuk menyimpan hasil analisis
if "results" not in st.session_state:
    st.session_state["results"] = []

# Pengaturan judul dan deskripsi aplikasi
st.title("Analisis Sentimen dengan Terjemahan")
st.write("Masukkan teks untuk diterjemahkan ke Bahasa Inggris dan dianalisis sentimennya.")

# Input teks dari pengguna
text = st.text_area("Masukkan teks di sini:")

# Analisis jika tombol diklik
if st.button("Analisis Sentimen", key="analyze"):
    if text.strip():
        # Terjemahkan teks
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        blob = TextBlob(translated)
        sentiment_score = blob.sentiment.polarity

        # Tentukan hasil sentimen
        if sentiment_score > 0:
            sentiment = "Positif"
            color = "green"
        elif sentiment_score < 0:
            sentiment = "Negatif"
            color = "red"
        else:
            sentiment = "Netral"
            color = "blue"

        # Simpan hasil dalam session_state
        st.session_state["results"].append({
            "Teks Awal": text,
            "Terjemahan": translated,
            "Sentimen": sentiment,
            "Skor Sentimen": sentiment_score
        })

        # Tampilkan hasil analisis
        st.markdown(f"""
            <p style='color:{color}; font-size:24px; font-weight:bold;'>
                Sentimen: {sentiment} (Skor: {sentiment_score:.2f})
            </p>
            <p style='font-size:20px;'><strong>Terjemahan:</strong> {translated}</p>
            """, unsafe_allow_html=True)
    else:
        st.warning("Masukkan teks untuk dianalisis.")

# Jika ada hasil, tampilkan dalam bentuk tabel
if st.session_state["results"]:
    df = pd.DataFrame(st.session_state["results"])
    st.subheader("Riwayat Analisis Sentimen")
    st.dataframe(df)

# Fungsi Reset
if st.button("Reset", key="reset"):
    st.session_state["results"] = []  # Menghapus semua hasil yang direkam
    st.success("Riwayat telah direset.")
