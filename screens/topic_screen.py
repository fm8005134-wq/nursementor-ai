from kivymd.uix.screen import MDScreen

from topics import TOPICS
from screens.topic_card import TopicCard


class TopicScreen(MDScreen):
    def load_topic(self, topic_name):
        info = TOPICS.get(topic_name, {})
        self.ids.toolbar.title = topic_name

        container = self.ids.cards_box
        container.clear_widgets()

        for title, body in info.get("sections", []):
            card = TopicCard(card_title=title, card_body=body)
            container.add_widget(card)

    def go_back(self):
        self.manager.go_home()