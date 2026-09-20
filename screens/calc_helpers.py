"""
Shared helpers for the Clinical Calculators module.
Builds input fields, result cards, and the safety disclaimer.
"""

from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

from calculators import SAFETY_DISCLAIMER


def make_input_field(hint_text, input_filter=None, size_hint_y=None):
    field = MDTextField(
        hint_text=hint_text,
        mode="rectangle",
        size_hint_y=size_hint_y,
        height=dp(56),
    )
    if input_filter == "float":
        # Accept digits and one decimal point
        field.input_filter = "float"
    elif input_filter == "int":
        field.input_filter = "int"
    return field


def make_calculate_button(text="Calculate", on_press=None):
    btn = MDRaisedButton(
        text=text,
        size_hint=(1, None),
        height=dp(50),
    )
    if on_press:
        btn.bind(on_release=on_press)
    return btn


def make_disclaimer_card():
    card = MDCard(
        orientation="vertical",
        padding=dp(14),
        spacing=dp(6),
        radius=[12],
        elevation=1,
        size_hint_y=None,
        height=dp(120),
        md_bg_color=(1.0, 0.95, 0.80, 1),  # pale amber
    )
    title = MDLabel(
        text="Safety Notice",
        bold=True,
        halign="left",
        size_hint_y=None,
        height=dp(22),
        theme_text_color="Custom",
        text_color=(0.60, 0.40, 0.0, 1),
    )
    title.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

    body = MDLabel(
        text=SAFETY_DISCLAIMER,
        halign="left",
        size_hint_y=None,
        theme_text_color="Custom",
        text_color=(0.35, 0.25, 0.0, 1),
        font_style="Caption",
    )
    body.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
    body.bind(texture_size=lambda i, v: setattr(i, "height", v[1]))

    card.add_widget(title)
    card.add_widget(body)
    return card


def make_result_card(title="Result"):
    card = MDCard(
        orientation="vertical",
        padding=dp(16),
        spacing=dp(8),
        radius=[12],
        elevation=2,
        size_hint_y=None,
        height=dp(200),
        md_bg_color=(0.94, 0.98, 0.97, 1),  # pale teal
    )
    header = MDLabel(
        text=title,
        bold=True,
        font_style="H6",
        halign="left",
        theme_text_color="Custom",
        text_color=(0.0, 0.54, 0.48, 1),
        size_hint_y=None,
        height=dp(28),
    )
    header.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))
    card.add_widget(header)

    body = MDBoxLayout(
        orientation="vertical",
        spacing=dp(4),
        size_hint_y=None,
        height=dp(140),
    )
    card.add_widget(body)
    card.body_box = body
    return card


def add_result_line(card, label, value, big=False):
    color = (0.0, 0.54, 0.48, 1) if big else (0.20, 0.20, 0.20, 1)
    row = MDBoxLayout(
        orientation="horizontal",
        size_hint_y=None,
        height=dp(34) if big else dp(28),
        spacing=dp(6),
    )
    lbl = MDLabel(
        text=label,
        halign="left",
        size_hint_y=None,
        height=dp(28) if big else dp(24),
        pos_hint={"center_y": .5},
        bold=big,
    )
    lbl.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

    val = MDLabel(
        text=str(value),
        halign="right",
        size_hint_y=None,
        height=dp(28) if big else dp(24),
        pos_hint={"center_y": .5},
        bold=big,
        font_style="H6" if big else "Body1",
        theme_text_color="Custom",
        text_color=color,
    )
    val.bind(width=lambda i, v: setattr(i, "text_size", (v, None)))

    row.add_widget(lbl)
    row.add_widget(val)
    card.body_box.add_widget(row)