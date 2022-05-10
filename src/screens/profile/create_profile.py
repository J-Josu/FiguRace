from tkinter import font
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import T

NAME = 'CREATE PROFILE'
BACK_GROUND_COLOR = '#112B3C'
BUTTON_COLOR = '#4BD9F2'
TEXT_BUTTON_COLOR = '#243F50'

def _title (name):
    return sg.Text(name,size=500,background_color= BACK_GROUND_COLOR, font=('Aquarius',60),pad= 0, text_color='#2D8BC5')

def _features():
    layout= [[sg.Text('Nick',size= (4,1),background_color= '#112B3C',font=('System',40),pad=(5,50)),
            sg.Input(size= (40,15),do_not_clear=False,background_color= BACK_GROUND_COLOR,font=('Sytem',30),text_color='white')],
            [sg.Text('Age',size= (4,1),background_color= BACK_GROUND_COLOR,font=('System',40),pad=(5,50)),
            sg.Input(size= (40,10),do_not_clear=False,background_color= BACK_GROUND_COLOR,font=('Sytem',30),text_color='white')],
            [sg.Text('Gender',size= (7,1),background_color= BACK_GROUND_COLOR,font=('System',40),pad=(5,50)),
            sg.Combo(('Female','Male','Undefined','Other'),'Female', background_color='#8DC3E4', font=('System',30),readonly=True,text_color=BACK_GROUND_COLOR)],
            [sg.VPush(background_color= BACK_GROUND_COLOR)],
            ]           
    return layout

def button():
    layout= [[sg.Button('Save',border_width=15,size=(15,1),button_color= (TEXT_BUTTON_COLOR,BUTTON_COLOR),mouseover_colors=BACK_GROUND_COLOR,font=('System',20),pad=(200,5)),
            sg.Push(background_color= BACK_GROUND_COLOR),
            sg.Button('Cancel',border_width=15,size=(15,1),button_color= (TEXT_BUTTON_COLOR,BUTTON_COLOR),mouseover_colors=BACK_GROUND_COLOR,font=('System',20),pad=(10,5))]
            ]
    return layout

layout= [[_title(NAME)],
        [sg.Column(_features(),background_color=BACK_GROUND_COLOR,expand_y=True)],
        [button()]
        ]

window = sg.Window('Figurace - ' + NAME, layout,background_color=BACK_GROUND_COLOR,resizable=True).finalize()

window.Maximize()

while True:
    events,values = window.read()
    if events in ('Cancel'):
        # TODO go to profile page
        print ('Cacel program...')
        break
    if events == sg.WIN_CLOSED:
        break
window.close()