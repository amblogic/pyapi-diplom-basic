import requests


class YaDiskApi:
    """Класс для работы с Полигоном ЯД"""

    BASE_URL = "https://cloud-api.yandex.net"

    def __init__(self, token):
        self.token = token
        self.headers = {"Authorization": f"OAuth {self.token}"}

    def create_folder(self, path):
        """Функция для создания папки на облачном диске

        Args:
            path (string): Путь к создаваемой папке.

        Raises:
            RuntimeError: Ошибки при работе с Полигоном
        """
        response = requests.put(
            f"{self.BASE_URL}/v1/disk/resources",
            headers=self.headers,
            params={"path": path},
        )
        if response.status_code not in (201, 409):
            raise RuntimeError(f"Не удалось создать папку {path}")

    def upload_file_by_url(self, url, disk_path):
        """Функция для загрузки файла по URL

        Args:
            url (string): URL к скачиваемому файлу
            disk_path (_type_): Путь, куда будет помещён файл.
        Raises:
            RuntimeError: Ошибки при работе загрузке файла
        """
        params = ({"path": disk_path, "url": url},)
        response = requests.post(
            f"{self.BASE_URL}/v1/disk/resources/upload",
            headers=self.headers,
            json=params,
        )

        if response.status_code not in (201, 409):
            raise RuntimeError(f"Не удалось загрузить файл {url}")
