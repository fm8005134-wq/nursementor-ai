from datetime import datetime

from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast

import database as db
import backup_manager as bm


class DashboardTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dialog = None
        Clock.schedule_once(self._load_stats, 0)

    # ------------------------------------------------------------------
    def _load_stats(self, *_):
        db.create_tables()
        stats = db.monthly_statistics()
        self._render(stats)

    def _render(self, stats):
        container = self.ids.get("stats_box")
        if container is None:
            return
        container.clear_widgets()

        month_name = datetime(stats["year"], stats["month"], 1).strftime("%B %Y")
        header = MDLabel(
            text=month_name,
            font_style="H5",
            bold=True,
            halign="left",
            size_hint_y=None,
            height="40dp",
            theme_text_color="Custom",
            text_color=(0.0, 0.54, 0.48, 1),
        )
        header.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        container.add_widget(header)

        container.add_widget(self._make_summary_row([
            ("Patients", str(stats["total_patients"]), "account-group"),
            ("Visits", str(stats["total_visits"]), "calendar-check"),
        ]))
        container.add_widget(self._make_summary_row([
            ("Procedures", str(stats["total_procedures"]), "needle"),
            ("Tests", str(stats["total_tests"]), "test-tube"),
        ]))
        container.add_widget(self._make_totals_card())
        container.add_widget(self._make_backup_card())

    # ------------------------------------------------------------------
    def _make_summary_row(self, items):
        row = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="120dp",
        )
        for title, value, icon in items:
            row.add_widget(self._make_stat_card(title, value, icon))
        return row

    def _make_stat_card(self, title, value, icon):
        card = MDCard(
            orientation="vertical",
            padding="12dp",
            spacing="4dp",
            radius=[12],
            elevation=2,
            size_hint=(1, 1),
        )

        icon_box = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="32dp",
        )
        icon_widget = MDIcon(
            icon=icon,
            halign="center",
            theme_text_color="Custom",
            text_color=(0.0, 0.54, 0.48, 1),
            font_size="26sp",
            size_hint=(1, 1),
        )
        icon_box.add_widget(icon_widget)

        value_label = MDLabel(
            text=value,
            halign="center",
            font_style="H4",
            bold=True,
            size_hint_y=None,
            height="40dp",
        )
        value_label.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        title_label = MDLabel(
            text=title,
            halign="center",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height="20dp",
        )
        title_label.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        card.add_widget(icon_box)
        card.add_widget(value_label)
        card.add_widget(title_label)
        return card

    # ------------------------------------------------------------------
    def _make_totals_card(self):
        card = MDCard(
            orientation="vertical",
            padding="16dp",
            spacing="10dp",
            radius=[12],
            elevation=2,
            size_hint_y=None,
            height="160dp",
        )

        title = MDLabel(
            text="All-Time Totals",
            font_style="H6",
            bold=True,
            halign="left",
            size_hint_y=None,
            height="28dp",
        )
        title.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        card.add_widget(title)

        total_patients = db.patient_count()
        total_visits = db.visit_count()

        card.add_widget(self._make_total_row(
            "Registered patients", total_patients, "account-multiple",
            (0.0, 0.54, 0.48, 1),
        ))
        card.add_widget(self._make_total_row(
            "Total visits", total_visits, "calendar-check",
            (0.13, 0.59, 0.95, 1),
        ))
        return card

    def _make_total_row(self, label, value, icon, color):
        row = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="34dp",
        )
        icon_w = MDIcon(
            icon=icon,
            theme_text_color="Custom",
            text_color=color,
            font_size="20sp",
            size_hint=(None, 1),
            width="28dp",
        )
        label_w = MDLabel(
            text=label,
            halign="left",
            size_hint_y=None,
            height="30dp",
            pos_hint={"center_y": .5},
        )
        label_w.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        value_w = MDLabel(
            text=str(value),
            halign="right",
            bold=True,
            theme_text_color="Custom",
            text_color=color,
            size_hint_y=None,
            height="30dp",
            pos_hint={"center_y": .5},
        )
        value_w.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

        row.add_widget(icon_w)
        row.add_widget(label_w)
        row.add_widget(value_w)
        return row

    # ------------------------------------------------------------------
    def _make_backup_card(self):
        card = MDCard(
            orientation="vertical",
            padding="16dp",
            spacing="10dp",
            radius=[12],
            elevation=2,
            size_hint_y=None,
            height="200dp",
        )

        title = MDLabel(
            text="Data Backup",
            font_style="H6",
            bold=True,
            halign="left",
            size_hint_y=None,
            height="28dp",
        )
        title.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        card.add_widget(title)

        desc = MDLabel(
            text="Save a copy of your clinic database, or restore from a previous backup.",
            halign="left",
            theme_text_color="Secondary",
            font_style="Caption",
            size_hint_y=None,
            height="40dp",
        )
        desc.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
        card.add_widget(desc)

        btn_row = MDBoxLayout(
            orientation="horizontal",
            spacing="10dp",
            size_hint_y=None,
            height="50dp",
        )
        btn_row.add_widget(MDRaisedButton(
            text="Create Backup",
            size_hint=(1, 1),
            on_release=lambda x: self.create_backup(),
        ))
        btn_row.add_widget(MDRaisedButton(
            text="Restore",
            size_hint=(1, 1),
            on_release=lambda x: self.show_backups(),
        ))
        card.add_widget(btn_row)
        return card

    # ------------------------------------------------------------------
    def create_backup(self):
        path = bm.create_backup()
        if path:
            filename = path.split("/")[-1]
            toast("Backup saved: {}".format(filename))
        else:
            toast("Backup failed")

    # ------------------------------------------------------------------
    def show_backups(self):
        backups = bm.list_backups()
        if not backups:
            toast("No backups found")
            return

        # Build simple list of buttons
        from kivymd.uix.boxlayout import MDBoxLayout as Box
        from kivymd.uix.button import MDFlatButton as Flat

        content = Box(
            orientation="vertical",
            spacing="6dp",
            size_hint_y=None,
            height=str(len(backups) * 50 + 20),
            padding="4dp",
        )
        for b in backups:
            btn = Flat(
                text="{}  |  {} KB  |  {}".format(
                    b["filename"], b["size_kb"], b["modified"]
                ),
                size_hint_y=None,
                height="50dp",
                on_release=lambda x, p=b["path"]: self.confirm_restore(p),
            )
            content.add_widget(btn)

        self._dialog = MDDialog(
            title="Available Backups",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CLOSE",
                             on_release=lambda x: self._close_dialog()),
            ],
        )
        self._dialog.open()

    def confirm_restore(self, backup_path):
        self._close_dialog()
        filename = backup_path.split("/")[-1]
        self._dialog = MDDialog(
            title="Restore Backup",
            text=(
                "Restore database from \"{}\"?\n\n"
                "The current database will be replaced. A safety copy "
                "will be kept as clinic.db.before_restore.".format(filename)
            ),
            buttons=[
                MDFlatButton(text="CANCEL",
                             on_release=lambda x: self._close_dialog()),
                MDRaisedButton(
                    text="RESTORE",
                    md_bg_color=(0.85, 0.20, 0.20, 1),
                    on_release=lambda x: self._do_restore(backup_path),
                ),
            ],
        )
        self._dialog.open()

    def _do_restore(self, backup_path):
        self._close_dialog()
        ok = bm.restore_backup(backup_path)
        if ok:
            toast("Database restored. Restart app to see changes.")
        else:
            toast("Restore failed")

    # ------------------------------------------------------------------
    def _close_dialog(self):
        d = self._dialog
        self._dialog = None
        if d is not None:
            try:
                d.dismiss()
            except Exception:
                pass