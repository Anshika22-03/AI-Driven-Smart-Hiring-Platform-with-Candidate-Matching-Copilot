from ollama_client import ask_ai

def rank_candidates(resume_list, job_description):
    """
    Rank multiple candidates based on the given Job Description.

    Parameters:
        resume_list: List of dictionaries
                     [
                        {"name": "Resume1.pdf", "text": "..."},
                        {"name": "Resume2.pdf", "text": "..."}
                     ]

        job_description: Job Description entered by HR
    """

    candidate_details = ""

    for i, resume in enumerate(resume_list, start=1):
        candidate_details += f"""
Candidate {i}
Name: {resume['name']}

Resume:
{resume['text'][:2000]}

----------------------------------------
"""

    prompt = f"""
You are an experienced HR Recruiter.

A company is hiring for the following role.

JOB DESCRIPTION

{job_description}

Below are multiple candidates.

Your task is to:

1. Rank all candidates from Best to Least Suitable.
2. Give each candidate a score out of 100.
3. Mention their strengths.
4. Mention their weaknesses.
5. Select the Best Candidate.
6. Explain WHY they are the best choice.

Return your response ONLY in this format.

🏆 Candidate Ranking

Rank 1
Candidate:
Score:
Strengths:
Weaknesses:

Rank 2
Candidate:
Score:
Strengths:
Weaknesses:

Rank 3
Candidate:
Score:
Strengths:
Weaknesses:

⭐ Best Candidate

Reason:
(3-4 lines)

Candidates

{candidate_details}
"""

    return ask_ai(prompt)