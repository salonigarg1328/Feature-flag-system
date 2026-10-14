import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { fetchHealth } from "../services/auth";

type Status = "checking" | "online" | "offline";

const MILESTONES = [
  { week: "Week 1", title: "Project setup and database (9 tables)", done: true },
  { week: "Week 2", title: "Registration, login and JWT authentication", done: true },
  { week: "Week 3", title: "Environments and feature flags", done: false },
  { week: "Week 4", title: "User groups and targeting rules", done: false },
  { week: "Week 5", title: "Flag versions and audit log", done: false },
  { week: "Week 6", title: "Frontend integration", done: false },
  { week: "Week 7", title: "Testing and final demo", done: false },
];

function formatDate(value: string | null): string {
  if (!value) return "-";
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "-"
    : date.toLocaleDateString(undefined, {
        day: "numeric",
        month: "short",
        year: "numeric",
      });
}

export default function Dashboard() {
  const { user } = useAuth();
  const [status, setStatus] = useState<Status>("checking");

  useEffect(() => {
    fetchHealth()
      .then(() => setStatus("online"))
      .catch(() => setStatus("offline"));
  }, []);

  if (!user) return null;

  return (
    <>
      <h1 className="page-title">Overview</h1>

      <div className="grid">
        <section className="card">
          <h2>Your account</h2>
          <dl className="details">
            <dt>Name</dt>
            <dd>{user.name}</dd>
            <dt>Email</dt>
            <dd>{user.email}</dd>
            <dt>Role</dt>
            <dd>{user.role}</dd>
            <dt>Status</dt>
            <dd>{user.is_active ? "Active" : "Inactive"}</dd>
            <dt>Member since</dt>
            <dd>{formatDate(user.created_at)}</dd>
          </dl>
        </section>

        <section className="card">
          <h2>System</h2>
          <dl className="details">
            <dt>Backend API</dt>
            <dd>
              <span className={`dot dot-${status}`} />
              {status === "checking" && "Checking..."}
              {status === "online" && "Online"}
              {status === "offline" && "Not reachable"}
            </dd>
            <dt>Session</dt>
            <dd>Signed in with a JWT token</dd>
          </dl>
        </section>
      </div>

      <section className="card">
        <h2>Project progress</h2>
        <table className="table">
          <thead>
            <tr>
              <th>Milestone</th>
              <th>Scope</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {MILESTONES.map((m) => (
              <tr key={m.week}>
                <td>{m.week}</td>
                <td>{m.title}</td>
                <td>
                  <span className={m.done ? "tag tag-done" : "tag"}>
                    {m.done ? "Done" : "Planned"}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}
