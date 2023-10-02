from abc import ABC, abstractmethod
from typing import TypedDict
from django.conf import settings as django_settings


class SocialAuthUser(TypedDict):
    """User info dictionary."""
    display_name: str


def social_provider(cls):
    cls.is_registered = True
    return cls


class BaseProvider(ABC):
    """Base Social OAuth2 Provider Class."""

    id = None
    name = None

    def __init__(self):
        settings = django_settings.SOCIAL_MEDIA_SETTINGS

        self.access_token = None

        self.APP_ID = settings[self.id].get("app_id")
        self.APP_SECRET = settings[self.id].get("app_secret")
        self.CALLBACK_URL = settings[self.id].get("callback_url")

    @abstractmethod
    def get_token(self, code: str):
        """Get access token from authentication code."""
        raise NotImplementedError

    @abstractmethod
    def get_user_info(self) -> SocialAuthUser:
        raise NotImplementedError

    @abstractmethod
    def get_oauth2_url(self) -> str:
        raise NotImplementedError
