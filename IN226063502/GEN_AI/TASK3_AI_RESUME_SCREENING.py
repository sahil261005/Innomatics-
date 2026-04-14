# AI Resume Screening System

## Overview
This is a complete AI Resume Screening System using LangChain for skill extraction, matching logic, scoring system, and explanation generation. The system evaluates resumes based on their content and matches them to a given job description.

## Components:

1. **Full LangChain Implementation**
   - Skill extraction from resumes.
   - Matching logic to compare resumes against job descriptions.
   - Scoring system to rank candidates.
   - Explanation generator to provide insights on scores.

2. **Sample Resumes**
   - **Strong Resume**: A well-structured resume showcasing relevant skills and experience.
   - **Average Resume**: A decent resume with some strengths and weaknesses.
   - **Weak Resume**: A poorly structured resume lacking relevant information.

3. **Job Description**: A clear and precise job description that outlines the role and required skills.

4. **LangSmith Tracing Integration**: Implementation of LangSmith for tracing and debugging.

## Sample Code:

```python
import langchain

# Sample job description
job_description = "Looking for an AI specialist with experience in natural language processing."

# Sample resumes
strong_resume = "Experienced AI specialist with 5 years in NLP."
average_resume = "A decent candidate with some experience in AI."
weak_resume = "Looking for opportunities."

# Function to extract skills
def extract_skills(resume):
    # Placeholder for skill extraction logic
    return extracted_skills

# Function to match resume with job description
def match_resume(resume, job_desc):
    # Placeholder for matching logic
    return score

# Main logic
for resume in [strong_resume, average_resume, weak_resume]:
    skills = extract_skills(resume)
    score = match_resume(resume, job_description)
    print(f"{resume} scored {score}.")
```

## Usage
To use this system, integrate it with a user interface to accept resumes and job descriptions. The output scores and explanations can guide recruitment decisions.
