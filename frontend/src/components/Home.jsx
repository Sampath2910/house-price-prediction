import { Link } from "react-router-dom";
import {
  MapPin,
  Cpu,
  Calculator,
  Star,
  Shield,
  Zap,
  ThumbsUp
} from "lucide-react";

export default function Home() {
  return (
    <div className="bg-[#FAE9D4] text-[#3E2F1C] min-h-screen">
      {/* Hero Section */}
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center py-16 px-8">
        <div className="md:w-1/2 mb-10 md:mb-0">
          <h1 className="text-6xl font-bold mb-6 leading-tight">
            Find Your <br /> Home’s Worth
          </h1>
          <p className="text-lg mb-8 text-gray-800">
            Get an instant estimate of your home’s market value based on your
            property’s details.
          </p>
          <Link to="/price-prediction">
            <button className="bg-[#E17933] text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-[#c56122] transition">
              Estimate Now
            </button>
          </Link>
        </div>
        <div className="md:w-1/2">
          <img src="house.png" alt="House" className="rounded-3xl shadow-2xl" />
        </div>
      </div>

      {/* Info Section */}
      <div className="bg-[#F6E3C6] py-16 rounded-t-[3rem] text-center">
        <h2 className="text-4xl font-bold mb-6">How It Works</h2>
        <p className="text-gray-700 max-w-2xl mx-auto mb-12 text-lg">
          Use our tool to find out the estimated market value of your property
          quickly and easily.
        </p>

        <h2 className="text-4xl font-bold mb-10">Why Choose Us</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-10 max-w-5xl mx-auto text-left">
          <div className="flex items-start gap-4">
            <MapPin className="w-8 h-8 text-[#E17933]" />
            <div>
              <h3 className="text-xl font-semibold mb-1">Enter Property Details</h3>
              <p className="text-gray-700">
                Provide accurate details to get a reliable price estimate.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <Cpu className="w-8 h-8 text-[#E17933]" />
            <div>
              <h3 className="text-xl font-semibold mb-1">Advanced Algorithms</h3>
              <p className="text-gray-700">
                Our AI-powered model calculates the most accurate estimates.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <Calculator className="w-8 h-8 text-[#E17933]" />
            <div>
              <h3 className="text-xl font-semibold mb-1">Get Your Estimate</h3>
              <p className="text-gray-700">
                Receive instant property valuations in just seconds.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <Star className="w-8 h-8 text-[#E17933]" />
            <div>
              <h3 className="text-xl font-semibold mb-1">Accurate Predictions</h3>
              <p className="text-gray-700">
                Our model is trained on verified and updated housing data.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <Shield className="w-8 h-8 text-[#E17933]" />
            <div>
              <h3 className="text-xl font-semibold mb-1">Secure Data</h3>
              <p className="text-gray-700">
                Your property data is safe, encrypted, and never shared.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4">
            <ThumbsUp className="w-8 h-8 text-[#E17933]" />
            <div>
              <h3 className="text-xl font-semibold mb-1">User-Friendly</h3>
              <p className="text-gray-700">
                Simple, elegant, and intuitive design for a smooth experience.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
