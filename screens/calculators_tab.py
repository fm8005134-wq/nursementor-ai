from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel


CALCULATORS = [
    ("calc_vial",      "Vial Dose Calculator",       "needle"),
    ("calc_dose",      "Dose Calculator (mg/kg)",    "medical-bag"),
    ("calc_dilution",  "Dilution Calculator",        "flask-outline"),
    ("calc_ivflow",    "IV Flow Calculator",         "water-outline"),
    ("calc_infusion",  "Infusion Calculator",        "speedometer"),
    ("calc_bmi",       "BMI Calculator",             "scale-bathroom"),
]


class CalcCard(MDCard):
    card_title = StringProperty("")
    icon_name = StringProperty("calculator")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = dp(16)
        self.spacing = dp(14)
        self.radius = [14]
        self.elevation = 2
        self.size_hint_y = None
        self.height = dp(76)
        self.ripple_behavior = True

        self._icon = MDIcon(
            icon=self.icon_name,
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0.0, 0.54, 0.48, 1),
            font_size="30sp",
            size_hint=(None, None),
            size=(dp(36), dp(36)),
            pos_hint={"center_y": .5},
        )
        self._label = MDLabel(
            text=self.card_title,
            font_style="H6",
            bold=True,
            pos_hint={"center_y": .5},
        )
        self.add_widget(self._icon)
        self.add_widget(self._label)

        self.bind(icon_name=lambda i, v: setattr(self._icon, "icon", v))
        self.bind(card_title=lambda i, v: setattr(self._label, "text", v))


class CalculatorsTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._build_cards, 0)

    def _build_cards(self, *_):
        container = self.ids.get("cards_box")
        if container is None:
            return
        container.clear_widgets()
        for screen_name, title, icon in CALCULATORS:
            card = CalcCard(card_title=title, icon_name=icon)
            card.bind(on_release=lambda inst, s=screen_name: self.open_calc(s))
            container.add_widget(card)

    def open_calc(self, screen_name):
        app = MDApp.get_running_app()
        app.root.current = screen_name