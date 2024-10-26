import streamlit as st
from textblob import TextBlob
from deep_translator import GoogleTranslator
import pandas as pd

st.set_page_config(page_title="Sentiment Analysis by Zartificial", page_icon="🔍")

# Inisialisasi session_state untuk menyimpan hasil analisis
if "results" not in st.session_state:
    st.session_state["results"] = []

# Pengaturan judul dan deskripsi aplikasi
st.title("🔍 Analisis Sentimen dengan Terjemahan")
st.write("Masukkan teks untuk diterjemahkan ke Bahasa Inggris dan dianalisis sentimennya. Hasil akan disimpan dalam riwayat di bawah.")

# Input teks dari pengguna
text_input = st.text_area("Masukkan teks di sini:", key="input_text", height=100)

# Tombol Analisis Sentimen
if st.button("Analisis Sentimen"):
    text = text_input.strip()
    if text:
        with st.spinner("⚙️ Memproses..."):
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
                <div style="border:1px solid {color}; padding: 16px; border-radius: 8px; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.2); margin-bottom: 20px;">
                    <p style='color:{color}; font-size:24px; font-weight:bold; margin-bottom: 4px;'>
                        Sentimen: {sentiment} (Skor: {sentiment_score:.2f})
                    </p>
                    <p style='font-size:20px; margin-top: 0;'><strong>Terjemahan:</strong> {translated}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Masukkan teks untuk dianalisis.")

# Tombol Reset hanya ditampilkan jika ada riwayat
if st.session_state["results"]:
    if st.button("Reset"):
        st.session_state["results"] = []  # Menghapus semua hasil yang direkam
        st.success("✅ Riwayat telah direset.")

# Menampilkan riwayat dalam bentuk card dengan satu baris 3 kolom jika ada hasil
if st.session_state["results"]:
    st.subheader("📊 Riwayat Analisis Sentimen")
    
    # Membuat tampilan dalam 3 kolom
    cols = st.columns(3)
    for i, result in enumerate(st.session_state["results"]):
        col = cols[i % 3]  # Pilih kolom berdasarkan urutan untuk tampilan 3 kolom
        color = "green" if result["Sentimen"] == "Positif" else "red" if result["Sentimen"] == "Negatif" else "blue"
        
        with col:
            st.markdown(f"""
                <div style="border:1px solid {color}; padding: 10px; border-radius: 8px; box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.2); margin-bottom: 16px;">
                    <p style='color:{color}; font-size:18px; font-weight:bold;'>
                        {result['Sentimen']}
                    </p>
                    <p><strong>Skor:</strong> {result['Skor Sentimen']:.2f}</p>
                    <p><strong>Terjemahan:</strong> {result['Terjemahan']}</p>
                    <p style="color: grey; font-size:14px;">{result['Teks Awal'][:40]}...</p>
                </div>
            """, unsafe_allow_html=True)

    # Opsi untuk mengunduh riwayat sebagai file CSV
    df = pd.DataFrame(st.session_state["results"])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Unduh Riwayat sebagai CSV",
        data=csv,
        file_name='riwayat_analisis_sentimen.csv',
        mime='text/csv'
    )
