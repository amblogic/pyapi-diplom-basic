from poligon_api import YaDiskApi
from dog_ceo_api import DogCeoApi
from progress.bar import Bar
from settings import yd_token
import pprint

try:
    # breed = input("Введите названием породы на английском: ")
    count = input("Введите количество загружаемых картинок: (по-умолчанию: 1): ") or 1
    breed = "bulldog"
    dog_api = DogCeoApi()
    dog_images = dog_api.get_breed_images(breed, count)
    if not dog_images:
        raise RuntimeError(f"Не удалось загрузить картинки к породе {breed}")
    # token = input("Введите токен Полигона ЯД: ")

    print(f"Для данной породы будет загружено картинок: {len(dog_images)} шт.")
    yad_folder = breed
    yad_client = YaDiskApi(yd_token)
    yad_client.create_folder(yad_folder)
    bar = Bar("Загрузка", max=len(dog_images))
    for image in dog_images:
        disk_file_path = f'{yad_folder}/{image.get("file_name")}'
        yad_client.upload_file_by_url(image.get("url"), disk_file_path)
        bar.next()
    bar.finish()
except (RuntimeError, TypeError) as err:
    print(f"Ошибка: {err}")
