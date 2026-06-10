app_content = '''import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import UploadResume from "./pages/uploadresume";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<UploadResume />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
'''

sidebar_content = '''import { useNavigate, useLocation } from "react-router-dom";
import {
  FiGrid,
  FiUser,
  FiUpload,
  FiSearch,
  FiHeart,
  FiFileText,
  FiSettings,
  FiLogOut,
} from "react-icons/fi";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const items = [
    { icon: <FiGrid />, label: "Dashboard", path: "/" },
    { icon: <FiUser />, label: "My Profile", path: "/profile" },
    { icon: <FiUpload />, label: "Upload Resume", path: "/upload" },
    { icon: <FiSearch />, label: "Search Jobs", path: "/search" },
    { icon: <FiHeart />, label: "Saved Jobs", path: "/saved" },
    { icon: <FiFileText />, label: "Applications", path: "/applications" },
    { icon: <FiSettings />, label: "Settings", path: "/settings" },
  ];

  return (
    <aside className="w-[270px] bg-[#060b1f] border-r border-slate-800 flex flex-col">
      <div className="p-5 border-b border-slate-800">
        <h1 className="text-3xl font-bold">
          Res<span className="text-purple-500">ú</span>Match AI
        </h1>
        <p className="text-sm text-slate-400 mt-1">AI-Powered Career Matching</p>
      </div>

      <nav className="flex-1 p-4">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={() => navigate(item.path)}
            className={`w-full flex items-center gap-4 px-5 py-4 rounded-xl mb-2 transition
              ${
                location.pathname === item.path
                  ? "bg-purple-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`}
          >
            {item.icon}
            {item.label}
          </button>
        ))}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <button className="w-full flex items-center gap-4 px-5 py-4 rounded-xl text-slate-300 hover:bg-slate-800">
          <FiLogOut />
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
'''

upload_content = '''import { useState } from "react";
import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";
import { FiUpload, FiFile, FiCheckCircle, FiAlertCircle } from "react-icons/fi";

const CANDIDATE_ID = 1;

function UploadResume() {
  const [resumeFile, setResumeFile] = useState(null);
  const [keywordsFile, setKeywordsFile] = useState(null);
  const [resumeStatus, setResumeStatus] = useState(null); // null | "uploading" | "success" | "error"
  const [keywordsStatus, setKeywordsStatus] = useState(null);
  const [resumeMessage, setResumeMessage] = useState("");
  const [keywordsMessage, setKeywordsMessage] = useState("");

  async function handleResumeUpload() {
    if (!resumeFile) return;
    setResumeStatus("uploading");
    const formData = new FormData();
    formData.append("file", resumeFile);
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/api/candidates/${CANDIDATE_ID}/resume`,
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
            <p className="text-slate-400 text-sm mb-6">PDF format only. Your skills and experience will be extracted automatically.</p>

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
          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-8">
            <h3 className="text-xl font-semibold mb-1">Keywords File</h3>
            <p className="text-slate-400 text-sm mb-6">TXT or CSV format. One keyword per line, e.g. Python, Data Engineer, UAE.</p>

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
        </div>
      </main>
    </div>
  );
}

export default UploadResume;
'''

import os

base = r"C:\Users\rayan\Desktop\Resumatch\frontend\src"

with open(os.path.join(base, "app.jsx"), "w", encoding="utf-8") as f:
    f.write(app_content)

with open(os.path.join(base, "components", "Sidebar", "sidebar.jsx"), "w", encoding="utf-8") as f:
    f.write(sidebar_content)

with open(os.path.join(base, "pages", "uploadresume.jsx"), "w", encoding="utf-8") as f:
    f.write(upload_content)

print("All files written successfully.")
