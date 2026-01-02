import subprocess
import time
import requests
import sys
import os

# Step 1: Start the Flask server
print("🚀 Starting Flask server...")
server = subprocess.Popen(
    [sys.executable, "app_api.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Step 2: Wait for the server to start
print("⏳ Waiting for Flask server to initialize...")
time.sleep(8)  # wait a bit longer to let the model load

# Step 3: Test connection loop (retry until server is live)
url = "http://127.0.0.1:5000/predict"
for i in range(5):
    try:
        print(f"🔍 Attempt {i+1}: Checking server connection...")
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code in [200, 404]:
            print("✅ Flask server is ready!")
            break
    except:
        time.sleep(2)
else:
    print("❌ Server did not start. Check app_api.py logs below.")
    out, err = server.communicate(timeout=5)
    print("STDOUT:", out.decode())
    print("STDERR:", err.decode())
    server.terminate()
    sys.exit(1)

# Step 4: Send test prediction
data = {
    "city": "Hyderabad",
    "bedrooms": 3,
    "bathrooms": 2,
    "area": 1600,
    "year_built": 2015,
    "condition": "Good",
    "garage_type": "Attached",
    "lot_area": 2000,
    "roof_matl": "CompShg"
}

print("📡 Sending test request to API...")
try:
    response = requests.post(url, json=data)
    print("✅ Response received!")
    print(response.json())
except Exception as e:
    print("❌ Error while testing API:", e)

# Step 5: Stop the server
server.terminate()
print("🛑 Server stopped.")
