from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# Place your calculate_news_score function here
def calculate_news_score(temperature, oxygen_saturation, heart_rate, respiratory_rate, systolic_bp, avpu):
    # Initialize the NEWS score
    news_score = 0

    # Calculate the score for Temperature
    if 36.1 <= temperature <= 38.0:
        news_score += 0
    elif 35.1 <= temperature < 36.1 or 38.1 <= temperature <= 39.0:
        news_score += 1
    elif temperature > 39.1:
        news_score += 2
    elif temperature < 35.0:
        news_score += 3

    # Calculate the score for Oxygen Saturation
    if oxygen_saturation > 96:
        news_score += 0
    elif 94 <= oxygen_saturation <= 95:
        news_score += 1
    elif 92 <= oxygen_saturation <= 93:
        news_score += 2
    elif oxygen_saturation < 91:
        news_score += 3

    # Calculate the score for Heart Rate
    if 51 <= heart_rate <= 90:
        news_score += 0
    elif (41 <= heart_rate <= 50) or (91 <= heart_rate <= 110):
        news_score += 1
    elif 111 <= heart_rate <= 130:
        news_score += 2
    elif heart_rate > 131 or heart_rate < 40:
        news_score += 3

    # Calculate the score for Respiratory Rate
    if 12 <= respiratory_rate <= 20:
        news_score += 0
    elif 9 <= respiratory_rate <= 11:
        news_score += 1
    elif 21 <= respiratory_rate <= 24:
        news_score += 2
    elif respiratory_rate > 25 or respiratory_rate < 8:
        news_score += 3

    # Calculate the score for Systolic Blood Pressure
    if 111 <= systolic_bp <= 219:
        news_score += 0
    elif 101 <= systolic_bp <= 110:
        news_score += 1
    elif 91 <= systolic_bp <= 100:
        news_score += 2
    elif systolic_bp < 90 or systolic_bp > 220:
        news_score += 3

    # Calculate the score for AVPU level
    if avpu == 'A':
        news_score += 0
    elif avpu in ['V', 'P', 'U']:
        news_score += 3

    print(f"Received values: {temperature}, {oxygen_saturation}, {heart_rate}, {respiratory_rate}, {systolic_bp}, {avpu}")
    return news_score


# Importing necessary libraries

# Defining the universe of discourse for each variable
sv_universe = np.arange(0, 1.1, 0.1) # Assuming a normalized score from 0 to 1
bd_universe = np.arange(0, 1.1, 0.1) # Assuming a normalized score from 0 to 1
rf_universe = np.arange(0, 1.1, 0.1) # Assuming a normalized score from 0 to 1
rs_universe = np.arange(0, 1.1, 0.1) # Assuming a normalized score from 0 to 1
severity_universe = np.arange(0, 1.1, 0.1) # Assuming a normalized score from 0 to 1

# Defining the antecedents and consequent with their respective universes
sv = ctrl.Antecedent(sv_universe, 'sv')
bd = ctrl.Antecedent(bd_universe, 'bd')
rf = ctrl.Antecedent(rf_universe, 'rf')
rs = ctrl.Antecedent(rs_universe, 'rs')
severity = ctrl.Consequent(severity_universe, 'severity')

# Defining the membership functions based on the provided diagram
sv['low'] = fuzz.trapmf(sv_universe, [0, 0, 4, 5])
sv['medium'] = fuzz.trapmf(sv_universe, [4, 5, 6, 7])
sv['high'] = fuzz.trapmf(sv_universe, [6, 7, 18, 18])

bd['minimal_or_absent'] = fuzz.trapmf(bd_universe, [0, 0, 0.25, 0.25])
bd['high'] = fuzz.trimf(bd_universe, [0.25, 0.5, 0.75])
bd['very_high'] = fuzz.trapmf(bd_universe, [0.75, 0.75, 1, 1])

rf['minimal_or_absent'] = fuzz.trapmf(rf_universe, [0, 0, 0.4, 0.6])
rf['meaningful'] = fuzz.trapmf(rf_universe, [0.4, 0.6, 1, 1])

rs['minimal_or_absent'] = fuzz.trapmf(rs_universe, [0, 0, 0.4, 0.6])
rs['meaningful'] = fuzz.trapmf(rs_universe, [0.4, 0.6, 1, 1])

severity['mild'] = fuzz.trimf(severity_universe, [0, 0, 0.3])
severity['moderate'] = fuzz.trimf(severity_universe, [0.2, 0.5, 0.8])
severity['severe'] = fuzz.trimf(severity_universe, [0.7, 0.7, 1])


# Repeat the above step for the rest of the variables...

