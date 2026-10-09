# BMI Calculator — OIBSIP Python Task 2

**Track:** Python Programming | **Task:** Task 2 — BMI Calculator

## Overview
A Python BMI calculator with a Tkinter GUI, input validation, BMI classification, named-user history saved to SQLite, and an optional Matplotlib trend chart.

## Feature checklist
### Beginner
- [x] Weight in kilograms and height in meters
- [x] BMI formula: `weight / (height ** 2)`
- [x] Underweight (<18.5), Normal (18.5–24.9), Overweight (25–29.9), Obese (≥30)
- [x] BMI rounded to 2 decimals and category displayed
- [x] Non-numeric, zero, and negative input validation

### Advanced
- [x] Tkinter GUI and Calculate button
- [x] Colour-coded categories
- [x] Named-user records
- [x] SQLite history
- [x] History view
- [x] Optional Matplotlib BMI trend chart
- [x] Database error handling

## Run on a computer
Install Python 3.10+. In a terminal opened in this folder:
```bash
python -m pip install -r requirements.txt
python bmi_calculator.py
```
Tkinter is included with most standard Python installations. On some Linux systems install `python3-tk`.

## Google Colab
Colab usually cannot display desktop Tkinter windows. Use the command-line mode:
```bash
python bmi_calculator.py --cli
```

## Example
60 kg and 1.65 m gives BMI 22.04, category Normal.

## Privacy
Records are saved locally in `bmi_history.db`; no data is sent to an external service. The database is excluded by `.gitignore`. Do not upload real personal data. BMI is a general adult screening measure, not a medical diagnosis.

## Submission
Put this folder inside the shared repository named exactly `OIBSIP` at:
`OIBSIP/Python-L1-Task2-BMICalculator/`

Add real screenshots, test the app, record a demo video, and share it on LinkedIn. The internship guide requests tagging `@Oasis Infobyte` and including `#oasisinfobyte`.
