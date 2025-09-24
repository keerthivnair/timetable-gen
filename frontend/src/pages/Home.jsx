import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center h-[80vh] text-center">
      <h2 className="text-3xl font-bold mb-4">Welcome to NEP Timetable Generator</h2>
      <p className="mb-6">Upload student, faculty, and course data to generate conflict-free schedules.</p>
      <Link to="/input" className="px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700">
        Get Started
      </Link>
    </div>
  );
}
