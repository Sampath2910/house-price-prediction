import joblib

pipeline = joblib.load("../models/pipeline.joblib")

# Get all columns expected after preprocessing
try:
    print("🧩 Feature columns in trained model:")
    print(pipeline.named_steps["preprocessor"].get_feature_names_out())
except Exception as e:
    print("Error fetching columns:", e)
