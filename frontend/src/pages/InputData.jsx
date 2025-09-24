import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function InputData() {
  const navigate = useNavigate();

  // Initialize states with example JSON so textareas are pre-filled
  const [students, setStudents] = useState(`[
  {
    "id": "S1",
    "name": "Alice",
    "enrolled": ["C101", "C102"]
  },
  {
    "id": "S2",
    "name": "Bob",
    "enrolled": ["C101", "C103"]
  }
]`);

  const [faculty, setFaculty] = useState(`[
  {
    "id": "F1",
    "name": "Dr. Sh",
    "unavailable": [6],
    "preferred": [0,1],
    "max_hours": 12
  },
  {
    "id": "F2",
    "name": "Dr. Si",
    "unavailable": [2],
    "preferred": [4,5],
    "max_hours": 12
  }
]`);

  const [courses, setCourses] = useState(`[
  {
    "id": "C101",
    "name": "Foundations",
    "faculty": "F1",
    "sessions_per_week": 3
  },
  {
    "id": "C102",
    "name": "Assessment",
    "faculty": "F2",
    "sessions_per_week": 2
  },
  {
    "id": "C103",
    "name": "TeachingPractice",
    "faculty": "F3",
    "sessions_per_week": 2
  }
]`);

  async function handleSubmit() {
    try {
      const payload = {
        students: JSON.parse(students),
        faculty: JSON.parse(faculty),
        courses: JSON.parse(courses),
        days: ["Mon", "Tue", "Wed", "Thu", "Fri"],
        periods_per_day: 5,
      };

      const res = await fetch("http://localhost:5000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      localStorage.setItem("timetable", JSON.stringify(data));
      navigate("/timetable");
    } catch (e) {
      alert("Invalid JSON or server error: " + e.message);
    }
  }

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold">Enter Data</h2>

      {/* Students */}
      <div>
        <label className="block font-medium">Students JSON</label>
        <textarea
          className="w-full border rounded p-2 font-mono text-sm"
          rows={8}
          value={students}
          onChange={(e) => setStudents(e.target.value)}
        />
      </div>

      {/* Faculty */}
      <div>
        <label className="block font-medium">Faculty JSON</label>
        <textarea
          className="w-full border rounded p-2 font-mono text-sm"
          rows={8}
          value={faculty}
          onChange={(e) => setFaculty(e.target.value)}
        />
      </div>

      {/* Courses */}
      <div>
        <label className="block font-medium">Courses JSON</label>
        <textarea
          className="w-full border rounded p-2 font-mono text-sm"
          rows={8}
          value={courses}
          onChange={(e) => setCourses(e.target.value)}
        />
      </div>

      <button
        onClick={handleSubmit}
        className="px-4 py-2 bg-green-600 text-white rounded shadow hover:bg-green-700"
      >
        Generate Timetable
      </button>
    </div>
  );
}
