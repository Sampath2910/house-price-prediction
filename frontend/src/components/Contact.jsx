import React, { useState } from "react";

export default function Contact() {
  const [form, setForm] = useState({ name: "", email: "", subject: "", message: "" });
  const [status, setStatus] = useState("");

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("https://house-price-prediction-7sk1.onrender.com/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      if (data.status === "success") setStatus("✅ Message sent successfully!");
      else setStatus("❌ Failed to send message.");
    } catch {
      setStatus("⚠️ Could not connect to the backend.");
    }
  };

  return (
    <div className="bg-[#FAE9D4] min-h-screen text-[#3E2F1C] py-16 px-6">
      <div className="max-w-4xl mx-auto bg-white p-10 rounded-3xl shadow-lg grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <img src="house.png" alt="House" className="rounded-2xl shadow-lg mb-6" />
          <h2 className="text-3xl font-bold mb-4">Get in Touch</h2>
          <p className="text-gray-700">
            We'd love to hear from you. Please fill out the form or contact us with any questions or inquiries.
          </p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input name="name" placeholder="Name" value={form.name} onChange={handleChange} className="w-full p-3 border rounded-lg" required />
          <input name="email" placeholder="Email" value={form.email} onChange={handleChange} className="w-full p-3 border rounded-lg" required />
          <input name="subject" placeholder="Subject" value={form.subject} onChange={handleChange} className="w-full p-3 border rounded-lg" />
          <textarea name="message" placeholder="Message" value={form.message} onChange={handleChange} className="w-full p-3 border rounded-lg h-32" />
          <button className="w-full bg-[#2F5732] text-white py-3 rounded-lg hover:bg-[#244827] transition">
            Send Message
          </button>
          {status && <p className="text-center mt-3 text-sm">{status}</p>}
        </form>
      </div>
    </div>
  );
}
