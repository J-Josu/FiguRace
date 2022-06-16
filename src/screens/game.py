import time
from dataclasses import dataclass

import PySimpleGUI as sg

from src import constants, csg, translations
from src.controllers import theme, run_controller as run_ctr, users_controller as users_ctr
from src.handlers import observer


SCREEN_NAME = '-GAME-'
SELECT_OPTION = '-SELECT-OPTION-'
CONFIRM_SELECTED_OPTION = '-CONFIRM-SELECTED-OPTION-'
SKIP_CARD = '-SKIP-CARD-'
END_RUN = '-END-RUN-'
ROUNDS_TABLE_SIZE = 20
EVENT_LOOP_TIMEOUT = 100
RUN_UPDATE_TIME_SEC = 1


@dataclass
class CardSection:
    type: sg.Text
    data: list[str]
    hints: list[list[sg.Text]]
    options: list[sg.Button]
    confirm_button: sg.Button
    selected: int = -1


@dataclass
class RunSection:
    difficulty: sg.Text
    time: sg.Text
    user: sg.Text
    points: sg.Text
    rounds: sg.Multiline
    forced_end: bool = False


@dataclass
class TimeState:
    run_start: int = 0
    run_end: int = 0
    round_start: int = 0
    round_end: int = 0
    last: int = 0
    actual: int = 0
    round_duration: int = 0


time_state = TimeState()


def create_button(text: str, key: str) -> sg.Button:
    return sg.Button(
        text,
        key=key,
        font=(theme.FONT_FAMILY, theme.T1_SIZE),
        button_color=(
            theme.TEXT_BUTTON,
            theme.BG_BUTTON
        ),
        mouseover_colors=theme.BG_BUTTON_HOVER,
        border_width=theme.BD_SECONDARY,
    )


run_section = RunSection(
    sg.Text(
        translations.DIFFICULTY_TO_ES[users_ctr.current_user.preferred_difficulty],
        font=(theme.FONT_FAMILY, theme.H3_SIZE),
        background_color=theme.BG_SECONDARY
    ),
    sg.Text(
        f'00:00',
        font=(theme.FONT_FAMILY, theme.T1_SIZE),
        background_color=theme.BG_SECONDARY
    ),
    sg.Text(
        users_ctr.current_user.nick,
        font=(theme.FONT_FAMILY, theme.T1_SIZE),
        background_color=theme.BG_SECONDARY,
        size=24,
        justification='center'
    ),
    sg.Text(
        'puntos',
        font=(theme.FONT_FAMILY, theme.T1_SIZE),
        background_color=theme.BG_SECONDARY,
        size=24,
        justification='center'
    ),
    sg.Multiline(
        '\n'.join([f' {i+1:<2}. {"":>3}' for i in range(ROUNDS_TABLE_SIZE)]),
        font=(theme.FONT_FAMILY_TEXT, theme.T2_SIZE),
        text_color=theme.TEXT_PRIMARY,
        background_color=theme.BG_SECONDARY,
        size=(10, ROUNDS_TABLE_SIZE),
        no_scrollbar=True,
        rstrip=False,
        disabled=True,
        border_width=0
    )
)


def create_run_state() -> sg.Column:
    layout = [
        [csg.vertical_spacer(theme.scale(24), theme.BG_SECONDARY)],
        [run_section.difficulty],
        [run_section.time],
        [run_section.user],
        [run_section.points],
        [run_section.rounds],
        [csg.vertical_spacer(theme.scale(16), theme.BG_SECONDARY)],
    ]
    return sg.Column(
        layout,
        background_color=theme.BG_SECONDARY,
        element_justification='center'
    )


def refresh_timer() -> None:
    time_left = time_state.round_duration - \
        (time_state.actual - time_state.round_start)
    run_section.time.update(
        f'{time_left:<2}:00'
    )


