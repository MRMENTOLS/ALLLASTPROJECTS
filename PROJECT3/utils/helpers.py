def format_profession(prof):
    return (
        f"💼 *{prof['name']}*\n\n"
        f"{prof['description']}\n\n"
        f"💰 Зарплата: {prof['salary']}\n\n"
        f"📚 Где учиться: {'\n  '.join(prof['education'])}"
    )