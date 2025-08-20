import re
import spacy
from typing import Dict, List, Any, Optional
import streamlit as st

class NLPExtractor:
    """Extracts structured information from resume text using NLP techniques"""
    
    def __init__(self):
        self.nlp = self._load_spacy_model()
        self.skill_keywords = self._load_skill_keywords()
        self.education_keywords = self._load_education_keywords()
    
    @st.cache_resource
    def _load_spacy_model(_self):
        """Load spaCy model with caching"""
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            st.error("spaCy English model not found. Please install it using: python -m spacy download en_core_web_sm")
            # Fallback to basic processing without advanced NLP
            return None
    
    def _load_skill_keywords(self) -> List[str]:
        """Load comprehensive list of technical skills and keywords"""
        return [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
            'spring', 'laravel', 'rails', 'asp.net', 'jquery', 'bootstrap', 'sass', 'less',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'oracle', 'mongodb', 'redis', 'elasticsearch',
            'cassandra', 'dynamodb', 'sqlite', 'mariadb',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'gitlab', 'github',
            'terraform', 'ansible', 'chef', 'puppet', 'ci/cd', 'devops',
            
            # Data Science & ML
            'machine learning', 'deep learning', 'artificial intelligence', 'data science',
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'opencv',
            'nlp', 'computer vision', 'statistics', 'data analysis', 'big data', 'hadoop', 'spark',
            
            # Mobile Development
            'android', 'ios', 'react native', 'flutter', 'xamarin', 'cordova', 'ionic',
            
            # Other Technologies
            'microservices', 'api', 'rest', 'graphql', 'soap', 'json', 'xml', 'agile', 'scrum',
            'kanban', 'jira', 'confluence', 'slack', 'linux', 'windows', 'macos',
            
            # Soft Skills
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical thinking',
            'project management', 'time management', 'adaptability', 'creativity', 'innovation'
        ]
    
    def _load_education_keywords(self) -> Dict[str, int]:
        """Load education level mappings"""
        return {
            'phd': 4, 'doctorate': 4, 'ph.d': 4,
            'master': 3, 'masters': 3, 'mba': 3, 'ms': 3, 'ma': 3, 'm.s': 3, 'm.a': 3,
            'bachelor': 2, 'bachelors': 2, 'bs': 2, 'ba': 2, 'b.s': 2, 'b.a': 2, 'be': 2, 'b.e': 2,
            'associate': 1, 'diploma': 1, 'certificate': 1,
            'high school': 0, 'secondary': 0, 'graduation': 0
        }
    
    def extract_information(self, text: str) -> Dict[str, Any]:
        """Extract structured information from resume text"""
        
        # Clean and preprocess text
        cleaned_text = self._clean_text(text)
        
        # Extract different components
        extracted_info = {
            'name': self._extract_name(cleaned_text),
            'email': self._extract_email(cleaned_text),
            'phone': self._extract_phone(cleaned_text),
            'skills': self._extract_skills(cleaned_text),
            'experience_years': self._extract_experience_years(cleaned_text),
            'education': self._extract_education(cleaned_text),
            'certifications': self._extract_certifications(cleaned_text),
            'organizations': self._extract_organizations(cleaned_text) if self.nlp else []
        }
        
        return extracted_info
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespaces and normalize
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name using NLP and heuristics"""
        if not self.nlp:
            return self._extract_name_fallback(text)
        
        try:
            doc = self.nlp(text[:500])  # Process first 500 characters
            
            # Look for PERSON entities
            for ent in doc.ents:
                if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                    return ent.text.strip()
            
            # Fallback to heuristic method
            return self._extract_name_fallback(text)
            
        except Exception:
            return self._extract_name_fallback(text)
    
    def _extract_name_fallback(self, text: str) -> str:
        """Fallback method to extract name without NLP"""
        lines = text.split('\n')[:5]  # Check first 5 lines
        
        for line in lines:
            line = line.strip()
            # Look for lines that could be names (2-4 words, mostly alphabetic)
            words = line.split()
            if (2 <= len(words) <= 4 and 
                all(word.replace('.', '').replace(',', '').isalpha() for word in words) and
                len(line) < 50):
                return line
        
        return "Name not found"
    
    def _extract_email(self, text: str) -> str:
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "Email not found"
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number"""
        phone_patterns = [
            r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'(\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',
            r'(\+\d{1,3}[-.\s]?)?\d{10}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0] if isinstance(phones[0], str) else ''.join(phones[0])
        
        return "Phone not found"
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using keyword matching"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        found_skills = list(set(found_skills))
        found_skills.sort()
        
        return found_skills[:50]  # Limit to top 50 skills
    
    def _extract_experience_years(self, text: str) -> float:
        """Extract years of experience from text"""
        
        # Patterns to match experience mentions
        experience_patterns = [
            r'(\d+\.?\d*)\s*(?:\+\s*)?(?:years?|yrs?)\s+(?:of\s+)?experience',
            r'(\d+\.?\d*)\s*(?:\+\s*)?(?:years?|yrs?)\s+(?:in|with|of)',
            r'experience\s*:?\s*(\d+\.?\d*)\s*(?:\+\s*)?(?:years?|yrs?)',
            r'(\d+\.?\d*)\s*(?:\+\s*)?(?:years?|yrs?)\s*(?:of\s+)?(?:professional\s+)?(?:work\s+)?experience'
        ]
        
        text_lower = text.lower()
        years_found = []
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                try:
                    years = float(match)
                    if 0 <= years <= 50:  # Reasonable range
                        years_found.append(years)
                except ValueError:
                    continue
        
        if years_found:
            return max(years_found)  # Return the highest experience mentioned
        
        # Alternative approach: count job positions and estimate
        job_indicators = ['worked at', 'employed at', 'position at', 'role at', 'job at']
        job_count = sum(text_lower.count(indicator) for indicator in job_indicators)
        
        if job_count > 0:
            return min(job_count * 2, 15)  # Estimate 2 years per job, max 15
        
        return 0.0
    
    def _extract_education(self, text: str) -> str:
        """Extract highest education level"""
        text_lower = text.lower()
        highest_level = 0
        highest_education = "Not specified"
        
        for education, level in self.education_keywords.items():
            if education in text_lower:
                if level > highest_level:
                    highest_level = level
                    highest_education = self._format_education_level(level)
        
        return highest_education
    
    def _format_education_level(self, level: int) -> str:
        """Convert education level number to string"""
        levels = {
            0: "High School",
            1: "Certificate/Diploma",
            2: "Bachelor's Degree",
            3: "Master's Degree",
            4: "PhD"
        }
        return levels.get(level, "Not specified")
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from text"""
        cert_patterns = [
            r'certified\s+in\s+([^.\n]+)',
            r'certification\s*:?\s*([^.\n]+)',
            r'cert\.\s*([^.\n]+)',
            r'([A-Z]{2,}\s+certified)',
        ]
        
        certifications = []
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend(matches)
        
        # Clean and filter certifications
        cleaned_certs = []
        for cert in certifications:
            cert = cert.strip()
            if len(cert) > 3 and len(cert) < 100:
                cleaned_certs.append(cert)
        
        return list(set(cleaned_certs))[:10]  # Limit to 10 certifications
    
    def _extract_organizations(self, text: str) -> List[str]:
        """Extract organization names using NLP"""
        if not self.nlp:
            return []
        
        try:
            doc = self.nlp(text)
            organizations = []
            
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    organizations.append(ent.text.strip())
            
            # Remove duplicates and filter
            organizations = list(set(organizations))
            return [org for org in organizations if len(org) > 2 and len(org) < 100][:20]
            
        except Exception:
            return []
