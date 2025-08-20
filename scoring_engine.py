import re
from typing import Dict, List, Any
import streamlit as st

class ScoringEngine:
    """Scores resumes against job requirements using various algorithms"""
    
    def __init__(self):
        self.weights = {
            'skills': 0.5,      # 50% weight for skills matching
            'experience': 0.3,   # 30% weight for experience
            'education': 0.2     # 20% weight for education
        }
    
    def score_resume(self, resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score a resume against job requirements
        
        Args:
            resume_data: Extracted resume information
            job_requirements: Job requirements and criteria
            
        Returns:
            Dictionary containing various scores and analysis
        """
        
        # Calculate individual component scores
        skills_score = self._score_skills(resume_data, job_requirements)
        experience_score = self._score_experience(resume_data, job_requirements)
        education_score = self._score_education(resume_data, job_requirements)
        
        # Calculate weighted total score
        total_score = (
            skills_score * self.weights['skills'] +
            experience_score * self.weights['experience'] +
            education_score * self.weights['education']
        )
        
        # Generate additional analysis
        skill_analysis = self._analyze_skills(resume_data, job_requirements)
        
        return {
            'total_score': round(total_score, 1),
            'skills_score': round(skills_score, 1),
            'experience_score': round(experience_score, 1),
            'education_score': round(education_score, 1),
            'matched_skills': skill_analysis['matched'],
            'missing_skills': skill_analysis['missing'],
            'additional_skills': skill_analysis['additional'],
            'recommendation': self._generate_recommendation(total_score)
        }
    
    def _score_skills(self, resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> float:
        """Score skills matching"""
        
        resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
        required_skills = [skill.lower() for skill in job_requirements.get('required_skills', [])]
        
        if not required_skills:
            return 80.0  # Default score if no requirements specified
        
        # Calculate exact matches
        exact_matches = len([skill for skill in required_skills if skill in resume_skills])
        exact_match_score = (exact_matches / len(required_skills)) * 100
        
        # Calculate fuzzy matches for similar skills
        fuzzy_matches = 0
        for req_skill in required_skills:
            if req_skill not in resume_skills:
                for resume_skill in resume_skills:
                    if self._skills_similarity(req_skill, resume_skill) > 0.7:
                        fuzzy_matches += 0.8  # Partial credit for similar skills
                        break
        
        fuzzy_match_score = (fuzzy_matches / len(required_skills)) * 100
        
        # Combine scores (prioritize exact matches)
        combined_score = min(exact_match_score + fuzzy_match_score * 0.5, 100)
        
        # Bonus for having many relevant skills
        skill_bonus = min(len(resume_skills) * 2, 20) if len(resume_skills) > 10 else 0
        
        return min(combined_score + skill_bonus, 100)
    
    def _score_experience(self, resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> float:
        """Score experience level"""
        
        resume_experience = float(resume_data.get('experience_years', 0))
        required_experience = float(job_requirements.get('experience_years', 0))
        
        if required_experience == 0:
            return 100.0  # No experience requirement
        
        if resume_experience >= required_experience:
            # Give full score for meeting requirements, bonus for exceeding
            base_score = 100
            bonus = min((resume_experience - required_experience) * 5, 20)  # Up to 20% bonus
            return min(base_score + bonus, 100)
        else:
            # Proportional score for partial experience
            ratio = resume_experience / required_experience
            return max(ratio * 80, 10)  # Minimum 10% for any experience
    
    def _score_education(self, resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> float:
        """Score education level"""
        
        education_levels = {
            "High School": 1,
            "Certificate/Diploma": 2,
            "Bachelor's Degree": 3,
            "Master's Degree": 4,
            "PhD": 5
        }
        
        resume_education = resume_data.get('education', 'Not specified')
        required_education = job_requirements.get('education_level', 'High School')
        
        resume_level = education_levels.get(resume_education, 1)
        required_level = education_levels.get(required_education, 1)
        
        if resume_level >= required_level:
            base_score = 100
            # Bonus for higher education
            bonus = max((resume_level - required_level) * 10, 0)
            return min(base_score + bonus, 100)
        else:
            # Penalty for lower education, but not too harsh
            ratio = resume_level / required_level
            return max(ratio * 70, 30)  # Minimum 30% score
    
    def _skills_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate similarity between two skills"""
        
        # Simple similarity based on common substrings
        skill1_lower = skill1.lower()
        skill2_lower = skill2.lower()
        
        # Exact match
        if skill1_lower == skill2_lower:
            return 1.0
        
        # Check if one is contained in the other
        if skill1_lower in skill2_lower or skill2_lower in skill1_lower:
            return 0.8
        
        # Check for common technology families
        tech_families = {
            'javascript': ['js', 'node.js', 'nodejs', 'react', 'angular', 'vue'],
            'python': ['django', 'flask', 'pandas', 'numpy', 'tensorflow'],
            'java': ['spring', 'hibernate', 'maven', 'gradle'],
            'database': ['sql', 'mysql', 'postgresql', 'oracle', 'mongodb'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes']
        }
        
        for family, related_skills in tech_families.items():
            if ((skill1_lower == family and skill2_lower in related_skills) or
                (skill2_lower == family and skill1_lower in related_skills) or
                (skill1_lower in related_skills and skill2_lower in related_skills)):
                return 0.7
        
        # Basic string similarity using common characters
        common_chars = set(skill1_lower) & set(skill2_lower)
        total_chars = set(skill1_lower) | set(skill2_lower)
        
        if len(total_chars) > 0:
            return len(common_chars) / len(total_chars)
        
        return 0.0
    
    def _analyze_skills(self, resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, List[str]]:
        """Analyze skills matching in detail"""
        
        resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
        required_skills = [skill.lower() for skill in job_requirements.get('required_skills', [])]
        
        matched_skills = []
        missing_skills = []
        additional_skills = []
        
        # Find matched skills
        for req_skill in required_skills:
            if req_skill in resume_skills:
                matched_skills.append(req_skill.title())
            else:
                # Check for similar skills
                found_similar = False
                for resume_skill in resume_skills:
                    if self._skills_similarity(req_skill, resume_skill) > 0.7:
                        matched_skills.append(f"{resume_skill.title()} (similar to {req_skill.title()})")
                        found_similar = True
                        break
                
                if not found_similar:
                    missing_skills.append(req_skill.title())
        
        # Find additional skills not in requirements
        for resume_skill in resume_skills:
            if resume_skill not in required_skills:
                is_additional = True
                for req_skill in required_skills:
                    if self._skills_similarity(resume_skill, req_skill) > 0.7:
                        is_additional = False
                        break
                
                if is_additional:
                    additional_skills.append(resume_skill.title())
        
        return {
            'matched': matched_skills,
            'missing': missing_skills,
            'additional': additional_skills[:20]  # Limit additional skills
        }
    
    def _generate_recommendation(self, total_score: float) -> str:
        """Generate hiring recommendation based on score"""
        
        if total_score >= 85:
            return "🟢 Strong Match - Highly Recommended"
        elif total_score >= 70:
            return "🟡 Good Match - Recommended"
        elif total_score >= 55:
            return "🟠 Fair Match - Consider with reservations"
        elif total_score >= 40:
            return "🔴 Poor Match - Not recommended"
        else:
            return "🔴 Very Poor Match - Reject"
    
    def adjust_weights(self, skills_weight: float, experience_weight: float, education_weight: float):
        """Adjust scoring weights"""
        
        # Normalize weights to sum to 1
        total = skills_weight + experience_weight + education_weight
        
        if total > 0:
            self.weights = {
                'skills': skills_weight / total,
                'experience': experience_weight / total,
                'education': education_weight / total
            }
    
    def batch_score_resumes(self, resumes: List[Dict[str, Any]], job_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Score multiple resumes efficiently"""
        
        scored_resumes = []
        
        for resume in resumes:
            try:
                score_data = self.score_resume(resume, job_requirements)
                scored_resume = {**resume, **score_data}
                scored_resumes.append(scored_resume)
            except Exception as e:
                st.error(f"Error scoring resume {resume.get('filename', 'Unknown')}: {str(e)}")
                continue
        
        # Sort by total score (descending)
        scored_resumes.sort(key=lambda x: x.get('total_score', 0), reverse=True)
        
        return scored_resumes