def reset_run_state() -> None:
    run_section.difficulty.update(
        translations.DIFFICULTY_TO_ES[users_ctr.current_user.preferred_difficulty]
    )
    refresh_timer()
    run_section.user.update(users_ctr.current_user.nick)
    run_section.points.update(' 0 puntos')
    run_section.rounds.update(
        '\n'.join([f' {i+1:<2}. {"":>3}' for i in range(run_ctr.max_rounds)])
    )
    run_section.forced_end = False


def refresh_run_state() -> None:
    score = run_ctr.score
    run_section.points.update(f'{sum(score)} puntos')
    scores = [
        f' {i+1:<2}. {score[i] if i < len(score) else "":>3}'
        for i in range(run_ctr.max_rounds)
    ]
    run_section.rounds.update('\n'.join(scores))
    time_state.actual = int(time.time())
    time_state.round_end = time_state.actual
    time_state.round_start = time_state.actual
    refresh_timer()


def create_option_button(text: str, key: str) -> sg.Button:
    return sg.Button(
        text,
        key=key,
        font=(theme.FONT_FAMILY, theme.scale(20)),
        button_color=(theme.TEXT_BUTTON, theme.BG_BUTTON),
        mouseover_colors=theme.BG_BUTTON_HOVER,
        border_width=theme.BD_SECONDARY,
        disabled_button_color=(theme.TEXT_PRIMARY, theme.BG_ERROR_SOFT),
        expand_x=True
    )


card_section = CardSection(
    sg.Text(
        translations.DATASET_TO_ES[run_ctr.dataset_type],
        font=(theme.FONT_FAMILY, theme.H2_SIZE),
        text_color=theme.TEXT_ACCENT,
        background_color=theme.BG_BASE
    ),
    run_ctr.options,
    [
        [
            sg.Text(
                characteristic,
                font=(theme.FONT_FAMILY, theme.T1_SIZE),
                text_color=theme.TEXT_PRIMARY,
                background_color=theme.BG_BASE
            ),
            sg.Text(
                'no loaded',
                font=(theme.FONT_FAMILY, theme.T1_SIZE),
                text_color=theme.TEXT_PRIMARY,
                background_color=theme.BG_BASE
            ),
        ] for characteristic in run_ctr.hints_types
    ],
    [
        create_option_button(
            f'{text.capitalize()}',
            f'{SELECT_OPTION} {i}'
        ) for i, text in enumerate(run_ctr.options)
    ],
    create_button(
        'Confirmar', f'{CONFIRM_SELECTED_OPTION}')
)


def create_card() -> sg.Column:
    
    layout = [
        [card_section.type],
        *[hint for hint in card_section.hints],
        *[[button] for button in card_section.options],
        [csg.vertical_spacer(theme.scale(16), background_color=theme.BG_BASE)],
        [
            card_section.confirm_button,
            sg.Push(theme.BG_BASE),
            create_button('Pasar', f'{SKIP_CARD}')
        ]
    ]
    return sg.Column(
        layout,
        background_color=theme.BG_BASE
    )


def refresh_card() -> None:
    hints = run_ctr.hints
    for i, row in enumerate(card_section.hints):
        if i < len(hints):
            row[1].update(hints[i])
        else:
            row[1].update('')


run_ctr.registry_event('bad_option', refresh_card)


def current_answer(index: str) -> None:
    if card_section.selected >= 0:
        card_section.options[card_section.selected].update(
            button_color=(theme.TEXT_BUTTON, theme.BG_BUTTON)
        )
    card_section.selected = int(index)
    card_section.options[card_section.selected].update(
        button_color=(theme.TEXT_BUTTON, theme.BG_SECONDARY)
    )
    card_section.confirm_button.update(
        disabled=False, button_color=(theme.TEXT_BUTTON, theme.BG_BUTTON)
    )


observer.subscribe(SELECT_OPTION, current_answer)


def new_answer() -> None:
    card_section.confirm_button.update(disabled=True, button_color=(
        theme.TEXT_BUTTON_DISABLED, theme.BG_BUTTON_DISABLED)
    )
    card_section.options[card_section.selected].update(
        disabled=True, button_color=(theme.TEXT_PRIMARY, theme.BG_ERROR_SOFT)
    )
    run_ctr.new_answer(card_section.data[card_section.selected])
    card_section.selected = -1


