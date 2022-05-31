"""Wrappers of sg elements
    Collection of wrapper classes/functions around sg elements to add facility when creating layouts
"""
from abc import ABC, abstractmethod
from typing import Any

import PySimpleGUI as sg

from src import constants


Element = Any
LayoutRow = list[Element]
FullLayout = list[LayoutRow]


class ChainedElement(ABC):
    """Wrapper to manage elements that will later be packaged depend on the type of list
    """
    @abstractmethod
    def __init__(self, **column_parameters: Any):
        ...

    @abstractmethod
    def add(self, content: Element | LayoutRow | FullLayout) -> Any:
        ...

    @abstractmethod
    def pack(self) -> sg.Column:
        ...


class HorizontalList(ChainedElement):
    """Horizontal list that extends from ChainedElement: class to manage the elements.
    """

    def __init__(self, **column_parameters: Any):
        """Initializes the attributes _container and _config
        Args:
            column_parameters: all the column parameter that will be applied as a configuration.
        """
        self._container: list[Element] = []
        self._config = column_parameters

    def add(self, content: Element | LayoutRow | FullLayout) -> 'HorizontalList':
        """Add to the list matching if is a element of a layout
        Args: 
            content: receive the content to add to the list.
        Returns: 
            the current information of the class after add the element pass by argument.
        """
        match content:
            case [[*_], *_]:
                element = sg.Column(content, **self._config)
            case [*_]:
                element = sg.Column([content], **self._config)
            case _:
                element = content
        self._container.append(element)
        return self

    def pack(self) -> sg.Column:
        """Packs the list item into a column.
        """
        return sg.Column([self._container], **self._config)


class VerticalList(ChainedElement):
    """
         Vertical list that extends from ChainedElement: class to manage the elements.
    """

    def __init__(self, **column_parameters: Any):
        """Initializes the attributes _container and _config
        Args:
            column_parameters: all the column parameter that will be applied as a configuration.
        """
        self._container: FullLayout = []
        self._config = column_parameters

    def add(self, content: Element | LayoutRow | FullLayout) -> 'VerticalList':
        """Add to the list matching if is a element of a layout
        Args: 
            content: receive the content to add to the list.
        Returns: 
            the current information of the class after add the element pass by argument.
        """
        match content:
            case [[*_], *_]:
                element = [sg.Column(content, **self._config)]
            case [*_]:
                element = content
            case _:
                element = [content]
        self._container.append(element)
        return self

    def pack(self) -> sg.Column:
        """Packs the list item into a column.
        """
        return sg.Column(self._container, **self._config)


def CenteredElement(element: Element, horizontal_only: bool = False, **column_parameters: Any) -> sg.Column:
    """ Create a column with elements at the center.
    Args:
        element: element to add to the column.
        horizontal_only: default : false.
        column_parameters: all the column parameter that will be applied as a configuration.
    Returns:
        A center column with all the configuration passed by args with the theme applied.
    """
    column_parameters['element_justification'] = 'center'
    column_parameters['expand_y'] = not horizontal_only
    column_parameters['expand_x'] = True
    background_color = column_parameters.get('background_color', None)
    if horizontal_only:
        return sg.Column(
            [
                [element]
            ],
            **column_parameters
        )
    return sg.Column(
        [
            [sg.VPush(background_color)],
            [element],
            [sg.VPush(background_color)]
        ],
        **column_parameters
    )


def CenteredLayout(layout: FullLayout, horizontal_only: bool = False, **column_parameters: Any) -> sg.Column:
    """ Create a centered layout.
    Args:
        layout: receive list of element to be put on the screen.
        horizontal_only: default : false.
        column_parameters: all the column parameter that will be applied as a configuration.
    Returns: 
        A center layout with all the configuration passed by args with the theme applied.
    """
    column_parameters['element_justification'] = 'center'
    column_parameters['expand_y'] = not horizontal_only
    column_parameters['expand_x'] = True
    background_color = column_parameters.get('background_color', None)
    if horizontal_only:
        return sg.Column(
            layout,
            **column_parameters
        )
    return sg.Column(
        [
            [sg.VPush(background_color)],
            *layout,
            [sg.VPush(background_color)]
        ],
        **column_parameters
    )


def horizontal_spacer(width: int, background_color: str | None = None) -> sg.Column:
    return sg.Column([[]], size=(width, 0), background_color=background_color)


def vertical_spacer(height: int, background_color: str | None = None) -> sg.Column:
    return sg.Column([[]], size=(0, height), background_color=background_color)


def custom_popup(layout: FullLayout, close_keys: list[str], background_color: str | None = None, duration: int | None = None) -> str:
    """Generates a custom pop up window
    Args:
         layout: layout that will display the popup
         close_keys: list of keys to refer the elements
         background_color: default : None
         duration: duration in seconds to close the pop up. default: none(permanently until close it).
    Returns: 
        A pop up with the theme applied and a timer for close it if is specified.
    """
    window = sg.Window(
        '', layout, background_color=background_color,
        no_titlebar=True, keep_on_top=True, finalize=True,
        margins=(0, 0), resizable=False, modal=True
    )

    timeout = duration * 1000 if duration else None

    while True:
        event, _ = window.read(timeout=timeout, timeout_key='-TIME-OUT-')
        if event is None or event == '-TIME-OUT-':
            event = constants.EXIT_APLICATION
            break
        if event in close_keys:
            break

    window.close()
    return event
