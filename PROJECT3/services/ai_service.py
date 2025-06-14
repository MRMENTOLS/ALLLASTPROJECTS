import openai
from config import Config

client = None
model_name = "mistralai/mistral-7b-instruct:free"

def init_ai():
    global client
    try:
        client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1", 
            api_key=Config.OPENROUTER_API_KEY
        )
        print("🧠 ИИ успешно инициализирован.")
    except Exception as e:
        print(f"❌ Ошибка инициализации ИИ: {e}")

def generate_profession_recommendations(subjects):
    prompt = f"""
    Пользователь выбрал следующие любимые школьные предметы: {', '.join(subjects)}.
    Предложи ТОП-3 профессии, которые ему подойдут. Для каждой укажи:
    - Название
    - Описание
    - Ключевые навыки
    - Зарплата: Junior / Middle / Senior
    - Где учиться: вуз или онлайн-курсы
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Ошибка при генерации профессий: {e}")
        return None

def parse_ai_response(text):
    import re
    if not text or not isinstance(text, str):
        return []

    professions = []
    blocks = re.split(r'\d+\.\s', text)[1:]

    for block in blocks:
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        if not lines:
            continue

        name = lines[0]
        data = {
            "name": name,
            "description": "",
            "skills": [],
            "salary": "",
            "education": []
        }

        for line in lines[1:]:
            if "описание" in line.lower():
                data["description"] = line.split(":", 1)[1].strip()
            elif "навыки" in line.lower():
                data["skills"] = [x.strip() for x in line.split(":", 1)[1].strip().split(",")]
            elif "зарплата" in line.lower():
                data["salary"] = line.split(":", 1)[1].strip()
            elif "учиться" in line.lower():
                data["education"] = [x.strip() for x in line.split(":", 1)[1].strip().split(",")]

        professions.append(data)

    return professions