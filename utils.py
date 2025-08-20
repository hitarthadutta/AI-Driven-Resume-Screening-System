import pandas as pd
import streamlit as st
from datetime import datetime
from typing import Dict, List, Any
import io

def export_to_csv(resume_data: List[Dict[str, Any]]) -> str:
    """Export resume screening results to CSV format"""
    
    # Create DataFrame
    df = pd.DataFrame(resume_data)
    
    # Select and rename columns for export
    export_columns = {
        'filename': 'Resume File',
        'name': 'Candidate Name',
        'email': 'Email',
        'phone': 'Phone',
        'total_score': 'Total Score',
        'skills_score': 'Skills Score',
        'experience_score': 'Experience Score',
        'education_score': 'Education Score',
        'experience_years': 'Years of Experience',
        'education': 'Education Level',
        'skills': 'Skills',
        'recommendation': 'Recommendation',
        'matched_skills': 'Matched Skills',
        'missing_skills': 'Missing Skills',
        'processed_at': 'Processed Date'
    }
    
    # Select available columns
    available_columns = {k: v for k, v in export_columns.items() if k in df.columns}
    export_df = df[list(available_columns.keys())].copy()
    export_df.rename(columns=available_columns, inplace=True)
    
    # Convert lists to strings for CSV export
    for col in export_df.columns:
        if export_df[col].dtype == 'object':
            export_df[col] = export_df[col].apply(
                lambda x: ', '.join(x) if isinstance(x, list) else str(x)
            )
    
    # Convert to CSV string
    return export_df.to_csv(index=False)

def create_sample_job_requirements() -> Dict[str, Any]:
    """Create sample job requirements for demonstration"""
    return {
        'job_title': 'Software Engineer',
        'required_skills': [
            'python', 'javascript', 'sql', 'git', 'react', 'django', 'flask',
            'html', 'css', 'rest api', 'json', 'agile', 'problem solving',
            'communication', 'teamwork', 'linux', 'aws', 'docker'
        ],
        'experience_years': 3,
        'education_level': "Bachelor's Degree"
    }

def format_skill_list(skills: List[str], max_display: int = 5) -> str:
    """Format skill list for display"""
    if not skills:
        return "None"
    
    if len(skills) <= max_display:
        return ", ".join(skills)
    else:
        return ", ".join(skills[:max_display]) + f" (+ {len(skills) - max_display} more)"

def calculate_match_percentage(matched_skills: List[str], required_skills: List[str]) -> float:
    """Calculate skill match percentage"""
    if not required_skills:
        return 100.0
    
    return (len(matched_skills) / len(required_skills)) * 100

def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate if file type is allowed"""
    if not filename:
        return False
    
    file_extension = filename.lower().split('.')[-1]
    return file_extension in [ext.lower() for ext in allowed_types]

def clean_text_for_display(text: str, max_length: int = 100) -> str:
    """Clean and truncate text for display"""
    if not text:
        return ""
    
    # Remove extra whitespace
    cleaned = ' '.join(text.split())
    
    # Truncate if too long
    if len(cleaned) > max_length:
        return cleaned[:max_length] + "..."
    
    return cleaned

def generate_summary_stats(resumes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate summary statistics for processed resumes"""
    if not resumes:
        return {}
    
    df = pd.DataFrame(resumes)
    
    stats = {
        'total_candidates': len(df),
        'average_score': df['total_score'].mean() if 'total_score' in df.columns else 0,
        'highest_score': df['total_score'].max() if 'total_score' in df.columns else 0,
        'lowest_score': df['total_score'].min() if 'total_score' in df.columns else 0,
        'qualified_candidates': len(df[df['total_score'] >= 70]) if 'total_score' in df.columns else 0,
        'average_experience': df['experience_years'].mean() if 'experience_years' in df.columns else 0,
    }
    
    return stats

def get_color_for_score(score: float) -> str:
    """Get color code for score visualization"""
    if score >= 85:
        return "#00C851"  # Green
    elif score >= 70:
        return "#ffbb33"  # Orange
    elif score >= 55:
        return "#FF8800"  # Dark Orange
    else:
        return "#FF4444"  # Red

def create_score_badge(score: float) -> str:
    """Create HTML badge for score display"""
    color = get_color_for_score(score)
    return f'<span style="background-color: {color}; color: white; padding: 2px 8px; border-radius: 12px; font-weight: bold;">{score:.1f}</span>'

def parse_years_from_text(text: str) -> float:
    """Parse years from various text formats"""
    import re
    
    # Common patterns for years
    patterns = [
        r'(\d+\.?\d*)\s*(?:years?|yrs?)',
        r'(\d+\.?\d*)\s*(?:months?|mos?)',  # Convert months to years
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            try:
                value = float(matches[0])
                # If pattern matched months, convert to years
                if 'month' in pattern or 'mos' in pattern:
                    value = value / 12
                return value
            except ValueError:
                continue
    
    return 0.0

def normalize_skill_name(skill: str) -> str:
    """Normalize skill names for better matching"""
    # Common skill name normalizations
    normalizations = {
        'js': 'javascript',
        'nodejs': 'node.js',
        'reactjs': 'react',
        'vuejs': 'vue',
        'c++': 'cpp',
        'c#': 'csharp',
        '.net': 'dotnet',
        'ai': 'artificial intelligence',
        'ml': 'machine learning',
    }
    
    skill_lower = skill.lower().strip()
    return normalizations.get(skill_lower, skill_lower)

def extract_contact_info_patterns():
    """Return regex patterns for extracting contact information"""
    return {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        'linkedin': r'linkedin\.com/in/[\w-]+',
        'github': r'github\.com/[\w-]+',
    }

@st.cache_data
def load_common_skills():
    """Load and cache common technical skills"""
    return [
        # Programming Languages
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go',
        'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell', 'PowerShell',
        
        # Web Technologies  
        'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express', 'Django',
        'Flask', 'Spring', 'Laravel', 'Rails', 'ASP.NET', 'jQuery', 'Bootstrap',
        
        # Databases
        'SQL', 'MySQL', 'PostgreSQL', 'Oracle', 'MongoDB', 'Redis', 'Elasticsearch',
        'Cassandra', 'DynamoDB', 'SQLite',
        
        # Cloud & DevOps
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
        'GitLab', 'GitHub', 'Terraform', 'Ansible', 'CI/CD', 'DevOps',
        
        # Data Science
        'Machine Learning', 'Deep Learning', 'Data Science', 'Pandas', 'NumPy',
        'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras', 'OpenCV', 'NLP',
        
        # Other
        'Agile', 'Scrum', 'JIRA', 'Linux', 'Windows', 'macOS', 'API', 'REST',
        'GraphQL', 'Microservices', 'JSON', 'XML'
    ]
