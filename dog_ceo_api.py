import requests


class DogCeoApi:
    BASE_URL = "https://dog.ceo/api/breed"

    def get_sub_breeds(self, breed):
        response = requests.get(
            f"{self.BASE_URL}/{breed}/list",
            headers=self.headers,
            params={"path": path},
        )
        res = response.json()
        if not res["status"] or (res["status"] != "success") or not res["message"]:
            raise RuntimeError(f"Не удалось получить список пород {breed}")
        return [] if not res["message"] else res["message"]

    def get_breed_images(self, breed):
        subbreeds = self.get_sub_breeds(breed)
        if not subbreeds:
            method = f"{self.BASE_URL}/breed/images/random"
        else:
            method = f"{self.BASE_URL}/breed/images/random"

        response = requests.get(
            f"{self.BASE_URL}/v1/disk/resources/upload",
            params={"path": disk_path},
            headers=self.headers,
        )

        upload_link = response.json()["href"]

        with open(local_path, "rb") as file:
            response = requests.put(upload_link, files={"file": file})
        if response.status_code == 201:
            print(f"Файл {disk_path} успешно загружен")
        else:
            print(f"Файл {disk_path} не загружен")
