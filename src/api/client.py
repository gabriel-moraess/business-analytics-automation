import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src.utils.logger import logger


class APIClient:
    """
    Cliente para consumir APIs REST.
    """

    def __init__(self, base_url: str, token: str = None):

        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        retry = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.headers = {
            "Content-Type": "application/json"
        }

        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get(self, endpoint, params=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info(f"GET -> {url}")

        response = self.session.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()