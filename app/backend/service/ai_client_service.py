from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

def request_chat_completion(messages: list[ChatCompletionMessageParam]) -> str:
    """
    OpenAI 활용 채팅 요청건 응답 처리
    :param messages: OpenAI 요청 메시지 목록
    :return: 생성된 응답 텍스트
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return response.choices[0].message.content or ""