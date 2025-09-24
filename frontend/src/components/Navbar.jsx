import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4 flex justify-between">
      <h1 className="font-bold">NEP Timetable</h1>
      <div className="space-x-4">
        <Link to="/" className="hover:underline">Home</Link>
        <Link to="/input" className="hover:underline">Input Data</Link>
        <Link to="/timetable" className="hover:underline">Timetable</Link>
      </div>
    </nav>
  );
}
