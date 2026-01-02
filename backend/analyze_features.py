import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the trained pipeline
pipeline = joblib.load("../models/pipeline.joblib")

# Extract model and preprocessor
model = pipeline.named_steps["model"]
preprocessor = pipeline.named_steps["preprocessor"]

# Get all feature names after preprocessing
feature_names = preprocessor.get_feature_names_out()

# Get feature importance values from XGBoost
importances = model.feature_importances_

# Combine into a DataFrame
feat_imp = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

print("✅ Top 20 most important features:")
print(feat_imp.head(20))

# Plot top 20 features
plt.figure(figsize=(10, 6))
plt.barh(feat_imp.head(20)["Feature"], feat_imp.head(20)["Importance"])
plt.gca().invert_yaxis()
plt.xlabel("Importance")
plt.title("Top 20 Most Important Features Influencing House Price")
plt.tight_layout()
plt.show()
