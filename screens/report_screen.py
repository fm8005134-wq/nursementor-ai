from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast

import database as db
import report_generator as rg


class ReportScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._patient_id = None
        self._report_text = ""

    def load_patient(self, patient_id):
        self._patient_id = patient_id
        Clock.schedule_once(self._render, 0.05)

    def _render(self, *_):
        patient = db.get_patient(self._patient_id)
        if not patient:
            return
        self.ids.report_toolbar.title = "Report - {}".format(patient["name"])
        self._report_text = rg.build_patient_report_text(self._patient_id)
        self.ids.report_text.text = self._report_text

    def go_back(self):
        self.manager.go_to_patient_detail(self._patient_id)

    def save_pdf(self):
        path = rg.build_patient_pdf(self._patient_id)
        if path:
            filename = path.split("/")[-1]
            toast("PDF saved: reports/{}".format(filename))
        else:
            toast("Failed to save PDF")

    def save_text(self):
        path = rg.save_patient_report_text(self._patient_id)
        if path:
            filename = path.split("/")[-1]
            toast("Text saved: reports/{}".format(filename))
        else:
            toast("Failed to save text")

    def copy_report(self):
        try:
            Clipboard.copy(self._report_text)
            toast("Report copied to clipboard")
        except Exception:
            toast("Failed to copy")