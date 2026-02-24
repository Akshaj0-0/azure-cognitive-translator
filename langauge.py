import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from gtts import gTTS
from io import BytesIO
from deep_translator import GoogleTranslator

# --- UI Setup ---
st.set_page_config(page_title="New Article Summarization", layout="wide")
st.title("New Article Summarization")
st.markdown("Analyze text for language, sentiment, and extract key summaries using Azure AI.")

# --- Configuration (Hardcoded) ---
ENDPOINT = "YOUR_AZURE_ENDPOINT_HERE"  # Replace with your Azure endpoint
API_KEY = "YOUE_AZURE_API_KEY_HERE"  # Replace with your Azure API key

def authenticate_client():
    ta_credential = AzureKeyCredential(API_KEY)
    return TextAnalyticsClient(endpoint=ENDPOINT, credential=ta_credential)

def create_audio(text, lang_code):
    """Converts text to an audio file in memory using the specified language code."""
    tts = gTTS(text=text, lang=lang_code)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp

# --- Main UI Area ---
default_text = (
    "Cryptography has evolved from simple substitution ciphers used in ancient times to complex "
    "mathematical algorithms that secure modern digital communications. Historically, methods like the "
    "Caesar cipher shifted letters in the alphabet to hide messages, which were easily broken as "
    "cryptanalysis advanced. The turning point in cryptographic history occurred during World War II "
    "with the Enigma machine, which prompted the development of early computing to break its codes. "
    "Today, digital security relies heavily on two main types of encryption: symmetric and asymmetric. "
    "Symmetric encryption uses a single key to both encrypt and decrypt data, making it fast and efficient "
    "for large volumes of information, much like the Advanced Encryption Standard (AES) used by governments "
    "and banks worldwide. However, securely sharing that single key presents a logistical challenge. "
    "This issue is resolved by asymmetric cryptography, also known as public-key cryptography. In this system, "
    "a pair of mathematically linked keys is used: a public key that anyone can use to encrypt a message, "
    "and a private key kept secret by the receiver to decrypt it. The RSA algorithm is a widely used asymmetric "
    "method that relies on the practical difficulty of factoring the product of two large prime numbers. "
    "Together, these cryptographic protocols form the foundation of secure web communications, virtual private "
    "networks, and data protection, ensuring that sensitive information remains confidential and protected "
    "from unauthorized interception across global networks."
)

text_input = st.text_area("Enter text to analyze:", value=default_text, height=200)

# Language mapping for translation and text-to-speech
language_options = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Japanese": "ja",
    "Italian": "it"
}

# Dropdown for user to select translation language
selected_language = st.selectbox("Select language for the summary:", list(language_options.keys()))
lang_code = language_options[selected_language]

if st.button("Analyze Text", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        try:
            client = authenticate_client()
            
            tab1, tab2, tab3 = st.tabs(["Language", "Sentiment", "Summary"])
            
            with st.spinner("Analyzing text..."):
                
                # 1. Language Detection
                lang_response = client.detect_language(documents=[text_input])[0]
                with tab1:
                    st.subheader("Language Detection")
                    st.metric("Detected Language", lang_response.primary_language.name)
                    st.progress(lang_response.primary_language.confidence_score, 
                                text=f"Confidence Score: {lang_response.primary_language.confidence_score * 100}%")

                # 2. Sentiment Analysis
                sent_response = client.analyze_sentiment(documents=[text_input])[0]
                with tab2:
                    st.subheader("Overall Sentiment")
                    st.markdown(f"### {sent_response.sentiment.capitalize()}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Positive", f"{sent_response.confidence_scores.positive * 100}%")
                    col2.metric("Neutral", f"{sent_response.confidence_scores.neutral * 100}%")
                    col3.metric("Negative", f"{sent_response.confidence_scores.negative * 100}%")

                # 3. Summarization & Translation & Audio
                with tab3:
                    st.subheader(f"Extractive Summary ({selected_language})")
                    poller = client.begin_extract_summary(documents=[text_input])
                    summary_results = poller.result()
                    
                    for result in summary_results:
                        if result.is_error:
                            st.error(f"Error: {result.error.code} - {result.error.message}")
                        else:
                            full_summary_text = ""
                            
                            # Combine sentences from Azure
                            for sentence in result.sentences:
                                full_summary_text += sentence.text + " "
                            
                            # Translate the text if a language other than the source is needed
                            # Using auto-detection for the source language
                            translator = GoogleTranslator(source='auto', target=lang_code)
                            translated_summary = translator.translate(full_summary_text)
                            
                            # Display translated summary as bullet points
                            # Splitting by period for cleaner visual formatting
                            translated_sentences = translated_summary.split(". ")
                            for sentence in translated_sentences:
                                if sentence.strip():
                                    st.markdown(f"- {sentence.strip()}.")
                            
                            # Generate and display the audio player in the selected language
                            if translated_summary:
                                st.markdown("### Audio Playback")
                                audio_data = create_audio(translated_summary, lang_code)
                                st.audio(audio_data, format="audio/mp3")
                                
        except Exception as e:
            st.error(f"An error occurred: {e}")