import { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";
import StatsCard from "../components/StatsCard/statscard";
import FilterPanel from "../components/FilterPanel/filterpanel";

import {
  FiBriefcase,
  FiTrendingUp,
  FiTarget,
  FiSend,
  FiBookmark,
} from "react-icons/fi";

// Hardcoded for now — later this comes from the upload flow
const CANDIDATE_ID = 1;

function getScoreColor(score) {
  if (score >= 75) return "text-green-400";
  if (score >= 50) return "text-orange-400";
  return "text-red-400";
}

function getLogoColor(index) {
  const colors = [
    "bg-purple-600", "bg-blue-600", "bg-orange-600",
    "bg-green-600", "bg-pink-600", "bg-yellow-600",
  ];
  return colors[index % colors.length];
}

function formatDate(dateStr) {
  if (!dateStr) return "—";
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now - date;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "1 day ago";
  if (diffDays < 7) return `${diffDays} days ago`;
  return date.toLocaleDateString();
}

function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/candidates/${CANDIDATE_ID}/jobs`)
      .then((res) => {
        if (!res.ok) throw new Error(`Server returned ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Derived stats from real data
  const totalJobs = jobs.length;
  const highMatchJobs = jobs.filter((j) => j.match_score >= 75).length;
  const avgScore =
    jobs.length > 0
      ? Math.round(jobs.reduce((sum, j) => sum + (j.match_score || 0), 0) / jobs.length)
      : 0;

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <div className="p-8">
          {/* Stats Cards */}
          <div className="grid grid-cols-5 gap-5">
            <StatsCard
              title="Total Jobs Found"
              value={loading ? "—" : totalJobs.toLocaleString()}
              change="Live from Adzuna"
              icon={<FiBriefcase />}
            />
            <StatsCard
              title="High Match Jobs"
              value={loading ? "—" : highMatchJobs}
              change="Score ≥ 75%"
              icon={<FiTrendingUp />}
            />
            <StatsCard
              title="Average Match Score"
              value={loading ? "—" : `${avgScore}%`}
              change="Across all results"
              icon={<FiTarget />}
            />
            <StatsCard
              title="Applications Sent"
              value="0"
              change="Track your applies"
              icon={<FiSend />}
            />
            <StatsCard
              title="Saved Jobs"
              value="0"
              change="Total saved jobs"
              icon={<FiBookmark />}
            />
          </div>

          {/* Main Dashboard Body */}
          <div className="grid grid-cols-12 gap-6 mt-8">
            {/* Filter Panel */}
            <div className="col-span-3">
              <FilterPanel />
            </div>

            {/* Top Job Matches */}
            <div className="col-span-9">
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl min-h-[650px] p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-semibold">Top Job Matches</h2>
                    <p className="text-slate-400 mt-1">
                      Ranked opportunities based on your profile
                    </p>
                  </div>
                  <button className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm font-medium transition">
                    View All Jobs
                  </button>
                </div>

                {/* Loading state */}
                {loading && (
                  <div className="flex items-center justify-center h-64 text-slate-400">
                    Loading jobs...
                  </div>
                )}

                {/* Error state */}
                {error && (
                  <div className="flex items-center justify-center h-64 text-red-400">
                    Failed to load jobs: {error}
                  </div>
                )}

                {/* Empty state */}
                {!loading && !error && jobs.length === 0 && (
                  <div className="flex items-center justify-center h-64 text-slate-500">
                    No jobs found. Run a job fetch first.
                  </div>
                )}

                {/* Job table */}
                {!loading && !error && jobs.length > 0 && (
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-slate-700 text-slate-400 text-sm">
                          <th className="text-left py-4">Job Details</th>
                          <th className="text-center py-4">Match Score</th>
                          <th className="text-left py-4">Matched Keywords</th>
                          <th className="text-center py-4">Posted</th>
                          <th className="text-center py-4">Actions</th>
                        </tr>
                      </thead>

                      <tbody>
                        {jobs.map((job, index) => {
                          // matched_keywords is stored as JSON string in backend
                          let keywords = [];
                          try {
                            keywords =
                              typeof job.matched_keywords === "string"
                                ? JSON.parse(job.matched_keywords)
                                : job.matched_keywords || [];
                          } catch {
                            keywords = [];
                          }

                          return (
                            <tr
                              key={job.id}
                              className="border-b border-slate-800 hover:bg-slate-800/20 transition"
                            >
                              {/* Job Details */}
                              <td className="py-5">
                                <div className="flex items-start gap-4">
                                  <div
                                    className={`w-12 h-12 rounded-xl ${getLogoColor(index)} flex items-center justify-center font-bold text-lg`}
                                  >
                                    {(job.company || "?")[0].toUpperCase()}
                                  </div>
                                  <div>
                                    <h3 className="font-semibold">{job.title}</h3>
                                    <p className="text-slate-400 text-sm">{job.company}</p>
                                    <p className="text-slate-500 text-sm">
                                      {job.location || "Remote"} •{" "}
                                      {job.job_type || "Full-Time"}
                                    </p>
                                  </div>
                                </div>
                              </td>

                              {/* Match Score */}
                              <td className="text-center">
                                <span
                                  className={`font-semibold text-lg ${getScoreColor(job.match_score)}`}
                                >
                                  {job.match_score ?? "—"}%
                                </span>
                              </td>

                              {/* Matched Keywords */}
                              <td>
                                <div className="flex flex-wrap gap-2">
                                  {keywords.slice(0, 4).map((kw, i) => (
                                    <span
                                      key={i}
                                      className="px-3 py-1 rounded-full bg-green-900/30 text-green-400 text-xs"
                                    >
                                      {kw}
                                    </span>
                                  ))}
                                  {keywords.length > 4 && (
                                    <span className="px-3 py-1 rounded-full bg-slate-700 text-slate-400 text-xs">
                                      +{keywords.length - 4} more
                                    </span>
                                  )}
                                </div>
                              </td>

                              {/* Posted Date */}
                              <td className="text-center text-slate-400 text-sm">
                                {formatDate(job.posted_at)}
                              </td>

                              {/* Actions */}
                              <td>
                                <div className="flex justify-center gap-2">
                                  
                                    href={job.url || "#"}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition"
                                    Apply
                                  <button className="border border-slate-600 hover:border-slate-400 px-4 py-2 rounded-lg text-sm transition">
                                    Save
                                  </button>
                                </div>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;