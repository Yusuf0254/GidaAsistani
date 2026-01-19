import streamlit as st
import google.generativeai as genai
from PIL import Image
from pillow_heif import register_heif_opener

# --- AYARLAR ---
api_key = "AIzaSyATwzgNkY3OqSswWra2R9QRgPNNB0PLC7o"  # Kendi anahtarını buraya yapıştır

register_heif_opener() # HEIC desteği
genai.configure(api_key=api_key)

# --- SAYFA TASARIMI ---
st.set_page_config(page_title="Gıda Analiz", page_icon="🍎")
st.title("Gıda Mühendisi Cebimde 🧬")

# --- SORUN ÇÖZÜCÜ: MODELİ SEN SEÇ ---
try:
    # Google'dan senin hesabına açık olan modelleri istiyoruz
    model_listesi = []
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_listesi.append(m.name)
    
    # Eğer liste boş gelirse API anahtarı yanlıştır
    if not model_listesi:
        st.error("Hiç model bulunamadı! API Anahtarını kontrol et.")
    else:
        # Kullanıcıya listeden seçim yaptırtıyoruz
        secilen_model = st.selectbox(
            "Kullanılacak Yapay Zeka Modelini Seç:", 
            model_listesi, 
            index=0
        )
        
        # Seçilen modeli yüklüyoruz
        model = genai.GenerativeModel(secilen_model)

        # --- FOTOĞRAF YÜKLEME VE ANALİZ ---
        st.info(f"Şu an aktif olan beyin: `{secilen_model}`")
        
        yuklenen_resim = st.file_uploader("Paket fotoğrafını seç", type=["jpg", "png", "jpeg", "heic", "heif"])

        if yuklenen_resim is not None:
            image = Image.open(yuklenen_resim)
            st.image(image, caption='Analiz edilen görsel', width=300)
            
            if st.button("Analiz Et"):
                with st.spinner('Yapay zeka içeriği inceliyor...'):
                    try:
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
                        En alta da "Gıda Mühendisi Yorumu" başlığıyla özet geç.
                        """
                        
                        cevap = model.generate_content([istek, image])
                        st.success("Analiz Tamamlandı!")
                        st.markdown(cevap.text)
                        
                    except Exception as h:
                        st.error(f"Analiz sırasında hata: {h}")

except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")
    st.warning("İnternet bağlantını ve API anahtarını kontrol et.")