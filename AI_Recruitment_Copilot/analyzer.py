from ollama_client import ask_ai

def analyze_resume(resume_text, job_description):
    """
    Analyze a resume against a job description using Ollama.
    """

    prompt = f"""
You are an experienced HR Recruiter and ATS (Applicant Tracking System).

Compare the candidate's resume with the job description.

Provide your response in the following format only:

# Resume Match Analysis

## Overall Match Score
(Give a score out of 100)

## Matching Skills
- Skill 1
- Skill 2
- Skill 3

## Missing Skills
- Skill 1
- Skill 2
- Skill 3

## Candidate Strengths
- Strength 1
- Strength 2
- Strength 3

## Areas for Improvement
- Improvement 1
- Improvement 2

## Hiring Recommendation
Choose one:
- Strongly Recommend
- Recommend
- Consider
- Not Recommended

Explain your recommendation in 2-3 sentences.

-----------------------------
JOB DESCRIPTION
-----------------------------
{job_description}

-----------------------------
CANDIDATE RESUME
-----------------------------
{resume_text[:3500]}
"""

    return ask_ai(prompt)