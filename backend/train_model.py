import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
import numpy as np
from sklearn import metrics


# ============================================================
# Paths
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "combined_data.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# ============================================================
# Load and Inspect Data
# ============================================================
print(f"📂 Loading dataset from: {DATA_FILE}")
df = pd.read_csv(DATA_FILE, low_memory=False)
print(f"✅ Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]:,} columns")

# Normalize column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# ============================================================
# Define target and features
# ============================================================
expected_features = [
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

target_candidates = ["sale_price", "price", "target"]
target_col = next((c for c in target_candidates if c in df.columns), None)
if not target_col:
    raise ValueError("❌ No target column (sale_price/price/target) found.")

# ============================================================
# Fix missing / inconsistent columns
# ============================================================
# Typo fix: 'neaarby_schools' → 'nearby_schools'
if "neaarby_schools" in df.columns:
    df.rename(columns={"neaarby_schools": "nearby_schools"}, inplace=True)

present_features = [c for c in expected_features if c in df.columns]
missing_features = [c for c in expected_features if c not in df.columns]

print(f"✅ Found {len(present_features)} matching features.")
if missing_features:
    print(f"⚠️ Missing features will be filled with zeros: {missing_features}")

# Fill missing columns
for col in missing_features:
    df[col] = 0

# ============================================================
# Handle location values (the cause of the crash)
# ============================================================
if "location" in df.columns:
    df["location"] = df["location"].astype(str).replace(["nan", "None", "0", "unknown", "NA"], "Unknown")
else:
    df["location"] = "Unknown"

# ============================================================
# Select feature and target data
# ============================================================
df = df.dropna(subset=[target_col])
df = df.fillna(0)
X = df[expected_features]
y = df[target_col]

# Ensure numeric conversion for non-categorical columns
for col in X.columns:
    if col != "location":
        X[col] = pd.to_numeric(X[col], errors="coerce").fillna(0)

# ============================================================
# Preprocessing Pipeline
# ============================================================
numeric_features = [col for col in X.columns if col != "location"]
categorical_features = ["location"]

numeric_transformer = Pipeline(steps=[
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# ============================================================
# Model Setup
# ============================================================
model = XGBRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.9,
    colsample_bytree=0.8,
    random_state=42,
    objective="reg:squarederror"
)

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", model)
])

# ============================================================
# Train/Test Split
# ============================================================
# ============================================================
# Clean target column (convert to numeric, drop invalid)
# ============================================================
y = pd.to_numeric(y, errors="coerce")  # Convert all to float, invalid → NaN
invalid_count = y.isna().sum()
if invalid_count > 0:
    print(f"⚠️ Found {invalid_count} invalid target values — removing them.")
    valid_mask = y.notna()
    X = X.loc[valid_mask]
    y = y.loc[valid_mask]

print(f"✅ Cleaned target column: {len(y):,} valid records.")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ============================================================
# Train Model
# ============================================================
print("🚀 Training the model (this may take a few minutes)...")
pipeline.fit(X_train, y_train)

# ============================================================
# Evaluate Model
# ============================================================
y_pred = pipeline.predict(X_test)
rmse = np.sqrt(metrics.mean_squared_error(y_test, y_pred))
r2 = metrics.r2_score(y_test, y_pred)


print(f"✅ RMSE: {rmse:,.2f}")
print(f"✅ R²: {r2:.3f}")

# ============================================================
# Save Model
# ============================================================
model_path = MODEL_DIR / "pipeline.joblib"
joblib.dump(pipeline, model_path)
print(f"💾 Model saved successfully to {model_path}")

import json
feat_path = MODEL_DIR / "raw_features.json"
with open(feat_path, "w") as f:
    json.dump(expected_features, f)
print("💾 Raw feature list saved to", feat_path)


# ============================================================
# Test One Prediction
# ============================================================
sample = X_test.iloc[0:1]
pred = pipeline.predict(sample)[0]
print(f"🔮 Sample prediction: ₹{pred:,.2f}")
