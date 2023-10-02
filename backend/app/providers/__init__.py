import importlib
import pathlib
import pkgutil
from collections import OrderedDict

from app.providers.base import BaseProvider


class ProviderRegistry(object):
    def __init__(self):
        self.provider_map: dict[str, BaseProvider] = OrderedDict()
        self.loaded = False

    def register(self, cls):
        self.provider_map[cls.id] = cls

    def as_choices(self):
        self.load()
        for provider_cls in self.provider_map.values():
            yield (provider_cls.id, provider_cls.name)

    def get_provider_ids(self):
        self.load()
        return self.provider_map.keys()

    def token_types_as_choices(self):
        self.load()
        for provider_cls in self.provider_map.values():
            for token_type in provider_cls.token_types:
                yield token_type

    def get_provider(self, provider_id: str) -> BaseProvider:
        return self.provider_map[provider_id]

    def load(self):
        # https://stackoverflow.com/questions/3430372/how-do-i-get-the-full-path-of-the-current-files-directory
        pkgpath = str(pathlib.Path(__file__).parent.resolve())

        # https://stackoverflow.com/questions/487971/is-there-a-standard-way-to-list-names-of-python-modules-in-a-package
        for _, name, _ in pkgutil.iter_modules([pkgpath]):
            provider_module = importlib.import_module(f"app.providers.{name}")

            for attr in dir(provider_module):
                obj = getattr(provider_module, attr)
                if getattr(obj, 'is_provider_cls'):
                    self.register(obj)
