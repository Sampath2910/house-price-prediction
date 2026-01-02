import pandas as pd
import csv
from pathlib import Path

# ======================================
# Absolute Paths Setup
# ======================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = DATA_DIR / "combined_data.csv"

print(f"📁 Base directory: {BASE_DIR}")
print(f"📁 Data folder: {DATA_DIR}")

# ======================================
# Find all CSV files
# ======================================
csv_files = [f for f in DATA_DIR.glob("*.csv") if f.name != "combined_data.csv"]

if not csv_files:
    print("❌ No CSV files found in /data.")
    exit()

print("\n📂 Found CSV files:")
for f in csv_files:
    print("  -", f.name)

datasets = {}

# ======================================
# Auto-detect delimiter and encoding
# ======================================
def smart_read_csv(filepath):
    encodings = ["utf-8", "utf-16", "ISO-8859-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as file:
                sample = file.read(2048)
                dialect = csv.Sniffer().sniff(sample)
                sep = dialect.delimiter
            df = pd.read_csv(filepath, encoding=enc, sep=sep)
            if df.shape[1] > 1:
                print(f"✅ {filepath.name:30s} — encoding={enc}, sep='{sep}', cols={df.shape[1]}")
                return df
        except Exception:
            continue
    print(f"⚠️ Could not auto-parse {filepath.name}, using default comma")
    return pd.read_csv(filepath, encoding="utf-8", sep=",")

# ======================================
# Load datasets
# ======================================
for f in csv_files:
    try:
        # Special handling for AmesHousing
        if f.name.lower().startswith("ameshousing"):
            print(f"⚙️ Special handling for {f.name}")
            df = pd.read_csv(f, header=None)
            # Drop first column if it’s all NaN or blank
            if df.shape[1] > 0 and (
                df.iloc[:, 0].isnull().all() or str(df.columns[0]).strip() == ""
            ):
                df = df.drop(df.columns[0], axis=1)
            # Add placeholder column names
            df.columns = [f"feature_{i}" for i in range(df.shape[1] - 1)] + ["sale_price"]
            print(f"✅ Loaded {f.name:30s} (no header fix applied, {df.shape[1]} columns)")
        else:
            df = smart_read_csv(f)
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
                .str.replace("-", "_")
            )

        datasets[f.name] = df

    except Exception as e:
        print(f"❌ Error loading {f.name}: {e}")

if not datasets:
    print("❌ No valid datasets loaded.")
    exit()

# ======================================
# Normalize price column
# ======================================
for name, df in datasets.items():
    for t in ["price", "saleprice", "sale_price", "house_price", "target"]:
        if t in df.columns:
            df.rename(columns={t: "sale_price"}, inplace=True)

# ======================================
# Merge all columns (union)
# ======================================
all_cols = set().union(*(set(df.columns) for df in datasets.values()))
for k in datasets:
    datasets[k] = datasets[k].reindex(columns=all_cols)

combined_df = pd.concat(datasets.values(), ignore_index=True)
combined_df.drop_duplicates(inplace=True)
combined_df.dropna(subset=["sale_price"], inplace=True)

# ======================================
# Save Combined File
# ======================================
combined_df.to_csv(OUTPUT_FILE, index=False)
print(f"\n💾 Combined dataset saved successfully to: {OUTPUT_FILE}")
print(f"✅ Final shape: {combined_df.shape}")

# ======================================
# Summary of what was loaded
# ======================================
print("\n📊 Summary of loaded datasets:")
for name, df in datasets.items():
    print(f"  {name:30s} → {df.shape[0]:6d} rows × {df.shape[1]:3d} cols")

print(f"\n🧾 Total rows merged: {combined_df.shape[0]:,}")
print(f"🧩 Total unique columns: {len(all_cols)}")
