from datetime import datetime

from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.textfield import MDTextField

from notes_store import load_notes, save_notes


class NotesTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dialog = None
        self._title_field = None
        self._body_field = None
        Clock.schedule_once(self._load_and_render, 0)

    def _load_and_render(self, *_):
        self._render(load_notes())

    def _render(self, notes):
        container = self.ids.get("notes_box")
        if container is None:
            return
        container.clear_widgets()

        if not notes:
            container.add_widget(MDLabel(
                text="No notes yet.\nTap  +  to add your first note.",
                theme_text_color="Secondary",
                halign="center",
                size_hint_y=None,
                height="100dp",
            ))
            return

        for note in notes:
            card = MDCard(
                orientation="vertical",
                padding="16dp",
                spacing="6dp",
                radius=[12],
                elevation=2,
                size_hint_y=None,
                height="100dp",
            )

            title = MDLabel(
                text=note.get("title", "Untitled"),
                font_style="H6",
                bold=True,
                size_hint_y=None,
                height="28dp",
                halign="left",
                text_size=(None, None),
            )

            body = MDLabel(
                text=note.get("body", ""),
                size_hint_y=None,
                halign="left",
            )
            body.bind(width=lambda inst, val: setattr(inst, "text_size", (val, None)))
            body.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1]))

            created = MDLabel(
                text=note.get("created", ""),
                theme_text_color="Secondary",
                font_style="Caption",
                size_hint_y=None,
                height="20dp",
                halign="left",
            )

            card.add_widget(title)
            card.add_widget(body)
            card.add_widget(created)

            # auto-fit card height to content
            def _fit(card=card, title=title, body=body, created=created):
                card.height = title.height + body.height + created.height + 48
            body.bind(texture_size=lambda *a, f=_fit: f())
            Clock.schedule_once(lambda *a, f=_fit: f(), 0)

            container.add_widget(card)

    def open_add_dialog(self):
        if self._dialog is not None:
            return

        self._title_field = MDTextField(
            hint_text="Title",
            mode="rectangle",
            size_hint_y=None,
            height="56dp",
        )
        self._body_field = MDTextField(
            hint_text="Write your note...",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height="140dp",
        )

        content = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="220dp",
            padding="4dp",
        )
        content.add_widget(self._title_field)
        content.add_widget(self._body_field)

        self._dialog = MDDialog(
            title="New Note",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self._close_dialog(),
                ),
                MDRaisedButton(
                    text="SAVE",
                    on_release=lambda x: self._save_note(),
                ),
            ],
        )
        self._dialog.open()

    def _close_dialog(self):
        if self._dialog is not None:
            self._dialog.dismiss()
            self._dialog = None
            self._title_field = None
            self._body_field = None

    def _save_note(self):
        title = (self._title_field.text or "").strip() if self._title_field else ""
        body = (self._body_field.text or "").strip() if self._body_field else ""

        if not title and not body:
            self._close_dialog()
            return

        notes = load_notes()
        notes.insert(0, {
            "title": title or "Untitled",
            "body": body,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
        save_notes(notes)
        self._close_dialog()
        self._render(notes)