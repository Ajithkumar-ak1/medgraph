import groq
import os
from dotenv import load_dotenv
from prompts import MEDICAL_PROMPT

load_dotenv()

groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_llm(prompt):
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def generate_answer(question, context):

    prompt = MEDICAL_PROMPT.format(
        context=context,
        question=question
    )

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content