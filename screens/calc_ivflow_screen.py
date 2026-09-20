from kivy.animation import Animation
from kivymd.uix.screen import MDScreen

from calculators import iv_flow_calculator


class CalcIVFlowScreen(MDScreen):
    def go_back(self):
        self.manager.current = "main"

    def calculate(self):
        # Read hours + minutes, combine into total hours
        hours_text = (self.ids.hours_field.text or "").strip()
        minutes_text = (self.ids.minutes_field.text or "").strip()

        hours = 0
        minutes = 0
        if hours_text:
            try:
                hours = int(hours_text)
            except ValueError:
                hours = 0
        if minutes_text:
            try:
                minutes = int(minutes_text)
            except ValueError:
                minutes = 0

        if hours == 0 and minutes == 0:
            self._show_error("Please enter a valid time (hours and/or minutes).")
            return

        # Convert to total hours
        total_hours = hours + (minutes / 60.0)

        result = iv_flow_calculator(
            self.ids.volume_field.text,
            total_hours,
            self.ids.factor_field.text,
        )

        if not result["success"]:
            self._show_error(result["error"])
            return

        # Show time summary
        self.ids.result_time_label.text = "Time used: {} hr {} min".format(
            hours, minutes
        )
        self.ids.error_line.text = ""
        self.ids.result_line1.text = "Flow Rate: {:.2f} mL/hour".format(
            result["ml_per_hour"]
        )
        self.ids.result_line2.text = "Drops: {:.1f} gtt/min".format(
            result["drops_per_minute"]
        )
        self.ids.result_line3.text = "(Approx. {} drops/min)".format(
            round(result["drops_per_minute"])
        )

        card = self.ids.result_card
        card.height = "210dp"
        Animation(opacity=1, duration=0.25).start(card)

    def _show_error(self, message):
        self.ids.result_line1.text = ""
        self.ids.result_line2.text = ""
        self.ids.result_line3.text = ""
        self.ids.result_time_label.text = ""
        self.ids.error_line.text = message

        card = self.ids.result_card
        card.height = "140dp"
        Animation(opacity=1, duration=0.25).start(card)