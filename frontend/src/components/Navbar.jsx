import React from "react";
import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const location = useLocation();

  const navLinks = [
    { name: "Home", path: "/" },
    { name: "Price Prediction", path: "/price-prediction" },
    { name: "About", path: "/about" },
    { name: "Contact", path: "/contact" },
  ];

  return (
    <nav className="bg-[#FDF1DE] text-[#3E2F1C] shadow-sm">
      <div className="max-w-7xl mx-auto flex justify-between items-center py-5 px-8">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2">
          <span className="text-3xl">🏠</span>
          <h1 className="text-2xl font-bold tracking-tight">HomeValue AI</h1>
        </Link>

        {/* Nav Links */}
        <ul className="flex gap-8 text-lg font-medium">
          {navLinks.map((link) => (
            <li key={link.name}>
              <Link
                to={link.path}
                className={`transition duration-200 pb-1 ${
                  location.pathname === link.path
                    ? "text-[#E17933] border-b-2 border-[#E17933]"
                    : "hover:text-[#E17933]"
                }`}
              >
                {link.name}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
