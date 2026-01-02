import kagglehub
import shutil
from pathlib import Path

# Target data directory
target_dir = Path("../data")
target_dir.mkdir(exist_ok=True)

datasets = {
    "ames": "shashanknecrothapa/ames-housing-dataset",
    "india": "mohamedafsal007/house-price-dataset-of-india",
    "metro": "ruchi798/housing-prices-in-metropolitan-areas-of-india"
}

for name, dataset in datasets.items():
    print(f"📦 Downloading {dataset} ...")
    path = Path(kagglehub.dataset_download(dataset))
    print("   ✅ Downloaded to:", path)

    # Copy all CSV files from dataset folder to data/
    for csv_file in path.rglob("*.csv"):
        dest = target_dir / csv_file.name
        shutil.copy(csv_file, dest)
        print(f"   📁 Copied {csv_file.name} → {dest}")

print("✅ All datasets downloaded and copied to /data folder.")
