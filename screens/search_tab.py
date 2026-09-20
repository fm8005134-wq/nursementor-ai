from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from topics import TOPICS
from screens.topic_button import TopicButton


class SearchTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._show_all, 0)

    def _show_all(self, *_):
        self._render_results(list(TOPICS.keys()))

    def on_search_text(self, text):
        text = (text or "").strip().lower()
        if not text:
            self._render_results(list(TOPICS.keys()))
            return

        results = []
        for name, info in TOPICS.items():
            haystack = name.lower() + " " + info.get("description", "").lower()
            for title, body in info.get("sections", []):
                haystack += " " + title.lower() + " " + body.lower()
            if text in haystack:
                results.append(name)
        self._render_results(results)

    def _render_results(self, names):
        container = self.ids.get("results_box")
        if container is None:
            return
        container.clear_widgets()

        if not names:
            container.add_widget(MDLabel(
                text="No matching topics found.",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height="60dp",
            ))
            return

        for name in names:
            info = TOPICS[name]
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