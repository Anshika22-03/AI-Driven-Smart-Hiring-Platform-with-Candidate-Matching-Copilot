from ollama_client import ask_ai

def chat_with_resume(resume_text, user_question):
    """
    Answer questions based only on the uploaded resume.
    """

    prompt = f"""
You are an AI Recruitment Assistant.

You have been given a candidate's resume.

Answer ONLY using the information available in the resume.
If the answer is not present in the resume, reply:
"Information not found in the resume."

Resume:
------------------------
{resume_text[:3500]}
------------------------

Recruiter's Question:
{user_question}

Provide a clear and professional answer.
"""

    return ask_ai(prompt)