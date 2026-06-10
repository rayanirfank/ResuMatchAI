import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";
import StatsCard from "../components/StatsCard/statscard";

import {
  FiActivity,
  FiTarget,
  FiTrendingUp,
  FiAlertCircle,
} from "react-icons/fi";

function CareerIntelligence() {
  const [atsData, setAtsData] = useState(null);
  const [skillGapData, setSkillGapData] = useState(null);
  const [recommendationData, setRecommendationData] = useState(null);
  const [salaryData, setSalaryData] = useState(null);
  const [resumeSuggestions, setResumeSuggestions] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const candidateId = localStorage.getItem("activeCandidateId");

    if (!candidateId) {
      setLoading(false);
      return;
    }

    Promise.all([
      fetch(
        `http://127.0.0.1:8000/api/career-intelligence/${candidateId}/ats-score`
      ).then((res) => res.json()),

      fetch(
        `http://127.0.0.1:8000/api/career-intelligence/${candidateId}/skill-gap`
      ).then((res) => res.json()),

      fetch(
        `http://127.0.0.1:8000/api/career-intelligence/${candidateId}/resume-suggestions`
      ).then((res) => res.json()),

      fetch(
        `http://127.0.0.1:8000/api/career-intelligence/${candidateId}/career-recommendations`
      ).then((res) => res.json()),

      fetch(
        `http://127.0.0.1:8000/api/career-intelligence/${candidateId}/salary-intelligence`
      ).then((res) => res.json()),
    ])
      .then(
        ([
          ats,
          skillGap,
          suggestions,
          recommendations,
          salary,
        ]) => {
          setAtsData(ats);
          setSkillGapData(skillGap);
          setResumeSuggestions(suggestions);
          setRecommendationData(recommendations);
          setSalaryData(salary);
        }
      )
      .finally(() => setLoading(false));
  }, []);

  const candidateExists = !!localStorage.getItem(
    "activeCandidateId"
  );

  if (!candidateExists) {
    return (
      <div className="min-h-screen bg-[#050816] text-white flex">
        <Sidebar />

        <main className="flex-1 overflow-y-auto">
          <Header />

          <div className="p-8">
            <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-12 text-center">
              <div className="w-20 h-20 mx-auto rounded-full bg-purple-600/20 flex items-center justify-center mb-6">
                <FiActivity className="text-3xl text-purple-400" />
              </div>

              <h2 className="text-3xl font-semibold mb-3">
                No Career Intelligence Yet
              </h2>

              <p className="text-slate-400">
                Upload your resume to generate AI-powered career insights.
              </p>
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-[#050816] text-white flex">
        <Sidebar />

        <main className="flex-1 overflow-y-auto">
          <Header />

          <div className="p-8 text-center text-slate-400">
            Loading Career Intelligence...
          </div>
        </main>
      </div>
    );
  }

  const atsScore = atsData?.ats_score ?? 0;

  const skillCoverage =
    skillGapData?.analysis?.coverage_score ?? 0;

  const profileStrength = Math.round(
    (atsScore + skillCoverage) / 2
  );

  const careerReadiness = profileStrength;

  const missingSkills =
    skillGapData?.analysis?.missing_skills ?? [];

  const skillFrequency =
    skillGapData?.analysis?.skill_frequency || {};

  const maxFrequency =
    Math.max(...Object.values(skillFrequency), 1);

    const countryMap = {
      us: "United States",
      gb: "United Kingdom",
      in: "India",
      ca: "Canada",
      au: "Australia",
      sg: "Singapore",
    };
    
  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <div className="p-8">

          <div className="grid grid-cols-4 gap-5">
            <StatsCard
              title="Profile Strength"
              value={`${profileStrength}/100`}
              change="Profile Completeness"
              icon={<FiTrendingUp />}
            />

            <StatsCard
              title="ATS Score"
              value={`${atsScore}/100`}
              change={atsData?.status || "Analyzing"}
              icon={<FiTarget />}
            />

            <StatsCard
              title="Career Readiness"
              value={`${careerReadiness}/100`}
              change="AI Assessment"
              icon={<FiActivity />}
            />

            <StatsCard
              title="Missing Skills"
              value={missingSkills.length}
              change="Growth Areas"
              icon={<FiAlertCircle />}
            />
          </div>

          <div className="grid grid-cols-12 gap-6 mt-8">

            <div className="col-span-7 space-y-6">

              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h2 className="text-2xl font-semibold mb-2">
                  Skill Gap Analysis
                </h2>

                <p className="text-slate-400 mb-6">
                  Most requested skills missing from your profile.
                </p>

                <div className="space-y-4">
                  {Object.entries(skillFrequency)
                    .sort((a, b) => b[1] - a[1])
                    .map(([skill, frequency]) => (
                      <div key={skill}>
                        <div className="flex justify-between mb-2">
                          <span className="capitalize font-medium">
                            {skill}
                          </span>

                          <span className="text-purple-400 text-sm">
                            {frequency} Jobs
                          </span>
                        </div>

                        <div className="w-full bg-slate-800 rounded-full h-2">
                          <div
                            className="bg-purple-500 h-2 rounded-full"
                            style={{
                              width: `${
                                (frequency / maxFrequency) * 100
                              }%`,
                            }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
              </div>

              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h2 className="text-2xl font-semibold mb-2">
                  Career Recommendations
                </h2>

                <p className="text-slate-400 mb-8">
                  Best-fit roles based on your profile.
                </p>

                <div className="space-y-4">
                  {recommendationData?.recommended_roles?.map(
                    (role, index) => {
                      const matchScore = Math.min(
                        Math.round(
                          (role.relevance_score / 35) * 100
                        ),
                        100
                      );

                      return (
                        <div
                          key={index}
                          className="border border-slate-700 rounded-xl p-4"
                        >
                          <div className="flex justify-between mb-3">
                            <h3 className="font-medium">
                              {role.role}
                            </h3>

                            <span className="text-green-400 font-semibold">
                              {matchScore}%
                            </span>
                          </div>

                          <div className="w-full bg-slate-800 rounded-full h-2 mb-3">
                            <div
                              className="bg-green-500 h-2 rounded-full"
                              style={{
                                width: `${matchScore}%`,
                              }}
                            />
                          </div>

                          <p className="text-slate-400 text-sm">
                            {role.match_reason}
                          </p>
                        </div>
                      );
                    }
                  )}
                </div>
              </div>

            </div>

            <div className="col-span-5">

              <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">
                <h2 className="text-2xl font-semibold mb-2">
                  Resume Suggestions
                </h2>

                <p className="text-slate-400 mb-6">
                  Improve your ATS performance.
                </p>

                <div className="space-y-4">
                  {resumeSuggestions?.resume_suggestions?.suggestions?.map(
                    (item, index) => (
                      <div
                        key={index}
                        className="border border-slate-700 rounded-xl p-5"
                      >
                        <div className="flex justify-between mb-3">
                          <h3 className="font-medium capitalize">
                            {item.skill}
                          </h3>

                          <span
                            className={`text-xs px-2 py-1 rounded-full ${
                              item.priority === "High"
                                ? "bg-red-500/20 text-red-400"
                                : item.priority === "Medium"
                                ? "bg-yellow-500/20 text-yellow-400"
                                : "bg-green-500/20 text-green-400"
                            }`}
                          >
                            {item.priority}
                          </span>
                        </div>

                        <p className="text-purple-400 text-sm mb-2">
                          {item.why}
                        </p>

                        <p className="text-slate-400 text-sm">
                          {item.resume_action}
                        </p>
                      </div>
                    )
                  )}
                </div>
              </div>

            </div>

          </div>

          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6 mt-6">

            <h2 className="text-2xl font-semibold mb-2">
              Salary Intelligence
            </h2>

            <p className="text-slate-400 mb-6">
              Salary insights across markets.
            </p>

            <div className="grid grid-cols-3 gap-4">

              {salaryData?.country_breakdown?.map(
                (country, index) => (
                  <div
                    key={index}
                    className="border border-slate-700 rounded-xl p-5"
                  >

                    <p className="text-green-400 text-xl font-bold">
                      {country.currency}{" "}
                      {Number(
                        country.average_salary
                      ).toLocaleString()}
                    </p>

                    <p className="text-slate-500 text-sm mt-2">
                      {country.job_count} matching jobs
                    </p>
                  </div>
                )
              )}

            </div>

          </div>

        </div>
      </main>
    </div>
  );
}

export default CareerIntelligence;