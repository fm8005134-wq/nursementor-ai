from kivy.animation import Animation
from kivymd.uix.screen import MDScreen

from calculators import dose_calculator


class CalcDoseScreen(MDScreen):
    def go_back(self):
        self.manager.current = "main"

    def calculate(self):
        result = dose_calculator(
            self.ids.weight_field.text,
            self.ids.dose_field.text,
            self.ids.conc_field.text,
        )

        card = self.ids.result_card
        if not result["success"]:
            self.ids.result_line1.text = ""
            self.ids.result_line2.text = ""
            self.ids.error_line.text = result["error"]
        else:
            self.ids.error_line.text = ""
            self.ids.result_line1.text = "Total Dose: {:.2f} mg".format(
                result["total_mg"]
            )
            self.ids.result_line2.text = "Volume: {:.2f} mL".format(
                result["volume_ml"]
            )

        # Auto-size + fade in
        card.height = "160dp"
        Animation(opacity=1, duration=0.25).start(card)