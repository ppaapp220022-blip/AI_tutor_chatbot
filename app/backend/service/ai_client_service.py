from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

def request_chat_completion(messages: list[ChatCompletionMessageParam]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return response.choices[0].message.content or ""
