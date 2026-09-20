from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


class TopicCard(MDCard):
    card_title = StringProperty("")
    card_body = StringProperty("")