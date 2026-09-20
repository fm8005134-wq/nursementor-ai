from kivy.animation import Animation
from kivymd.uix.screen import MDScreen

from calculators import infusion_calculator


class CalcInfusionScreen(MDScreen):
    def go_back(self):
        self.manager.current = "main"

    def calculate(self):
        result = infusion_calculator(
            self.ids.volume_field.text,
            self.ids.duration_field.text,
        )

        card = self.ids.result_card
        if not result["success"]:
            self.ids.result_line1.text = ""
            self.ids.error_line.text = result["error"]
        else:
            self.ids.error_line.text = ""
            self.ids.result_line1.text = "Infusion Rate: {:.2f} mL/hour".format(
                result["ml_per_hour"]
            )

        card.height = "140dp"
        Animation(opacity=1, duration=0.25).start(card)