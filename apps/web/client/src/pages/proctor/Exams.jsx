import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Monitor, FileText, X } from 'lucide-react';
import { exams as startingExams } from '../../data.js';
import Pill from '../../components/Pill.jsx';

const filters = ['All', 'Live', 'Scheduled', 'Completed', 'Draft'];
const emptyForm = { name: '', code: '', department: '', start: '', end: '', expected: '' };

export default function Exams() {
  const [exams, setExams] = useState(startingExams);
  const [filter, setFilter] = useState('All');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState(emptyForm);

  const visible = exams.filter((e) => filter === 'All' || e.status === filter);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  function createExam(e) {
    e.preventDefault();
    const newExam = {
      id: `EX-${4822 + exams.length - startingExams.length}`,
      name: form.code ? `${form.code} · ${form.name}` : form.name,
      department: form.department || '—',
      status: 'Draft',
      students: Number(form.expected) || 0,
      schedule: '—',
    };
    setExams([newExam, ...exams]);
    setForm(emptyForm);
    setShowForm(false);
  }

  return (
    <div className="page">
      <div className="toolbar">
        <div className="tabs">
          {filters.map((f) => (
            <button key={f} className={`tab ${filter === f ? 'on' : ''}`} onClick={() => setFilter(f)}>{f}</button>
          ))}
        </div>
        <button className="btn btn-blue" onClick={() => setShowForm(true)}>
          <Plus size={16} /> Create Exam
        </button>
      </div>

      <div className="card table-wrap">
        <table className="table">
          <thead>
            <tr><th>Exam</th><th>Department</th><th>Status</th><th>Students</th><th>Schedule</th><th>Actions</th></tr>
          </thead>
          <tbody>
            {visible.map((e) => (
              <tr key={e.id}>
                <td><span className="exam-name">{e.name}</span><span className="sub-id">{e.id}</span></td>
                <td className="cell-muted">{e.department}</td>
                <td>{e.status === 'Draft' ? <Pill tone="scheduled">Draft</Pill> : <Pill tone={e.status.toLowerCase()}>{e.status}</Pill>}</td>
                <td className="num-cell">{e.students}</td>
                <td className="mono-cell">{e.schedule.replace('–', '-')}</td>
                <td>
                  <div className="row-actions">
                    {e.status === 'Live' && (
                      <Link to="/proctor/live-monitoring" className="btn btn-blue btn-small"><Monitor size={14} /> Monitor</Link>
                    )}
                    <button className="btn btn-outline btn-small">Edit</button>
                    <Link to="/proctor/reports" className="btn btn-ghost btn-small"><FileText size={14} /> Report</Link>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showForm && (
        <div className="modal-overlay" role="dialog" aria-modal="true" onClick={() => setShowForm(false)}>
          <form className="modal-box" onClick={(e) => e.stopPropagation()} onSubmit={createExam}>
            <div className="modal-head">
              <h2>Create New Exam</h2>
              <button type="button" className="modal-close" aria-label="Close" onClick={() => setShowForm(false)}><X size={20} /></button>
            </div>

            <label className="form-field">Exam Name
              <input required value={form.name} onChange={update('name')} placeholder="e.g. CS-401 Machine Learning Midterm" />
            </label>
            <div className="form-row">
              <label className="form-field">Course Code
                <input value={form.code} onChange={update('code')} placeholder="CS-401" />
              </label>
              <label className="form-field">Department
                <input value={form.department} onChange={update('department')} placeholder="Computer Science" />
              </label>
            </div>
            <div className="form-row">
              <label className="form-field">Start Time
                <input type="datetime-local" value={form.start} onChange={update('start')} />
              </label>
              <label className="form-field">End Time
                <input type="datetime-local" value={form.end} onChange={update('end')} />
              </label>
            </div>
            <label className="form-field">Expected Students
              <input type="number" min="0" value={form.expected} onChange={update('expected')} placeholder="120" />
            </label>

            <div className="modal-actions">
              <button type="button" className="btn btn-outline" onClick={() => setShowForm(false)}>Cancel</button>
              <button type="submit" className="btn btn-blue">Create Exam</button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
