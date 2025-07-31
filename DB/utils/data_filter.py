import re
from string import ascii_letters
from typing import Union, List, Dict, Any


def validate_user_input(login: str, password: str)-> list[Any] | bool | None:
    errors = []
    lower_case = False
    upper_case = False
    is_digits = False
    special_chars = bool(re.search(r'[^a-zA-Z0-9]', password))
    len_login = len(login)
    len_password = len(password)

    if len_login < 8:
        errors.append({"message": "Длина лоигина меньше 8"})

    if len_password < 8:
        errors.append({"message": "Длина пароля меньше 8"})

    if errors:
        return errors


    for char in password:
        if char.isdigit():
            is_digits = True

        if char.isupper():
            upper_case = True

        if char.islower():
            lower_case = True

    if lower_case and upper_case and is_digits and special_chars:
        return True
    else:
        return errors.append({"message": "Используйте заглавные буквы, маленькие буквы, цифры и специальные символы для создания пароля"})
