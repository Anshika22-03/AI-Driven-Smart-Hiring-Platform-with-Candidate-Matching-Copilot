from ollama_client import ask_ai

def generate_questions(role):
    """
    Generate interview questions based on the selected job role.
    """

    prompt = f"""
You are an experienced Technical Interviewer.

Generate interview questions for the following role:

Role: {role}

Provide the response in the following format.

# Interview Questions for {role}

## Technical Questions
1.
2.
3.
4.
5.

## HR Questions
1.
2.
3.
4.
5.

## Scenario-Based Questions
1.
2.
3.

## Coding Question
Provide one coding question suitable for this role.

## Evaluation Tips
Mention what the interviewer should look for in a candidate while evaluating answers.
"""

    return ask_ai(prompt)