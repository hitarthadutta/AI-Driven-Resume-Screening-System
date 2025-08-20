import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import zipfile
import os
from datetime import datetime

from resume_processor import ResumeProcessor
from scoring_engine import ScoringEngine
from utils import export_to_csv, create_sample_job_requirements

# Configure page with modern styling
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean light theme
st.markdown("""
<style>
    .main > div {
        padding-top: 1rem;
    }
    
    .stApp {
        background: #f8f9fa;
    }
    
    .main .block-container {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #f8f9fa;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        color: #495057;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        border: 1px solid #dee2e6;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #007bff !important;
        color: white !important;
        border-color: #007bff !important;
        box-shadow: 0 2px 8px rgba(0,123,255,0.3);
    }
    
    .metric-card {
        background: #007bff;
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,123,255,0.2);
    }
    
    .success-card {
        background: #28a745;
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(40,167,69,0.2);
    }
    
    .warning-card {
        background: #ffc107;
        padding: 1rem;
        border-radius: 8px;
        color: #212529;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(255,193,7,0.2);
    }
    
    .info-card {
        background: #17a2b8;
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(23,162,184,0.2);
    }
    
    .stSidebar > div {
        background: white;
        border-right: 1px solid #dee2e6;
    }
    
    .stButton > button {
        background: #007bff;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,123,255,0.2);
    }
    
    .stButton > button:hover {
        background: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,123,255,0.3);
    }
    
    .header-style {
        color: #212529;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        color: #6c757d;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .stSelectbox > div > div {
        background: white;
        border: 1px solid #ced4da;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border: 1px solid #ced4da;
        border-radius: 6px;
    }
    
    .stTextArea > div > div > textarea {
        background: white;
        border: 1px solid #ced4da;
        border-radius: 6px;
    }
    
    .stFileUploader > div {
        border: 2px dashed #ced4da;
        border-radius: 8px;
        background: #f8f9fa;
        padding: 2rem;
        text-align: center;
    }
    
    .stDataFrame {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        overflow: hidden;
    }
    
    h1, h2, h3, h4 {
        color: #212529;
    }
    
    .element-container {
        color: #495057;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_resumes' not in st.session_state:
    st.session_state.processed_resumes = []
if 'job_requirements' not in st.session_state:
    st.session_state.job_requirements = create_sample_job_requirements()
if 'scoring_engine' not in st.session_state:
    st.session_state.scoring_engine = ScoringEngine()

def main():
    # Clean header
    st.markdown('<h1 class="header-style">🎯 AI Resume Screening System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional candidate evaluation and ranking using advanced NLP technology</p>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Job Requirements Section
        st.markdown("#### 📋 Job Requirements")
        job_title = st.text_input("Job Title", value="Software Engineer")
        
        # Skills with suggestions
        st.markdown("**Required Skills**")
        suggested_skills = ["Python", "JavaScript", "SQL", "Git", "Machine Learning", "React", "Django", "AWS", "Docker", "Communication", "Problem Solving"]
        selected_skills = st.multiselect(
            "Select from common skills or add custom ones:",
            suggested_skills,
            default=["Python", "Machine Learning", "SQL", "Git", "Communication"]
        )
        
        custom_skills = st.text_input("Additional custom skills (comma-separated)", "")
        if custom_skills:
            selected_skills.extend([skill.strip() for skill in custom_skills.split(',') if skill.strip()])
        
        experience_years = st.number_input("Minimum Years of Experience", min_value=0, max_value=20, value=2)
        education_level = st.selectbox(
            "Minimum Education Level",
            ["High School", "Bachelor's Degree", "Master's Degree", "PhD"]
        )
        
        # Update job requirements
        if st.button("🔄 Update Job Requirements", use_container_width=True):
            st.session_state.job_requirements = {
                'job_title': job_title,
                'required_skills': [skill.strip().lower() for skill in selected_skills],
                'experience_years': experience_years,
                'education_level': education_level
            }
            st.success("✅ Job requirements updated!")
            
        # Quick stats
        if st.session_state.processed_resumes:
            st.markdown("---")
            st.markdown("#### 📊 Quick Stats")
            total_resumes = len(st.session_state.processed_resumes)
            avg_score = sum(r['total_score'] for r in st.session_state.processed_resumes) / total_resumes
            qualified = len([r for r in st.session_state.processed_resumes if r['total_score'] >= 70])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", total_resumes)
            with col2:
                st.metric("Avg Score", f"{avg_score:.1f}")
            with col3:
                st.metric("Qualified", qualified)
    
    # User guide link
    with st.expander("📖 User Guide & Help"):
        st.markdown("""
        **Quick Start:**
        1. Configure job requirements in the sidebar
        2. Upload resume files (PDF, DOCX, TXT)
        3. Click 'Process Resumes' to analyze candidates
        4. View results and export data
        
        **Scoring:** Skills (50%) + Experience (30%) + Education (20%)
        
        **Need Help?** See the complete USER_GUIDE.md file for detailed instructions.
        """)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload Resumes", "📊 Results Dashboard", "🔍 Candidate Details", "📈 Analytics"])
    
    with tab1:
        upload_resumes_tab()
    
    with tab2:
        results_dashboard_tab()
    
    with tab3:
        candidate_details_tab()
    
    with tab4:
        analytics_tab()

def upload_resumes_tab():
    st.markdown("### 📤 Upload and Process Resumes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📁 File Upload")
        uploaded_files = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx', 'txt'],
            accept_multiple_files=True,
            help="Drag and drop files here or click to browse. Supported formats: PDF, DOCX, TXT"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) selected for processing")
            
            # Show file details
            file_details = []
            for file in uploaded_files:
                file_size = file.size / 1024  # Convert to KB
                file_details.append(f"📄 {file.name} ({file_size:.1f} KB)")
            
            with st.expander("📋 View Selected Files"):
                for detail in file_details:
                    st.write(detail)
            
            if st.button("🚀 Process Resumes", type="primary", use_container_width=True):
                process_uploaded_resumes(uploaded_files)
        else:
            st.info("📁 No files selected. Please upload resume files to begin processing.")
    
    with col2:
        st.markdown("#### ⚙️ Current Job Requirements")
        job_req = st.session_state.job_requirements
        
        st.markdown(f"""
        <div class="info-card">
            <h4>📋 {job_req['job_title']}</h4>
            <p><strong>Experience:</strong> {job_req['experience_years']}+ years</p>
            <p><strong>Education:</strong> {job_req['education_level']}</p>
            <p><strong>Skills:</strong> {len(job_req['required_skills'])} required</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show top skills
        top_skills = job_req['required_skills'][:5]
        if top_skills:
            st.markdown("**🔧 Key Skills:**")
            for skill in top_skills:
                st.write(f"• {skill.title()}")
            if len(job_req['required_skills']) > 5:
                st.write(f"• ... and {len(job_req['required_skills']) - 5} more")

def process_uploaded_resumes(uploaded_files):
    processor = ResumeProcessor()
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    processed_count = 0
    total_files = len(uploaded_files)
    
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Process the resume
            extracted_data = processor.process_resume(uploaded_file)
            
            if extracted_data:
                # Score the resume
                score_data = st.session_state.scoring_engine.score_resume(
                    extracted_data, 
                    st.session_state.job_requirements
                )
                
                # Combine data
                resume_data = {
                    'filename': uploaded_file.name,
                    'processed_at': datetime.now(),
                    **extracted_data,
                    **score_data
                }
                
                st.session_state.processed_resumes.append(resume_data)
                processed_count += 1
            else:
                st.error(f"Failed to process {uploaded_file.name}")
                
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
        
        progress_bar.progress((i + 1) / total_files)
    
    status_text.text("Processing complete!")
    st.success(f"Successfully processed {processed_count} out of {total_files} resumes")
    
    if processed_count > 0:
        st.rerun()

def results_dashboard_tab():
    st.markdown("### 📊 Screening Results Dashboard")
    
    if not st.session_state.processed_resumes:
        st.info("🔍 No resumes processed yet. Please upload and process resumes first.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.processed_resumes)
    
    # Top controls with modern styling
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        min_score = st.slider("Minimum Score", 0, 100, 0)
    
    with col2:
        min_experience = st.number_input("Min Experience (years)", 0, 20, 0)
    
    with col3:
        skill_filter = st.text_input("Filter by Skill", "")
    
    with col4:
        export_button = st.button("📥 Export to CSV", use_container_width=True)
    
    # Apply filters
    filtered_df = df[df['total_score'] >= min_score].copy()
    if min_experience > 0:
        filtered_df = filtered_df[filtered_df['experience_years'] >= min_experience]
    if skill_filter:
        filtered_df = filtered_df[
            filtered_df['skills'].apply(
                lambda x: skill_filter.lower() in [skill.lower() for skill in x] if isinstance(x, list) else False
            )
        ]
    
    # Display results
    st.markdown(f"#### 🎯 Candidates ({len(filtered_df)} / {len(df)})")
    
    if len(filtered_df) == 0:
        st.warning("No candidates match the current filters.")
        return
    
    # Ranking display
    display_df = filtered_df.copy()
    display_df = display_df.sort_values('total_score', ascending=False).reset_index(drop=True)
    display_df['rank'] = display_df.index + 1
    
    # Format skills for display
    display_df['skills_display'] = display_df['skills'].apply(
        lambda x: ', '.join(x[:3]) + ('...' if len(x) > 3 else '') if isinstance(x, list) else 'N/A'
    )
    
    # Create display dataframe
    columns_to_show = ['rank', 'filename', 'name', 'total_score', 'experience_years', 'education', 'skills_display']
    available_columns = [col for col in columns_to_show if col in display_df.columns]
    result_display = display_df[available_columns].copy()
    
    # Rename columns
    column_names = {
        'rank': 'Rank',
        'filename': 'Resume File', 
        'name': 'Candidate',
        'total_score': 'Score',
        'experience_years': 'Experience',
        'education': 'Education',
        'skills_display': 'Key Skills'
    }
    result_display.columns = [column_names.get(col, col) for col in result_display.columns]
    
    st.dataframe(
        result_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                help="Overall matching score",
                min_value=0,
                max_value=100,
            )
        }
    )
    
    # Export functionality
    if export_button:
        csv_data = export_to_csv(filtered_df.to_dict('records'))
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"resume_screening_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

