from typing import List
from openai import OpenAI
import os
from dotenv import load_dotenv

from .prompt import LLM_JUDGE_SENTIMENT_PROMPT, LLM_JUDGE_SENTIMENT_SYSTEM

load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

models = client.models.list()
model = models.data[0].id

def generate(messages: List, temperature=0.3, top_p=0.9, max_token=20):
    response = client.chat.completions.create(
        model=model,
        messages= messages,
        temperature=temperature,
        top_p=top_p,
        stream=False,
        stop=["</s>", "<|im_end|>", "<|endoftext|>"],
        max_tokens=max_token
    )
    return response.choices[0].message.content


async def judge_response(sentiment: str, user_input: str, bot_response: str) -> str:

    prompt = LLM_JUDGE_SENTIMENT_PROMPT.format(
        sentiment=sentiment,
        user_input=user_input,
        bot_response=bot_response
    )

    messages = [
        {"role": "system", "content": LLM_JUDGE_SENTIMENT_SYSTEM},
        {"role": "user", "content": prompt}
    ]

    return generate(messages, max_token=3)

