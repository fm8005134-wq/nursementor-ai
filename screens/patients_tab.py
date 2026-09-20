from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton

import database as db
from screens.patient_card import PatientCard
from screens.patient_dialogs import AddPatientDialogContent


class PatientsTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dialog = None
        self._all_patients = []
        Clock.schedule_once(self._load, 0)

    # ------------------------------------------------------------------
    def _load(self, *_):
        db.create_tables()
        self._all_patients = db.list_patients()
        self._render(self._all_patients)

    def _render(self, patients):
        container = self.ids.get("patients_box")
        if container is None:
            return
        container.clear_widgets()

        if not patients:
            container.add_widget(MDLabel(
                text="No patients yet.\nTap  +  to register your first patient.",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height="100dp",
            ))
            return

        for p in patients:
            count = db.get_visit_count(p["id"])
            meta_bits = []
            if p.get("age"):
                meta_bits.append("{}y".format(p["age"]))
            if p.get("gender"):
                meta_bits.append(p["gender"])
            if p.get("phone"):
                meta_bits.append(p["phone"])
            meta = "  |  ".join(meta_bits) if meta_bits else "No details"

            card = PatientCard(
                patient_name=p["name"],
                patient_meta=meta,
                visits_label="{} visit{}".format(count, "" if count == 1 else "s"),
            )
            card.bind(on_release=lambda inst, pid=p["id"]: self._open_patient(pid))
            container.add_widget(card)

    # ------------------------------------------------------------------
    def _open_patient(self, patient_id):
        app = MDApp.get_running_app()
        ids = [p["id"] for p in self._all_patients]
        app.root.go_to_patient_detail(patient_id, patient_ids=ids)

    # ------------------------------------------------------------------
    def on_search_text(self, text):
        text = (text or "").strip()
        if not text:
            self._render(self._all_patients)
            return
        filtered = [p for p in self._all_patients
                    if text.lower() in (p.get("name", "") or "").lower()
                    or text in (p.get("phone", "") or "")]
        self._render(filtered)

    # ------------------------------------------------------------------
    def open_add_patient_dialog(self):
        if self._dialog is not None:
            return
        content = AddPatientDialogContent()
        self._dialog = MDDialog(
            title="Register New Patient",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._close_dialog()),
                MDRaisedButton(text="SAVE",
                               on_release=lambda x: self._save_patient(content)),
            ],
        )
        self._dialog.open()

    def _close_dialog(self):
        if self._dialog is not None:
            self._dialog.dismiss()
            self._dialog = None

    def _save_patient(self, content):
        name = (content.name_field.text or "").strip()
        if not name:
            return  # don't save empty
        age_text = (content.age_field.text or "").strip()
        age = int(age_text) if age_text.isdigit() else None

        db.add_patient(
            name=name,
            age=age,
            gender=(content.gender_field.text or "").strip() or None,
            phone=(content.phone_field.text or "").strip() or None,
            address=(content.address_field.text or "").strip() or None,
        )
        self._close_dialog()
        self._load()