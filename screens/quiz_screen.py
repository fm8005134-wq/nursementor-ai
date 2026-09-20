import random

from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from scenarios import SCENARIOS


class QuizScreen(MDScreen):
    def on_enter(self, *args):
        self._questions = []
        self._index = 0
        self._score = 0
        self._answered = False
        self._build_questions()
        Clock.schedule_once(self._load_question, 0.05)

    # ------------------------------------------------------------------
    def _build_questions(self):
        pool = list(SCENARIOS)
        random.shuffle(pool)
        self._questions = pool[:10]

    def go_back(self):
        self.manager.go_home()

    # ------------------------------------------------------------------
    def _load_question(self, *_):
        self._answered = False
        q = self._questions[self._index]

        self.ids.progress_label.text = (
            "Question {} of {}".format(self._index + 1, len(self._questions))
        )
        self.ids.score_label.text = "Score: {}".format(self._score)
        self.ids.topic_chip.text = q["topic"]
        self.ids.question_label.text = q["question"]

        self.ids.explanation_card.opacity = 0
        self.ids.explanation_card.height = 0
        self.ids.next_button.opacity = 0
        self.ids.next_button.disabled = True

        options_box = self.ids.options_box
        options_box.clear_widgets()

        for i, opt in enumerate(q["options"]):
            btn = MDRaisedButton(
                text=opt,
                size_hint_x=1,
                size_hint_y=None,
                height="52dp",
                font_size="15sp",
            )
            btn.bind(on_release=lambda inst, idx=i: self._on_answer(idx))
            options_box.add_widget(btn)

    # ------------------------------------------------------------------
    def _on_answer(self, chosen_index):
        if self._answered:
            return
        self._answered = True

        q = self._questions[self._index]
        correct = q["correct"]
        options_box = self.ids.options_box

        for child in options_box.children:
            child.disabled = True

        buttons_in_order = list(reversed(options_box.children))

        buttons_in_order[correct].md_bg_color = (0.30, 0.69, 0.31, 1)
        if chosen_index != correct:
            buttons_in_order[chosen_index].md_bg_color = (0.90, 0.22, 0.21, 1)
        else:
            self._score += 1
            self.ids.score_label.text = "Score: {}".format(self._score)

        self.ids.explanation_label.text = q["explanation"]
        self.ids.explanation_title.text = (
            "Correct!" if chosen_index == correct else "Not quite"
        )
        Clock.schedule_once(self._reveal_explanation, 0.1)

    def _reveal_explanation(self, *_):
        self.ids.explanation_card.height = "200dp"
        anim = Animation(opacity=1, duration=0.25)
        anim.start(self.ids.explanation_card)

        self.ids.next_button.disabled = False
        next_anim = Animation(opacity=1, duration=0.25)
        next_anim.start(self.ids.next_button)

    # ------------------------------------------------------------------
    def on_next_pressed(self):
        self._index += 1
        if self._index >= len(self._questions):
            self._show_result()
        else:
            self._load_question()

    # ------------------------------------------------------------------
    def _show_result(self):
        total = len(self._questions)
        score = self._score
        percent = int(round((score / float(total)) * 100))

        if percent >= 90:
            grade = "Excellent"
            color = (0.30, 0.69, 0.31, 1)
        elif percent >= 70:
            grade = "Good"
            color = (0.13, 0.59, 0.95, 1)
        elif percent >= 50:
            grade = "Pass"
            color = (1.0, 0.76, 0.03, 1)
        else:
            grade = "Needs Practice"
            color = (0.90, 0.22, 0.21, 1)

        self.ids.options_box.clear_widgets()
        self.ids.question_label.text = ""
        self.ids.topic_chip.text = "Result"
        self.ids.progress_label.text = "Simulator complete"
        self.ids.score_label.text = ""

        self.ids.explanation_card.height = 0
        self.ids.explanation_card.opacity = 0
        self.ids.next_button.opacity = 0
        self.ids.next_button.disabled = True

        card = MDCard(
            orientation="vertical",
            padding="20dp",
            spacing="14dp",
            radius=[14],
            elevation=3,
            size_hint_y=None,
            height="340dp",
        )

        title = MDLabel(
            text="Your Result",
            bold=True,
            font_style="H5",
            halign="center",
            size_hint_y=None,
            height="40dp",
        )
        title.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        big_score = MDLabel(
            text="{}/{}".format(score, total),
            bold=True,
            font_style="H2",
            halign="center",
            theme_text_color="Custom",
            text_color=color,
            size_hint_y=None,
            height="70dp",
        )
        big_score.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        pct = MDLabel(
            text="{}%  -  {}".format(percent, grade),
            bold=True,
            halign="center",
            theme_text_color="Custom",
            text_color=color,
            size_hint_y=None,
            height="30dp",
        )
        pct.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        msg = MDLabel(
            text=(
                "Keep practising to sharpen your clinical judgement."
                if percent < 70 else
                "Great work! Your clinical reasoning is solid."
            ),
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="50dp",
        )
        msg.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        restart_btn = MDRaisedButton(
            text="TRY AGAIN",
            size_hint_x=1,
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self._restart(),
        )

        home_btn = MDRaisedButton(
            text="BACK TO HOME",
            size_hint_x=1,
            size_hint_y=None,
            height="50dp",
            on_release=lambda x: self.go_back(),
        )

        card.add_widget(title)
        card.add_widget(big_score)
        card.add_widget(pct)
        card.add_widget(msg)
        card.add_widget(restart_btn)
        card.add_widget(home_btn)

        self.ids.options_box.add_widget(card)

    def _restart(self):
        self._index = 0
        self._score = 0
        self._answered = False
        self._build_questions()
        Clock.schedule_once(self._load_question, 0.05)