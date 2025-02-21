import hashlib
import random
import string

async def generate_referral_code(user_id: int) -> str:
    """
    Генерация уникального реферального кода на основе user_id.
    
    :param user_id: Идентификатор пользователя
    :return: Строка с реферальным кодом
    """
    # Преобразуем user_id в строку и хэшируем его
    user_id_str = str(user_id)
    hash_object = hashlib.sha256(user_id_str.encode())
    hex_dig = hash_object.hexdigest()
    
    # Берем первые 8 символов из хеша и добавляем случайные буквы/цифры
    referral_code = hex_dig[:8] + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    return referral_code
