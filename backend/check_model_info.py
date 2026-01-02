import joblib

# Load your trained pipeline
pipeline = joblib.load("../models/pipeline.joblib")

# Access the preprocessor
preprocessor = pipeline.named_steps["preprocessor"]

print("\n✅ Preprocessor found:", type(preprocessor))

# The categorical part (should be 'cat')
cat_transformer = preprocessor.named_transformers_.get("cat")

print("🔍 Category transformer type:", type(cat_transformer))

# If it's a pipeline, extract the encoder
if hasattr(cat_transformer, "named_steps"):
    encoder = cat_transformer.named_steps.get("encoder") or cat_transformer.named_steps.get("onehotencoder")
    print("🧠 Extracted encoder from inside pipeline:", type(encoder))
else:
    encoder = cat_transformer


# Print categories
if hasattr(encoder, "categories_"):
    print("\n✅ OneHotEncoder categories for 'location':")
    for i, cats in enumerate(encoder.categories_):
        print(f"  Feature {i}: {list(cats)[:20]}{'...' if len(cats) > 20 else ''}")
else:
    print("\n⚠️ No categories_ attribute found. The encoder might not be an sklearn OneHotEncoder.")
