from kivy.animation import Animation
from kivymd.uix.screen import MDScreen

from calculators import dilution_calculator


class CalcDilutionScreen(MDScreen):
    def go_back(self):
        self.manager.current = "main"

    def calculate(self):
        result = dilution_calculator(
            self.ids.available_field.text,
            self.ids.required_field.text,
            self.ids.volume_field.text,
        )

        card = self.ids.result_card
        if not result["success"]:
            self.ids.result_line1.text = ""
            self.ids.result_line2.text = ""
            self.ids.error_line.text = result["error"]
        else:
            self.ids.error_line.text = ""
            self.ids.result_line1.text = "Drug Amount: {:.2f} mL".format(
                result["drug_amount_ml"]
            )
            self.ids.result_line2.text = "Diluent Amount: {:.2f} mL".format(
                result["diluent_amount_ml"]
            )

        card.height = "160dp"
        Animation(opacity=1, duration=0.25).start(card)