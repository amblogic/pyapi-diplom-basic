from poligon_api import YaDiskApi
from dog_ceo_api import DogCeoApi
from pathlib import Path
import os
import sys
from pprint import pprint
from settings import yd_token

folder_path = input("Введите названием породы на английском: ")
local_path = Path(folder_path)
disk_folder = f"бэкап_{local_path.name}"

if not local_path.exists() or not local_path.is_dir():
    print("Указан неверный путь")
    sys.exit(1)

yad_client = YaDiskApi(yd_token)
yad_client.create_folder(disk_folder)