def candidate_details_tab():
    st.header("Detailed Candidate Information")
    
    if not st.session_state.processed_resumes:
        st.info("No resumes processed yet.")
        return
    
    # Select candidate
    candidate_names = [resume['filename'] for resume in st.session_state.processed_resumes]
    selected_candidate = st.selectbox("Select Candidate", candidate_names)
    
    if selected_candidate:
        # Find selected resume data
        selected_resume = next(
            resume for resume in st.session_state.processed_resumes 
            if resume['filename'] == selected_candidate
        )
        
        # Display detailed information
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Basic Information")
            st.write(f"**Name:** {selected_resume.get('name', 'Not extracted')}")
            st.write(f"**Email:** {selected_resume.get('email', 'Not extracted')}")
            st.write(f"**Phone:** {selected_resume.get('phone', 'Not extracted')}")
            st.write(f"**Experience:** {selected_resume.get('experience_years', 0)} years")
            st.write(f"**Education:** {selected_resume.get('education', 'Not specified')}")
            
            st.subheader("🎯 Scoring Breakdown")
            st.write(f"**Overall Score:** {selected_resume['total_score']:.1f}/100")
            st.write(f"**Skills Match:** {selected_resume['skills_score']:.1f}/100")
            st.write(f"**Experience Score:** {selected_resume['experience_score']:.1f}/100")
            st.write(f"**Education Score:** {selected_resume['education_score']:.1f}/100")
        
        with col2:
            st.subheader("🔧 Skills Analysis")
            all_skills = selected_resume.get('skills', [])
            required_skills = st.session_state.job_requirements['required_skills']
            
            matched_skills = [skill for skill in all_skills if skill.lower() in required_skills]
            missing_skills = [skill for skill in required_skills if skill not in [s.lower() for s in all_skills]]
            
            if matched_skills:
                st.success("**Matched Skills:**")
                for skill in matched_skills:
                    st.write(f"✅ {skill}")
            
            if missing_skills:
                st.warning("**Missing Skills:**")
                for skill in missing_skills:
                    st.write(f"❌ {skill}")
            
            additional_skills = [skill for skill in all_skills if skill.lower() not in required_skills]
            if additional_skills:
                st.info("**Additional Skills:**")
                for skill in additional_skills[:10]:  # Show top 10
                    st.write(f"➕ {skill}")

