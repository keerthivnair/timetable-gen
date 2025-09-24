import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import InputData from "./pages/InputData";
import Timetable from "./pages/TimeTable";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/input" element={<InputData />} />
          <Route path="/timetable" element={<Timetable/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
