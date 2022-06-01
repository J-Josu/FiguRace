from typing import Any, Callable, TypedDict

import PySimpleGUI as sg

from src import csg, common
from src.controllers import theme, users_controller as users_ctr
from src.handlers import observer
from src.handlers.screen import Screen


SCREEN_NAME = '-CREATE-PROFILE-'
LOAD_USER_FIELD = '-LOAD-USER-FIELD-'
EVENT_ADD_PROFILE = '-ADD-PROFILE-'


class FormInput(TypedDict):
    input: sg.Input
    state: bool
    validate_fn: Callable[[sg.Input], bool]


def create_input(key: str) -> sg.Input:
    return sg.Input(
        size=(20, 1),
        background_color=theme.BG_BASE,
        font=(theme.FONT_FAMILY, theme.H3_SIZE),
        text_color=theme.TEXT_ACCENT,
        border_width=theme.BD_SECONDARY,
        key=f'{LOAD_USER_FIELD} {key}',
        enable_events=True
    )


def validate_nick(input: sg.Input) -> bool:
    nick = input.get()
    if nick == '' or nick in users_ctr.users_transform(lambda user: user.nick):
        input.update(background_color=theme.BG_ERROR_NORMAL)
        return False
    input.update(background_color=theme.BG_BASE)
    return True


def validate_age(input: sg.Input) -> bool:
    age = input.get()
    try:
        age = int(age)
        if age <= 0 or age > 100:
            raise ValueError
    except ValueError:
        input.update(background_color=theme.BG_ERROR_NORMAL)
        return False
    input.update(background_color=theme.BG_BASE)
    return True


def validate_gender(input: sg.Input) -> bool:
    gender = input.get()
    if gender == '':
        input.update(background_color=theme.BG_ERROR_NORMAL)
        return False
    input.update(background_color=theme.BG_BASE)
    return True


FIELDS_LIST = [
    ('nick', validate_nick),
    ('age', validate_age),
    ('gender', validate_gender),
]

inputs: dict[str, FormInput] = {}

for type, validation_fn in FIELDS_LIST:
    inputs[type] = {
        'input': create_input(type),
        'state': False,
        'validate_fn': validation_fn
    }

create_button = sg.Button(
    'Crear',
    button_color=(theme.TEXT_BUTTON, theme.BG_BUTTON),
    mouseover_colors=theme.BG_BUTTON_HOVER,
    font=(theme.FONT_FAMILY, theme.H4_SIZE),
    pad=theme.scale(32),
    disabled=True,
    key=EVENT_ADD_PROFILE,
    border_width=theme.BD_ACCENT
)


def disable_create_button() -> None:
    create_button.update(
        disabled=True,
        button_color=(theme.TEXT_BUTTON_DISABLED, theme.BG_BUTTON_DISABLED)
    )


def enable_create_button() -> None:
    create_button.update(
        disabled=False,
        button_color=(theme.TEXT_BUTTON, theme.BG_BUTTON)
    )


def create_field(name: str, input: sg.Input) -> tuple[sg.Text, sg.Input]:
    return (
        sg.Text(
            name,
            size=(6, 1),
            background_color=theme.BG_BASE,
            font=(theme.FONT_FAMILY, theme.H3_SIZE),
            pad=theme.scale(25)
        ),
        input
    )


def create_formulary() -> sg.Column:
    layout = [
        [*create_field('Nick', inputs['nick']['input'])],
        [*create_field('Edad', inputs['age']['input'])],
        [*create_field('Genero', inputs['gender']['input'])],
        [
            sg.Push(theme.BG_BASE),
            create_button,
            sg.Push(theme.BG_BASE)
        ]
    ]

    return csg.CenteredLayout(
        layout,
        background_color=theme.BG_BASE
    )


def reset_formulary() -> None:
    for value in inputs.values():
        value['input'].update('', background_color=theme.BG_BASE)
        value['state'] = False
    disable_create_button()


def validate_inputs(key: str):
    inputs[key]['state'] = inputs[key]['validate_fn'](inputs[key]['input'])

    for _, valid, _ in inputs.values():
        if not valid:
            disable_create_button()
            break
    else:
        enable_create_button()


observer.subscribe(LOAD_USER_FIELD, validate_inputs)


def create_new_user_message(nick: str) -> list[list[Any]]:
    return [
        [sg.Text(
            f'Perfil {nick}\ncreado exitosamente',
            font=(theme.FONT_FAMILY, theme.T1_SIZE),
            text_color=theme.TEXT_ACCENT,
            background_color=theme.BG_SECONDARY,
            pad=(theme.scale(32),)*2,
            justification='center'
        )],
    ]


def create_user():
    nick: str = inputs['nick']['input'].get()
    users_ctr.add(
        nick,
        int(inputs['age']['input'].get()),
        inputs['gender']['input'].get()
    )
    reset_formulary()
    csg.custom_popup(
        create_new_user_message(nick),
        [],
        background_color=theme.BG_SECONDARY,
        duration=2
    )


observer.subscribe(EVENT_ADD_PROFILE, create_user)


screen_layout = [
    [common.screen_title('crear perfil', True)],
    [create_formulary()],
    [common.goback_button('Menu Selección', padding=(theme.scale(64),)*2)],
]

screen_config = {
    'background_color': theme.BG_BASE,
}


def reset() -> None:
    reset_formulary()


screen = Screen(
    SCREEN_NAME,
    screen_layout,
    screen_config,
    reset
)
