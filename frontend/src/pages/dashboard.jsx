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

const JOBS_PER_PAGE = 7;

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
  const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "1 day ago";
  if (diffDays < 7) return `${diffDays} days ago`;
  return date.toLocaleDateString();
}

function getPaginationPages(current, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);
  if (current <= 4) return [1, 2, 3, 4, 5, "...", total];
  if (current >= total - 3) return [1, "...", total - 4, total - 3, total - 2, total - 1, total];
  return [1, "...", current - 1, current, current + 1, "...", total];
}

// The default/empty filter state — one place to define it
const DEFAULT_FILTERS = {
  search: "",
  location: "All Locations",
  minScore: 0,
};

function applyFilters(jobs, filters) {
  return jobs.filter((job) => {
    // Search: title or company contains the search term
    if (filters.search.trim()) {
      const term = filters.search.toLowerCase();
      const inTitle = (job.title || "").toLowerCase().includes(term);
      const inCompany = (job.company || "").toLowerCase().includes(term);
      if (!inTitle && !inCompany) return false;
    }

    // Location
if (filters.location !== "All Locations") {
  const jobLoc = (job.location || "").toLowerCase();
  const jobCountry = (job.country || "").toLowerCase();
  const filterTerm = filters.location.split(",")[0].toLowerCase().trim();

  const matchesLocation = jobLoc.includes(filterTerm);
  const matchesRemote = filterTerm === "remote" && 
    (jobLoc.includes("remote") || jobCountry.includes("remote"));

  if (!matchesLocation && !matchesRemote) return false;
}
    // Match Score minimum
    if ((job.match_score ?? 0) < filters.minScore) return false;

    return true;
  });
}

