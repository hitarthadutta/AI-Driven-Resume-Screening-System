# 🤖📄 AI-Driven Resume Screening System

An intelligent, AI-driven resume screening application leveraging advanced Natural Language Processing (NLP) and machine learning techniques, built with Streamlit for automated candidate evaluation, ranking, and informed hiring decision support.

## Features

- **AI-Powered Multi-format Processing:** Seamlessly process PDF, DOCX, and TXT resume files with smart text extraction  
- **Advanced NLP & Machine Learning:** Utilize spaCy and custom algorithms to accurately extract, analyze, and interpret candidate information  
- **Intelligent Scoring Algorithm:** Apply a weighted AI-driven scoring model considering skills (50%), experience (30%), and education (20%) for precise candidate ranking  
- **Modern, Interactive UI:** Responsive, user-friendly interface featuring sophisticated gradient styling and smooth animations  
- **Real-time Data Analytics:** Dynamic, AI-enhanced charts and dashboards delivering deep candidate insights and trends  
- **Effortless Export:** Download comprehensive screening results as CSV files for seamless integration with recruitment workflows  

## Quick Start

### Install Dependencies

```bash
pip install streamlit pandas plotly spacy pypdf2 python-docx
python -m spacy download en_core_web_sm
```

### Run Application

```bash
streamlit run app.py --server.address localhost --server.port 5000
```

### Usage Instructions

1. **Configure Job Requirements:**  
   - Set the job title and required skills using the intuitive UI  
   - Define experience and education requirements clearly  
   - Click **Update Job Requirements** to apply settings  

2. **Process Resumes:**  
   - Upload resumes in supported formats (PDF, DOCX, or TXT)  
   - Click **Process Resumes** to start AI-driven analysis  

3. **View Results:**  
   - Explore candidate evaluations and rankings in an interactive dashboard powered by AI insights  

4. **Export Data:**  
   - Download the candidate screening results as CSV for reporting or integration  

## Project Structure

```
├── app.py                  # Main Streamlit application entry point  
├── resume_processor.py     # Smart resume file processing and text extraction module  
├── nlp_extractor.py        # NLP and AI-based candidate data extraction component  
├── scoring_engine.py       # AI-driven candidate scoring and ranking algorithms  
├── utils.py                # Helper functions including CSV export utilities  
├── USER_GUIDE.md           # Comprehensive user guide and documentation  
└── .streamlit/             # Streamlit configuration directory  
    └── config.toml         # Streamlit server and UI configuration  
```

## Scoring Algorithm

This AI-driven system evaluates and ranks candidates using a weighted scoring model tailored to your job requirements:

| Criteria       | Weight | Description                                                  |
|----------------|--------|--------------------------------------------------------------|
| Skills Matching| 50%    | AI-driven exact and fuzzy matching of required skills         |
| Experience     | 30%    | Comparative analysis of years and relevance of experience    |
| Education      | 20%    | Matching educational qualifications to job requirements      |

## Supported File Formats

- **PDF:** Text-based PDFs only (scanned images not supported)  
- **DOCX:** Microsoft Word documents  
- **TXT:** Plain text files  

## System Requirements

- Python 3.7 or higher  
- Streamlit framework  
- spaCy with English language model (`en_core_web_sm`)  
- pandas data analysis library  
- plotly for interactive charts  
- PyPDF2 for PDF parsing  
- python-docx for Word document handling

## Video Tutorial
https://github.com/user-attachments/assets/d19936b5-2191-47ab-9e9a-cdea8ebfcda7

## License

This project is open source and freely available for educational, research, and commercial applications.

***
