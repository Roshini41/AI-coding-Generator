import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# "groq" (cloud) or "ollama" (local Llama). Defaults to groq.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

SYSTEM_PROMPT = """You are an expert coding challenge creator.
Your task is to generate a coding question with multiple choice answers.
The question should be appropriate for the specified difficulty level.

For easy questions: focus on basic syntax, simple operations, or common concepts.
For medium questions: focus on data structures, algorithms, or language features.
For hard questions: focus on advanced concepts, design patterns, or optimization.

Return the challenge in the following JSON structure:
{
    "title": "The question title",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correct_answer_id": 0,
    "explanation": "Detailed explanation of why the correct answer is right"
}

Make sure the options are plausible, with only one clearly correct answer.
Respond with ONLY the JSON object, no extra text.
"""


def _messages(difficulty: str):
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Generate a {difficulty} difficulty coding challenge.",
        },
    ]


def _generate_with_groq(difficulty: str) -> str:
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=_messages(difficulty),
        response_format={"type": "json_object"},  # force JSON
        temperature=0.7,
    )
    return response.choices[0].message.content


def _generate_with_ollama(difficulty: str) -> str:
    import ollama

    response = ollama.chat(
        model=os.getenv("OLLAMA_MODEL", "llama3.1"),
        messages=_messages(difficulty),
        format="json",                 # force JSON
        options={"temperature": 0.7},
    )
    return response["message"]["content"]


def _fallback_challenge() -> Dict[str, Any]:
    return {
        "title": "Basic Python List Operation",
        "options": [
            "my_list.append(5)",
            "my_list.add(5)",
            "my_list.push(5)",
            "my_list.insert(5)",
        ],
        "correct_answer_id": 0,
        "explanation": "In Python, append() adds an element to the end of a list.",
    }


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    try:
        if LLM_PROVIDER == "ollama":
            content = _generate_with_ollama(difficulty)
        else:
            content = _generate_with_groq(difficulty)

        challenge_data = json.loads(content)

        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data

    except Exception as e:
        print(e)
        return _fallback_challenge()