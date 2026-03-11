from poligon_api import YaDiskApi
from dog_ceo_api import DogCeoApi
from progress.bar import Bar
import re
import json

try:
    breed = input("Введите названием породы на английском: ")
    if not re.match(r"^[A-Za-z]+$", breed):
        raise RuntimeError(f"название введено неверно")
    sub_breeds = DogCeoApi.get_sub_breeds(breed)
    if sub_breeds:
        print(f"Для данной породы найдено: {len(sub_breeds)} подпород.\n")
        inp_text = (
            "Введите количество загружаемых картинок для каждой подпороды"
            " от 1 до 5: (по-умолчанию: 1): "
        )
    else:
        inp_text = (
            "Введите количество загружаемых картинок от 1 до 5: (по-умолчанию: 1): "
        )
    count = input(inp_text) or 1

    if not re.match(r"^[1-5]?$", count):
        count = 1
        print("Количество введено неверно. Будет загружена 1 картинка")
    else:
        count = int(count)
    print("Поиск...")
    dog_images = DogCeoApi.get_breed_images(breed, sub_breeds, count)
    if not dog_images:
        raise RuntimeError(f"Не удалось загрузить картинки к породе {breed}")
    yd_token = input("Введите токен Полигона ЯД: ")

    print(f"Для данной породы будет загружено картинок: {len(dog_images)} шт.")
    yad_folder = breed
    yad_client = YaDiskApi(yd_token)
    yad_client.create_folder(yad_folder)
    bar = Bar("Загрузка", max=len(dog_images))
    uploaded_files = []
    for image in dog_images:
        disk_file_path = f'{yad_folder}/{image.get("file_name")}'
        yad_client.upload_file_by_url(image.get("url"), disk_file_path)
        # добавляем в список загруженных только те, что загрузились успешно
        uploaded_files.append(image.get("file_name"))
        bar.next()
    bar.finish()
    data = {
        "folder": breed,
        "total_uploaded": len(uploaded_files),
        "files": uploaded_files,
    }
    with open("result.json", "w") as f:
        json.dump(data, f)
    print(f"Результат загрузки сохранен в файл result.json")
except (RuntimeError, TypeError, ValueError) as err:
    print(f"Ошибка: {err}")
