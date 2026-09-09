from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- MOCK DATA FOR DEMO ---
patients = {
    "P001": {
        "id": "P001", "name": "Ramesh Kumar", "abha_id": "14-2234-5567-8890", "age": 45, "village": "Chandrapur",
        "records": [
            {"date": "2023-05-12", "facility": "Sub-Centre Wadsa", "diagnosis": "Fever", "type": "visit"},
            {"date": "2023-05-14", "facility": "PHC Armori", "diagnosis": "Malaria", "type": "lab_report"},
        ]
    }
}

doctors = [
    {"id": "D1", "name": "Dr. Sharma", "specialty": "General Physician", "status": "Available", "consultations_done": 142},
    {"id": "D2", "name": "Dr. Patil", "specialty": "Pediatrician", "status": "Busy", "consultations_done": 89},
]

queue = [
    {"id": "Q1", "patient": "Suresh", "symptoms": "High fever and chills", "triage": "Yellow", "time": "10:30 AM", "status": "Waiting"},
    {"id": "Q2", "patient": "Anita", "symptoms": "Severe chest pain", "triage": "Red", "time": "10:45 AM", "status": "Escalated to 108"},
]

referrals = [
    {"id": "REF-892", "patient": "Sita Ram", "from_facility": "Sub-Centre Wadsa", "to_facility": "PHC Chandrapur", "reason": "Severe Anemia", "status": "Pending"}
]

inventory = [
    {"item": "Paracetamol", "stock": 450, "status": "Sufficient", "facility": "PHC Chandrapur"},
    {"item": "ORS Packets", "stock": 12, "status": "Critical", "facility": "PHC Chandrapur"},
    {"item": "Iron Folic Acid", "stock": 0, "status": "Stockout", "facility": "Sub-Centre Wadsa"}
]

asha_tasks = [
    {"patient": "Sunita Devi", "task": "ANC Visit (Month 8)", "priority": "High"},
    {"patient": "Rahul", "task": "Immunization Follow-up", "priority": "Medium"}
]

ussd_sessions = {}

@app.route('/')
def index(): return render_template('index.html')

@app.route('/ussd')
def ussd(): return render_template('ussd.html')

@app.route('/triage')
def triage(): return render_template('triage.html')

@app.route('/dashboard')
def dashboard(): return render_template('dashboard.html', queue=queue, doctors=doctors, patients=patients, referrals=referrals, inventory=inventory)

@app.route('/asha')
def asha(): return render_template('asha.html', tasks=asha_tasks)

@app.route('/analytics')
def analytics(): return render_template('analytics.html', inventory=inventory)

@app.route('/teleconsult')
def teleconsult(): 
    patient = request.args.get('patient', 'Suresh')
    return render_template('teleconsult.html', patient=patient)

@app.route('/locator')
def locator(): return render_template('locator.html')

@app.route('/architecture')
def architecture(): return render_template('architecture.html')

