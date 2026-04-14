
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)


# SAMPLE DATA

JOB_DESCRIPTION = """
Job Title: Data Scientist
Company: Tech Corp
Experience Required: 3-5 years
Required Skills:
- Python
- Machine Learning
- Data Analysis
- SQL
- Statistics
- TensorFlow or PyTorch
- Data Visualization (Matplotlib, Seaborn)
Responsibilities:
- Develop ML models for prediction
- Analyze large datasets
- Create data visualizations
- Collaborate with engineering teams
"""

STRONG_RESUME = """
Name: Sahil Pawar
Experience:
- Senior Data Scientist at AI Labs (2021-Present, 3 years)
  * Developed ML models using TensorFlow
  * Analyzed datasets with 10M+ records
  * Created dashboards using Python and Seaborn
- ML Engineer at DataCorp (2018-2021, 3 years)
  * Built recommendation systems
  * Used Python for data processing
  * Implemented statistical models
Skills: Python, Machine Learning, TensorFlow, PyTorch, SQL, Statistics, Matplotlib, Seaborn, Data Analysis
Education: MS in Data Science
Certifications: ML specialization from Coursera
"""

AVERAGE_RESUME = """
Name: Jake
Experience:
- Data Analyst at RetailCo (2022-Present, 2 years)
  * Analyzed sales data using SQL
  * Created basic reports in Excel
  * Some Python scripting for automation
- Junior Analyst at FinanceHub (2020-2022, 2 years)
  * Data entry and basic analysis
  * SQL queries for reporting
Skills: Python (basic), SQL, Data Analysis, Excel, Matplotlib
Education: Bachelor's in Business Analytics
"""

WEAK_RESUME = """
Name: Tom
Experience:
- Data Entry Clerk at Services Inc (2023-Present, 1 year)
  * Entered data into databases
  * Basic spreadsheet work
- Internship at TechStart (2023, 3 months)
  * Learned some Python basics
Skills: Excel, Basic Python, Data Entry
Education: High School Diploma
"""

# STEP 1: SKILL EXTRACTION


skill_extraction_prompt = PromptTemplate(
    input_variables=["resume"],
    template="""Extract skills, experience, and tools from the following resume.
Return a JSON object with keys: "skills", "years_experience", "tools", "education".

Resume:
{resume}

JSON Output:"""
)

skill_extraction_chain = skill_extraction_prompt | llm | JsonOutputParser()



matching_prompt = PromptTemplate(
    input_variables=["job_description", "resume_skills", "resume_experience"],
    template="""Compare the candidate's skills and experience with the job requirements.
Return a JSON object with keys: "matched_skills", "missing_skills", "match_percentage".

Job Description:
{job_description}

Resume Skills: {resume_skills}
Resume Experience: {resume_experience}

JSON Output:"""
)

matching_chain = matching_prompt | llm | JsonOutputParser()



scoring_prompt = PromptTemplate(
    input_variables=["matched_skills", "missing_skills", "match_percentage", "years_experience"],
    template="""Based on skill matching and experience, assign a score from 0-100.
Return a JSON object with keys: "score", "score_breakdown".

Matched Skills: {matched_skills}
Missing Skills: {missing_skills}
Match Percentage: {match_percentage}
Years of Experience: {years_experience}

Scoring Rules:
- Each matched core skill: +10 points (max 60)
- Experience (3+ years): +20 points
- Match percentage (80%+): +10 points
- Education level: +5 points
- Missing skills: -5 points each (max -30)

JSON Output:"""
)

scoring_chain = scoring_prompt | llm | JsonOutputParser()


explanation_prompt = PromptTemplate(
    input_variables=["score", "matched_skills", "missing_skills", "experience"],
    template="""Provide a clear explanation for the resume score.
Return a JSON object with keys: "summary", "strengths", "weaknesses", "recommendation".

Score: {score}
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}
Experience: {experience}

Provide a 2-3 sentence summary, list strengths, list weaknesses, and give a hiring recommendation (STRONG MATCH / AVERAGE MATCH / WEAK MATCH).

JSON Output:"""
)

explanation_chain = explanation_prompt | llm | JsonOutputParser()


# MAIN PIPELINE


def screen_resume(resume_text, resume_name):
    print(f"\n{'='*60}")
    print(f"Screening: {resume_name}")
    print(f"{'='*60}")
    
    try:

        print("\n[Step 1] Extracting Skills...")
        extracted = skill_extraction_chain.invoke({"resume": resume_text})
        print(f"Extracted Skills: {extracted.get('skills', [])}")
        print(f"Years of Experience: {extracted.get('years_experience', 'N/A')}")
        

        print("\n[Step 2] Matching with Job Requirements...")
        matched = matching_chain.invoke({
            "job_description": JOB_DESCRIPTION,
            "resume_skills": str(extracted.get('skills', [])),
            "resume_experience": extracted.get('years_experience', '0')
        })
        print(f"Matched Skills: {matched.get('matched_skills', [])}")
        print(f"Missing Skills: {matched.get('missing_skills', [])}")
        print(f"Match Percentage: {matched.get('match_percentage', '0')}%")
        
      
        print("\n[Step 3] Calculating Score...")
        score = scoring_chain.invoke({
            "matched_skills": str(matched.get('matched_skills', [])),
            "missing_skills": str(matched.get('missing_skills', [])),
            "match_percentage": matched.get('match_percentage', '0'),
            "years_experience": extracted.get('years_experience', '0')
        })
        print(f"Final Score: {score.get('score', '0')}/100")
        print(f"Score Breakdown: {score.get('score_breakdown', {})}")
        

        print("\n[Step 4] Generating Explanation...")
        explanation = explanation_chain.invoke({
            "score": score.get('score', '0'),
            "matched_skills": str(matched.get('matched_skills', [])),
            "missing_skills": str(matched.get('missing_skills', [])),
            "experience": extracted.get('years_experience', '0')
        })
        print(f"\nSummary: {explanation.get('summary', 'N/A')}")
        print(f"Strengths: {explanation.get('strengths', [])}")
        print(f"Weaknesses: {explanation.get('weaknesses', [])}")
        print(f"Recommendation: {explanation.get('recommendation', 'N/A')}")
        
        return {
            "resume_name": resume_name,
            "score": score.get('score', 0),
            "matched_skills": matched.get('matched_skills', []),
            "missing_skills": matched.get('missing_skills', []),
            "recommendation": explanation.get('recommendation', 'N/A')
        }
        
    except Exception as e:
        print(f"Error screening resume: {str(e)}")
        return None


if __name__ == "__main__":
    print("\n" + "="*60)
    print("AI RESUME SCREENING SYSTEM")
    print("="*60)
    
    results = []
    

    results.append(screen_resume(STRONG_RESUME, "STRONG CANDIDATE"))
    results.append(screen_resume(AVERAGE_RESUME, "AVERAGE CANDIDATE"))
    results.append(screen_resume(WEAK_RESUME, "WEAK CANDIDATE"))
    
    # Summary
    print(f"\n{'='*60}")
    print("SCREENING RESULTS SUMMARY")
    print(f"{'='*60}")
    
    for result in results:
        if result:
            print(f"\n{result['resume_name']}: {result['score']}/100 - {result['recommendation']}")
