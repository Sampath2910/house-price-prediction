import React, { useState } from "react";

export default function PricePrediction() {
  const [form, setForm] = useState({
    location: "",
    area: "",
    bedrooms: "",
    bathrooms: "",
    floors: "",
    ac: "No",
    garage: "No",
    swimmingpool: "No",
    multipurpose_room: "No",
    golfcourse_view: "No",
    distance_mainroad: "",
    distance_railway: "",
    distance_busstop: "",
    nearby_schools: "",
  });

  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrice(null);
    try {
      const res = await fetch("https://house-price-prediction-7sk1.onrender.com/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (data.status === "success") {
        setPrice(data.predicted_price);
      } else {
        setError(data.message || "Prediction failed");
      }
    } catch (err) {
      setError("Could not connect to backend. Is Flask running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-[#FDF1DE] min-h-screen flex flex-col items-center">
      {/* ===== HERO SECTION ===== */}
      <section className="w-full max-w-6xl flex items-center justify-between py-20 px-10">
        {/* Left - Illustration */}
        <div className="w-1/2 flex justify-center">
          <img
            src="/house.png"
            alt="House Illustration"
            className="w-[80%] rounded-2xl shadow-lg"
          />
        </div>

        {/* Right - Intro Text */}
        <div className="w-1/2 pl-12">
          <h1 className="text-5xl font-extrabold text-[#3E2F1C] mb-4 leading-tight">
            Discover Your Home’s True Value Instantly
          </h1>
          <p className="text-gray-800 text-lg leading-relaxed">
            Accurate home price predictions using advanced machine learning
            algorithms.
          </p>
        </div>
      </section>

      {/* ===== FORM SECTION ===== */}
      <section className="w-full bg-[#FBE8C3] py-16 px-10 flex flex-col items-center rounded-t-3xl shadow-inner">
        <div className="max-w-5xl w-full bg-[#FFF7ED] p-10 rounded-3xl shadow-lg">
          <h2 className="text-4xl font-bold text-center text-[#3E2F1C] mb-4">
            Get Your Home Price Estimate
          </h2>
          <p className="text-center text-gray-700 mb-10 text-lg">
            Enter your home details to receive a price estimate instantly.
          </p>

          <form
            onSubmit={handleSubmit}
            className="grid grid-cols-2 gap-6 max-w-4xl mx-auto"
          >
            {/* Text Inputs */}
            <input name="location" placeholder="Location" value={form.location} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" required />
            <input name="area" placeholder="Area (sqft)" value={form.area} onChange={handleChange} type="number" className="p-4 border border-gray-300 rounded-lg text-lg" required />
            <input name="bedrooms" placeholder="Bedrooms" value={form.bedrooms} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />
            <input name="bathrooms" placeholder="Bathrooms" value={form.bathrooms} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />
            <input name="floors" placeholder="Floors" value={form.floors} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />
            <input name="distance_mainroad" placeholder="Distance to main road (m)" value={form.distance_mainroad} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />
            <input name="distance_railway" placeholder="Distance to railway (m)" value={form.distance_railway} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />
            <input name="distance_busstop" placeholder="Distance to bus stop (m)" value={form.distance_busstop} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />
            <input name="nearby_schools" placeholder="Nearby Schools (count)" value={form.nearby_schools} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg" />

            {/* Dropdowns */}
            <select name="ac" value={form.ac} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg">
              <option>No</option>
              <option>Yes</option>
            </select>

            <select name="garage" value={form.garage} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg">
              <option>No</option>
              <option>Yes</option>
            </select>

            <select name="swimmingpool" value={form.swimmingpool} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg">
              <option>No</option>
              <option>Yes</option>
            </select>

            <select name="multipurpose_room" value={form.multipurpose_room} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg">
              <option>No</option>
              <option>Yes</option>
            </select>

            <select name="golfcourse_view" value={form.golfcourse_view} onChange={handleChange} className="p-4 border border-gray-300 rounded-lg text-lg">
              <option>No</option>
              <option>Yes</option>
            </select>

            <div className="col-span-2 mt-6">
              <button
                type="submit"
                className="w-full bg-[#E17933] text-white py-4 text-xl rounded-lg font-semibold hover:bg-[#cc6525] transition"
              >
                {loading ? "Estimating..." : "Get Estimate"}
              </button>
            </div>
          </form>

          {/* Result */}
          {price !== null && (
            <div className="mt-10 p-6 bg-[#F9FAF5] border border-[#E0C3A1] rounded-xl text-center">
              <p className="text-gray-700 text-lg mb-2">Estimated Market Value</p>
              <h3 className="text-4xl font-bold text-[#3E2F1C]">
                ₹{Number(price).toLocaleString("en-IN")}
              </h3>
            </div>
          )}
          {error && <div className="mt-4 text-red-600 text-center">{error}</div>}
        </div>
      </section>
    </div>
  );
}
