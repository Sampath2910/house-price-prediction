export default function About() {
  return (
    <div className="bg-[#FDF1DE] min-h-screen py-16 px-10 flex flex-col items-center">
      <div className="max-w-6xl w-full">
        {/* Top Section */}
        <div className="flex items-center justify-between mb-16">
          {/* Left: Image */}
          <div className="w-1/2 flex justify-center">
            <img
              src="/about_house.png"
              alt="House Illustration"
              className="w-[80%] rounded-2xl shadow-lg"
            />
          </div>

          {/* Right: Text */}
          <div className="w-1/2 pl-10 text-left">
            <h1 className="text-5xl font-extrabold text-[#3E2F1C] mb-6">
              About Us
            </h1>
            <h2 className="text-3xl font-bold text-[#3E2F1C] mb-4">
              Your Trusted Partner in Home Valuation
            </h2>
            <p className="text-gray-700 leading-relaxed text-lg">
              We specialize in providing instant and accurate home valuations using advanced algorithms
              and comprehensive data analysis. We help homeowners and real estate professionals make
              informed decisions based on trustworthy data.
            </p>
          </div>
        </div>

        {/* Mission Section */}
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-[#3E2F1C] mb-4">Our Mission</h2>
          <p className="max-w-3xl mx-auto text-gray-700 text-lg leading-relaxed">
            Our mission is to simplify the home valuation process, offering a seamless and trustworthy
            experience. We aim to empower users with the information they need to understand their home’s
            true market value.
          </p>
        </div>

        {/* Why Choose Us Section */}
        <div className="bg-[#FBE8C3] py-12 rounded-3xl shadow-inner">
          <h2 className="text-3xl font-bold text-[#3E2F1C] text-center mb-10">
            Why Choose Us?
          </h2>

          <div className="grid grid-cols-3 gap-10 max-w-5xl mx-auto text-center">
            <div>
              <div className="text-3xl mb-3">⭐</div>
              <h3 className="text-xl font-bold text-[#3E2F1C] mb-2">
                Expert Analysis
              </h3>
              <p className="text-gray-700">
                Benefit from our expertise and innovative valuation techniques.
              </p>
            </div>

            <div>
              <div className="text-3xl mb-3">✅</div>
              <h3 className="text-xl font-bold text-[#3E2F1C] mb-2">
                Reliable Data
              </h3>
              <p className="text-gray-700">
                Rely on accurate and comprehensive data for your property assessments.
              </p>
            </div>

            <div>
              <div className="text-3xl mb-3">🎧</div>
              <h3 className="text-xl font-bold text-[#3E2F1C] mb-2">
                Customer Support
              </h3>
              <p className="text-gray-700">
                Receive personalized support from our dedicated team.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
