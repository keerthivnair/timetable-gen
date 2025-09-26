export default function TimetableTable({ data }) {
   const dayIndex = ["Mon", "Tue", "Wed", "Thu", "Fri"]


  const sortedData = [...data].sort((a,b)=> {
    const dayDiff = dayIndex.indexOf(a.day)-dayIndex.indexOf(b.day);
    if(dayDiff!==0) return dayDiff
    return a.period - b.period
  })
  return (
    <table className="min-w-full border border-gray-300">
      <thead className="bg-gray-100">
        <tr>
          <th className="border px-2 py-1">Course ID</th>
          <th className="border px-2 py-1">Course Name</th>
          <th className="border px-2 py-1">Faculty</th>
          <th className="border px-2 py-1">Timeslot</th>
          <th className="border px-2 py-1">Day</th>
          <th className="border px-2 py-1">Period</th>
        </tr>
      </thead>
      <tbody>
        {sortedData.map((row, idx) => (
          <tr key={idx} className="hover:bg-gray-50">
            <td className="border px-2 py-1">{row.course_id}</td>
            <td className="border px-2 py-1">{row.course_name}</td>
            <td className="border px-2 py-1">{row.faculty_id}</td>
            <td className="border px-2 py-1">{row.timeslot}</td>
            <td className="border px-2 py-1">{row.day}</td>
            <td className="border px-2 py-1">{row.period}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
