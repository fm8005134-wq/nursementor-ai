from kivy.properties import StringProperty
from kivymd.uix.card import MDCard


class PatientCard(MDCard):
    patient_name = StringProperty("")
    patient_meta = StringProperty("")
    visits_label = StringProperty("")