from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "yandex/YandexGPT-5-Lite-8B-pretrain"

# Загружаем токенизатор и модель один раз при запуске Django
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, legacy=False)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    device_map="auto",
    torch_dtype="auto",
)


def generate_image_prompt(lyrics, genres, mood, max_new_tokens=100):
    prompt_text = (
        f"Ты — генератор визуальных промптов для изображений в стиле Midjourney. "
        f"Сгенерируй описание изображения для обложки музыкального трека.\n\n"
        f"Текст песни:\n{lyrics}\n\n"
        f"Жанры: {', '.join(genres)}\n"
        f"Настроение: {mood}\n\n"
        f"Ответ начни сразу с описания изображения, без вступлений и пояснений."
    )

    input_ids = tokenizer(prompt_text, return_tensors="pt").to("cuda")
    outputs = model.generate(**input_ids, max_new_tokens=max_new_tokens)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_text
