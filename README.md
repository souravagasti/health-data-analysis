# health-data-analysis

I have been wearing a fitness watch for the last 5 years.  
This repository contains code to analyze my health data (**steps, sleep, and heart rate**).  

The project uses:
- **PostgreSQL** for structured storage of Apple Health exports  
- **Python + Pandas** for data processing and feature engineering  
- **LLMs (Ollama / OpenAI GPT)** to generate natural-language health insights  
- **Streamlit** to provide an interactive dashboard  
- **Metabase** (optionally, with [Tailscale](https://tailscale.com/)) for mobile-friendly reports  

---

## Repository Structure

```bash
health-data-analysis/
│
├── apps/streamlit/ # Streamlit UI for insights
├── data/ # Raw and processed data
├── docker/ # Docker and Postgres configs
├── scripts/ # Utility scripts (ingest, persist, query)
└── src/ # Core Python modules
├── db.py # Database engine helpers
├── extract_apple.py # Parsers for Apple Health XML
├── llm.py # LLM client and insight generation
├── prompts.py # Prompt templates
├── settings.py # Configuration loader
└── utils.py # Shared utilities
```

---

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/health-data-analysis.git
   cd health-data-analysis
   ```
2. **Create a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Add a .env file (at minimum include):**
    ```makefile
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=
    POSTGRES_PORT=
    LLM_MODEL=
    OPENAI_API_KEY=   # (only if using GPT models)
    ```

5. **Start Postgres using Docker Compose**
    ```bash
    docker-compose -f docker/docker-compose.yml up -d
    ```

## Usage
1. Ingest Apple Health data into Postgres
    ```bash
    python3 -m scripts.ingest_xml_to_db
    ```
2. Build features for analysis
    ```bash
    python3 -m scripts.persist_features_for_analysis
    ```
3. Run the Streamlit app
    ```bash
    streamlit run apps/streamlit/app.py
    ```

## Example Questions to Ask in the Streamlit App
- Are steps and sleep hours correlated?
- Do higher activity levels reduce average heart rate?
- What patterns exist between REM sleep and daily steps?

## Notes
- Apple Health data is exported in XML. The parser extracts steps, sleep, and heart rate.
- All analysis happens locally unless you configure OpenAI’s API key.
- This project is for personal exploration only. The insights are not medical advice.