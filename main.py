import streamlit as st
import google.generativeai as genai
from PIL import Image
from pillow_heif import register_heif_opener

# --- AYARLAR ---
# Şifreyi Streamlit Secrets (Gizli Kasa) içinden alıyoruz
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("API Anahtarı bulunamadı! Lütfen Streamlit Secrets ayarlarını kontrol et.")
        st.stop()
except FileNotFoundError:
    st.error("Secrets dosyası bulunamadı. Bu kod şu an sadece Streamlit Cloud üzerinde çalışır.")
    st.stop()

# HEIC format desteği
register_heif_opener()

# Yapay zeka ayarları
genai.configure(api_key=api_key)

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Gıda Analiz", page_icon="🍎")
st.title("Gıda Mühendisi Cebimde 🧬")

# --- MODEL SEÇİMİ VE ANALİZ ---
try:
    # Model listesini çekiyoruz
    model_listesi = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_listesi.append(m.name)
            
    if not model_listesi:
        st.error("Hiç model bulunamadı! API Anahtarı hatalı olabilir.")
    else:
        # Model seçimi
        secilen_model = st.selectbox("Yapay Zeka Modeli:", model_listesi, index=0)
        model = genai.GenerativeModel(secilen_model)

        # Bilgi mesajı
        st.info(f"Aktif Beyin: {secilen_model}")

        # --- FOTOĞRAF YÜKLEME ---
        yuklenen_resim = st.file_uploader("Paket fotoğrafını seç", type=["jpg", "png", "jpeg", "heic", "heif"])

        if yuklenen_resim is not None:
            image = Image.open(yuklenen_resim)
            st.image(image, caption='Analiz edilen görsel', width=300)
            
            if st.button("Analiz Et"):
                with st.spinner('Yapay zeka içeriği inceliyor...'):
                    istek = """
                    Sen uzman bir Gıda Mühendisisin. Bu fotoğraftaki içindekiler listesini oku.
                    Her bir maddeyi tek tek analiz et.
                    
                    Bana şu formatta bir tablo oluştur:
                    | Madde | Ne İşe Yarar? | Sağlık Durumu |
                    |---|---|---|
                    
                    Sağlık Durumu sütununda şunları kullan:
                    🟢 (Zararsız/Doğal)
                    🟡 (Dikkatli Tüketilmeli)
                    🔴 (Potansiyel Zararlı/Katkı Maddesi)
                    
                    En alta da "Gıda Mühendisi Yorumu" başlığıyla, bu ürünün genel olarak sağlıklı olup olmadığına dair kısa, net bir özet geç.
                    """
                    
                    cevap = model.generate_content([istek, image])
                    st.success("Analiz Tamamlandı!")
                    st.markdown(cevap.text)

except Exception as e:
    st.error(f"Bir hata oluştu: {e}")
