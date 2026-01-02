import joblib
import pandas as pd

# ======================================================
# Load the trained model
# ======================================================
pipeline = joblib.load("../models/pipeline.joblib")
print("✅ Model loaded successfully!")

# ======================================================
# Define test samples (various cities & house types)
# ======================================================
samples = [
    # 🏠 Small houses
    {"location": "hyderabad", "area": 800, "no._of_bedrooms": 2, "bathrooms": 2},
    {"location": "mumbai", "area": 850, "no._of_bedrooms": 2, "bathrooms": 1},
    {"location": "delhi", "area": 900, "no._of_bedrooms": 2, "bathrooms": 2},

    # 🏡 Medium houses
    {"location": "chennai", "area": 1500, "no._of_bedrooms": 3, "bathrooms": 2, "ac": 1},
    {"location": "kolkata", "area": 1800, "no._of_bedrooms": 3, "bathrooms": 3, "wifi": 1},
    {"location": "hyderabad", "area": 2000, "no._of_bedrooms": 3, "bathrooms": 3, "garage": 1},

    # 🏰 Luxury houses
    {"location": "mumbai", "area": 3200, "no._of_bedrooms": 4, "bathrooms": 4, "ac": 1, "swimmingpool": 1},
    {"location": "delhi", "area": 3500, "no._of_bedrooms": 5, "bathrooms": 4, "golfcourse": 1, "ac": 1},
    {"location": "hyderabad", "area": 4000, "no._of_bedrooms": 5, "bathrooms": 5, "swimmingpool": 1, "gymnasium": 1},
]

# ======================================================
# Helper function for safe prediction
# ======================================================
def safe_predict(pipeline, data: dict):
    df = pd.DataFrame([data])
    for col in pipeline.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    df = df[pipeline.feature_names_in_]
    return round(float(pipeline.predict(df)[0]), 2)

# ======================================================
# Run predictions for all test samples
# ======================================================
print("\n🏡 Predicted House Prices (Model Comparison):")
print("─" * 85)
print(f"{'City':<12}{'Area (sqft)':<12}{'Bedrooms':<10}{'Baths':<8}{'Amenities':<25}{'Predicted Price (₹)':>20}")
print("─" * 85)

for s in samples:
    amenities = ", ".join([k for k, v in s.items() if v == 1 and k not in ["ac", "wifi", "garage", "swimmingpool", "golfcourse", "gymnasium"]])
    if s.get("ac", 0): amenities += " AC,"
    if s.get("wifi", 0): amenities += " Wi-Fi,"
    if s.get("garage", 0): amenities += " Garage,"
    if s.get("swimmingpool", 0): amenities += " Pool,"
    if s.get("golfcourse", 0): amenities += " Golf,"
    if s.get("gymnasium", 0): amenities += " Gym,"
    amenities = amenities.strip(", ")

    price = safe_predict(pipeline, s)
    print(f"{s['location']:<12}{s['area']:<12}{s.get('no._of_bedrooms', 0):<10}{s.get('bathrooms', 0):<8}{amenities:<25}{price:>20,.2f}")

print("─" * 85)
print("✅ All predictions completed successfully.")
