import streamlit as st
import PyPDF2
import docx
import io
import re
from typing import Dict, Any, Optional
from nlp_extractor import NLPExtractor

class ResumeProcessor:
    """Handles resume file processing and text extraction"""
    
    def __init__(self):
        self.nlp_extractor = NLPExtractor()
    
    def process_resume(self, uploaded_file) -> Optional[Dict[str, Any]]:
        """
        Process an uploaded resume file and extract information
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary containing extracted information or None if processing fails
        """
        try:
            # Extract text based on file type
            text = self._extract_text(uploaded_file)
            
            if not text or len(text.strip()) < 50:
                st.error(f"Could not extract sufficient text from {uploaded_file.name}")
                return None
            
            # Extract structured information using NLP
            extracted_info = self.nlp_extractor.extract_information(text)
            
            # Add raw text for additional processing if needed
            extracted_info['raw_text'] = text
            extracted_info['file_type'] = uploaded_file.type
            
            return extracted_info
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            return None
    
    def _extract_text(self, uploaded_file) -> str:
        """Extract text from various file formats"""
        
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        try:
            if file_extension == 'pdf':
                return self._extract_from_pdf(uploaded_file)
            elif file_extension == 'docx':
                return self._extract_from_docx(uploaded_file)
            elif file_extension == 'txt':
                return self._extract_from_txt(uploaded_file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            st.error(f"Error extracting text from {uploaded_file.name}: {str(e)}")
            raise
    
    def _extract_from_pdf(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            # Reset file pointer for potential reuse
            uploaded_file.seek(0)
            
            return text.strip()
            
        except Exception as e:
            # Try alternative approach if PyPDF2 fails
            st.warning(f"Primary PDF extraction failed for {uploaded_file.name}, trying alternative method")
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                # Read as binary and try to extract basic text
                content = uploaded_file.read()
                text = content.decode('utf-8', errors='ignore')
                uploaded_file.seek(0)
                return text
            except:
                raise Exception(f"Could not extract text from PDF: {str(e)}")
    
    def _extract_from_docx(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Reset file pointer
            uploaded_file.seek(0)
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Could not extract text from DOCX: {str(e)}")
    
    def _extract_from_txt(self, uploaded_file) -> str:
        """Extract text from TXT file"""
        try:
            # Try UTF-8 first
            text = uploaded_file.read().decode('utf-8')
            uploaded_file.seek(0)
            return text.strip()
            
        except UnicodeDecodeError:
            try:
                # Try latin-1 if UTF-8 fails
                uploaded_file.seek(0)
                text = uploaded_file.read().decode('latin-1')
                uploaded_file.seek(0)
                return text.strip()
            except Exception as e:
                raise Exception(f"Could not decode text file: {str(e)}")
        except Exception as e:
            raise Exception(f"Could not read text file: {str(e)}")
    
    def validate_extracted_data(self, data: Dict[str, Any]) -> bool:
        """Validate that extracted data contains minimum required information"""
        required_fields = ['skills', 'experience_years']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False
        
        # Check if skills is a non-empty list
        if not isinstance(data['skills'], list) or len(data['skills']) == 0:
            return False
        
        # Check if experience_years is a valid number
        try:
            float(data['experience_years'])
        except (ValueError, TypeError):
            return False
        
        return True
