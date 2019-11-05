import codecs
import json
from errno import ENOENT
from typing import Any, Callable, Optional

import six


class Persistence(object):
    def __init__(self, data: Optional[dict] = None) -> None:
        self._data = data

    @property
    def data(self) -> dict:
        if self._data is None:
            self._data = {}
        return self._data

    def update(self, data: Optional[dict] = None, **kwargs) -> None:
        self.data.update((data or {}), **kwargs)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def save(self) -> None:
        pass


class FilePersistence(Persistence):
    def __init__(self, get_filename: Callable) -> None:
        super(FilePersistence, self).__init__()
        self.get_filename = get_filename

    @property
    def data(self) -> dict:
        if self._data is None:
            self._load()
        return self._data

    def _load(self) -> None:
        filename = self.get_filename()
        try:
            with codecs.open(filename, 'r', encoding='UTF-8') as infp:
                self._data = json.load(infp)
        except EnvironmentError as ee:
            if ee.errno != ENOENT:
                raise
            self._data = {}
        except Exception as exc:  # pragma: no cover
            six.raise_from(RuntimeError('could not read configuration file %s' % filename), exc)

    def save(self) -> None:
        filename = self.get_filename()
        with codecs.open(filename, 'w', encoding='UTF-8') as outfp:
            json.dump(self.data, outfp, ensure_ascii=False, indent=2, sort_keys=True)
