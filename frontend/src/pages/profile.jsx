import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FiUser, FiUpload } from "react-icons/fi";
import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";

function BadgeList({ items }) {
  if (!items || items.length === 0) {
    return <p className="text-slate-500">No data available</p>;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {items.map((item, index) => (
        <span
          key={index}
          className="px-3 py-1 rounded-full bg-purple-600/20 border border-purple-500/30 text-purple-300 text-sm"
        >
          {item}
        </span>
      ))}
    </div>
  );
}

function Profile() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const candidateId = localStorage.getItem("activeCandidateId");

    if (!candidateId) {
      setError("No candidate found. Please upload a resume first.");
      setLoading(false);
      return;
    }

    fetch(`http://127.0.0.1:8000/api/candidates/${candidateId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load profile.");
        }
        return res.json();
      })
      .then((data) => {
        setProfile(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <div className="p-8">
          {loading && (
            <div className="text-center py-20 text-slate-400">
              Loading profile...
            </div>
          )}

{error && (
  <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-10 min-h-[550px] flex flex-col justify-center">

    <div className="flex flex-col items-center text-center">

      <div className="w-20 h-20 rounded-full bg-purple-600/10 border border-purple-500/20 flex items-center justify-center mb-8">
        <FiUser className="text-5xl text-purple-400" />
      </div>

      <h2 className="text-4xl font-bold mb-4">
        No Profile Yet
      </h2>

      <p className="text-slate-400 text-lg max-w-2xl mb-8">
        Upload your resume and keywords to generate your AI-powered career profile.
      </p>

      <button
        onClick={() => navigate("/upload")}
        className="bg-purple-600 hover:bg-purple-700 px-8 py-4 rounded-xl font-semibold transition flex items-center gap-3 mb-10"
      >
        <FiUpload />
        Upload Resume
      </button>

      <div className="grid grid-cols-4 gap-10 w-full max-w-6xl">

        <div className="text-center">
          <div className="w-12 h-12 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-lg font-bold mb-4">
            1
          </div>

          <h3 className="font-semibold mb-2">
            Upload Resume
          </h3>

          <p className="text-slate-400 text-sm">
            Upload your resume in PDF format
          </p>
        </div>

        <div className="text-center">
          <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-xl font-bold mb-4">
            2
          </div>

          <h3 className="font-semibold mb-2">
            Extract Skills & Experience
          </h3>

          <p className="text-slate-400 text-sm">
            We'll extract your skills, experience and education
          </p>
        </div>

        <div className="text-center">
          <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-xl font-bold mb-4">
            3
          </div>

          <h3 className="font-semibold mb-2">
            Build Career Profile
          </h3>

          <p className="text-slate-400 text-sm">
            Generate your AI-powered profile
          </p>
        </div>

        <div className="text-center">
          <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-xl font-bold mb-4">
            4
          </div>

          <h3 className="font-semibold mb-2">
            View AI Insights
          </h3>

          <p className="text-slate-400 text-sm">
            Explore personalized recommendations
          </p>
        </div>

      </div>

    </div>

  </div>
)}

          {!loading && !error && profile && (
            <div className="space-y-6">
              {/* Basic Information */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h2 className="text-2xl font-semibold mb-6">
                  Candidate Profile
                </h2>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-slate-400 text-sm">Full Name</p>
                    <p className="font-medium mt-1">
                      {profile.full_name || "Not Available"}
                    </p>
                  </div>

                  <div>
                    <p className="text-slate-400 text-sm">Current Title</p>
                    <p className="font-medium mt-1">
                      {profile.current_title || "Not Available"}
                    </p>
                  </div>

                  <div>
                    <p className="text-slate-400 text-sm">Email</p>
                    <p className="font-medium mt-1">
                      {profile.email || "Not Available"}
                    </p>
                  </div>

                  <div>
                    <p className="text-slate-400 text-sm">Phone</p>
                    <p className="font-medium mt-1">
                      {profile.phone || "Not Available"}
                    </p>
                  </div>
                </div>
              </div>

              {/* Career Information */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">
                  Career Information
                </h3>

                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-slate-400 text-sm">
                      Years of Experience
                    </p>
                    <p className="font-medium mt-1">
                      {profile.years_experience ?? 0}
                    </p>
                  </div>

                  <div>
                    <p className="text-slate-400 text-sm">
                      Seniority Level
                    </p>
                    <p className="font-medium mt-1 capitalize">
                      {profile.seniority_level || "Unknown"}
                    </p>
                  </div>
                </div>
              </div>

              {/* Skills */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">Skills</h3>
                <BadgeList items={profile.skills} />
              </div>

              {/* Tools */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">Tools</h3>
                <BadgeList items={profile.tools} />
              </div>

              {/* Keywords */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">
                  Unified Keywords
                </h3>
                <BadgeList items={profile.unified_keywords} />
              </div>

              {/* Education */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">Education</h3>

                <p className="text-slate-300 whitespace-pre-wrap">
                  {profile.education || "No education information found."}
                </p>
              </div>

              {/* Certifications */}
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h3 className="text-xl font-semibold mb-4">
                  Certifications
                </h3>

                <BadgeList items={profile.certifications} />
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default Profile;