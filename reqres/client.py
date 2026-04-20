import requests
from typing import Union

class ReqResClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({"x-api-key": api_key})

    def login(self, email: str, password: str) -> requests.Response:
        data = {"email": email, "password": password}
        return self.session.post(f"{self.base_url}/login", json=data)

    def get_users(self, page: int = 1, per_page: int = None) -> requests.Response:
        params = {"page": page}
        if per_page:
            params["per_page"] = per_page
        return self.session.get(f"{self.base_url}/users", params=params)

    def get_user(self, user_id: Union[int, str]) -> requests.Response:
        return self.session.get(f"{self.base_url}/users/{user_id}")

    def create_user(self, name: str, job: str) -> requests.Response:
        data = {"name": name, "job": job}
        return self.session.post(f"{self.base_url}/users", json=data)

    def delete_user(self, user_id: Union[int, str]) -> requests.Response:
        return self.session.delete(f"{self.base_url}/users/{user_id}")
