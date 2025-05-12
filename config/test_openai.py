import os
from openai import OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: ключ не знайдено")
    exit(1)
client = OpenAI(api_key=api_key)
resp = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role":"user","content":"Hello"}],
    max_tokens=5
)
print("GPT відповів:", resp.choices[0].message.content)
