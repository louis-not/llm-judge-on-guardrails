import logging
from typing import Optional
import re

from transformers import AutoTokenizer

from nemoguardrails.actions import action
from llm_as_judge.llm import judge_response

log = logging.getLogger(__name__)

@action(is_system_action=True)
async def llm_sentiment_judge(context: Optional[dict] = None) -> bool:
    try:
        if context is None:
            raise ValueError("Context is required")
        sentiment = context.get('sentiment')
        user_input = extract_user_prompt(context.get('user_message', ''))
        bot_response = context.get("bot_message")
        if bot_response and user_input:
            response = await judge_response(
                sentiment=sentiment,
                user_input=user_input,
                bot_response=bot_response,
            )
            log.info(f"Output self-checking result is: `{response}`.")
            response = response.lower().strip()
            return "yes" not in response
        else:
            log.warning("Missing bot_response or user_input")
            raise ValueError("Missing bot_response or user_input")
    except Exception as e:
        log.error(f"Error in llm_sentiment_judge: {str(e)}")
        return True

def extract_user_prompt(formatted_prompt):
    messages = parse_qwen_formatted_prompt_qwen(formatted_prompt)
    # Hardcoded to return user messages
    return messages[1]['content']

# Utils: parsing templated chat
def parse_qwen_formatted_prompt_qwen(formatted_prompt):
    pattern = r'<\|im_start\|>(\w+)\n(.*?)<\|im_end\|>'
    matches = re.findall(pattern, formatted_prompt, re.DOTALL)
    
    messages = []
    for role, content in matches:
        messages.append({'role': role, 'content': content.strip()})
    
    return messages