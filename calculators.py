"""
Nurse Mentor AI - Clinical Calculators (pure math).

Educational and calculation-assistance tool only.
The app performs mathematical operations on user-provided values.
It does NOT recommend treatment, prescribe medication, or suggest doses.

Every result should be independently verified.
"""


def _to_float(value):
    try:
        return float(str(value).strip())
    except Exception:
        return None


def _fail(msg):
    return {"success": False, "error": msg}


def _ok(**values):
    result = {"success": True, "error": None}
    result.update(values)
    return result


# ---------------------------------------------------------------------------
# 1. Dose Calculator (mg/kg based)
# ---------------------------------------------------------------------------
def dose_calculator(weight_kg, ordered_mg_per_kg, concentration_mg_per_ml):
    w = _to_float(weight_kg)
    d = _to_float(ordered_mg_per_kg)
    c = _to_float(concentration_mg_per_ml)

    if w is None or d is None or c is None:
        return _fail("Please enter valid numbers in all fields.")
    if w <= 0:
        return _fail("Weight must be greater than zero.")
    if d <= 0:
        return _fail("Ordered dose must be greater than zero.")
    if c <= 0:
        return _fail("Concentration must be greater than zero.")

    total_mg = w * d
    volume_ml = total_mg / c
    return _ok(
        total_mg=total_mg,
        volume_ml=volume_ml,
        weight_kg=w,
        ordered_mg_per_kg=d,
        concentration_mg_per_ml=c,
    )


# ---------------------------------------------------------------------------
# 2. Vial Dose Calculator (direct mg, with dilution)
# ---------------------------------------------------------------------------
def vial_dose_calculator(ordered_mg, vial_strength_mg, diluent_ml, weight_kg=None):
    """
    Inputs:
        ordered_mg        - dose the doctor ordered (in mg)
        vial_strength_mg  - total mg in the vial (e.g. 1000 for 1g)
        diluent_ml        - how much diluent the staff added (in mL)
        weight_kg         - optional; if given, ordered_mg is per kg
    Outputs:
        total_dose_mg     - mg to administer
        concentration     - mg/mL after reconstitution
        volume_ml         - how much to draw
    """
    o = _to_float(ordered_mg)
    v = _to_float(vial_strength_mg)
    d = _to_float(diluent_ml)
    w = _to_float(weight_kg) if weight_kg not in (None, "") else None

    if o is None or v is None or d is None:
        return _fail("Please enter valid numbers in all fields.")
    if o <= 0:
        return _fail("Ordered dose must be greater than zero.")
    if v <= 0:
        return _fail("Vial strength must be greater than zero.")
    if d <= 0:
        return _fail("Diluent volume must be greater than zero.")

    concentration = v / d  # mg/mL

    if w is not None:
        if w <= 0:
            return _fail("Weight must be greater than zero.")
        total_dose_mg = w * o
    else:
        total_dose_mg = o

    volume_ml = total_dose_mg / concentration

    warning = None
    if volume_ml > 20:
        warning = (
            "Calculated volume is large (>20 mL). "
            "Please verify vial strength, diluent volume and ordered dose."
        )

    return _ok(
        total_dose_mg=total_dose_mg,
        concentration_mg_per_ml=concentration,
        volume_ml=volume_ml,
        vial_strength_mg=v,
        diluent_ml=d,
        ordered_mg=o,
        weight_kg=w,
        warning=warning,
    )


# ---------------------------------------------------------------------------
# 3. Drug Dilution Calculator
# ---------------------------------------------------------------------------
def dilution_calculator(available_strength, required_strength, final_volume):
    c1 = _to_float(available_strength)
    c2 = _to_float(required_strength)
    v2 = _to_float(final_volume)

    if c1 is None or c2 is None or v2 is None:
        return _fail("Please enter valid numbers in all fields.")
    if c1 <= 0 or c2 <= 0:
        return _fail("Strengths must be greater than zero.")
    if v2 <= 0:
        return _fail("Final volume must be greater than zero.")
    if c2 > c1:
        return _fail("Required strength cannot exceed available strength.")

    drug_amount = (c2 * v2) / c1
    diluent_amount = v2 - drug_amount

    if drug_amount < 0 or diluent_amount < 0:
        return _fail("Invalid combination of strengths and volume.")

    return _ok(
        drug_amount_ml=drug_amount,
        diluent_amount_ml=diluent_amount,
        available_strength=c1,
        required_strength=c2,
        final_volume_ml=v2,
    )


# ---------------------------------------------------------------------------
# 4. IV Flow Rate Calculator
# ---------------------------------------------------------------------------
def iv_flow_calculator(total_volume_ml, time_hours, drop_factor):
    v = _to_float(total_volume_ml)
    t = _to_float(time_hours)
    f = _to_float(drop_factor)

    if v is None or t is None or f is None:
        return _fail("Please enter valid numbers in all fields.")
    if v <= 0:
        return _fail("Volume must be greater than zero.")
    if t <= 0:
        return _fail("Time must be greater than zero.")
    if f <= 0:
        return _fail("Drop factor must be greater than zero.")

    ml_per_hour = v / t
    drops_per_min = (v * f) / (t * 60.0)

    return _ok(
        ml_per_hour=ml_per_hour,
        drops_per_minute=drops_per_min,
        total_volume_ml=v,
        time_hours=t,
        drop_factor=f,
    )


# ---------------------------------------------------------------------------
# 5. Infusion Rate Calculator
# ---------------------------------------------------------------------------
def infusion_calculator(volume_ml, duration_hours):
    v = _to_float(volume_ml)
    t = _to_float(duration_hours)

    if v is None or t is None:
        return _fail("Please enter valid numbers in all fields.")
    if v <= 0:
        return _fail("Volume must be greater than zero.")
    if t <= 0:
        return _fail("Duration must be greater than zero.")

    ml_per_hour = v / t
    return _ok(
        ml_per_hour=ml_per_hour,
        volume_ml=v,
        duration_hours=t,
    )


# ---------------------------------------------------------------------------
# 6. BMI Calculator
# ---------------------------------------------------------------------------
def bmi_calculator(weight_kg, height_cm):
    w = _to_float(weight_kg)
    h = _to_float(height_cm)

    if w is None or h is None:
        return _fail("Please enter valid numbers in all fields.")
    if w <= 0:
        return _fail("Weight must be greater than zero.")
    if h <= 0:
        return _fail("Height must be greater than zero.")

    height_m = h / 100.0
    bmi = w / (height_m * height_m)

    if bmi < 16.0:
        category = "Severe Thinness"
    elif bmi < 17.0:
        category = "Moderate Thinness"
    elif bmi < 18.5:
        category = "Mild Thinness"
    elif bmi < 25.0:
        category = "Normal"
    elif bmi < 30.0:
        category = "Overweight"
    elif bmi < 35.0:
        category = "Obese Class I"
    elif bmi < 40.0:
        category = "Obese Class II"
    else:
        category = "Obese Class III"

    return _ok(
        bmi=bmi,
        category=category,
        weight_kg=w,
        height_cm=h,
    )


# ---------------------------------------------------------------------------
SAFETY_DISCLAIMER = (
    "Calculation result only. Always verify with physician orders, "
    "institutional policy, and medication references before clinical use."
)