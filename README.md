# Productimate Content Generator

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-yes-brightgreen)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/fastapi-yes-blue)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

---

## 🚀 Project Overview

**Productimate Content Generator** is a Retrieval-Augmented Generation (RAG) system designed to streamline content strategy and caption creation for social media platforms. It employs advanced LLM-based agents and dynamic chains to produce tailored SEO-focused content calendars and captions for Instagram, Facebook, and LinkedIn, all wrapped in an intuitive Streamlit UI and backed by a robust FastAPI service.

### Key Features

* **Document Upload & Summarization**: Supports PDF, DOCX, TXT, and URL inputs. Automatically summarizes and indexes content.
* **Multi-Platform Chains**: Generates platform-specific strategies and captions for Instagram, Facebook, and LinkedIn.
* **Content Calendar Output**: Provides a weekly content calendar with posts, themes, and scheduling recommendations.
* **Tone Selector**: Choose between professional, friendly, aggressive, or custom tones.
* **Persona-Based Output**: Tailor content for SMB owners, marketing agencies, or other defined personas.
* **Auto-Summarizer**: Condenses brochures or long web copy into concise briefs.
* **RAG-Powered Q\&A**: Ask questions about uploaded documents and get context-aware answers.
* **Database Integration**: Logs user inputs and outputs for audit and reusability.

---

## 🏗️ Architecture & Folder Structure

```
Productimate-Content-Generator/
├── app/               # Streamlit UI components
│   └── streamlit_app.py         # Main Streamlit app file
├── api/               # FastAPI server
│   ├── main.py        # API entrypoint
│   └── models.py      # Pydantic models
├── src/               # Core RAG, chains & agent logic
│   ├── chains/        # Chain implementations
│   ├── loaders/       # Document & data loaders
│   ├── agents/        # Agent orchestration
│   ├── prompts/       # Prompt templates
│   ├── tools/         # Utility tools (calendar, strategy, content)
│   ├── langchain_utils.py
│   ├── rag_pipeline.py
│   └── rebuild_index.py
├── data/              # Sample inputs & outputs
│   ├── Productimate Brochure.pdf
│   ├── social_media_links.json
│   └── output/
│       ├── instagram_contents/
│       ├── facebook_contents/
│       ├── linkedin_contents/
│       ├── strategies/
│       └── calendar/
├── basics.ipynb       # Experiment notebook
├── requirements.txt   # Dependencies
├── pyproject.toml     # Project metadata
├── .gitignore         # Ignored files
├── .python-version    # Python version
└── README.md          # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/saurabhpandey2108/Productimate-Content-Generator.git
   cd Productimate-Content-Generator
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   # Copy example
   cp .env.example .env
   # Then edit .env with your keys (OPENAI_API_KEY, DATABASE_URL, etc.)
   ```

---

## 🚀 Usage

### 1. Run the FastAPI backend

```bash
uvicorn api.main:app --reload
```

API will be available at `http://localhost:8000`.

### 2. Launch the Streamlit UI

```bash
streamlit run app/main.py
```

Open your browser at `http://localhost:8501`.

---

## 🔧 Configuration

* **OpenAI API Key**: `OPENAI_API_KEY`
* **Database URL**: `DATABASE_URL` (e.g., PostgreSQL, SQLite)
* **Vector Store Path/Settings**: `VECTOR_STORE_PATH`

---

## 🎯 Example Workflow

1. Upload a PDF brochure or input a website URL.
2. Select the target platform (Instagram, Facebook, LinkedIn).
3. Choose tone and persona.
4. Click **Generate Strategy** to receive a content calendar.
5. Click **Generate Captions** to fetch platform-specific post captions.

---

## 🛠️ Technologies Used

* **Python 3.10+** - Core language
* **LangChain** - RAG and chaining
* **OpenAI GPT** - LLM backend
* **Streamlit** - Frontend UI
* **FastAPI** - API server
* **Pydantic** - Data validation
* **Weaviate/FAISS** - Vector Database

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Open a Pull Request

---

## 📫 Contact

* **Developer**: Saurabh Pandey
* **Email**: [saurabh.pandey@example.com](mailto:saurabhpandey59254@gmail.com)

Feel free to open issues or reach out with questions!
