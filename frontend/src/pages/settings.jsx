import Sidebar from "../components/Sidebar/sidebar";
import Header from "../components/Header/header";

function Settings() {
  function clearCandidateData() {
    localStorage.removeItem("activeCandidateId");

    alert("Candidate data cleared.");
  }

  function clearSavedJobs() {
    localStorage.removeItem("savedJobs");
    localStorage.removeItem("savedJobIds");

    alert("Saved jobs cleared.");
  }

  return (
    <div className="min-h-screen bg-[#050816] text-white flex">
      <Sidebar />

      <main className="flex-1 overflow-y-auto">
        <Header />

        <div className="p-8">
          <div className="bg-[#0B1228] border border-slate-800 rounded-2xl p-6">

            <div className="space-y-6">
              {/* Candidate Data */}
              <div className="border border-slate-700 rounded-xl p-5">
                <h3 className="text-lg font-semibold mb-2">
                  Candidate Data
                </h3>

                <p className="text-slate-400 mb-4">
                  Remove the currently active candidate profile.
                </p>

                <button
                  onClick={clearCandidateData}
                  className="bg-yellow-600 hover:bg-yellow-700 px-4 py-2 rounded-lg transition"
                >
                  Clear Candidate Data
                </button>
              </div>

              {/* Saved Jobs */}
              <div className="border border-slate-700 rounded-xl p-5">
                <h3 className="text-lg font-semibold mb-2">
                  Saved Jobs
                </h3>

                <p className="text-slate-400 mb-4">
                  Remove all saved jobs from local storage.
                </p>

                <button
                  onClick={clearSavedJobs}
                  className="bg-orange-600 hover:bg-orange-700 px-4 py-2 rounded-lg transition"
                >
                  Clear Saved Jobs
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Settings;