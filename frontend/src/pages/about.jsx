import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";
import {
  FiTarget,
  FiTrendingUp,
  FiBarChart2,
  FiFileText,
  FiBriefcase,
  FiDollarSign,
} from "react-icons/fi";

const About = () => {
  const features = [
    {
      icon: <FiTarget size={22} />,
      title: "Honest Job Matching",
      description:
        "Every job in your results is scored as a percentage based on how well your profile aligns with the role. You'll see exactly which of your skills matched, which didn't, and why a job ranked where it did.",
    },
    {
      icon: <FiTrendingUp size={22} />,
      title: "Skill Gap Analysis",
      description:
        "If a role requires something you don't have, ResuMátch AI flags it clearly. Not to discourage you, but to give you a concrete, prioritized list of skills worth building. It even highlights which gaps are most in demand across the job market right now, so you know what's worth your time.",
    },
    {
      icon: <FiFileText size={22} />,
      title: "Resume Improvement Suggestions",
      description:
        "ResuMátch AI reviews your resume against what top employers are actively looking for and tells you where it can be strengthened. Think of it as a quiet career advisor sitting alongside you, pointing out what a recruiter would notice first.",
    },
    {
      icon: <FiBarChart2 size={22} />,
      title: "ATS Scoring",
      description:
        "Most large companies run resumes through an Applicant Tracking System before a human ever sees them. ResuMátch AI gives you an ATS score for your resume and explains what's helping you pass — and what's getting you filtered out before you even get a chance.",
    },
    {
      icon: <FiBriefcase size={22} />,
      title: "Alternative Field Recommendations",
      description:
        "Sometimes the most surprising part of using ResuMátch AI is discovering fields you never considered but are genuinely well-suited for. Based on your existing skill set and experience, it suggests adjacent roles and industries where your profile is competitive — because you're likely more capable than you've given yourself credit for.",
    },
    {
      icon: <FiDollarSign size={22} />,
      title: "Salary and Location Intelligence",
      description:
        "ResuMátch AI surfaces the top-paying countries for your target roles, alongside average salary benchmarks. Whether you're open to relocation or just want to understand your market value globally, this gives you a clearer picture of what your skills are actually worth.",
    },
  ];

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <div className="p-8">
          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-8">

            {/* Introduction */}
            <div className="max-w-6xl text-slate-300 leading-8">
              <p>
                ResuMátch AI is built around one simple idea: Your resume deserves more than just a keyword scanner.
                Most job platforms tell you what's available, but ResuMátch AI tells you where you actually stand.
                And more importantly, what to do about it.
              </p>

              <p className="mt-6">
                When you upload your resume, ResuMátch AI doesn't just read it.
                It understands it. It pulls out your skills, experience,
                certifications, job titles, and tools, then cross-references all
                of that against real, active job listings fetched live from the
                web. The result isn't a generic list of jobs. It's a ranked,
                scored, and explained breakdown of where you fit, why you fit,
                and what's holding you back.
              </p>
            </div>

            <div className="h-px bg-slate-700 my-10" />

            {/* Features Header */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-white mb-3">
                What ResuMátch AI Actually Does For You
              </h2>

              <p className="text-slate-400">
                ResuMátch AI goes well beyond matching keywords. Here's what you
                can expect the moment your resume is processed.
              </p>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {features.map((feature, index) => (
                <div
                  key={index}
                  className="bg-[#101936] border border-slate-700 rounded-xl p-6 hover:border-purple-500/40 transition"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <div className="text-purple-400">
                      {feature.icon}
                    </div>

                    <h3 className="font-semibold text-lg text-white">
                      {feature.title}
                    </h3>
                  </div>

                  <p className="text-slate-400 leading-7">
                    {feature.description}
                  </p>
                </div>
              ))}
            </div>

            {/* Disclaimer */}
            <div className="mt-10 border border-yellow-500/30 bg-yellow-500/10 rounded-xl p-6">
            <h3 className="text-yellow-400 font-semibold text-lg mb-6 text-center">
            ⚠️ Disclaimer ⚠️
            </h3>
          
              <p className="text-slate-300 leading-7">
                ResuMátch AI is a student-built project, developed independently
                as a learning exercise and portfolio demonstration. It is not
                affiliated with or endorsed by, or connected to any recruitment
                agency, employer, or job platform. The job listings, match
                scores, salary data, and recommendations it produces are
                generated programmatically and should be treated as
                informational guidance, not professional career advice.
              </p>

              <p className="text-slate-300 leading-7 mt-4">
                Results may vary depending on the content of your resume and the
                availability of live job data at the time of your search.
              Please use your own judgment when making any career-related decisions.</p>
                
              
            </div>

          </div>
        </div>
      </main>
    </div>
  );
};

export default About;