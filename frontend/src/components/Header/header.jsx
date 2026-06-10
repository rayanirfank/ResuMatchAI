import { useLocation, useNavigate } from "react-router-dom";
import { FiUpload } from "react-icons/fi";

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const pageData = {
    "/": {
      title: "Dashboard",
      subtitle: "Your personalized job matches overview",
    },

    "/profile": {
      title: "My Profile",
      subtitle: "View your AI-generated candidate profile",
    },

    "/upload": {
      title: "Upload Resume",
      subtitle: "Upload files to generate career insights",
    },
    
    "/career-intelligence": {
  title: "Career Intelligence",
  subtitle:
    "AI-powered insights to strengthen your profile and accelerate your career",
  },
  
    "/saved": {
      title: "Saved Jobs",
      subtitle: "Manage your bookmarked opportunities",
  },

    "/about": {
  title: "About ResúMatch AI",
  subtitle: "Know more about the platform.",
  },

    "/settings": {
      title: "Settings",
      subtitle: "Manage your ResúMatch workspace",
    },
  };

  const currentPage = pageData[location.pathname] || pageData["/"];

  return (
    <header className="h-24 border-b border-slate-800 flex items-center justify-between px-8">
      <div>
        <h1 className="text-3xl font-bold">
          {currentPage.title}
        </h1>

        <p className="text-slate-400">
          {currentPage.subtitle}
        </p>
      </div>

      {location.pathname === "/" && (
        <button
          onClick={() => navigate("/upload")}
          className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 px-5 py-3 rounded-xl font-medium transition"
        >
          <FiUpload />
          Upload Resume
        </button>
      )}
    </header>
  );
};

export default Header;