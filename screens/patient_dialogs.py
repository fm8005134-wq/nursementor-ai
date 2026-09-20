from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel


class AddPatientDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "300dp"
        self.padding = "4dp"

        self.name_field = MDTextField(
            hint_text="Full name *",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.age_field = MDTextField(
            hint_text="Age",
            mode="rectangle",
            input_filter="int",
            size_hint_y=None,
            height="56dp",
        )
        self.gender_field = MDTextField(
            hint_text="Gender (M / F / Other)",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.phone_field = MDTextField(
            hint_text="Phone",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.address_field = MDTextField(
            hint_text="Address",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )

        self.add_widget(self.name_field)
        self.add_widget(self.age_field)
        self.add_widget(self.gender_field)
        self.add_widget(self.phone_field)
        self.add_widget(self.address_field)


class EditPatientDialogContent(MDBoxLayout):
    def __init__(self, patient=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "300dp"
        self.padding = "4dp"

        patient = patient or {}

        self.name_field = MDTextField(
            hint_text="Full name *",
            text=str(patient.get("name") or ""),
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.age_field = MDTextField(
            hint_text="Age",
            text=str(patient.get("age") or ""),
            mode="rectangle",
            input_filter="int",
            size_hint_y=None,
            height="56dp",
        )
        self.gender_field = MDTextField(
            hint_text="Gender (M / F / Other)",
            text=str(patient.get("gender") or ""),
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.phone_field = MDTextField(
            hint_text="Phone",
            text=str(patient.get("phone") or ""),
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.address_field = MDTextField(
            hint_text="Address",
            text=str(patient.get("address") or ""),
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )

        self.add_widget(self.name_field)
        self.add_widget(self.age_field)
        self.add_widget(self.gender_field)
        self.add_widget(self.phone_field)
        self.add_widget(self.address_field)


class AddProcedureDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "140dp"
        self.padding = "4dp"

        self.name_field = MDTextField(
            hint_text="Procedure name *  (e.g., Injection)",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.details_field = MDTextField(
            hint_text="Details (optional)",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )

        self.add_widget(self.name_field)
        self.add_widget(self.details_field)


class AddTestDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "140dp"
        self.padding = "4dp"

        self.name_field = MDTextField(
            hint_text="Test name *  (e.g., CBC)",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.result_field = MDTextField(
            hint_text="Result (leave blank if pending)",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )

        self.add_widget(self.name_field)
        self.add_widget(self.result_field)


class UpdateTestResultDialogContent(MDBoxLayout):
    def __init__(self, test_name="", current_result="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "10dp"
        self.size_hint_y = None
        self.height = "110dp"
        self.padding = "4dp"

        name_label = MDLabel(
            text="Test: {}".format(test_name),
            bold=True,
            size_hint_y=None,
            height="30dp",
            halign="left",
        )
        name_label.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        self.add_widget(name_label)

        self.result_field = MDTextField(
            hint_text="Result",
            text=current_result or "",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self.add_widget(self.result_field)