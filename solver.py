import json
import csv
from pathlib import Path
from ortools.sat.python import cp_model

DATA_PATH = Path(__file__).parent / "sample_data.json"
OUTPUT_CSV = Path(__file__).parent / "timetable.csv"


def timeslot_map(days, periods_per_day):
    out = []
    for d_i, d in enumerate(days):
        for p in range(periods_per_day):
            t = d_i * periods_per_day + p
            out.append({"id": t, "day": d, "period": p + 1, "label": f"{d}-P{p+1}"})
    return out


def load_data(path=DATA_PATH):
    with open(path, "r") as f:
        return json.load(f)


def build_and_solve(data, time_limit_seconds=10):
    days = data["days"]
    ppd = int(data["periods_per_day"])
    T = len(days) * ppd

    courses = data["courses"]
    faculty = data["faculty"]
    students = data["students"]

    
    for c in courses:
        if int(c["sessions_per_week"]) > T:
            raise SystemExit(
                f"Course {c['id']} needs more sessions ({c['sessions_per_week']}) than timeslots ({T})"
            )


    # which courses each faculty teaches
    faculty_courses = {}
    for f in faculty:
        faculty_courses[f["id"]] = [c["id"] for c in courses if c["faculty"] == f["id"]]

    # which courses each student takes
    student_courses = {}
    for s in students:
        student_courses[s["id"]] = s.get("enrolled", [])

    model = cp_model.CpModel()

    # Variables: y[(course_id,t)]
    y = {}
    for c in courses:
        cid = c["id"]
        for t in range(T):
            y[(cid, t)] = model.NewBoolVar(f"y_{cid}_{t}")

    # --- HARD CONSTRAINTS ---

    # 1) Each course gets required number of sessions per week
    for c in courses:
        cid = c["id"]
        req = int(c["sessions_per_week"])
        model.Add(sum(y[(cid, t)] for t in range(T)) == req)

    # 2) Faculty unavailability, no double booking, and max hours
    for f in faculty:
        fid = f["id"]
        unavailable = set(f.get("unavailable", []))
        # unavailability -> that course cannot be scheduled at those t
        for cid in faculty_courses.get(fid, []):
            for t in unavailable:
                if 0 <= t < T:
                    model.Add(y[(cid, t)] == 0)

        # no double booking for faculty at any timeslott
        for t in range(T):
            model.Add(sum(y[(cid, t)] for cid in faculty_courses.get(fid, [])) <= 1)

        # optional max hours for f that week
        maxh = int(f.get("max_hours") or 0)
        if maxh > 0:
            model.Add(
                sum(y[(cid, t)] for cid in faculty_courses.get(fid, []) for t in range(T))
                <= maxh
            )

    # 3) Students cannot attend more than one course in same timeslot
    for s in students:
        sid = s["id"]
        cids = student_courses.get(sid, [])
        for t in range(T):
            model.Add(sum(y[(cid, t)] for cid in cids) <= 1)

    # --- SOFT OBJECTIVE: keep faculty preferred times ---
    penalty_terms = []
    for c in courses:
        cid = c["id"]
        fid = c["faculty"]
        pref = set(next((f.get("preferred", []) for f in faculty if f["id"] == fid), []))
        for t in range(T):
            if t not in pref:
                penalty_terms.append(y[(cid, t)])

    model.Minimize(sum(penalty_terms))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_seconds
    solver.parameters.num_search_workers = 8

    print(
        f"Solving (T={T} timeslots, {len(courses)} courses, {len(students)} students)..."
    )
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No feasible solution found. Status:", status)
        return None

    # Build output rows
    times = timeslot_map(days, ppd)
    times_map = {t["id"]: t for t in times}
    rows = []
    for c in courses:
        cid = c["id"]
        for t in range(T):
            if solver.Value(y[(cid, t)]) == 1:
                rows.append(
                    {
                        "course_id": cid,
                        "course_name": c.get("name", ""),
                        "faculty_id": c.get("faculty", ""),
                        "timeslot": t,
                        "day": times_map[t]["day"],
                        "period": times_map[t]["period"],
                    }
                )

    # Write CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["course_id", "course_name", "faculty_id", "timeslot", "day", "period"]
        )
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Wrote {len(rows)} scheduled slots to {OUTPUT_CSV}")
    return rows


if __name__ == "__main__":
    data = load_data()
    out = build_and_solve(data, time_limit_seconds=15)
    if out is None:
        print("No feasible schedule with current data.")
    else:
        # print ordered by timeslot for easy reading
        for r in sorted(out, key=lambda x: x["timeslot"]):
            print(f"{r['day']} P{r['period']}: {r['course_id']} - {r['faculty_id']}")
