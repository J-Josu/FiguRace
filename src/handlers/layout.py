from typing import Callable
import PySimpleGUI as sg

from src.PyCustomGUI.missing_typings import ElementLayout

GOTO_VIEW = '-GOTO-VIEW-'

class Screen:
    def __init__(self, key: str, layout: ElementLayout, reset: Callable[..., None]):
        self.key = key
        self.is_visible = False
        self.container = sg.Column(layout, key=key, visible=False)
        self._reset = reset
    
    def turn_visivility(self) -> None:
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.reset()
        self.container.update(visible= self.is_visible)
    
    def reset(self) -> None:
        self._reset(None)

class WindowLayoutController:

    def __init__(self):
        self.actual_layout: str = ''
        self.layout_stack: list[str] = []
        self.layouts: dict[str, Screen] = {}
        self.composed_layout: list[sg.Element] = []

    def goto_layout(self, key: str) -> None:
        key = key.lstrip('0123456789')
        self.layouts[self.actual_layout].turn_visivility()
        if key in self.layout_stack:
            self.actual_layout = self.layout_stack.pop()
        else:
            self.layout_stack.append(self.actual_layout)
            self.actual_layout = key

        self.layouts[self.actual_layout].turn_visivility()

    def register(self, screen: Screen) -> None:
        if screen.key in self.layouts:
            raise Exception(f'Already registered a layout with key {screen.key}')
        self.layouts[screen.key] = screen
        self.composed_layout.append(screen.container)

    def get_composed_layout(self) -> ElementLayout:
        return [self.composed_layout]
    
    def init(self, key:str)-> None:
        if key not in self.layouts:
            raise Exception(f'{key} isnt a registered at composed layouts')
        self.actual_layout = key
        self.layouts[key].turn_visivility()
