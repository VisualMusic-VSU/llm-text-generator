import requests
import json

API_KEY = "AQVNyU6FlzunsRRNMuCe1W0lke-lHamP6AljPbZK"
FOLDER_ID = "b1gt7p0a7aju0u4km2j0"

def generate_prompt(lyrics, genres, mood):
    prompt_text = (
        "Ты — генератор визуальных промптов для изображений в стиле Midjourney. "
        f"Сгенерируй описание изображения для обложки музыкального трека. "
        f"Жанр: {', '.join(genres)}. Настроение: {mood}. "
        f"Текст песни (отрывок): {lyrics[:300]}...\n\n"
        "Ответ начни сразу с описания изображения, без вступлений и пояснений. Только визуальный промпт на русском."
    )

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
        "messages": [
            {
                "role": "user",
                "text": prompt_text
            }
        ]
    }

    response = requests.post(
        "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
        headers=headers,
        data=json.dumps(body)
    )

    if response.status_code == 200:
        result = response.json()
        reply = result["result"]["alternatives"][0]["message"]["text"]
        print("\n🎨 Сгенерированный промпт:\n", reply)
        return reply
    else:
        print("❌ Ошибка:", response.text)
        return None

# Пример использования
if __name__ == "__main__":
    lyrics = "В этом мире мы одни, и ветер нас ведёт..."
    genres = ["Hip hop"]
    mood = "Энергичное"

    generate_prompt(lyrics, genres, mood)