# Define the fuzzy rules as per the paper's guidelines
# Note: The following rules are placeholders and should be replaced with actual rules from the paper
rule1 = ctrl.Rule(antecedent=(sv['low'] & bd['minimal_or_absent'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['mild'])
rule2 = ctrl.Rule(antecedent=(sv['low'] & bd['minimal_or_absent'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['mild'])
rule3 = ctrl.Rule(antecedent=(sv['low'] & bd['minimal_or_absent'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['mild'])
rule4 = ctrl.Rule(antecedent=(sv['low'] & bd['minimal_or_absent'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule5 = ctrl.Rule(antecedent=(sv['low'] & bd['high'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['moderate'])
rule6 = ctrl.Rule(antecedent=(sv['low'] & bd['high'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule7 = ctrl.Rule(antecedent=(sv['low'] & bd['high'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule8 = ctrl.Rule(antecedent=(sv['low'] & bd['high'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule9 = ctrl.Rule(antecedent=(sv['low'] & bd['very_high'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule10 = ctrl.Rule(antecedent=(sv['low'] & bd['very_high'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule11 = ctrl.Rule(antecedent=(sv['low'] & bd['very_high'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule12 = ctrl.Rule(antecedent=(sv['low'] & bd['very_high'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule13 = ctrl.Rule(antecedent=(sv['medium'] & bd['minimal_or_absent'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['mild'])
rule14 = ctrl.Rule(antecedent=(sv['medium'] & bd['minimal_or_absent'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['moderate'])
rule15 = ctrl.Rule(antecedent=(sv['medium'] & bd['minimal_or_absent'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['moderate'])
rule16 = ctrl.Rule(antecedent=(sv['medium'] & bd['minimal_or_absent'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['moderate'])
rule17 = ctrl.Rule(antecedent=(sv['medium'] & bd['high'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['moderate'])
rule18 = ctrl.Rule(antecedent=(sv['medium'] & bd['high'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule19 = ctrl.Rule(antecedent=(sv['medium'] & bd['high'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule20 = ctrl.Rule(antecedent=(sv['medium'] & bd['high'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule21 = ctrl.Rule(antecedent=(sv['medium'] & bd['very_high'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule22 = ctrl.Rule(antecedent=(sv['medium'] & bd['very_high'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule23 = ctrl.Rule(antecedent=(sv['medium'] & bd['very_high'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule24 = ctrl.Rule(antecedent=(sv['medium'] & bd['very_high'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule25 = ctrl.Rule(antecedent=(sv['high'] & bd['minimal_or_absent'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['moderate'])
rule26 = ctrl.Rule(antecedent=(sv['high'] & bd['minimal_or_absent'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule27 = ctrl.Rule(antecedent=(sv['high'] & bd['minimal_or_absent'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule28 = ctrl.Rule(antecedent=(sv['high'] & bd['minimal_or_absent'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule29 = ctrl.Rule(antecedent=(sv['high'] & bd['high'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule30 = ctrl.Rule(antecedent=(sv['high'] & bd['high'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule31 = ctrl.Rule(antecedent=(sv['high'] & bd['high'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule32 = ctrl.Rule(antecedent=(sv['high'] & bd['high'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])
rule33 = ctrl.Rule(antecedent=(sv['high'] & bd['very_high'] & rf['minimal_or_absent'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule34 = ctrl.Rule(antecedent=(sv['high'] & bd['very_high'] & rf['minimal_or_absent'] & rs['meaningful']),
                  consequent=severity['severe'])
rule35 = ctrl.Rule(antecedent=(sv['high'] & bd['very_high'] & rf['meaningful'] & rs['minimal_or_absent']),
                  consequent=severity['severe'])
rule36 = ctrl.Rule(antecedent=(sv['high'] & bd['very_high'] & rf['meaningful'] & rs['meaningful']),
                  consequent=severity['severe'])

# Create the control system and simulation object
triage_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                  rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20,
                                  rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30,
                                  rule31, rule32, rule33, rule34, rule35, rule36])
triage_sim = ctrl.ControlSystemSimulation(triage_ctrl)

# Function to evaluate the triage system
def evaluate_triage(sv_val, bd_val, rf_val, rs_val):
    # Pass inputs to the ControlSystem
    triage_sim.input['sv'] = sv_val
    triage_sim.input['bd'] = bd_val
    triage_sim.input['rf'] = rf_val
    triage_sim.input['rs'] = rs_val

    # Crunch the numbers
    triage_sim.compute()

    # Define values for each membership degree in severity
    mild = fuzz.interp_membership(severity_universe, severity['mild'].mf, triage_sim.output['severity'])
    moderate = fuzz.interp_membership(severity_universe, severity['moderate'].mf, triage_sim.output['severity'])
    severe = fuzz.interp_membership(severity_universe, severity['severe'].mf, triage_sim.output['severity'])

    return mild, moderate, severe


@app.route('/')
def index():
    return render_template('patient.html')

@app.route('/process', methods=['POST'])
def process():
    # Extracting other form data as before
    temperature = float(request.form.get('temperature', 0))
    oxygen_saturation = int(request.form.get('o2-saturation', 0))
    heart_rate = int(request.form.get('heart-rate', 0))
    respiratory_rate = int(request.form.get('breath-rate', 0))
    systolic_bp = int(request.form.get('blood-pressure', 0))
    avpu_level = request.form.get('avpu-level', 'A')
    breathing_difficulty = float(request.form.get('breathing-difficulty', 0))

    # Handling checkbox values for risk factors and other risks
    risk_factors = ['60-years', 'smoking', 'obese', 'asthma', 'pregnant', 'diabetic', 'heart-disease']
    risk_factors_score = sum(1 for factor in risk_factors if request.form.get(factor) == 'on') / 7

    other_risks = ['fever', 'diarrhea', 'cough', 'weak', 'chest-pain', 'dehydration']
    other_risks_score = sum(1 for risk in other_risks if request.form.get(risk) == 'on') / 6

    # Calculating NEWS score
    news_score = calculate_news_score(temperature, oxygen_saturation, heart_rate, respiratory_rate, systolic_bp, avpu_level)
    
    # Evaluating triage with breathing difficulty, risk factors score, and other risks score
    mild_deg, moderate_deg, severe_deg = evaluate_triage(news_score, breathing_difficulty, risk_factors_score, other_risks_score)
    print(mild_deg, moderate_deg, severe_deg)
        # Determine the highest value
    max_value = max(mild_deg, moderate_deg, severe_deg)
    if max_value == mild_deg:
        priority = 'low'
    elif max_value == moderate_deg:
        priority = 'medium'
    else:
        priority = 'high'

    # Render the template with the priority level
    return render_template('result_fragment.html', priority=priority)

@app.route('/patient')
def patient():
    return render_template('patient.html')


if __name__ == '__main__':
    app.run(debug=True)
