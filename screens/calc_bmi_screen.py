from kivy.animation import Animation
from kivymd.uix.screen import MDScreen

from calculators import bmi_calculator


class CalcBMIScreen(MDScreen):
    def go_back(self):
        self.manager.current = "main"

    def calculate(self):
        result = bmi_calculator(
            self.ids.weight_field.text,
            self.ids.height_field.text,
        )

        card = self.ids.result_card
        if not result["success"]:
            self.ids.result_line1.text = ""
            self.ids.result_line2.text = ""
            self.ids.error_line.text = result["error"]
        else:
            self.ids.error_line.text = ""
            self.ids.result_line1.text = "BMI: {:.2f}".format(result["bmi"])
            self.ids.result_line2.text = "Category: {}".format(result["category"])

        card.height = "160dp"
        Animation(opacity=1, duration=0.25).start(card)