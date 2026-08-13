import ollama

MODEL_NAME = "llama3.2"


def ask_ai(prompt):
    """
    Sends a prompt to Ollama and returns the AI response.
    """
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Alias for compatibility
def ask_llm(prompt):
    """
    Alias for ask_ai() so other modules can use ask_llm().
    """
    return ask_ai(prompt)