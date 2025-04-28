from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import json

API_KEY = "AQVNyU6FlzunsRRNMuCe1W0lke-lHamP6AljPbZK"
FOLDER_ID = "b1gt7p0a7aju0u4km2j0"

def build_prompt(lyrics, genres, mood):
    return (
        "Ты — генератор визуальных промптов для изображений в стиле Midjourney. "
        f"Сгенерируй описание изображения для обложки музыкального трека. "
        f"Жанр: {', '.join(genres)}. Настроение: {mood}. "
        f"Текст песни (отрывок): {lyrics[:300]}...\n\n"
        "Ответ начни сразу с описания изображения, без вступлений и пояснений. Только визуальный промпт на русском."
    )

@api_view(['POST'])
def generate_prompt(request):
    data = request.data
    try:
        lyrics = data["lyrics"]
        genres = data["genres"]
        mood = data["mood"]

        prompt_text = build_prompt(lyrics, genres, mood)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {API_KEY}"
        }

        body = {
            "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.8,
                "maxTokens": 100
            },
            "messages": [{"role": "user", "text": prompt_text}]
        }

        response = requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
            headers=headers,
            data=json.dumps(body)
        )

        if response.status_code == 200:
            result = response.json()
            reply = result["result"]["alternatives"][0]["message"]["text"]
            return Response({"prompt": reply})
        else:
            return Response({"error": response.text}, status=response.status_code)

    except KeyError as e:
        return Response({"error": f"Missing key: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