def analytics_tab():
    st.markdown("### 📈 Screening Analytics")
    
    if not st.session_state.processed_resumes:
        st.info("📊 No data available for analytics. Process some resumes first!")
        return
    
    df = pd.DataFrame(st.session_state.processed_resumes)
    
    # Summary metrics at the top
    st.markdown("#### 📊 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Candidates", len(df), delta=None)
    with col2:
        avg_score = df['total_score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}", delta=f"{avg_score-50:.1f}" if avg_score > 50 else None)
    with col3:
        qualified = len(df[df['total_score'] >= 70])
        st.metric("Qualified (70+)", qualified, delta=f"{(qualified/len(df)*100):.0f}%" if qualified > 0 else None)
    with col4:
        top_score = df['total_score'].max()
        st.metric("Top Score", f"{top_score:.1f}", delta="🏆" if top_score >= 85 else None)
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution with clean styling
        st.markdown("#### 📊 Score Distribution")
        fig_hist = px.histogram(
            df, 
            x='total_score', 
            nbins=15, 
            title="Distribution of Candidate Scores",
            color_discrete_sequence=['#007bff']
        )
        fig_hist.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#212529'),
            title_font_size=16,
            showlegend=False
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Experience vs Score correlation
        st.markdown("#### 🎯 Experience vs Performance")
        fig_scatter = px.scatter(
            df, 
            x='experience_years', 
            y='total_score',
            title="Experience Years vs Total Score",
            hover_data=['name'],
            color='total_score',
            color_continuous_scale='Viridis',
            size='total_score',
            size_max=15
        )
        fig_scatter.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#212529'),
            title_font_size=16
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Top skills analysis
        st.markdown("#### 🔧 Most Common Skills")
        all_skills = []
        for resume in st.session_state.processed_resumes:
            skills = resume.get('skills', [])
            if isinstance(skills, list):
                all_skills.extend(skills)
        
        if all_skills:
            skills_df = pd.DataFrame({'skill': all_skills})
            skill_counts = skills_df['skill'].value_counts().head(12)
            
            fig_bar = px.bar(
                x=skill_counts.values,
                y=skill_counts.index,
                orientation='h',
                title="Top Skills in Candidate Pool",
                color=skill_counts.values,
                color_continuous_scale='Blues'
            )
            fig_bar.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#212529'),
                title_font_size=16,
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Education distribution
        st.markdown("#### 🎓 Education Levels")
        education_counts = df['education'].value_counts()
        fig_pie = px.pie(
            values=education_counts.values,
            names=education_counts.index,
            title="Education Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#212529'),
            title_font_size=16
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Advanced analytics
    st.markdown("---")
    st.markdown("#### 🔍 Advanced Insights")
    
    insights_col1, insights_col2 = st.columns(2)
    
    with insights_col1:
        # Score ranges
        score_ranges = {
            'Excellent (85-100)': len(df[df['total_score'] >= 85]),
            'Good (70-84)': len(df[(df['total_score'] >= 70) & (df['total_score'] < 85)]),
            'Fair (55-69)': len(df[(df['total_score'] >= 55) & (df['total_score'] < 70)]),
            'Poor (0-54)': len(df[df['total_score'] < 55])
        }
        
        st.markdown("**Score Distribution:**")
        for range_name, count in score_ranges.items():
            percentage = (count / len(df)) * 100 if len(df) > 0 else 0
            st.write(f"• {range_name}: {count} candidates ({percentage:.1f}%)")
    
    with insights_col2:
        # Skills match analysis
        req_skills = set(st.session_state.job_requirements.get('required_skills', []))
        if req_skills and all_skills:
            skill_match_stats = []
            for resume in st.session_state.processed_resumes:
                resume_skills = set([s.lower() for s in resume.get('skills', [])])
                matched = len(req_skills.intersection(resume_skills))
                skill_match_stats.append(matched)
            
            avg_matched = sum(skill_match_stats) / len(skill_match_stats) if skill_match_stats else 0
            max_matched = max(skill_match_stats) if skill_match_stats else 0
            
            st.markdown("**Skills Matching:**")
            st.write(f"• Required skills: {len(req_skills)}")
            st.write(f"• Average matched: {avg_matched:.1f}")
            st.write(f"• Best match: {max_matched}")
            st.write(f"• Perfect matches: {skill_match_stats.count(len(req_skills))}")

if __name__ == "__main__":
    main()
