# 🏥 MedReach (SIH 26133)
**Bridging the Gap in Rural Healthcare Access & Quality**

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Framework-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**MedReach** is a comprehensive, ecosystem-driven prototype built for the **Smart India Hackathon (Problem Statement 26133)** by the Government of Maharashtra. It provides an integrated care-access and quality support solution specifically tailored for rural, low-connectivity, and underserved areas.

---

## 🌟 Key Features Implemented

### 1. 📱 Dual-Flow USSD & IVR Gateway
* **Problem:** 60% of rural India lacks smartphones/internet.
* **Solution:** A feature-phone accessible gateway (`*444#`).
  * **Patient Mode:** Fully numbered menus (no typing required) to request doctor callbacks, check PHC queues, and trigger 108 emergencies.
  * **ASHA Worker Mode:** Advanced text-input menus to book appointments via ABHA ID, run AI Triage, and check live medicine inventory.

### 2. 🤖 Multilingual AI Triage (Bhashini Integrated)
* **Problem:** Language barriers in rural healthcare.
* **Solution:** An AI symptom checker that understands native inputs (e.g., Marathi: *"mala tap ahe"* or Hindi: *"mujhe bukhar hai"*), assigns a Red/Yellow/Green clinical severity tag, and replies in the local language.

### 3. 📶 Offline-First ASHA Companion App
* **Problem:** Sub-centres often lack network connectivity.
* **Solution:** A mobile-first interface designed for frontline workers that caches data locally. Features include high-risk patient alerts (e.g., ANC visits) and a one-tap **SOS Emergency Escalation** that dispatches ambulances and alerts district hospitals instantly.

### 4. 📋 ABDM-Compliant Longitudinal Records & Dashboards
* **Problem:** Fragmented patient history across Sub-centres, PHCs, and District Hospitals.
* **Solution:** A unified dashboard tracking the entire patient journey. 
  * **Smart Referral Tracking:** End-to-end status tracking from initiation to completion.
  * **Live Medicine Inventory:** Real-time visibility into local stockouts.
  * **Queue Management:** Token-based queue generation with live estimated wait times.

### 5. 🩺 Assisted Teleconsultation & Facility Locator
* **Assisted Teleconsultation:** Connects pooled specialists with patients via ASHA workers, featuring live vital syncing and e-prescriptions.
* **Live Facility Map:** GPS locator showing the nearest facilities, live wait times, and active doctor counts.

---

## 🛠️ Technical Architecture (Under the Hood)
While this repository contains the rapid prototype, the production architecture utilizes:
* **APIs:** Africa's Talking (USSD), Bhashini (Translation), ABDM Sandbox (HL7 FHIR R4).
* **Offline Sync:** IndexedDB / PouchDB with background Service Workers (CRDTs).
* **Teleconsultation:** Low-bandwidth WebRTC with local STUN/TURN servers.
* **Frontend:** HTML5, Bootstrap 5, Chart.js, Leaflet.js.
* **Backend:** Python (Flask), SQLite/PostgreSQL.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/suryaa2106/SIH26133.git
   cd SIH26133
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```bash
   python app.py
   ```

4. **Access the prototype:**
   Open your browser and navigate to `http://127.0.0.1:5000/`

---
