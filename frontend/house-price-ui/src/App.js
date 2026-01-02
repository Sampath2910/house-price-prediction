import React, { useState } from "react";

export default function App() {
  const [formData, setFormData] = useState({
    location: "",
    area: "",
    bedrooms: "",
    bathrooms: "",
    multipurpose_room: "No",
    golfcourse_view: "No",
    ac: "No",
    floors: "",
    garage: "No",
    swimmingpool: "No",
    distance_mainroad: "",
    distance_railway: "",
    distance_busstop: "",
    nearby_schools: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setPrediction(null);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      setLoading(false);
      if (result.status === "success") {
        setPrediction(result.predicted_price);
      } else {
        setError(result.message);
      }
    } catch (err) {
      setLoading(false);
      setError("❌ Could not connect to the backend API. Is Flask running?");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center p-6">
      <div className="bg-white shadow-2xl rounded-2xl w-full max-w-2xl p-10 border border-emerald-100">
        <h1 className="text-3xl font-bold text-center text-emerald-700 mb-10 flex items-center justify-center gap-2">
          🏠 House Price Predictor
        </h1>

        <form onSubmit={handleSubmit} className="space-y-5">
          {[
            { label: "🏙️ Location", name: "location", type: "text", placeholder: "Enter city or area (e.g., Hyderabad)" },
            { label: "📏 Area (sqft)", name: "area", type: "number", placeholder: "e.g., 2000" },
            { label: "🛏 Bedrooms", name: "bedrooms", type: "number", placeholder: "e.g., 3" },
            { label: "🛁 Bathrooms", name: "bathrooms", type: "number", placeholder: "e.g., 2" },
            { label: "🏢 No. of Floors", name: "floors", type: "number", placeholder: "e.g., 2" },
            { label: "🛣️ Distance to Main Road (m)", name: "distance_mainroad", type: "number", placeholder: "e.g., 100" },
            { label: "🚉 Nearby Railway Station (km)", name: "distance_railway", type: "number", placeholder: "e.g., 3" },
            { label: "🚌 Nearby Bus Stop (m)", name: "distance_busstop", type: "number", placeholder: "e.g., 250" },
            { label: "🏫 Nearby Schools (count)", name: "nearby_schools", type: "number", placeholder: "e.g., 4" },
          ].map((field) => (
            <div key={field.name}>
              <label className="block text-gray-700 font-semibold mb-1">
                {field.label}
              </label>
              <input
                type={field.type}
                name={field.name}
                placeholder={field.placeholder}
                value={formData[field.name]}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-emerald-400 outline-none"
                required={["location", "area"].includes(field.name)}
              />
            </div>
          ))}

          <div className="grid grid-cols-2 gap-4 mt-6">
            {[
              { name: "multipurpose_room", label: "🧩 Multipurpose Room" },
              { name: "golfcourse_view", label: "⛳ Golf Course View" },
              { name: "ac", label: "❄️ Air Conditioning (AC)" },
              { name: "garage", label: "🚗 Garage Availability" },
              { name: "swimmingpool", label: "🏊 Swimming Pool" },
            ].map((field) => (
              <div key={field.name}>
                <label className="block text-gray-700 font-semibold mb-1">
                  {field.label}
                </label>
                <select
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-emerald-400"
                >
                  <option>No</option>
                  <option>Yes</option>
                </select>
              </div>
            ))}
          </div>

          <button
            type="submit"
            className="w-full mt-8 bg-emerald-500 text-white py-3 rounded-xl hover:bg-emerald-600 transition-all font-semibold text-lg shadow-md"
          >
            {loading ? "⏳ Predicting..." : "🔍 Predict Price"}
          </button>
        </form>

        <div className="mt-8 text-center">
          {prediction && (
            <p className="text-2xl font-semibold text-emerald-700 bg-emerald-50 py-3 rounded-xl shadow-sm">
                💰 Predicted Price: ₹{Number(prediction).toLocaleString("en-IN", { maximumFractionDigits: 2 })}

            </p>
        )}

          {error && (
            <p className="text-red-600 font-medium mt-2 bg-red-50 py-2 rounded-md">
              {error}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
