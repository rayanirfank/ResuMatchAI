import { FiSearch } from "react-icons/fi";

const LOCATIONS = [
  "All Locations",
  "London, UK",
  "Manchester, UK",
  "New York, US",
  "San Francisco, US",
  "Toronto, Canada",
  "Sydney, Australia",
  "Melbourne, Australia",
  "Bangalore, India",
  "Singapore",
  "Remote",
];
const EXPERIENCE_LEVELS = ["All Levels", "Internship", "Junior", "Mid-Level", "Senior", "Lead"];
const JOB_TYPES = ["All Job Types", "Full-Time", "Part-Time", "Contract", "Internship", "Remote"];

const FilterPanel = ({ filters, onChange, onApply, onReset }) => {
  function update(field, value) {
    onChange({ ...filters, [field]: value });
  }

  return (
    <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6 min-h-[686px]">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold">Refine Results</h2>
        <button onClick={onReset} className="text-purple-400 text-sm hover:text-purple-300 transition">
          Reset
        </button>
      </div>

      {/* Search */}
      <div className="mb-5">
        <label className="block text-sm text-slate-400 mb-2">Search Keywords</label>
        <div className="relative">
          <input
            type="text"
            value={filters.search}
            onChange={(e) => update("search", e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && onApply()}
            placeholder="e.g. Data Engineer, Python..."
            className="w-full bg-[#081020] border border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-purple-500 transition"
          />
          <FiSearch className="absolute right-4 top-4 text-slate-400" />
        </div>
      </div>

      {/* Location */}
      <div className="mb-5">
        <label className="block text-sm text-slate-400 mb-2">Location</label>
        <select
          value={filters.location}
          onChange={(e) => update("location", e.target.value)}
          className="w-full bg-[#081020] border border-slate-700 rounded-xl px-4 py-3 outline-none focus:border-purple-500 transition"
        >
          {LOCATIONS.map((l) => <option key={l}>{l}</option>)}
        </select>
      </div>

      {/* Match Score */}
      <div className="mb-8">
        <label className="block text-sm text-slate-400 mb-3">
          Minimum Match Score
        </label>
        <input
          type="range"
          min="0"
          max="100"
          value={filters.minScore}
          onChange={(e) => update("minScore", Number(e.target.value))}
          className="w-full accent-purple-500"
        />
        <p className="text-sm text-purple-400 mt-2">
          Show jobs ≥ {filters.minScore}%
        </p>
      </div>

      <button
        onClick={onApply}
        className="w-full bg-purple-600 hover:bg-purple-700 py-3 rounded-xl font-medium transition"
      >
        Apply Filters
      </button>

      <button
        onClick={onReset}
        className="w-full mt-3 text-slate-400 hover:text-white transition"
      >
        Clear Filters
      </button>
    </div>
  );
};


export default FilterPanel;