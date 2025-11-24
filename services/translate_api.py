import requests
from config_data.config import site


class TranslationAPIError(Exception):
    """
    Исключение, возникающее при ошибке перевода текста.
    """
    pass

def log_error(message):
    """
    Записывает сообщение об ошибке в файл.

    Args:
        message (str): Сообщение об ошибке.
    """
    with open('exceptions.txt', 'a', encoding='utf8') as errors_log:
        errors_log.write(f"{message}\n")

def split_into_sentences(text):
    """
    Разбивает текст на предложения для более точного перевода.

    Args:
        text (str): Исходный текст.

    Returns:
        list: Список предложений.
    """
    # Простое разделение по точкам, восклицательным и вопросительным знакам
    import re
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return sentences

def translate_text(text, target_language="ru"):
    """
    Переводит текст с английского на целевой язык с использованием API перевода.

    Args:
        text (str): Текст для перевода.
        target_language (str): Целевой язык. По умолчанию русский ("ru").

    Returns:
        str: Переведенный текст или None, если перевод не удался.

    Raises:
        TranslationAPIError: Если возникает ошибка при запросе к API перевода.
    """
    if not text:
        return None

    # Разбиваем текст на предложения для более точного перевода
    sentences = split_into_sentences(text)
    translated_sentences = []

    url = site.translate_api
    timeout = 10    # секунд

    for sentence in sentences:
        if not sentence.strip():
            continue

        params = {
            "client": "gtx",
            "sl": "en",  # Source language (English)
            "tl": target_language,  # Target language (Russian by default)
            "dt": "t",  # Request translation
            "q": sentence,  # Text to translate
        }

        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()

            result = response.json()
            if not result or not isinstance(result, list) or len(result) == 0:
                error_message = f"Некорректный формат ответа от API перевода для предложения: {sentence}"
                log_error(error_message)
                raise TranslationAPIError(error_message)

            translated_sentences.append(result[0][0][0])    # Извлечение переведённого текста

        except requests.exceptions.Timeout:
            error_message = f"Таймаут при переводе предложения: {sentence}"
            log_error(error_message)
            raise TranslationAPIError(error_message)
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP ошибка при переводе предложения '{sentence}': {e}"
            log_error(error_message)
            raise TranslationAPIError(error_message)
        except requests.exceptions.RequestException as e:
            error_message = f"Ошибка сети при переводе предложения '{sentence}': {e}"
            log_error(error_message)
            raise TranslationAPIError(error_message)

    # Объединяем переведенные предложения
    return " ".join(translated_sentences) if translated_sentences else None
