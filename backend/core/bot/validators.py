import re


PHONE_RE = re.compile(r"^(?:\+7|7|8)\d{10}$")


def normalize_phone(phone):
    value = phone.strip()
    value = re.sub(r"[\s\-()]", "", value)

    if not PHONE_RE.fullmatch(value):
        return None

    if value.startswith("8"):
        return "+7" + value[1:]

    if value.startswith("7"):
        return "+" + value

    return value
