import os

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens.main_screen import MainScreen      # noqa: F401
from screens.home_tab import HomeTab            # noqa: F401
from screens.search_tab import SearchTab        # noqa: F401
from screens.notes_tab import NotesTab          # noqa: F401
from screens.dashboard_tab import DashboardTab  # noqa: F401
from screens.patients_tab import PatientsTab    # noqa: F401
from screens.patient_card import PatientCard    # noqa: F401
from screens.patient_dialogs import (           # noqa: F401
    AddPatientDialogContent,
    AddProcedureDialogContent,
    AddTestDialogContent,
    UpdateTestResultDialogContent,
)
from screens.patient_detail_screen import PatientDetailScreen  # noqa: F401
from screens.report_screen import ReportScreen                  # noqa: F401
from screens.topic_button import TopicButton    # noqa: F401
from screens.topic_card import TopicCard        # noqa: F401
from screens.topic_screen import TopicScreen    # noqa: F401
from screens.quiz_screen import QuizScreen      # noqa: F401

# --- Calculators module ---
from screens.calculators_tab import CalculatorsTab             # noqa: F401
from screens.calc_vial_screen import CalcVialScreen          # noqa: F401
from screens.calc_dose_screen import CalcDoseScreen          # noqa: F401
from screens.calc_dilution_screen import CalcDilutionScreen  # noqa: F401
from screens.calc_ivflow_screen import CalcIVFlowScreen      # noqa: F401
from screens.calc_infusion_screen import CalcInfusionScreen  # noqa: F401
from screens.calc_bmi_screen import CalcBMIScreen            # noqa: F401


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KV_DIR = os.path.join(BASE_DIR, "kv")

KV_FILES = [
    "root.kv",
    "main.kv",
    "home_tab.kv",
    "search_tab.kv",
    "notes_tab.kv",
    "dashboard_tab.kv",
    "patients_tab.kv",
    "patient_detail.kv",
    "report.kv",
    "topic.kv",
    "quiz.kv",
    "calculators_tab.kv",
    "calc_vial.kv",
    "calc_dose.kv",
    "calc_dilution.kv",
    "calc_ivflow.kv",
    "calc_infusion.kv",
    "calc_bmi.kv",
]


class RootManager(ScreenManager):
    def go_to_topic(self, topic_name):
        topic_screen = self.get_screen("topic")
        topic_screen.load_topic(topic_name)
        self.current = "topic"

    def go_home(self):
        self.current = "main"

    def go_to_patient_detail(self, patient_id, patient_ids=None):
        detail = self.get_screen("patient_detail")
        detail.load_patient(patient_id, patient_ids=patient_ids)
        self.current = "patient_detail"

    def go_to_report(self, patient_id):
        report = self.get_screen("report")
        report.load_patient(patient_id)
        self.current = "report"

    def on_start(self):
        try:
            main_screen = self.get_screen("main")
            bottom_nav = main_screen.ids.get("bottom_nav")
            if bottom_nav is not None:
                bottom_nav.switch_tab("home_tab")
        except Exception:
            pass


class NurseMentorApp(MDApp):
    def build(self):
        self.title = "Nurse Mentor AI"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Light"

        for fn in KV_FILES:
            Builder.load_file(os.path.join(KV_DIR, fn))

        return RootManager()


if __name__ == "__main__":
    NurseMentorApp().run()