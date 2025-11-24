import requests
from config_data.config import site


class CatFactAPIError(Exception):
    """
    Исключение, возникающее при ошибке получения факта о кошке.
    """
    pass

def check_error(response):
    """
    Проверяет статус ответа на запрос и вызывает исключение при ошибке.

    Args:
        response (requests.Response): Ответ на запрос.

    Raises:
        CatFactAPIError: Если статус ответа не 200.
    """
    if response.status_code != 200:
        raise CatFactAPIError(f"Ошибка запроса: {response.status_code}")

def log_error(message):
    """
    Записывает сообщение об ошибке в файл.

    Args:
        message (str): Сообщение об ошибке.
    """
    with open('exceptions.txt', 'a', encoding='utf8') as errors_log:
        errors_log.write(f"{message}\n")

def get_cat_fact(url=site.cat_facts_api, timeout=10):
    """
    Получает факт о кошке из API.

    Args:
        url (str): URL API для получения факта. По умолчанию используется site.cat_facts_api.
        timeout (int): Время ожидания ответа в секундах. По умолчанию 10 секунд.

    Returns:
        str: Текст факта или сообщение об ошибке.

    Raises:
        CatFactAPIError: Если возникает ошибка при запросе.
    """
    try:
        response = requests.get(url, timeout=timeout)
        check_error(response)
        data = response.json().get('fact', '')  # Безопасный доступ к данным
        return data
    except requests.exceptions.RequestException as e:
        error_message = f"Ошибка подключения: {e}"
        log_error(error_message)
        return error_message

url = site.cat_facts_api
timeout = 10  # секунд
try:
    fact = get_cat_fact(url, timeout)
except CatFactAPIError as e:
    log_error(f"Ошибка: {e}")
