# NLP Resume Screening System

## Overview

This is a Streamlit-based web application that automates candidate evaluation and ranking using natural language processing (NLP). The system processes resume files (PDF, DOCX, and TXT), extracts structured information like skills, experience, and education, then scores candidates against job requirements. It provides a comprehensive dashboard for recruiters and hiring managers to efficiently screen large volumes of resumes with detailed analytics and export capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework for rapid prototyping and deployment
- **UI Components**: Interactive sidebar configuration, file upload interface, data tables, and visualization charts using Plotly
- **State Management**: Streamlit session state for maintaining processed resumes, job requirements, and scoring engine instances across user interactions

### Backend Architecture
- **Modular Design**: Separated into distinct components for resume processing, NLP extraction, scoring, and utilities
- **Core Components**:
  - `ResumeProcessor`: Handles file upload and text extraction from multiple formats
  - `NLPExtractor`: Performs natural language processing and information extraction
  - `ScoringEngine`: Implements scoring algorithms with configurable weights
  - `utils`: Provides export functionality and sample data generation

### Data Processing Pipeline
- **Text Extraction**: Multi-format support (PDF via PyPDF2, DOCX via python-docx, plain text)
- **NLP Processing**: Uses spaCy for advanced natural language processing with fallback mechanisms
- **Information Extraction**: Pattern-matching and keyword-based extraction for skills, experience, education, and contact information
- **Scoring Algorithm**: Weighted scoring system (50% skills, 30% experience, 20% education) with component-level analysis

### Scoring and Analytics
- **Multi-dimensional Scoring**: Separate scores for skills matching, experience level, and education requirements
- **Skills Analysis**: Identifies matched skills, missing requirements, and additional candidate strengths
- **Recommendation Engine**: Generates hire/reject recommendations based on total scores
- **Visualization**: Interactive charts showing score distributions and candidate comparisons

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **spaCy**: Advanced NLP library for text processing and entity extraction (requires en_core_web_sm model)
- **pandas**: Data manipulation and analysis for handling candidate data
- **plotly**: Interactive data visualization for charts and graphs

### Document Processing
- **PyPDF2**: PDF text extraction and processing
- **python-docx**: Microsoft Word document processing
- **io**: Built-in library for handling file streams and text processing

### Data Export
- **CSV Export**: Built-in pandas CSV functionality for exporting screening results
- **Excel Support**: Potential future integration for advanced spreadsheet features

### NLP Model Requirements
- **spaCy English Model**: Requires installation of en_core_web_sm language model for full NLP functionality
- **Fallback Processing**: Basic text processing without advanced NLP if model unavailable