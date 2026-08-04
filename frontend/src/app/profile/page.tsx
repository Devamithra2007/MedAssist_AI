"use client";

import { useEffect, useState } from "react";
import {
  getPatientProfile,
  updatePatientProfile,
} from "@/services/patient";

export default function ProfilePage() {
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getPatientProfile();
      setProfile(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setProfile({
      ...profile,
      [e.target.name]: e.target.value,
    });
  };

  const saveProfile = async () => {
    try {
      setSaving(true);

      await updatePatientProfile(profile);

      alert("Profile updated successfully.");

      setEditing(false);
    } catch (err) {
      console.error(err);
      alert("Unable to update profile.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center bg-slate-100">
        <h1 className="text-2xl font-semibold text-blue-700 animate-pulse">
          Loading Profile...
        </h1>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 py-10 px-6">

      <div className="max-w-6xl mx-auto">

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">

          {/* Header */}

          <div className="bg-gradient-to-r from-blue-700 to-cyan-600 text-white p-8">

            <div className="flex items-center gap-6">

              <div className="w-28 h-28 rounded-full bg-white text-blue-700 flex items-center justify-center text-5xl font-bold shadow-lg">

                {profile.full_name
                  ? profile.full_name.charAt(0).toUpperCase()
                  : "P"}

              </div>

              <div>

                <h1 className="text-4xl font-bold">
                  {profile.full_name}
                </h1>

                <p className="text-blue-100 text-lg mt-2">
                  {profile.email}
                </p>

                <span className="inline-block mt-4 px-4 py-2 rounded-full bg-white text-blue-700 font-semibold">
                  {profile.role}
                </span>

              </div>

              <div className="ml-auto">

                {!editing ? (

                  <button
                    onClick={() => setEditing(true)}
                    className="bg-white text-blue-700 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition"
                  >
                    Edit Profile
                  </button>

                ) : (

                  <button
                    onClick={saveProfile}
                    disabled={saving}
                    className="bg-green-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-green-600 transition"
                  >
                    {saving ? "Saving..." : "Save Changes"}
                  </button>

                )}

              </div>

            </div>

          </div>

          {/* Personal Information */}

          <div className="p-8">

            <h2 className="text-2xl font-bold text-blue-700 mb-6">
              Personal Information
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

              <div>

                <label className="block text-sm font-medium mb-2">
                  Phone Number
                </label>

                <input
                  type="text"
                  name="phone"
                  value={profile.phone || ""}
                  onChange={handleChange}
                  disabled={!editing}
                  className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                />

              </div>

              <div>

                <label className="block text-sm font-medium mb-2">
                  Date of Birth
                </label>

                <input
                  type="text"
                  name="date_of_birth"
                  value={profile.date_of_birth || ""}
                  onChange={handleChange}
                  disabled={!editing}
                  className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                />

              </div>

              <div>

                <label className="block text-sm font-medium mb-2">
                  Gender
                </label>

                <input
                  type="text"
                  name="gender"
                  value={profile.gender || ""}
                  onChange={handleChange}
                  disabled={!editing}
                  className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                />

              </div>

              <div>

                <label className="block text-sm font-medium mb-2">
                  Blood Group
                </label>

                <input
                  type="text"
                  name="blood_group"
                  value={profile.blood_group || ""}
                  onChange={handleChange}
                  disabled={!editing}
                  className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                />

              </div>
                            <div>

                <label className="block text-sm font-medium mb-2">
                  Height (cm)
                </label>

                <input
                  type="text"
                  name="height"
                  value={profile.height || ""}
                  onChange={handleChange}
                  disabled={!editing}
                  className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                />

              </div>

              <div>

                <label className="block text-sm font-medium mb-2">
                  Weight (kg)
                </label>

                <input
                  type="text"
                  name="weight"
                  value={profile.weight || ""}
                  onChange={handleChange}
                  disabled={!editing}
                  className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                />

              </div>

            </div>

            {/* Contact Information */}

            <div className="mt-10">

              <h2 className="text-2xl font-bold text-blue-700 mb-6">
                Contact Information
              </h2>

              <div className="grid grid-cols-1 gap-6">

                <div>

                  <label className="block text-sm font-medium mb-2">
                    Address
                  </label>

                  <textarea
                    rows={3}
                    name="address"
                    value={profile.address || ""}
                    onChange={handleChange}
                    disabled={!editing}
                    className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                  />

                </div>

                <div>

                  <label className="block text-sm font-medium mb-2">
                    Emergency Contact
                  </label>

                  <input
                    type="text"
                    name="emergency_contact"
                    value={profile.emergency_contact || ""}
                    onChange={handleChange}
                    disabled={!editing}
                    className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                  />

                </div>

              </div>

            </div>

            {/* Medical Information */}

            <div className="mt-10">

              <h2 className="text-2xl font-bold text-blue-700 mb-6">
                Medical Information
              </h2>

              <div className="space-y-6">

                <div>

                  <label className="block text-sm font-medium mb-2">
                    Allergies
                  </label>

                  <textarea
                    rows={3}
                    name="allergies"
                    value={profile.allergies || ""}
                    onChange={handleChange}
                    disabled={!editing}
                    className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                  />

                </div>

                <div>

                  <label className="block text-sm font-medium mb-2">
                    Medical History
                  </label>

                  <textarea
                    rows={5}
                    name="medical_history"
                    value={profile.medical_history || ""}
                    onChange={handleChange}
                    disabled={!editing}
                    className="w-full border rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500"
                  />

                </div>

              </div>

            </div>

            {/* Health Summary */}

            <div className="mt-12">

              <h2 className="text-2xl font-bold text-blue-700 mb-6">
                Health Summary
              </h2>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">

                <div className="bg-blue-50 rounded-xl p-6 shadow">

                  <p className="text-sm text-gray-500">
                    Blood Group
                  </p>

                  <h3 className="text-3xl font-bold text-blue-700 mt-2">
                    {profile.blood_group || "-"}
                  </h3>

                </div>

                <div className="bg-green-50 rounded-xl p-6 shadow">

                  <p className="text-sm text-gray-500">
                    Height
                  </p>

                  <h3 className="text-3xl font-bold text-green-700 mt-2">
                    {profile.height || "-"} cm
                  </h3>

                </div>

                <div className="bg-yellow-50 rounded-xl p-6 shadow">

                  <p className="text-sm text-gray-500">
                    Weight
                  </p>

                  <h3 className="text-3xl font-bold text-yellow-700 mt-2">
                    {profile.weight || "-"} kg
                  </h3>

                </div>

                <div className="bg-red-50 rounded-xl p-6 shadow">

                  <p className="text-sm text-gray-500">
                    Allergies
                  </p>

                  <h3 className="text-lg font-semibold text-red-700 mt-2">
                    {profile.allergies
                      ? "Available"
                      : "None"}
                  </h3>

                </div>

              </div>

            </div>
                        {/* Footer */}

            <div className="mt-12 border-t pt-8">

              <div className="flex flex-col sm:flex-row justify-between items-center gap-4">

                <div>

                  <p className="text-gray-500">
                    Keep your medical profile updated for better AI-based
                    disease prediction and healthcare recommendations.
                  </p>

                </div>

                <div className="flex gap-4">

                  {editing && (

                    <button
                      onClick={() => {
                        setEditing(false);
                        loadProfile();
                      }}
                      className="px-6 py-3 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition"
                    >
                      Cancel
                    </button>

                  )}

                  <button
                    onClick={editing ? saveProfile : () => setEditing(true)}
                    disabled={saving}
                    className={`px-6 py-3 rounded-lg font-semibold transition ${
                      editing
                        ? "bg-blue-600 text-white hover:bg-blue-700"
                        : "bg-green-600 text-white hover:bg-green-700"
                    }`}
                  >
                    {editing
                      ? saving
                        ? "Saving..."
                        : "Save Changes"
                      : "Edit Profile"}
                  </button>

                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>

  );
}