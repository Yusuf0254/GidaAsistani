import streamlit as st
import google.generativeai as genai
from PIL import Image
from pillow_heif import register_heif_opener

# --- AYARLAR ---
# ARTIK ŞİFREYİ KODUN İÇİNE YAZMIYORUZ!
# Kodumuz şifreyi Streamlit'in gizli kasasından (Secrets) otomatik alacak.
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol et.")
        st.stop()
except FileNotFoundError:
    st.error("Secrets dosyası bulunamadı. Bu kod şu an sadece Streamlit Cloud'da çalışır.")
    st.stop()

# HEIC formatındaki resimleri açabilmesi için ayar
register_heif_opener()

# Yapay zekayı hazırlıyoruz
genai.configure(api_key=api_key)

# --- SAYFA TASARIMI ---
st.set_page_config(page_title="Gıda Analiz", page_icon="🍎")
st.title("Gıda Mühendisi Cebimde 🧬")

# --- MODEL SEÇİMİ VE ANALİZ ---
try:
    # Model listesini alalım
    model_listesi = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_listesi.append(m.name)
            
    if not model_listesi:
        st.error("Hiç model bulunamadı! API Anahtarı hatalı olabilir.")
    else:
        # Kullanıcıya model seçtiriyoruz (Genelde flash en hızlısıdır)
        secilen_model = st.selectbox("Yapay Zeka Modeli:", model_listesi, index=0)
        model = genai.GenerativeModel(secilen_model)

        st.info(f
