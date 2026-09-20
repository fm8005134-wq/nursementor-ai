from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


class TopicButton(MDCard):
    topic_name = StringProperty("")
    topic_icon = StringProperty("medical-bag")
    topic_desc = StringProperty("")