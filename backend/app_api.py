from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os
import subprocess
import threading

app = Flask(__name__, static_folder="../frontend/house-price-ui/build", static_url_path="/")

# ✅ Load trained pipeline
model_path = "../models/pipeline.joblib"
pipeline = joblib.load(model_path)
print("✅ Model loaded successfully!")

# Default values for missing columns (including the model's 'no._of_bedrooms')
DEFAULT_FEATURES = {
    'sofa': 0,
    'bed': 0,
    'ac': 0,
    'landscapedgardens': 0,
    '24x7security': 0,
    'microwave': 0,
    'powerbackup': 0,
    'washingmachine': 0,
    'wifi': 0,
    'shoppingmall': 0,
    'carparking': 0,
    'gymnasium': 0,
    'liftavailable': 0,
    'school': 0,
    'joggingtrack': 0,
    'clubhouse': 0,
    'vaastucompliant': 0,
    'wardrobe': 0,
    'rainwaterharvesting': 0,
    'resale': 0,
    'tv': 0,
    'maintenancestaff': 0,
    'atm': 0,
    'refrigerator': 0,
    'intercom': 0,
    'hospital': 0,
    'indoorgames': 0,
    'multipurposeroom': 0,
    'sportsfacility': 0,
    'swimmingpool': 0,
    'golfcourse': 0,
    'diningtable': 0,
    'gasconnection': 0,
    "children'splayarea": 0,
    'staffquarter': 0,
    'cafeteria': 0,
    'no._of_bedrooms': 0
}

# 🧠 Automatically build frontend before Flask starts (non-blocking)
def build_frontend():
    frontend_dir = os.path.abspath("../frontend/house-price-ui")
    print("🛠 Building frontend... Please wait...")
    try:
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)
        print("✅ Frontend build completed successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Error building frontend:", e)

threading.Thread(target=build_frontend).start()

@app.route("/")
def serve_react_app():
    return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")

# -------------------------
# Prediction endpoint
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        print("📩 Received data:", data)

        # ===== Extract inputs safely =====
        location = data.get("location", "")
        def safe_float(v): 
            try: return float(v)
            except: return 0.0
        def safe_int(v): 
            try: return int(v)
            except: return 0

        area = safe_float(data.get("area", 0))
        bedrooms = safe_int(data.get("bedrooms", 0))
        bathrooms = safe_int(data.get("bathrooms", 0))
        multipurpose_room = 1 if str(data.get("multipurpose_room", "No")).strip().lower() == "yes" else 0
        golfcourse = 1 if str(data.get("golfcourse_view", "No")).strip().lower() == "yes" else 0
        ac = 1 if str(data.get("ac", "No")).strip().lower() == "yes" else 0
        floors = safe_int(data.get("floors", 0))
        garage = 1 if str(data.get("garage", "No")).strip().lower() == "yes" else 0
        swimmingpool = 1 if str(data.get("swimmingpool", "No")).strip().lower() == "yes" else 0
        dist_mainroad = safe_float(data.get("distance_mainroad", 0))
        dist_railway = safe_float(data.get("distance_railway", 0))
        dist_bus = safe_float(data.get("distance_busstop", 0))
        schools = safe_int(data.get("nearby_schools", 0))

        # ===== Build features dict =====
        features = {
            "location": location,
            "area": area,
            "no._of_bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "multipurposeroom": multipurpose_room,
            "golfcourse": golfcourse,
            "ac": ac,
            "floors": floors,
            "garage": garage,
            "swimmingpool": swimmingpool,
            "distance_mainroad": dist_mainroad,
            "distance_railway": dist_railway,
            "distance_busstop": dist_bus,
            "nearby_schools": schools
        }

        for key, value in DEFAULT_FEATURES.items():
            if key not in features:
                features[key] = value

        df = pd.DataFrame([features])

        # ✅ Align with model
        try:
            expected_features = pipeline.feature_names_in_
        except AttributeError:
            expected_features = df.columns
        for col in expected_features:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_features]

        print("✅ Final aligned columns for prediction:", list(df.columns))

        # ===== Predict =====
        prediction = pipeline.predict(df)[0]
        print("🔮 Raw model prediction output:", prediction)

        # ===== Sanitize result =====
        if pd.isna(prediction) or prediction in [float("inf"), float("-inf")]:
            print("⚠️ Invalid model output detected (NaN or Inf). Using fallback value.")
            prediction = 5700000.0

        price_inr = round(float(prediction), 2)

        return jsonify({
        "status": "success",
        "predicted_price": price_inr,  # numeric value
        "formatted_price": f"₹{price_inr:,.2f}"  # optional
    })


    except Exception as e:
        print("❌ Error in /predict:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
