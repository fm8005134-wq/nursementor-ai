from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.toast import toast

import database as db
from screens.patient_dialogs import (
    AddProcedureDialogContent,
    AddTestDialogContent,
    UpdateTestResultDialogContent,
    EditPatientDialogContent,
)


class PatientDetailScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._patient_id = None
        self._patient_ids = []
        self._dialog = None

    # ------------------------------------------------------------------
    def load_patient(self, patient_id, patient_ids=None):
        self._patient_id = patient_id
        self._patient_ids = patient_ids or [patient_id]
        Clock.schedule_once(self._render, 0.05)

    def go_back(self):
        self.manager.go_home()

    def open_report(self):
        if self._patient_id is None:
            return
        self.manager.go_to_report(self._patient_id)

    def go_previous(self):
        if not self._patient_ids:
            return
        try:
            idx = self._patient_ids.index(self._patient_id)
        except ValueError:
            return
        if idx > 0:
            self.load_patient(self._patient_ids[idx - 1], self._patient_ids)

    def go_next(self):
        if not self._patient_ids:
            return
        try:
            idx = self._patient_ids.index(self._patient_id)
        except ValueError:
            return
        if idx < len(self._patient_ids) - 1:
            self.load_patient(self._patient_ids[idx + 1], self._patient_ids)

    # ------------------------------------------------------------------
    def _render(self, *_):
        patient = db.get_patient(self._patient_id)
        if not patient:
            return

        db.get_or_create_today_visit(self._patient_id)
        self.ids.patient_toolbar.title = patient["name"]

        box = self.ids.detail_box
        box.clear_widgets()

        box.add_widget(self._make_info_card(patient))
        box.add_widget(self._make_action_row())

        header = MDLabel(
            text="Visit History",
            font_style="H6",
            bold=True,
            halign="left",
            size_hint_y=None,
            height="30dp",
        )
        header.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        box.add_widget(header)

        visits = db.get_patient_visits(self._patient_id)
        if not visits:
            box.add_widget(MDLabel(
                text="No visits recorded yet.",
                theme_text_color="Secondary",
                halign="left",
                size_hint_y=None,
                height="30dp",
            ))
            return

        total = len(visits)
        for i, visit in enumerate(visits):
            visit_no = total - i
            box.add_widget(self._make_visit_card(visit, visit_no))

    # ------------------------------------------------------------------
    def _make_info_card(self, patient):
        card = MDCard(
            orientation="vertical",
            padding="16dp",
            spacing="6dp",
            radius=[12],
            elevation=2,
            size_hint_y=None,
            height="180dp",
        )

        def add_line(text, color=None, bold=False):
            lbl = MDLabel(text=text, halign="left", size_hint_y=None,
                          height="24dp", bold=bold)
            if color:
                lbl.theme_text_color = "Custom"
                lbl.text_color = color
            lbl.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
            card.add_widget(lbl)

        add_line(patient["name"], color=(0.0, 0.54, 0.48, 1), bold=True)

        meta_bits = []
        if patient.get("age"):
            meta_bits.append("Age: {}".format(patient["age"]))
        if patient.get("gender"):
            meta_bits.append("Gender: {}".format(patient["gender"]))
        add_line("   ".join(meta_bits) if meta_bits else "Age / Gender: -")
        add_line("Phone: {}".format(patient.get("phone") or "-"))
        add_line("Address: {}".format(patient.get("address") or "-"))

        count = db.get_visit_count(self._patient_id)
        add_line("Total visits: {}".format(count),
                 color=(0.0, 0.54, 0.48, 1), bold=True)
        return card

    # ------------------------------------------------------------------
    def _make_action_row(self):
        row = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="50dp",
        )
        row.add_widget(MDRaisedButton(
            text="Add Procedure", size_hint=(1, 1),
            on_release=lambda x: self.open_add_procedure_dialog(),
        ))
        row.add_widget(MDRaisedButton(
            text="Add Test", size_hint=(1, 1),
            on_release=lambda x: self.open_add_test_dialog(),
        ))
        return row

    # ------------------------------------------------------------------
    def _make_visit_card(self, visit, visit_no):
        procs = db.get_visit_procedures(visit["id"])
        tests = db.get_visit_tests(visit["id"])

        line_count = 1 + len(procs) + len(tests)
        if not procs and not tests:
            line_count += 1
        height = 30 + line_count * 36 + 20

        card = MDCard(
            orientation="vertical",
            padding="14dp",
            spacing="4dp",
            radius=[12],
            elevation=1,
            size_hint_y=None,
            height="{}dp".format(height),
        )

        header = MDLabel(
            text="Visit #{}  -  {}".format(visit_no, visit["visit_date"]),
            bold=True,
            halign="left",
            theme_text_color="Custom",
            text_color=(0.0, 0.54, 0.48, 1),
            size_hint_y=None,
            height="24dp",
        )
        header.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        card.add_widget(header)

        for p in procs:
            card.add_widget(self._make_procedure_row(p))

        for t in tests:
            card.add_widget(self._make_test_row(t))

        if not procs and not tests:
            lbl = MDLabel(text="  No entries for this visit.",
                          halign="left", theme_text_color="Secondary",
                          size_hint_y=None, height="28dp")
            lbl.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
            card.add_widget(lbl)

        return card

    # ------------------------------------------------------------------
    def _make_procedure_row(self, proc):
        row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="34dp",
            spacing="4dp",
        )

        text = "  - Procedure: {}".format(proc["name"])
        if proc.get("details"):
            text += "  ({})".format(proc["details"])

        lbl = MDLabel(
            text=text,
            halign="left",
            size_hint_y=None,
            height="30dp",
            pos_hint={"center_y": .5},
        )
        lbl.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        row.add_widget(lbl)

        del_btn = MDIconButton(
            icon="delete-outline",
            theme_text_color="Custom",
            text_color=(0.85, 0.20, 0.20, 1),
            size_hint=(None, 1),
            size=("40dp", "40dp"),
            on_release=lambda x, p=proc: self.confirm_delete_procedure(p),
        )
        row.add_widget(del_btn)
        return row

    # ------------------------------------------------------------------
    def _make_test_row(self, test):
        is_pending = not test.get("result")

        row = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="34dp",
            spacing="4dp",
        )

        label_text = "  - Test: {}".format(test["name"])
        if is_pending:
            label_text += "  (Pending)"
        else:
            label_text += "  (Result: {})".format(test["result"])

        lbl = MDLabel(
            text=label_text,
            halign="left",
            size_hint_y=None,
            height="30dp",
            pos_hint={"center_y": .5},
        )
        if is_pending:
            lbl.theme_text_color = "Custom"
            lbl.text_color = (0.95, 0.6, 0.0, 1)
        lbl.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        row.add_widget(lbl)

        edit_btn = MDIconButton(
            icon="pencil",
            theme_text_color="Custom",
            text_color=(0.0, 0.54, 0.48, 1),
            size_hint=(None, 1),
            size=("36dp", "36dp"),
            on_release=lambda x, t=test: self.open_update_test_dialog(t),
        )
        row.add_widget(edit_btn)

        del_btn = MDIconButton(
            icon="delete-outline",
            theme_text_color="Custom",
            text_color=(0.85, 0.20, 0.20, 1),
            size_hint=(None, 1),
            size=("36dp", "36dp"),
            on_release=lambda x, t=test: self.confirm_delete_test(t),
        )
        row.add_widget(del_btn)
        return row

    # ==================================================================
    # EDIT PATIENT
    # ==================================================================
    def open_edit_patient_dialog(self):
        self._force_close_dialog()
        patient = db.get_patient(self._patient_id)
        if not patient:
            return

        content = EditPatientDialogContent(patient=patient)
        self._dialog = MDDialog(
            title="Edit Patient",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(text="SAVE",
                               on_release=lambda x: self._save_edit_patient(content)),
            ],
        )
        self._dialog.open()

    def _save_edit_patient(self, content):
        name = (content.name_field.text or "").strip()
        if not name:
            toast("Name cannot be empty")
            return
        age_text = (content.age_field.text or "").strip()
        age = int(age_text) if age_text.isdigit() else None

        db.update_patient(
            self._patient_id,
            name=name,
            age=age,
            gender=((content.gender_field.text or "").strip().upper()) or None,
            phone=(content.phone_field.text or "").strip() or None,
            address=(content.address_field.text or "").strip() or None,
        )
        self._force_close_dialog()
        toast("Patient updated")
        Clock.schedule_once(lambda *a: self._render(), 0.25)

    # ==================================================================
    # DELETE PATIENT
    # ==================================================================
    def confirm_delete_patient(self):
        self._force_close_dialog()
        patient = db.get_patient(self._patient_id)
        if not patient:
            return

        self._dialog = MDDialog(
            title="Delete Patient",
            text=(
                "Are you sure you want to delete \"{}\"?\n\n"
                "All visits, procedures and tests will also be deleted. "
                "This cannot be undone.".format(patient["name"])
            ),
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.85, 0.20, 0.20, 1),
                    on_release=lambda x: self._do_delete_patient(),
                ),
            ],
        )
        self._dialog.open()

    def _do_delete_patient(self):
        pid = self._patient_id
        self._force_close_dialog()
        db.delete_patient(pid)
        toast("Patient deleted")
        # Navigate back to home; patient tab will refresh
        Clock.schedule_once(lambda *a: self.manager.go_home(), 0.2)

    # ==================================================================
    # DELETE PROCEDURE
    # ==================================================================
    def confirm_delete_procedure(self, proc):
        self._force_close_dialog()
        self._dialog = MDDialog(
            title="Delete Procedure",
            text="Delete procedure \"{}\"?".format(proc["name"]),
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.85, 0.20, 0.20, 1),
                    on_release=lambda x: self._do_delete_procedure(proc["id"]),
                ),
            ],
        )
        self._dialog.open()

    def _do_delete_procedure(self, proc_id):
        self._force_close_dialog()
        db.delete_procedure(proc_id)
        toast("Procedure deleted")
        Clock.schedule_once(lambda *a: self._render(), 0.25)

    # ==================================================================
    # DELETE TEST
    # ==================================================================
    def confirm_delete_test(self, test):
        self._force_close_dialog()
        self._dialog = MDDialog(
            title="Delete Test",
            text="Delete test \"{}\"?".format(test["name"]),
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(0.85, 0.20, 0.20, 1),
                    on_release=lambda x: self._do_delete_test(test["id"]),
                ),
            ],
        )
        self._dialog.open()

    def _do_delete_test(self, test_id):
        self._force_close_dialog()
        db.delete_test(test_id)
        toast("Test deleted")
        Clock.schedule_once(lambda *a: self._render(), 0.25)

    # ==================================================================
    # ADD PROCEDURE
    # ==================================================================
    def open_add_procedure_dialog(self):
        self._force_close_dialog()
        content = AddProcedureDialogContent()
        self._dialog = MDDialog(
            title="Add Procedure",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(text="SAVE",
                               on_release=lambda x: self._save_procedure(content)),
            ],
        )
        self._dialog.open()

    def _save_procedure(self, content):
        name = (content.name_field.text or "").strip()
        if not name:
            self._force_close_dialog()
            return
        visit_id = db.get_or_create_today_visit(self._patient_id)
        db.add_procedure(
            visit_id=visit_id,
            name=name,
            details=(content.details_field.text or "").strip() or None,
        )
        self._force_close_dialog()
        Clock.schedule_once(lambda *a: self._render(), 0.25)

    # ==================================================================
    # ADD TEST
    # ==================================================================
    def open_add_test_dialog(self):
        self._force_close_dialog()
        content = AddTestDialogContent()
        self._dialog = MDDialog(
            title="Add Test",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(text="SAVE",
                               on_release=lambda x: self._save_test(content)),
            ],
        )
        self._dialog.open()

    def _save_test(self, content):
        name = (content.name_field.text or "").strip()
        if not name:
            self._force_close_dialog()
            return
        visit_id = db.get_or_create_today_visit(self._patient_id)
        db.add_test(
            visit_id=visit_id,
            name=name,
            result=(content.result_field.text or "").strip() or None,
        )
        self._force_close_dialog()
        Clock.schedule_once(lambda *a: self._render(), 0.25)

    # ==================================================================
    # UPDATE TEST RESULT
    # ==================================================================
    def open_update_test_dialog(self, test):
        self._force_close_dialog()
        content = UpdateTestResultDialogContent(
            test_name=test["name"],
            current_result=test.get("result") or "",
        )
        self._dialog = MDDialog(
            title="Update Test: {}".format(test["name"]),
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._force_close_dialog()),
                MDRaisedButton(
                    text="SAVE",
                    on_release=lambda x: self._save_test_result(test["id"], content),
                ),
            ],
        )
        self._dialog.open()

    def _save_test_result(self, test_id, content):
        result = (content.result_field.text or "").strip()
        db.update_test_result(test_id, result or None)
        self._force_close_dialog()
        Clock.schedule_once(lambda *a: self._render(), 0.25)

    # ==================================================================
    def _force_close_dialog(self):
        d = self._dialog
        self._dialog = None
        if d is not None:
            try:
                d.dismiss()
            except Exception:
                pass