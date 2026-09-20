from kivy.animation import Animation
from kivymd.uix.screen import MDScreen

from calculators import vial_dose_calculator


class CalcVialScreen(MDScreen):
    _mode = "direct"  # or "perkg"

    def on_enter(self, *args):
        self.set_mode(self._mode)

    def go_back(self):
        self.manager.current = "main"

    def set_mode(self, mode):
        self._mode = mode
        weight_field = self.ids.weight_field

        if mode == "perkg":
            weight_field.height = "56dp"
            weight_field.opacity = 1
            self.ids.ordered_field.hint_text = "Ordered Dose (mg/kg)"
            # highlight selected
            self.ids.mode_direct_btn.md_bg_color = (1, 1, 1, 1)
            self.ids.mode_perkg_btn.md_bg_color = (0.0, 0.54, 0.48, 0.25)
        else:
            weight_field.height = "0dp"
            weight_field.opacity = 0
            weight_field.text = ""
            self.ids.ordered_field.hint_text = "Ordered Dose (mg)"
            self.ids.mode_direct_btn.md_bg_color = (0.0, 0.54, 0.48, 0.25)
            self.ids.mode_perkg_btn.md_bg_color = (1, 1, 1, 1)

    def calculate(self):
        weight = self.ids.weight_field.text if self._mode == "perkg" else None

        result = vial_dose_calculator(
            ordered_mg=self.ids.ordered_field.text,
            vial_strength_mg=self.ids.vial_field.text,
            diluent_ml=self.ids.diluent_field.text,
            weight_kg=weight,
        )

        card = self.ids.result_card

        if not result["success"]:
            self._clear_results()
            self.ids.error_line.text = result["error"]
            card.height = "160dp"
            Animation(opacity=1, duration=0.25).start(card)
            return

        # Success
        self.ids.error_line.text = ""
        self.ids.result_concentration.text = "Concentration: {:.2f} mg/mL".format(
            result["concentration_mg_per_ml"]
        )
        self.ids.result_line1.text = "Total Dose: {:.2f} mg".format(
            result["total_dose_mg"]
        )
        self.ids.result_line2.text = "Volume to Draw: {:.2f} mL".format(
            result["volume_ml"]
        )
        self.ids.warning_line.text = result.get("warning") or ""

        height = 220 if result.get("warning") else 200
        card.height = "{}dp".format(height)
        Animation(opacity=1, duration=0.25).start(card)

    def _clear_results(self):
        self.ids.result_concentration.text = ""
        self.ids.result_line1.text = ""
        self.ids.result_line2.text = ""
        self.ids.warning_line.text = ""