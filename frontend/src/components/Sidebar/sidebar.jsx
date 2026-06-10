import { useNavigate, useLocation } from "react-router-dom";
import {
  FiGrid,
  FiUser,
  FiUpload,
  FiHeart,
  FiSettings,
  FiLogOut,
  FiZap,
  FiStar,
  FiCpu,
} from "react-icons/fi";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleResetWorkspace = () => {
    const confirmed = window.confirm(
      "Reset all ResuMatch data and start fresh?"
    );

    if (!confirmed) return;

    localStorage.removeItem("activeCandidateId");
    localStorage.removeItem("savedJobs");
    localStorage.removeItem("savedJobIds");
    localStorage.removeItem("keywordsUploaded");

    window.location.href = "/upload";
  };

  const items = [
    { icon: <FiGrid />, label: "Dashboard", path: "/" },
    { icon: <FiUser />, label: "My Profile", path: "/profile" },
    { icon: <FiUpload />, label: "Upload Resume", path: "/upload" },
    { icon: <FiCpu />, label: "Career Intelligence", path: "/career-intelligence",},
    { icon: <FiHeart />, label: "Saved Jobs", path: "/saved" },
    { icon: <FiUser />, label: "About ResúMatch AI", path: "/about",},
    { icon: <FiSettings />, label: "Settings", path: "/settings" },
  ];

  return (
    <aside className="w-[270px] bg-[#060b1f] border-r border-slate-800 flex flex-col">
      {/* Logo */}
      <div className="p-5 border-b border-slate-800">
        <h1 className="text-2xl font-bold">
          Res<span className="text-purple-500">ú</span>Match AI
        </h1>

        <p className="text-sm text-slate-400 mt-1">
          AI-Powered Career Matching
        </p>
      </div>

      {/* Navigation */}
      <nav className="p-4">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={() => navigate(item.path)}
            className={`w-full flex items-center gap-4 px-5 py-4 rounded-xl mb-2 transition ${
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

      {/* Dashboard Only Cards */}
      {location.pathname === "/" && (
        <div className="px-4 pb-4 space-y-4">
          {/* AI Insight */}
          <div className="bg-[#0B1228] border border-slate-800 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-3">
              <FiZap className="text-purple-400" />
              <h3 className="text-purple-400 font-semibold text-sm">
                AI INSIGHT
              </h3>
            </div>

            <div className="h-px bg-purple-500/20 mb-3" />

            <p className="text-slate-300 text-sm leading-relaxed">
              Resumes with clearly defined skills, tools, and measurable
              achievements tend to generate stronger match scores.
            </p>
          </div>

          {/* Tip Of The Day */}
          <div className="bg-[#0B1228] border border-slate-800 rounded-xl p-4">
            <div className="flex items-center gap-2 mb-3">
              <FiStar className="text-purple-400" />
              <h3 className="text-purple-400 font-semibold text-sm">
                TIP OF THE DAY
              </h3>
            </div>

            <div className="h-px bg-purple-500/20 mb-3" />

            <p className="text-slate-300 text-sm leading-relaxed">
              Tailor your resume keywords to the role you're targeting.
              Generic resumes usually produce weaker AI match results.
            </p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="mt-auto p-4 border-t border-slate-800">
        <button
          onClick={handleResetWorkspace}
          className="w-full flex items-center gap-4 px-5 py-4 rounded-xl text-slate-300 hover:bg-slate-800 transition"
        >
          <FiLogOut />
          Reset Workspace
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;