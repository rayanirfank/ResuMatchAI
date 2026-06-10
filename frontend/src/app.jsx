import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/dashboard";
import UploadResume from "./pages/uploadresume";
import SavedJobs from "./pages/savedjobs";
import Profile from "./pages/profile";
import Settings from "./pages/settings";
import CareerIntelligence from "./pages/careerintelligence";
import About from "./pages/about";

<Route path="/saved" element={<SavedJobs />} />
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<UploadResume />} />
        <Route path="/saved" element={<SavedJobs />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/career-intelligence" element={<CareerIntelligence />}/>
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