observer.subscribe(CONFIRM_SELECTED_OPTION, new_answer)


def reset_card() -> None:
    card_section.type.update(translations.DATASET_TO_ES[run_ctr.dataset_type])
    card_section.data = run_ctr.options
    if run_ctr.dataset_type in translations.DATASET_HEADER:
        characteristics = translations.DATASET_HEADER[run_ctr.dataset_type]
    else:
        characteristics = run_ctr.hints_types
    hints = run_ctr.hints

    for i, row in enumerate(card_section.hints):
        row[0].update(f'{characteristics[i]}: ')
        if i < len(hints):
            row[1].update(hints[i])
        else:
            row[1].update('')

    for option, content in zip(card_section.options, card_section.data):
        option.update(content, disabled=False, button_color=(
            theme.TEXT_BUTTON, theme.BG_BUTTON))

    card_section.selected = -1
    card_section.confirm_button.update(disabled=True, button_color=(
        theme.TEXT_BUTTON_DISABLED, theme.BG_BUTTON_DISABLED)
    )


def end_round() -> None:
    refresh_run_state()
    reset_card()


run_ctr.registry_event('win_round', end_round)
run_ctr.registry_event('loose_round', end_round)


def create_leave_button() -> sg.Button:
    return sg.Button(
        'Abandonar partida',
        key=f'{END_RUN}',
        font=(theme.FONT_FAMILY, theme.T1_SIZE),
        button_color=(theme.TEXT_BUTTON, theme.BG_BUTTON),
        mouseover_colors=theme.BG_BUTTON_HOVER,
        border_width=theme.BD_PRIMARY,
        pad=(0, 0)
    )


def finish_game() -> None:
    total_score = sum(run_ctr.score)
    if not run_section.forced_end:
        users_ctr.current_user.update_score(
            users_ctr.current_user.preferred_difficulty, total_score
        )
    time_state.run_end = time_state.actual
    stats = run_ctr.stats
    stats['total_time'] = time_state.run_end - time_state.run_start
    stats['average_time'] = stats['total_time'] // stats['rounds_completed'] if stats['rounds_completed'] else stats['total_time']
    observer.post_event(constants.RUN_RESULT, stats)
    observer.post_event(constants.GOTO_VIEW, '-RESULT-')


run_ctr.registry_event('end_run', finish_game)


def force_end_round() -> None:
    run_ctr.end_round()
    end_round()


observer.subscribe(SKIP_CARD, force_end_round)


def force_end_game() -> None:
    run_section.forced_end = True
    run_ctr.end_run()


observer.subscribe(END_RUN, force_end_game)


def reset_time() -> None:
    time_stamp = int(time.time())
    time_state.run_start = time_stamp
    time_state.round_start = time_stamp
    time_state.last = time_stamp
    time_state.actual = time_stamp
    time_state.round_duration = run_ctr.round_time
    refresh_timer()


def update_time() -> None:
    time_state.actual = int(time.time())
    delta_time = time_state.actual - time_state.last
    if delta_time < RUN_UPDATE_TIME_SEC:
        return
    refresh_timer()
    time_state.last = time_state.actual
    if (time_state.actual - time_state.round_start) < time_state.round_duration:
        return
    time_state.round_end = time_state.actual
    force_end_round()


screen_layout = [
    [sg.VPush(theme.BG_BASE)],
    [
        csg.CenteredElement(
            create_run_state(),
            background_color=theme.BG_BASE
        ),
        create_card(),
        sg.Push(theme.BG_BASE)
    ],
    [create_leave_button()],
    [sg.VPush(theme.BG_BASE)]
]

screen_config = {
    'background_color': theme.BG_BASE,
    'element_justification': 'center',
}


def screen_reset() -> None:
    run_ctr.reset()
    reset_run_state()
    reset_card()
    reset_time()
    observer.subscribe(constants.TIMEOUT, update_time)
    observer.post_event(constants.UPDATE_TIMEOUT, EVENT_LOOP_TIMEOUT)
