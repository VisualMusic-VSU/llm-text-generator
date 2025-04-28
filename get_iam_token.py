import requests
import json

key_id = "aje99q2peet7m4a4qcn0"
key_secret = "AQVNyU6FlzunsRRNMuCe1W0lke-lHamP6AljPbZK"

# Запрос IAM токена
response = requests.post(
    "https://iam.api.cloud.yandex.net/iam/v1/tokens",
    headers={"Content-Type": "application/json"},
    json={
        "yandexPassportOauthToken": None,
        "serviceAccountId": key_id,
        "keyId": key_id,
        "secret": key_secret
    }
)

# Проверим и выведем IAM токен
if response.ok:
    token = response.json()["iamToken"]
    print("✅ IAM Token:\n", token)
else:
    print("❌ Ошибка при получении токена:\n", response.text)