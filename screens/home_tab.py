from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

from topics import TOPICS
from screens.topic_button import TopicButton


class HomeTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._build_topics, 0)

    def _build_topics(self, *_):
        container = self.ids.get("topics_box")
        if container is None:
            return
        container.clear_widgets()
        for name, info in TOPICS.items():
            btn = TopicButton(
                topic_name=name,
                topic_icon=info.get("icon", "medical-bag"),
                topic_desc=info.get("description", ""),
            )
            btn.bind(on_release=lambda inst, n=name: self.open_topic(n))
            container.add_widget(btn)

    def open_topic(self, topic_name):
        app = MDApp.get_running_app()
        app.root.go_to_topic(topic_name)

    def open_clinic_simulator(self):
        app = MDApp.get_running_app()
        app.root.current = "quiz"