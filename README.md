# azure-cognitive-translator
Python-based NLP tool leveraging Azure Cognitive Services for extractive summarization and translation.

# 🧠 AI Text Analyzer & Summarizer

A powerful web application built with **Streamlit** and **Azure AI Language Services** that analyzes text, generates concise summaries, translates them into multiple languages, and provides audio playback.

## 🚀 Features

* **Language Detection:** Automatically identifies the language of the input text.
* **Sentiment Analysis:** Determines if the text is positive, negative, or neutral with confidence scores.
* **Extractive Summarization:** Uses Azure AI to pull the most critical sentences from long articles.
* **Multi-Language Translation:** Instantly translates summaries into Spanish, French, German, Hindi, Japanese, and more.
* **Text-to-Speech (Audio):** Listen to the summarized and translated text in its native accent.

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit** (Frontend UI)
* **Azure AI Text Analytics** (NLP Engine)
* **Deep Translator** (Translation)
* **gTTS** (Google Text-to-Speech)

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/your-username/azure-ai-text-summarizer.git](https://github.com/your-username/azure-ai-text-summarizer.git)
    cd azure-ai-text-summarizer
    ```

2.  **Install dependencies**
    ```bash
    pip install streamlit azure-ai-textanalytics deep-translator gTTS
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

## 🔑 Configuration

This project requires an **Azure Language Service** resource.
1.  Go to the [Azure Portal](https://portal.azure.com).
2.  Create a **Language Service** resource.
3.  Copy your `API Key` and `Endpoint` into the `app.py` file (or set them as environment variables).

## 📸 Usage

1.  Paste any article or text block into the input area.
2.  Select your preferred target language from the dropdown.
3.  Click **"Analyze Text"**.
4.  Navigate through the tabs to view Language confidence, Sentiment scores, and the Translated Audio Summary.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
