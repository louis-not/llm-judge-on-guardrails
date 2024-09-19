import os
from dotenv import load_dotenv
from nemoguardrails import LLMRails, RailsConfig

from prompt import PROMPT_SUPPORT, PROMPT_ARGUE

load_dotenv()

CONFIG_PATH = './config'

def check_config_files():
    if os.path.exists(CONFIG_PATH):
        print(f"Walking through: {CONFIG_PATH}")
        for root, dirs, files in os.walk(CONFIG_PATH):
            for file in files:
                print(os.path.join(root, file))
    else:
        raise ValueError(f"{CONFIG_PATH} doesn't exists")
    
def rails_colang_check(rails):
    # Test 1: Random
    messages = [
        {"role": "user", "content": "Three words about you"}
    ]
    completion = rails.generate(messages=messages)
    print(completion['content'])

    # Test 2: Ping
    messages = [
        {"role": "user", "content": "ping"}
    ]
    completion = rails.generate(messages=messages)
    if completion.get('content') == "test acknowledged":
        print('guardrails active')
        return True
    return False

def format_qwen_messages(messages):
    formatted = ""
    for msg in messages:
        if msg['role'] == 'system':
            formatted += f"<|im_start|>system\n{msg['content']}<|im_end|>\n"
        elif msg['role'] == 'user':
            formatted += f"<|im_start|>user\n{msg['content']}<|im_end|>\n"
        elif msg['role'] == 'assistant':
            formatted += f"<|im_start|>assistant\n{msg['content']}<|im_end|>\n"
    return formatted.strip()

def main():
    config = RailsConfig.from_path(CONFIG_PATH)
    rails = LLMRails(config)

    from config.actions import llm_sentiment_judge
    rails.register_action(llm_sentiment_judge, "llm_sentiment_judge")

    if not rails_colang_check(rails): return -1

    # Testing The judge
    # TODO: currently NemoGuardrails doesn't support system message, so this is only a quick workarounds
    real_messages_1 = [
        {'role':'system','content':PROMPT_SUPPORT},
        {'role':'user', 'content': 'Indonesia have the best city in South East Asia'}
    ]

    messages_1 = [
        {'role':'context','content':{'sentiment':'negative'}},
        {'role':'user', 'content': format_qwen_messages(real_messages_1) }
    ]
    response_1 = rails.generate(messages=messages_1)
    print("This should return bot response")
    print("Bot Response:")
    print(response_1['content'])

    real_messages_2 = [
        {'role':'system','content':PROMPT_ARGUE},
        {'role':'user', 'content': 'Indonesia have the best city in South East Asia'}
    ]

    messages_2 = [
        {'role':'context','content':{'sentiment':'negative'}}, 
        {'role':'user', 'content': format_qwen_messages(real_messages_2) }
    ]
    response_2 = rails.generate(messages=messages_2)
    print("This should return discarded responses")
    print("Bot Response:")
    print(response_2['content'])

if __name__ == '__main__':
    main()
