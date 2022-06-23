from copy import copy
from dataclasses import dataclass
from typing import Any

from .. import constants, default
from . import observer, file


@dataclass
class Settings:
    title: str
    full_screen: bool
    starting_page: str
    theme: str
    default_user: str


class SettingsController:
    def __init__(self, settings_path: str) -> None:
        self._file_path = settings_path
        raw_settings: dict[str, Any] = file.load_json(
            settings_path, default.SETTINGS
        )
        self._settings = {
            name: Settings(**definition) for name, definition in raw_settings.items()
        }
        if 'custom' not in self._settings:
            self._settings['custom'] = copy(self._settings['default'])
        self._setting = self._settings['custom']
        self._reset_starting_page = self._setting.starting_page != self._settings[
            'default'].starting_page
        observer.subscribe(constants.USER_CHANGE, self._set_default_user)

    @property
    def settings(self) -> Settings:
        return self._setting

    def _set_default_user(self, user: Any) -> None:
        self._setting.default_user = user.nick

    def set_starting_page(self, screen_name: str) -> None:
        self._setting.starting_page = screen_name
        self._reset_starting_page = False

    def save(self) -> None:
        if self._reset_starting_page:
            self._setting.starting_page = self._settings['default'].starting_page
        file.save_json(
            self._file_path,
            self._settings,
            is_custom_class=True
        )
