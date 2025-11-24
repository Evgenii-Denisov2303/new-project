import requests
from config_data.config import site


class CatAPIError(Exception):
    """
    Исключение, возникающее при ошибке получения изображения кота.
    """
    pass

def check_api_response(data):
    """
    Проверяет формат ответа API.

    Args:
        data (list): Данные из ответа API.

    Raises:
        CatAPIError: Если формат ответа неверный.
    """
    if not data or not isinstance(data, list) or len(data) == 0:
        raise CatAPIError(f"Неверный формат ответа API: {data}")

def check_image_url(data):
    """
    Проверяет наличие URL изображения в ответе API.

    Args:
        data (list): Данные из ответа API.

    Returns:
        str: URL изображения.

    Raises:
        CatAPIError: Если URL изображения отсутствует.
    """
    image_url = data[0].get('url')
    if not image_url:
        raise CatAPIError("URL изображения отсутствует в ответе API")
    return image_url

def random_image_cat():
    """
    Получает случайное изображение кота из The Cat API.

    Делает запрос к API для получения случайного изображения кота.
    Обрабатывает потенциальные ошибки во время запроса.

    Args:
        None

    Returns:
        str: URL изображения кота или сообщение об ошибке.
    """
    url = site.cat_api
    timeout = 10  # секунд

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        data = response.json()

        check_api_response(data)
        image_url = check_image_url(data)

        return image_url

    except requests.exceptions.Timeout as e:
        error_message = "Таймаут при запросе изображения кота."
        log_error(error_message)
        return error_message
    except requests.exceptions.RequestException as e:
        error_message = f"Ошибка при запросе изображения кота: {e}"
        log_error(error_message)
        return error_message

def log_error(message):
    """
    Записывает сообщение об ошибке в файл.

    Args:
        message (str): Сообщение об ошибке.
    """
    with open('exceptions.txt', 'a', encoding='utf8') as errors_log:
        errors_log.write(f"{message}\n")
