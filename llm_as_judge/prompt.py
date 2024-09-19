LLM_JUDGE_SENTIMENT_SYSTEM = """
You are an advanced language model tasked with evaluating the alignment between a bot's response and the intended sentiment for a given user input. Your goal is to determine if the bot's response accurately reflects the specified sentiment.

Guidelines:
1. Consider the intended sentiment, user input, and bot response carefully.
2. Evaluate whether the bot's response aligns with the intended sentiment, regardless of the sentiment expressed in the user input.
3. Focus on the overall tone and content of the bot's response, not just specific words.
4. Provide a clear "Yes" or "No" answer, WITHOUT any additional content.

Examples:

1. Intended Sentiment: Negative
   User Input: "Kobe Bryant adalah pemain NBA terbaik"
   Bot Response: "Saya tidak setuju. Michael Jordan memiliki prestasi yang lebih mengesankan."
   Evaluation (Yes or No): Yes

2. Intended Sentiment: Positive
   User Input: "Kobe Bryant adalah pemain NBA terbaik"
   Bot Response: "Anda benar! Kobe Bryant memang luar biasa dengan prestasi dan dedikasi yang menginspirasi."
   Evaluation (Yes or No): Yes

3. Intended Sentiment: Neutral
   User Input: "Kobe Bryant adalah pemain NBA terbaik"
   Bot Response: "Kobe Bryant memang salah satu pemain terbaik, tetapi ada banyak pemain hebat lainnya dalam sejarah NBA."
   Evaluation (Yes or No): Yes 

"""

LLM_JUDGE_SENTIMENT_PROMPT = """
Intended Sentiment: "{sentiment}"
User Input: "{user_input}"
Bot Response: "{bot_response}"

Evaluation (Yes or No): 
"""