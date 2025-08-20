# 🚀 AI Resume Screening System - User Guide

## Overview
The AI Resume Screening System is a powerful tool that helps recruiters and hiring managers automatically evaluate and rank candidates using advanced Natural Language Processing (NLP) technology. The system processes resume files, extracts key information, and scores candidates against job requirements.

## Features
- **Multi-format Support**: Upload PDF, DOCX, and TXT resume files
- **Smart Extraction**: Automatically extracts names, skills, experience, education, and contact information
- **Intelligent Scoring**: Scores candidates using weighted algorithms (50% skills, 30% experience, 20% education)
- **Interactive Dashboard**: View results with filtering, sorting, and export capabilities
- **Modern UI**: Clean, responsive interface with real-time updates

## Getting Started

### 1. Configure Job Requirements
Before processing resumes, set up your job requirements in the sidebar:

#### Job Details
- **Job Title**: Enter the position you're hiring for
- **Required Skills**: Select from common skills or add custom ones
- **Experience**: Set minimum years of experience required
- **Education**: Choose minimum education level

#### Pro Tips:
- Use specific skill names (e.g., "React" instead of "Frontend")
- Include both technical and soft skills
- Consider using skill variations (e.g., "JavaScript", "JS")

### 2. Upload and Process Resumes

#### Upload Process
1. Go to the "📤 Upload Resumes" tab
2. Click "Choose resume files" or drag and drop files
3. Select multiple files (PDF, DOCX, TXT supported)
4. Click "🚀 Process Resumes"

#### What Happens During Processing:
- Text extraction from all file formats
- NLP analysis for information extraction
- Skills matching against requirements
- Experience and education evaluation
- Overall scoring calculation

### 3. Review Results

#### Dashboard Overview
The "📊 Results Dashboard" shows:
- **Candidate Rankings**: Sorted by total score
- **Filtering Options**: Score, experience, and skill filters
- **Export Function**: Download results as CSV

#### Understanding Scores
- **Total Score**: Overall candidate rating (0-100)
- **Skills Score**: How well skills match requirements
- **Experience Score**: Experience level evaluation
- **Education Score**: Education requirement matching

#### Score Interpretation:
- **85-100**: 🟢 Strong Match - Highly Recommended
- **70-84**: 🟡 Good Match - Recommended
- **55-69**: 🟠 Fair Match - Consider with reservations
- **40-54**: 🔴 Poor Match - Not recommended
- **0-39**: 🔴 Very Poor Match - Reject

### 4. Analyze Individual Candidates

#### Detailed Candidate View
The "🔍 Candidate Details" tab provides:
- **Basic Information**: Name, email, phone, experience, education
- **Scoring Breakdown**: Component-wise score analysis
- **Skills Analysis**: 
  - ✅ Matched skills (meets requirements)
  - ❌ Missing skills (gaps to address)
  - ➕ Additional skills (bonus strengths)

### 5. View Analytics

#### Analytics Dashboard
The "📈 Analytics" tab offers:
- **Score Distribution**: Histogram of candidate scores
- **Experience vs Score**: Correlation analysis
- **Common Skills**: Most frequent skills in candidate pool
- **Summary Statistics**: Key metrics and insights

## Best Practices

### For Accurate Results
1. **Complete Job Requirements**: Fill in all fields accurately
2. **Specific Skills**: Use precise skill names and include variations
3. **Regular Updates**: Update requirements as needs change
4. **Quality Control**: Review high-scoring candidates manually

### Optimizing the System
1. **Batch Processing**: Upload multiple resumes at once for efficiency
2. **Use Filters**: Apply filters to focus on specific candidate segments
3. **Export Data**: Download results for further analysis or record-keeping
4. **Monitor Trends**: Use analytics to understand your candidate pool

## Troubleshooting

### Common Issues

#### "No Text Extracted" Error
- **Cause**: File might be corrupted or image-based PDF
- **Solution**: Try converting to different format or use OCR tool

#### "Processing Failed" Error
- **Cause**: File format not supported or file too large
- **Solution**: Check file format (PDF/DOCX/TXT) and size limits

#### Low Scores for Good Candidates
- **Cause**: Skills mismatch or requirements too specific
- **Solution**: Review and adjust skill requirements

#### Missing Information
- **Cause**: Resume format or unclear text structure
- **Solution**: Candidates should use standard resume formats

### Performance Tips
- Process resumes in batches of 20-50 for optimal performance
- Use specific skill keywords for better matching
- Regularly clear old results to maintain system performance

## Technical Requirements

### System Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Stable internet connection
- JavaScript enabled

### File Requirements
- **Formats**: PDF, DOCX, TXT
- **Size**: Maximum 10MB per file
- **Quality**: Text should be selectable (not scanned images)

## Data Privacy & Security

### Data Handling
- Resume data is processed in memory only
- No permanent storage of candidate information
- Files are deleted after processing session ends

### Privacy Compliance
- System follows data minimization principles
- No tracking or analytics on candidate data
- Secure processing environment

## Support & Updates

### Getting Help
- Review this guide for common issues
- Check system requirements and file formats
- Contact system administrator for technical support

### Feature Requests
- Submit feedback for new features
- Report bugs or issues
- Suggest improvements to scoring algorithms

## Advanced Features

### Custom Scoring Weights
The system uses default weights:
- Skills: 50%
- Experience: 30% 
- Education: 20%

These can be adjusted based on role requirements.

### Bulk Operations
- Export filtered results
- Process multiple job requirements
- Batch candidate comparison

### Integration Capabilities
- CSV export for ATS systems
- API endpoints for custom integrations
- Webhook support for automated workflows

---

## Quick Reference

### Navigation
- **Upload**: Process new resumes
- **Dashboard**: View and filter results
- **Details**: Individual candidate analysis
- **Analytics**: Pool insights and trends

### Keyboard Shortcuts
- **Ctrl+U**: Upload files
- **Ctrl+E**: Export results
- **Ctrl+F**: Open filters
- **Ctrl+R**: Refresh results

### File Formats
- ✅ PDF (text-based)
- ✅ DOCX (Microsoft Word)
- ✅ TXT (plain text)
- ❌ Images (JPG, PNG)
- ❌ Scanned PDFs without OCR

---

*Last updated: Version 2.0 - Enhanced NLP Processing with Modern UI*