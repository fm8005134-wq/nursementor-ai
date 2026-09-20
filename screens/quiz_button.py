from kivy.properties import NumericProperty
from kivymd.uix.button import MDRaisedButton


class OptionButton(MDRaisedButton):
    option_index = NumericProperty(-1)