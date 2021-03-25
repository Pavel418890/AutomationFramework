from typing import Any


class Singleton(type):
    instances = {}

    def __call__(cls: type, *args: Any, **kwargs: Any) -> object:
        existing_instance = Singleton.instances.get(cls)
        if existing_instance is None:
            existing_instance = super().__call__(*args, **kwargs)
            Singleton.instances[cls] = existing_instance

        return existing_instance


