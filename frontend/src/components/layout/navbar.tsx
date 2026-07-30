"use client";

import { Bell, Search, UserCircle } from "lucide-react";

export default function Navbar() {
  const today = new Date().toLocaleDateString("en-US", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <header className="flex h-20 items-center justify-between border-b border-gray-200 bg-white px-8 shadow-sm">
      {/* Left Section */}
      <div>
        <h2 className="text-2xl font-bold text-gray-800">
          Dashboard
        </h2>
        <p className="text-sm text-gray-500">{today}</p>
      </div>

      {/* Center Search */}
      <div className="hidden w-full max-w-md items-center rounded-xl border border-gray-300 bg-gray-50 px-4 py-2 md:flex">
        <Search className="mr-2 text-gray-500" size={18} />
        <input
          type="text"
          placeholder="Search..."
          className="w-full bg-transparent outline-none"
        />
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-6">
        <button className="relative rounded-full p-2 transition hover:bg-gray-100">
          <Bell size={22} />
          <span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500"></span>
        </button>

        <div className="flex items-center gap-3">
          <UserCircle size={42} className="text-sky-700" />

          <div className="hidden md:block">
            <h3 className="font-semibold text-gray-800">
              Welcome
            </h3>
            <p className="text-sm text-gray-500">
              Patient
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}