function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);

  // Filters state lives here in Dashboard — FilterPanel only reads/updates these
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  // pendingFilters = what user is currently editing in the panel (before clicking Apply)
  const [pendingFilters, setPendingFilters] = useState(DEFAULT_FILTERS);

  // Track saved job IDs so Save button shows state
  const [savedIds, setSavedIds] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("savedJobIds") || "[]");
    } catch { return []; }
  });

  useEffect(() => {
    const candidateId = localStorage.getItem("activeCandidateId");
  
    if (!candidateId) {
      setError("No candidate found. Please upload a resume first.");
      setLoading(false);
      return;
    }
  
    fetch(`http://127.0.0.1:8000/api/candidates/${candidateId}/jobs`)
      .then((res) => {
        if (res.status === 404) throw new Error("Candidate not found. Please upload a new resume.");
        if (!res.ok) throw new Error(`Server returned ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setJobs(data.sort((a, b) => (b.match_score ?? 0) - (a.match_score ?? 0)));
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Save/unsave a job — persists to localStorage
  function toggleSave(job) {
    const stored = JSON.parse(localStorage.getItem("savedJobs") || "[]");
    const alreadySaved = savedIds.includes(job.id);

    let newIds, newStored;
    if (alreadySaved) {
      newIds = savedIds.filter((id) => id !== job.id);
      newStored = stored.filter((j) => j.id !== job.id);
    } else {
      newIds = [...savedIds, job.id];
      newStored = [...stored, job];
    }
    setSavedIds(newIds);
    localStorage.setItem("savedJobIds", JSON.stringify(newIds));
    localStorage.setItem("savedJobs", JSON.stringify(newStored));
  }

  // Apply pending filters → resets to page 1
  function handleApplyFilters() {
    setFilters(pendingFilters);
    setCurrentPage(1);
  }

  // Reset everything
  function handleResetFilters() {
    setPendingFilters(DEFAULT_FILTERS);
    setFilters(DEFAULT_FILTERS);
    setCurrentPage(1);
  }

  const filteredJobs = applyFilters(jobs, filters);
  const totalJobs = jobs.length;
  const highMatchJobs = jobs.filter((j) => j.match_score >= 75).length;
  const avgScore =
    jobs.length > 0
      ? Math.round(jobs.reduce((sum, j) => sum + (j.match_score || 0), 0) / jobs.length)
      : 0;

  const totalPages = Math.ceil(filteredJobs.length / JOBS_PER_PAGE);
  const paginatedJobs = filteredJobs.slice(
    (currentPage - 1) * JOBS_PER_PAGE,
    currentPage * JOBS_PER_PAGE
  );
  const pageStart = filteredJobs.length === 0 ? 0 : (currentPage - 1) * JOBS_PER_PAGE + 1;
  const pageEnd = Math.min(currentPage * JOBS_PER_PAGE, filteredJobs.length);

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
  <Header />

  <div className="p-8">

          <div className="grid grid-cols-5 gap-5">
            <StatsCard title="Total Jobs Found" value={loading ? "—" : totalJobs.toLocaleString()} change="Live from Adzuna" icon={<FiBriefcase />} />
            <StatsCard title="High Match Jobs" value={loading ? "—" : highMatchJobs} change="Score >= 75%" icon={<FiTrendingUp />} />
            <StatsCard title="Average Match Score" value={loading ? "—" : `${avgScore}%`} change="Across all results" icon={<FiTarget />} />
            <StatsCard title="Applications Sent" value="0" change="Track your applies" icon={<FiSend />} />
            <StatsCard title="Saved Jobs" value={savedIds.length} change="Total saved jobs" icon={<FiBookmark />} />
          </div>

          <div className="grid grid-cols-12 gap-6 mt-8">
            <div className="col-span-3">
              <FilterPanel
                filters={pendingFilters}
                onChange={setPendingFilters}
                onApply={handleApplyFilters}
                onReset={handleResetFilters}
              />
            </div>

            <div className="col-span-9">
              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl min-h-[650px] p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-semibold">Top Job Matches</h2>
                    <p className="text-slate-400 mt-1">
                      {filteredJobs.length < totalJobs
                        ? `${filteredJobs.length} of ${totalJobs} jobs match your filters`
                        : "Ranked opportunities based on your profile"}
                    </p>
                  </div>
                  <button className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm font-medium transition">
                    View All Jobs
                  </button>
                </div>

                {loading && (
                  <div className="flex items-center justify-center h-64 text-slate-400">Loading jobs...</div>
                )}
                {error && (
  <div className="flex flex-col items-center justify-center py-20 text-center">
    <div className="w-24 h-24 rounded-full bg-purple-600/20 flex items-center justify-center mb-6">
      <span className="text-4xl">💼</span>
    </div>

    <h3 className="text-3xl font-semibold mb-3">
      No Job Matches Yet
    </h3>

    <p className="text-slate-400 max-w-lg mb-12">
      Upload your resume and keywords to discover personalized opportunities.
    </p>

    <div className="grid grid-cols-4 gap-10 w-full max-w-5xl">
      <div>
        <div className="w-12 h-12 mx-auto rounded-full bg-purple-600 flex items-center justify-center font-bold mb-3">
          1
        </div>
        <h4 className="font-medium">Upload Resume</h4>
        <p className="text-slate-500 text-sm mt-1">
          Add your latest resume
        </p>
      </div>

      <div>
        <div className="w-12 h-12 mx-auto rounded-full bg-purple-600 flex items-center justify-center font-bold mb-3">
          2
        </div>
        <h4 className="font-medium">Upload Keywords</h4>
        <p className="text-slate-500 text-sm mt-1">
          Add skills & target roles
        </p>
      </div>

      <div>
        <div className="w-12 h-12 mx-auto rounded-full bg-purple-600 flex items-center justify-center font-bold mb-3">
          3
        </div>
        <h4 className="font-medium">Fetch Jobs</h4>
        <p className="text-slate-500 text-sm mt-1">
          Search opportunities worldwide
        </p>
      </div>

      <div>
        <div className="w-12 h-12 mx-auto rounded-full bg-purple-600 flex items-center justify-center font-bold mb-3">
          4
        </div>
        <h4 className="font-medium">View AI Matches</h4>
        <p className="text-slate-500 text-sm mt-1">
          See ranked recommendations
        </p>
      </div>
    </div>
  </div>
)}
                {!loading && !error && jobs.length === 0 && (
                  <div className="flex items-center justify-center h-64 text-slate-500">No jobs found. Run a job fetch first.</div>
                )}
                {!loading && !error && jobs.length > 0 && filteredJobs.length === 0 && (
                  <div className="flex items-center justify-center h-64 text-slate-500">
                    No jobs match your current filters. Try adjusting them.
                  </div>
                )}

                {!loading && !error && filteredJobs.length > 0 && (
                  <>
                    <div className="overflow-x-auto">
                      <table className="w-full">
                        <thead>
                          <tr className="border-b border-slate-700 text-slate-400 text-sm">
                            <th className="text-left py-4">Job Details</th>
                            <th className="text-center py-4">Match Score</th>
                            <th className="text-center py-4">Posted</th>
                            <th className="text-center py-4">Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {paginatedJobs.map((job, index) => (
                            <tr key={job.id} className="border-b border-slate-800 hover:bg-slate-800/20 transition">
                              <td className="py-5">
                                <div className="flex items-start gap-4">
                                  <div className={`w-12 h-12 rounded-xl ${getLogoColor(index)} flex items-center justify-center font-bold text-lg`}>
                                    {(job.company || "?")[0].toUpperCase()}
                                  </div>
                                  <div>
                                    <h3 className="font-semibold">{job.title}</h3>
                                    <p className="text-slate-400 text-sm">{job.company}</p>
                                    <p className="text-slate-500 text-sm">{job.location || "Remote"} • {job.job_type || "Full-Time"}</p>
                                  </div>
                                </div>
                              </td>
                              <td className="text-center">
                                <span className={`font-semibold text-lg ${getScoreColor(job.match_score)}`}>
                                  {job.match_score ?? "—"}%
                                </span>
                              </td>
                              <td className="text-center text-slate-400 text-sm">{formatDate(job.posted_at)}</td>
                              <td>
  <div className="flex justify-center gap-2">
    <a
      href={job.url || "#"}
      target="_blank"
      rel="noopener noreferrer"
      className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg text-sm transition"
    >
      Apply
    </a>

    <button
      onClick={() => toggleSave(job)}
      className={`px-4 py-2 rounded-lg text-sm transition border ${
        savedIds.includes(job.id)
          ? "bg-purple-600 border-purple-600 text-white"
          : "border-slate-600 hover:border-slate-400"
      }`}
    >
      {savedIds.includes(job.id) ? "Saved" : "Save"}
    </button>
  </div>
</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>

                    {totalPages > 1 && (
                      <div className="flex items-center justify-between mt-6 pt-4 border-t border-slate-700">
                        <p className="text-slate-400 text-sm">
                          Showing {pageStart}–{pageEnd} of {filteredJobs.length} jobs
                        </p>
                        <div className="flex gap-2 items-center">
                          <button
                            onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
                            disabled={currentPage === 1}
                            className="px-3 py-2 rounded-lg border border-slate-600 text-sm disabled:opacity-30 hover:border-slate-400 transition"
                          >
                            ←
                          </button>
                          {getPaginationPages(currentPage, totalPages).map((page, i) =>
                            page === "..." ? (
                              <span key={`ellipsis-${i}`} className="px-2 text-slate-500">...</span>
                            ) : (
                              <button
                                key={page}
                                onClick={() => setCurrentPage(page)}
                                className={`px-3 py-2 rounded-lg text-sm transition ${
                                  currentPage === page
                                    ? "bg-purple-600 text-white"
                                    : "border border-slate-600 hover:border-slate-400"
                                }`}
                              >
                                {page}
                              </button>
                            )
                          )}
                          <button
                            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
                            disabled={currentPage === totalPages}
                            className="px-3 py-2 rounded-lg border border-slate-600 text-sm disabled:opacity-30 hover:border-slate-400 transition"
                          >
                            →
                          </button>
                        </div>
                      </div>
                    )}
                  </>
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