from ollama_client import ask_ai

def generate_talent_insights(resume_text):
    """
    Extract structured information from the candidate's resume.
    """

    prompt = f"""
You are an experienced HR Talent Analyst.

Analyze the following resume and extract the information.

Return ONLY in the following format.

# Candidate Profile

## Personal Information
- Name:
- Email:
- Phone:
- Location:

## Professional Summary
(3-4 lines)

## Education
- Degree
- College
- Year

## Work Experience
- Company
- Role
- Duration

## Technical Skills
- Programming Languages
- Frameworks
- Databases
- Tools
- Technologies

## Projects
- Project Name
- Description
- Technologies Used

## Certifications
- Certification 1
- Certification 2

## Achievements
- Achievement 1
- Achievement 2

## Soft Skills
- Communication
- Leadership
- Teamwork
- Problem Solving

## Languages Known
- Language 1
- Language 2

## Career Level
Choose one:
- Fresher
- Entry Level
- Mid Level
- Senior Level

## Recommended Job Roles
Suggest 5 suitable job roles.

## Overall Candidate Summary
Provide a professional summary in 4-5 lines.

Resume

{resume_text[:3500]}
"""

    return ask_ai(prompt)