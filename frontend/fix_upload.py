content = '''import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";
import { FiUpload, FiFile, FiCheckCircle, FiAlertCircle, FiSearch } from "react-icons/fi";

const CANDIDATE_ID = 1;

function UploadResume() {
  const navigate = useNavigate();
  const [resumeFile, setResumeFile] = useState(null);
  const [keywordsFile, setKeywordsFile] = useState(null);
  const [resumeStatus, setResumeStatus] = useState(null);
  const [keywordsStatus, setKeywordsStatus] = useState(null);
  const [resumeMessage, setResumeMessage] = useState("");
  const [keywordsMessage, setKeywordsMessage] = useState("");
  const [findingJobs, setFindingJobs] = useState(false);
  const [findJobsMessage, setFindJobsMessage] = useState("");
  const [findJobsError, setFindJobsError] = useState("");

  async function handleResumeUpload() {
    if (!resumeFile) return;
    setResumeStatus("uploading");
    const formData = new FormData();
    formData.append("file", resumeFile);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/candidates/upload`,
        { method: "POST", body: formData }
      );
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      setResumeStatus("success");
      setResumeMessage("Resume uploaded and parsed successfully.");
    } catch (err) {
      setResumeStatus("error");
      setResumeMessage(err.message);
    }
  }

  async function handleKeywordsUpload() {
    if (!keywordsFile) return;
    setKeywordsStatus("uploading");
    const formData = new FormData();
    formData.append("file", keywordsFile);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/candidates/${CANDIDATE_ID}/keywords`,
        { method: "POST", body: formData }
      );
      if (!res.ok) throw new Error(`Server error ${res.status}`);
      setKeywordsStatus("success");
      setKeywordsMessage("Keywords uploaded and merged successfully.");
    } catch (err) {
      setKeywordsStatus("error");
      setKeywordsMessage(err.message);
    }
  }

  async function handleFindJobs() {
    setFindingJobs(true);
    setFindJobsError("");
    setFindJobsMessage("Step 1/3: Fetching live jobs from Adzuna...");

    try {
      // Step 1: Fetch jobs
      const fetchRes = await fetch(
        `http://127.0.0.1:8000/api/candidates/${CANDIDATE_ID}/fetch-jobs`,
        { method: "POST" }
      );
      if (!fetchRes.ok) throw new Error(`Fetch jobs failed: ${fetchRes.status}`);
      const fetchData = await fetchRes.json();

      setFindJobsMessage(`Step 2/3: Scoring ${fetchData.stored} jobs against your profile...`);

      // Step 2: Score jobs
      const scoreRes = await fetch(
        `http://127.0.0.1:8000/api/candidates/${CANDIDATE_ID}/score-jobs`,
        { method: "POST" }
      );
      if (!scoreRes.ok) throw new Error(`Score jobs failed: ${scoreRes.status}`);

      setFindJobsMessage("Step 3/3: Done! Redirecting to your dashboard...");

      // Step 3: Redirect after short delay so user sees the success message
      setTimeout(() => navigate("/"), 1500);

    } catch (err) {
      setFindJobsError(err.message);
      setFindingJobs(false);
    }
  }

const [bothUploaded, setBothUploaded] = useState(false);

useEffect(() => {
  if (resumeStatus === "success" && keywordsStatus === "success") {
    setBothUploaded(true);
  }
}, [resumeStatus, keywordsStatus]);

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <Header />
        <div className="p-8 max-w-3xl">
          <h2 className="text-3xl font-bold mb-2">Upload Your Documents</h2>
          <p className="text-slate-400 mb-10">
            Upload your resume and keywords file to power your job matches.
          </p>

          {/* Resume Upload */}
          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-8 mb-6">
            <h3 className="text-xl font-semibold mb-1">Resume</h3>
            <p className="text-slate-400 text-sm mb-6">
              PDF format only. Your skills and experience will be extracted automatically.
            </p>

            <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-xl p-10 cursor-pointer hover:border-purple-500 transition">
              <FiUpload className="text-4xl text-slate-400 mb-3" />
              <span className="text-slate-400 text-sm">
                {resumeFile ? resumeFile.name : "Click to select your resume PDF"}
              </span>
              <input
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={(e) => {
                  setResumeFile(e.target.files[0]);
                  setResumeStatus(null);
                  setResumeMessage("");
                }}
              />
            </label>

            {resumeFile && (
              <div className="flex items-center gap-2 mt-4 text-slate-300 text-sm">
                <FiFile /> {resumeFile.name}
              </div>
            )}
            {resumeStatus === "success" && (
              <div className="flex items-center gap-2 mt-4 text-green-400 text-sm">
                <FiCheckCircle /> {resumeMessage}
              </div>
            )}
            {resumeStatus === "error" && (
              <div className="flex items-center gap-2 mt-4 text-red-400 text-sm">
                <FiAlertCircle /> {resumeMessage}
              </div>
            )}

            <button
              onClick={handleResumeUpload}
              disabled={!resumeFile || resumeStatus === "uploading"}
              className="mt-6 bg-purple-600 hover:bg-purple-700 disabled:opacity-40 px-6 py-3 rounded-xl font-medium transition"
            >
              {resumeStatus === "uploading" ? "Uploading..." : "Upload Resume"}
            </button>
          </div>

          {/* Keywords Upload */}
          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-8 mb-6">
            <h3 className="text-xl font-semibold mb-1">Keywords File</h3>
            <p className="text-slate-400 text-sm mb-6">
              TXT or CSV format. One keyword per line, e.g. Python, Data Engineer, UAE.
            </p>

            <label className="flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-xl p-10 cursor-pointer hover:border-purple-500 transition">
              <FiUpload className="text-4xl text-slate-400 mb-3" />
              <span className="text-slate-400 text-sm">
                {keywordsFile ? keywordsFile.name : "Click to select your keywords file"}
              </span>
              <input
                type="file"
                accept=".txt,.csv"
                className="hidden"
                onChange={(e) => {
                  setKeywordsFile(e.target.files[0]);
                  setKeywordsStatus(null);
                  setKeywordsMessage("");
                }}
              />
            </label>

            {keywordsFile && (
              <div className="flex items-center gap-2 mt-4 text-slate-300 text-sm">
                <FiFile /> {keywordsFile.name}
              </div>
            )}
            {keywordsStatus === "success" && (
              <div className="flex items-center gap-2 mt-4 text-green-400 text-sm">
                <FiCheckCircle /> {keywordsMessage}
              </div>
            )}
            {keywordsStatus === "error" && (
              <div className="flex items-center gap-2 mt-4 text-red-400 text-sm">
                <FiAlertCircle /> {keywordsMessage}
              </div>
            )}

            <button
              onClick={handleKeywordsUpload}
              disabled={!keywordsFile || keywordsStatus === "uploading"}
              className="mt-6 bg-purple-600 hover:bg-purple-700 disabled:opacity-40 px-6 py-3 rounded-xl font-medium transition"
            >
              {keywordsStatus === "uploading" ? "Uploading..." : "Upload Keywords"}
            </button>
          </div>

          {/* Find Jobs — only appears after both uploads succeed */}
          {bothUploaded && (
            <div className="bg-[#0B1228] border border-purple-700 rounded-2xl p-8">
              <h3 className="text-xl font-semibold mb-1">Ready to Find Jobs</h3>
              <p className="text-slate-400 text-sm mb-6">
                Both files uploaded. Click below to fetch live jobs and score them against your profile.
              </p>

              {findJobsMessage && !findJobsError && (
                <div className="flex items-center gap-2 mb-4 text-purple-300 text-sm">
                  <FiSearch /> {findJobsMessage}
                </div>
              )}
              {findJobsError && (
                <div className="flex items-center gap-2 mb-4 text-red-400 text-sm">
                  <FiAlertCircle /> {findJobsError}
                </div>
              )}

              <button
                onClick={handleFindJobs}
                disabled={findingJobs}
                className="bg-purple-600 hover:bg-purple-700 disabled:opacity-40 px-8 py-4 rounded-xl font-semibold text-lg transition flex items-center gap-3"
              >
                <FiSearch />
                {findingJobs ? "Finding Jobs..." : "Find My Jobs"}
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default UploadResume;
'''

path = r"C:\Users\rayan\Desktop\Resumatch\frontend\src\pages\uploadresume.jsx"
with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print("uploadresume.jsx written successfully.")