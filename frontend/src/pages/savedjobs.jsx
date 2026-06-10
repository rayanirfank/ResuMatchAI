import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {
  FiSearch,
  FiBookmark,
  FiSend,
  FiHeart,
} from "react-icons/fi";
import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";

function SavedJobs() {
  const navigate = useNavigate();
  const [savedJobs, setSavedJobs] = useState([]);

  useEffect(() => {
    const jobs = JSON.parse(localStorage.getItem("savedJobs") || "[]");
    setSavedJobs(jobs);
  }, []);

  function removeSavedJob(jobId) {
    const updatedJobs = savedJobs.filter((job) => job.id !== jobId);

    setSavedJobs(updatedJobs);

    localStorage.setItem("savedJobs", JSON.stringify(updatedJobs));

    const savedIds = JSON.parse(
      localStorage.getItem("savedJobIds") || "[]"
    ).filter((id) => id !== jobId);

    localStorage.setItem("savedJobIds", JSON.stringify(savedIds));
  }

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <div className="p-8">
          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
            

            <p className="text-slate-400 mb-6">
              <b>Jobs you've bookmarked for later.</b>
            </p>

            {savedJobs.length === 0 ? (
  <div className="min-h-[500px] flex items-center justify-center">
    <div className="w-full max-w-5xl text-center">

      <div className="w-20 h-20 mx-auto rounded-full bg-purple-600/10 border border-purple-500/20 flex items-center justify-center mb-8">
        <FiBookmark className="text-5xl text-purple-400" />
      </div>

      <h3 className="text-4xl font-bold mb-3">
        No Saved Jobs Yet
      </h3>

      <p className="text-slate-400 text-base max-w-xl mx-auto mb-6">
        Save interesting opportunities from your job matches and build your personal shortlist.
      </p>

      <button
        onClick={() => navigate("/")}
        className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-xl font-semibold transition mb-8"
      >
        Browse Job Matches
      </button>

      <div className="grid grid-cols-3 gap-6 max-w-4xl mx-auto">

        <div>
          <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-lg font-bold mb-4">
            1
          </div>

          <FiSearch className="text-4xl text-purple-400 mx-auto mb-4" />

          <h4 className="font-semibold text-xl mb-2">
            Discover Jobs
          </h4>

          <p className="text-slate-400">
            Find the right opportunities with AI-powered matching.
          </p>
        </div>

        <div>
          <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-lg font-bold mb-4">
            2
          </div>

          <FiHeart className="text-4xl text-purple-400 mx-auto mb-4" />

          <h4 className="font-semibold text-xl mb-2">
            Save Opportunities
          </h4>

          <p className="text-slate-400">
            Bookmark jobs that interest you for quick access later.
          </p>
        </div>

        <div>
          <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-500 mx-auto flex items-center justify-center text-lg font-bold mb-4">
            3
          </div>

          <FiSend className="text-4xl text-purple-400 mx-auto mb-4" />

          <h4 className="font-semibold text-xl mb-2">
            Apply Later
          </h4>

          <p className="text-slate-400">
            Review your saved jobs and apply with confidence.
          </p>
        </div>

      </div>

      <div className="mt-12 bg-slate-900/50 border border-slate-800 rounded-xl p-4">
        <p className="text-slate-400">
          Save jobs you like to track opportunities and never miss the right role.
        </p>
      </div>

    </div>
  </div>
) : (
              <div className="space-y-4">
                {savedJobs.map((job) => (
                  <div
                    key={job.id}
                    className="border border-slate-700 rounded-xl p-5 flex items-center justify-between"
                  >
                    <div>
                      <h3 className="font-semibold text-lg">
                        {job.title}
                      </h3>

                      <p className="text-slate-400">
                        {job.company}
                      </p>

                      <p className="text-slate-500 text-sm mt-1">
                        {job.location || "Remote"}
                      </p>

                      <p className="text-purple-400 mt-2">
                        Match Score: {job.match_score ?? 0}%
                      </p>
                    </div>

                    <div className="flex gap-3">
                      <a
                        href={job.url || "#"}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg"
                      >
                        Apply
                      </a>

                      <button
                        onClick={() => removeSavedJob(job.id)}
                        className="border border-red-500 text-red-400 hover:bg-red-500 hover:text-white px-4 py-2 rounded-lg transition"
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default SavedJobs;