@app.route('/api/ussd', methods=['POST'])
def handle_ussd():
    data = request.json
    session_id = data.get('session_id', 'default')
    text = data.get('text', '').strip()
    
    # 1. Initial Entry
    if session_id not in ussd_sessions or text == '*444#':
        ussd_sessions[session_id] = {'state': 'role_select'}
        return jsonify({
            "message": "Welcome to MedReach\nSelect User:\n1. Patient\n2. ASHA Worker", 
            "type": "menu"
        })
    
    state = ussd_sessions[session_id].get('state')
    
    # 2. Role Selection
    if state == 'role_select':
        if text == '1':
            ussd_sessions[session_id]['state'] = 'patient_menu'
            return jsonify({"message": "MedReach Patient Menu:\n1. Doctor Call Me\n2. Check Queue\n3. Emergency (108)", "type": "menu"})
        elif text == '2':
            ussd_sessions[session_id]['state'] = 'asha_menu'
            return jsonify({"message": "MedReach ASHA Menu:\n1. Book Appointment\n2. AI Triage Patient\n3. Check Meds Stock", "type": "menu"})
        else:
            return jsonify({"message": "Invalid option.\n1. Patient\n2. ASHA Worker", "type": "menu"})
            
    # --- PATIENT FLOWS (NO TYPING REQUIRED) ---
    elif state == 'patient_menu':
        if text == '1':
            ussd_sessions[session_id]['state'] = 'end'
            return jsonify({"message": "Request logged! A doctor will call you in 5 mins. Please explain your symptoms on the call.", "type": "end"})
        elif text == '2':
            ussd_sessions[session_id]['state'] = 'end'
            return jsonify({"message": "Nearest PHC (Chandrapur) has 12 patients waiting. Est Wait: 40 mins.", "type": "end"})
        elif text == '3':
            ussd_sessions[session_id]['state'] = 'end'
            return jsonify({"message": "108 Ambulance dispatched to your registered location.", "type": "end"})
        else:
            return jsonify({"message": "Invalid.\n1. Doctor Call Me\n2. Check Queue\n3. Emergency", "type": "menu"})
    
    # --- ASHA WORKER FLOWS (TYPING SUPPORTED) ---
    elif state == 'asha_menu':
        if text == '1':
            ussd_sessions[session_id]['state'] = 'asha_book'
            return jsonify({"message": "Enter Patient ABHA ID or Mobile:", "type": "input"})
        elif text == '2':
            ussd_sessions[session_id]['state'] = 'asha_triage'
            return jsonify({"message": "Enter patient symptoms (e.g. fever, pain):", "type": "input"})
        elif text == '3':
            ussd_sessions[session_id]['state'] = 'asha_med'
            return jsonify({"message": "Enter Medicine Name:", "type": "input"})
        else:
            return jsonify({"message": "Invalid.\n1. Book Appt\n2. AI Triage\n3. Check Meds Stock", "type": "menu"})
            
    elif state == 'asha_book':
        ussd_sessions[session_id]['state'] = 'end'
        return jsonify({"message": f"Appointment successfully booked for {text}. Token #45.", "type": "end"})
        
    elif state == 'asha_triage':
        ussd_sessions[session_id]['state'] = 'end'
        if 'pain' in text.lower() or 'breath' in text.lower() or 'blood' in text.lower():
            triage_res = "RED! High Urgency. Dispatching 108."
        else:
            triage_res = "YELLOW. Moderate. Send patient to nearest PHC."
        return jsonify({"message": f"AI Result: {triage_res}", "type": "end"})
        
    elif state == 'asha_med':
        ussd_sessions[session_id]['state'] = 'end'
        return jsonify({"message": f"Inventory Alert: '{text}' is AVAILABLE at PHC Chandrapur (3km away).", "type": "end"})

    # Fallback
    return jsonify({"message": "Session ended. Dial *444# to restart.", "type": "end"})

@app.route('/api/triage', methods=['POST'])
def process_triage():
    symptoms = request.json.get('symptoms', '').lower()
    
    # 1. MARATHI / HINDI (Emergency - Chest Pain)
    if 'chhatit' in symptoms or 'छातीत' in symptoms or 'seene mein' in symptoms or 'सीने में' in symptoms:
        return jsonify({
            "triage_level": "RED", 
            "recommendation": "आणीबाणी! 108 रुग्णवाहिका त्वरित पाठवत आहे. (Emergency! Dispatching 108 Ambulance immediately.)"
        })
        
    # 2. MARATHI / HINDI (Moderate - Fever)
    elif 'tap' in symptoms or 'ताप' in symptoms or 'bukhar' in symptoms or 'बुखार' in symptoms:
        return jsonify({
            "triage_level": "YELLOW", 
            "recommendation": "मध्यम निकड. कृपया 24 तासांच्या आत जवळच्या PHC ला भेट द्या. (Moderate urgency. Please visit nearest PHC within 24 hours. Token #12 generated.)"
        })
        
    # 3. ENGLISH (Emergency)
    elif 'chest pain' in symptoms or 'breath' in symptoms:
        return jsonify({"triage_level": "RED", "recommendation": "Emergency! Dispatching 108 Ambulance immediately."})
        
    # 4. ENGLISH (Moderate)
    elif 'fever' in symptoms or 'pain' in symptoms:
        return jsonify({"triage_level": "YELLOW", "recommendation": "Moderate urgency. Please visit nearest PHC within 24 hours. Token #12 generated."})
        
    # 5. DEFAULT (Low)
    else:
        return jsonify({
            "triage_level": "GREEN", 
            "recommendation": "काळजीचे कारण नाही. भरपूर द्रव प्या. (Low urgency. Drink plenty of fluids. Doctor will call you.)"
        })

@app.route('/api/queue/accept', methods=['POST'])
def accept_queue():
    q_id = request.json.get('id')
    global queue
    queue = [q for q in queue if q['id'] != q_id]
    return jsonify({"success": True})

@app.route('/api/referral/accept', methods=['POST'])
def accept_referral():
    r_id = request.json.get('id')
    for r in referrals:
        if r['id'] == r_id:
            r['status'] = 'Accepted'
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
