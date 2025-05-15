from django.db import models
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from django.core.cache import cache
import torch

MODEL_NAME = "yandex/YandexGPT-5-Lite-8B-pretrain"

# Загружаем токенизатор и модель один раз при запуске Django
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, legacy=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype="auto",
)


def generate_image_prompt(lyrics, genres, mood, max_new_tokens=100, request_id=None):
    if request_id:
        cache.set(f'generation_status_{request_id}', 'started', timeout=3600)

    prompt_text = (
        f"Ты — генератор визуальных промптов для изображений в стиле Midjourney. "
        f"Сгенерируй описание изображения для обложки музыкального трека.\n\n"
        f"Текст песни:\n{lyrics}\n\n"
        f"Жанры: {', '.join(genres)}\n"
        f"Настроение: {mood}\n\n"
        f"Ответ начни сразу с описания изображения, без вступлений и пояснений."
    )

    if request_id:
        cache.set(f'generation_status_{request_id}', 'processing', timeout=3600)

    try:
        # Определяем доступное устройство
        device = "cuda" if torch.cuda.is_available() else "cpu"
        input_ids = tokenizer(prompt_text, return_tensors="pt").to(device)
        outputs = model.generate(
            **input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2
        )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        if request_id:
            cache.set(f'generation_status_{request_id}', 'completed', timeout=3600)
            cache.set(f'generation_result_{request_id}', generated_text, timeout=3600)

        return generated_text
    except Exception as e:
        if request_id:
            cache.set(f'generation_status_{request_id}', 'error', timeout=3600)
            cache.set(f'generation_error_{request_id}', str(e), timeout=3600)
        raise e