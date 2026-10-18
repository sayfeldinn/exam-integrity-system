import express from 'express';
import cors from 'cors';

const app = express();
const PORT = process.env.PORT || 4000;
app.use(cors({ origin: process.env.CLIENT_ORIGIN || 'http://localhost:5173' }));
app.use(express.json({ limit: '1mb' }));

const students = [
  { id:'ST-2048', name:'Amelia Mitchell', exam:'Computer Science Midterm', status:'In progress', risk:'Low', timeLeft:'00:42:18' },
  { id:'ST-2051', name:'Samuel Kim', exam:'Computer Science Midterm', status:'In progress', risk:'Low', timeLeft:'00:41:02' },
  { id:'ST-2064', name:'Jordan Davis', exam:'Data Structures Quiz', status:'Review needed', risk:'High', timeLeft:'00:28:44' },
  { id:'ST-2070', name:'Lily Nguyen', exam:'Computer Science Midterm', status:'In progress', risk:'Low', timeLeft:'00:39:51' },
  { id:'ST-2078', name:'Noah Wilson', exam:'Database Systems', status:'Disconnected', risk:'Medium', timeLeft:'00:12:09' }
];
const exams = [
  { id:'EX-1024', name:'Computer Science Midterm', instructor:'Dr. Sarah Chen', students:128, status:'In progress', date:'2026-10-10' },
  { id:'EX-1023', name:'Data Structures Quiz', instructor:'Prof. James Lee', students:64, status:'In progress', date:'2026-10-10' },
  { id:'EX-1022', name:'Database Systems', instructor:'Dr. Emily White', students:92, status:'Scheduled', date:'2026-10-11' }
];
const violations = [
  { id:'V-001', severity:'High', event:'Multiple faces detected', student:'Jordan Davis', examId:'EX-1023', status:'Needs review' },
  { id:'V-002', severity:'Medium', event:'Camera disconnected', student:'Noah Wilson', examId:'EX-1022', status:'Open' },
  { id:'V-003', severity:'Low', event:'Tab switch detected', student:'Emma Carter', examId:'EX-1023', status:'Reviewed' }
];

app.get('/api/health', (_req, res) => res.json({ ok:true, service:'ExamGuard AI API', mode:'mock-data' }));
app.get('/api/dashboard/summary', (_req, res) => res.json({
  activeStudents:1284, liveExams:8, integrityScore:98.4, flaggedEvents:23,
  sessions:2846, completionRate:96.8
}));
app.get('/api/students', (req, res) => {
  const q = String(req.query.q || '').toLowerCase();
  res.json(students.filter(s => `${s.id} ${s.name} ${s.exam}`.toLowerCase().includes(q)));
});
app.get('/api/students/:id', (req, res) => {
  const student = students.find(s => s.id === req.params.id);
  if (!student) return res.status(404).json({ error:'Student not found' });
  res.json(student);
});
app.get('/api/exams', (_req, res) => res.json(exams));
app.get('/api/exams/:id', (req, res) => {
  const exam = exams.find(e => e.id === req.params.id);
  if (!exam) return res.status(404).json({ error:'Exam not found' });
  res.json(exam);
});
app.get('/api/violations', (_req, res) => res.json(violations));
app.post('/api/demo/login', (req, res) => {
  const { email, password } = req.body || {};
  if (!email || !password) return res.status(400).json({ error:'Email and password are required' });
  // Deliberately a demo endpoint. Replace with real authentication before deployment.
  res.json({ demo:true, user:{ email, name:'Alex Morgan', role:'Administrator' } });
});
app.use((req, res) => res.status(404).json({ error:'API route not found' }));
app.listen(PORT, () => console.log(`ExamGuard API listening on http://localhost:${PORT}`));
