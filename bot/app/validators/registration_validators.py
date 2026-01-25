def validate_age(value: str | None):
    try:
        age = int(value)  # type: ignore
        if not 10 <= age <= 100:
            return False, "⚠️ Укажи возраст числом от 10 до 100."
        return True, None
    except Exception:
        return False, "⚠️ Пожалуйста, введи возраст числом."


def validate_description(text: str | None):
    if not text or len(text) < 20:
        return False, "⚠️ Описание не должно быть короче 20 символов."
    if len(text) > 500:
        return False, "⚠️ Описание не должно превышать 500 символов."
    return True, None


def validate_gender(value: str | None):
    if value not in ["Мужской", "Женский"]:
        return False, "⚠️ Пожалуйста, выбери валидный пол."
    return True, None


def validate_prefer_gender(value: str | None):
    if value not in ["Мужской", "Женский", "Неважно"]:
        return False, "⚠️ Пожалуйста, выбери валидный пол."
    return True, None
