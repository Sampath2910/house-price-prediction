import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message

# =========================================================
# PATHS
# =========================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD = os.path.abspath(os.path.join(CURRENT_DIR, "..", "frontend", "build"))
MODEL_PATH = os.path.join(CURRENT_DIR, "model", "pipeline.joblib")

print("🔍 FRONTEND_BUILD:", FRONTEND_BUILD)
print("🔍 MODEL_PATH:", MODEL_PATH)

# =========================================================
# FLASK APP
# =========================================================
app = Flask(__name__, static_folder=FRONTEND_BUILD, static_url_path="/")
from flask_cors import CORS

CORS(app, resources={
    r"/*": {
        "origins": [
            "https://house-price-prediction-frontend-w35f.onrender.com"
        ]
    }
})


# =========================================================
# EMAIL CONFIGURATION
# =========================================================
# =========================================================
# EMAIL CONFIGURATION
# =========================================================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")

if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
    raise RuntimeError("❌ MAIL_USERNAME or MAIL_PASSWORD not set in environment variables")

mail = Mail(app)


# =========================================================
# LOAD MODEL
# =========================================================
try:
    pipeline = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully from:", MODEL_PATH)
except Exception as e:
    print("❌ Failed to load model:", e)
    pipeline = None

# =========================================================
# SERVE FRONTEND (ALL ROUTES)
# =========================================================
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    from pathlib import Path
    requested_path = Path(FRONTEND_BUILD) / path
    if path and requested_path.exists():
        return send_from_directory(FRONTEND_BUILD, path)
    else:
        return send_from_directory(FRONTEND_BUILD, "index.html")

# =========================================================
# PRICE PREDICTION ENDPOINT
# =========================================================
@app.route("/predict", methods=["POST"])
def predict():
    if pipeline is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    try:
        data = request.get_json() or {}
        print("📩 Received data:", data)

        # --- Exact raw features used in training ---
        RAW_FEATURES = [
            "location", "area", "no._of_bedrooms", "bathrooms", "multipurposeroom",
            "golfcourse", "ac", "floors", "garage", "swimmingpool", "distance_mainroad",
            "distance_railway", "distance_busstop", "nearby_schools", "sofa", "bed",
            "landscapedgardens", "24x7security", "microwave", "powerbackup",
            "washingmachine", "wifi", "shoppingmall", "carparking", "gymnasium",
            "liftavailable", "school", "joggingtrack", "clubhouse", "vaastucompliant",
            "wardrobe", "rainwaterharvesting", "resale", "tv", "maintenancestaff", "atm",
            "refrigerator", "intercom", "hospital", "indoorgames", "sportsfacility",
            "diningtable", "gasconnection", "children'splayarea", "staffquarter", "cafeteria"
        ]

        def safe_float(v):
            try:
                return float(v) if v not in ("", None) else 0.0
            except:
                return 0.0

        def safe_int(v):
            try:
                return int(float(v)) if v not in ("", None) else 0
            except:
                return 0

        def yes_no_to_int(v):
            if v is None:
                return 0
            if isinstance(v, bool):
                return 1 if v else 0
            s = str(v).strip().lower()
            return 1 if s in ("yes", "y", "true", "1") else 0

        mapping = {
            "location": "location",
            "area": "area",
            "bedrooms": "no._of_bedrooms",
            "bathrooms": "bathrooms",
            "multipurpose_room": "multipurposeroom",
            "golfcourse_view": "golfcourse",
            "ac": "ac",
            "floors": "floors",
            "garage": "garage",
            "swimmingpool": "swimmingpool",
            "distance_mainroad": "distance_mainroad",
            "distance_railway": "distance_railway",
            "distance_busstop": "distance_busstop",
            "nearby_schools": "nearby_schools"
        }

        row = {feat: 0 for feat in RAW_FEATURES}
        for k, raw in mapping.items():
            if k in data:
                v = data[k]
                if raw == "location":
                    row[raw] = str(v).strip().lower()
                elif raw in ("area", "distance_mainroad", "distance_railway", "distance_busstop"):
                    row[raw] = safe_float(v)
                elif raw in ("no._of_bedrooms", "bathrooms", "floors", "nearby_schools"):
                    row[raw] = safe_int(v)
                else:
                    row[raw] = yes_no_to_int(v)

        df = pd.DataFrame([row], columns=RAW_FEATURES)
        for c in RAW_FEATURES:
            if c != "location":
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        print("🧾 Input DataFrame:\n", df.head())
        pred = pipeline.predict(df)[0]
        print("🔮 Prediction:", pred)

        return jsonify({
            "status": "success",
            "predicted_price": round(float(pred), 2),
            "formatted_price": f"₹{float(pred):,.2f}"
        })

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================================================
# CONTACT FORM ENDPOINT
# =========================================================
@app.route("/contact", methods=["POST"])
def contact():
    try:
        data = request.get_json()
        print("📩 Received contact form:", data)

        name = data.get("name", "")
        email = data.get("email", "")
        subject = data.get("subject", "New Inquiry")
        message = data.get("message", "")

        if not email or not message:
            return jsonify({"status": "error", "message": "Email and message are required"}), 400

        msg = Message(
            subject=f"📬 New Contact from {name or 'Unknown'} - {subject}",
            recipients=["akkapallysampath12@gmail.com"],
  # <-- change this to your real receiving address
            body=f"""
You have received a new contact form submission:

👤 Name: {name}
📧 Email: {email}
📝 Subject: {subject}
💬 Message:
{message}

---
Sent from HomeValue AI contact form
"""
        )

        mail.send(msg)
        print("✅ Email sent successfully!")

        return jsonify({"status": "success", "message": "Message sent successfully!"})

    except Exception as e:
        print("❌ Email sending failed:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================================================
# START SERVER
# =========================================================
if __name__ == "__main__":
    app.run()

