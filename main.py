from prompt_generator import generate_image_prompt

lyrics = "Я свободен, словно птица в небесах..."
genres = ["Рок"]
mood = "Энергичное"

prompt = generate_image_prompt(lyrics, genres, mood)
print("\n🎨 Сгенерированный промпт:\n", prompt)
