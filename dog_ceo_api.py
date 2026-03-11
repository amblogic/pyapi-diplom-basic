import requests
from urllib.parse import urlparse
from pathlib import Path


class DogCeoApi:
    BASE_URL = "https://dog.ceo/api/breed"
    """Класс для работы с API ресурса dog.ceo
    """

    @staticmethod
    def get_sub_breeds(breed) -> list:
        """Получает суб-породы по названию основной породы

        Args:
            breed (str): Название породы

        Raises:
            RuntimeError: _description_

        Returns:
            list: список подпород. Пустой если подпород нет
        """
        response = requests.get(
            f"{DogCeoApi.BASE_URL}/{breed}/list",
        )
        res = response.json()
        if not res["status"]:
            raise RuntimeError(f"Не удалось получить список пород '{breed}'")
        return res.get("message", [])

    @staticmethod
    def get_breed_images(breed, subbreeds, count=1) -> list:
        """Функция получает список URL картинок для породы

        Args:
            breed (str): Название породы
            subbreeds (list): Подпороды
            count (int, optional): Кол-во картинок для загрузки. По-умолчанию: 1.
        Returns:
            list: список url для загрузки
        """
        #  сначала запросим есть ли суб-породы
        breed_images = []

        if not subbreeds:
            breed_images += DogCeoApi.__get_image(breed, count)
        else:
            for subbreed in subbreeds:
                breed_images += DogCeoApi.__get_image(breed, count, subbreed)

        return breed_images

    @staticmethod
    def __get_image(breed, count, subbreed="") -> list:
        """Получает ссылку на картинку и формирует словарь
            с названием файла и url для скачивания

        Args:
            breed (str): Название породы
            count (int): Кол-во картинок для скачивания
            subbreed (str, optional): Название Подпороды. По-умолчанию: "".

        Raises:
            RuntimeError: Ошибка получения ссылки

        Returns:
            dict: Словарь с именем файла и URL
        """
        method = (
            f"{breed}/{subbreed}/images/random/{count}"
            if subbreed
            else f"{breed}/images/random/{count}"
        )
        response = requests.get(f"{DogCeoApi.BASE_URL}/{method}")
        res = response.json()

        if response.status_code == 404 and res["message"]:
            raise RuntimeError(f"Такой породы не существует")
        if response.status_code != 200:
            raise RuntimeError(
                f"Не удалось получить выполнить запрос на получение картинок. ({res.get("message","")})"
            )
        # сразу сформируем название файла, т.к. для под-породы оно другое
        breed_dict = []
        for url in res["message"]:
            img_file_name = Path(urlparse(url).path).name
            file_name = (
                f"{breed}_{subbreed}_{img_file_name}"
                if subbreed
                else f"{breed}_{img_file_name}"
            )
            breed_dict.append({"file_name": file_name, "url": url})
        return breed_dict
