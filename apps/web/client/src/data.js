// Demo data used across the prototype. Nothing here comes from a real database.

export const students = [
  { id: 'STU-2026-001', name: 'Ahmed Ali Hassan',       first: 'Ahmed',  score: 82, level: 'High',   violations: 4, lastEvent: 'Phone detected',      time: '10:47:22', color: '#3b82f6' },
  { id: 'STU-2026-002', name: 'Sara Mohammed Al-Rashid', first: 'Sara',   score: 61, level: 'Review', violations: 2, lastEvent: 'Voice detected',      time: '10:45:10', color: '#f59e0b' },
  { id: 'STU-2026-003', name: 'Omar Khaled Ibrahim',    first: 'Omar',   score: 18, level: 'Normal', violations: 0, lastEvent: 'No violations',       time: '10:30:00', color: '#e11d48' },
  { id: 'STU-2026-004', name: 'Fatima Yusuf Al-Amri',   first: 'Fatima', score: 74, level: 'High',   violations: 3, lastEvent: 'Head turn detected',  time: '10:49:05', color: '#3b82f6' },
  { id: 'STU-2026-005', name: 'Khalid Nasser Salim',    first: 'Khalid', score: 35, level: 'Low',    violations: 1, lastEvent: 'Tab switch detected', time: '10:38:42', color: '#3b82f6' },
  { id: 'STU-2026-006', name: 'Nour Hassan Al-Zahra',   first: 'Nour',   score: 12, level: 'Normal', violations: 0, lastEvent: 'No violations',       time: '10:30:00', color: '#8b5cf6' },
  { id: 'STU-2026-007', name: 'Yusuf Ali Al-Qahtan',    first: 'Yusuf',  score: 55, level: 'Review', violations: 2, lastEvent: 'Multiple persons',    time: '10:43:17', color: '#14b8a6' },
  { id: 'STU-2026-008', name: 'Layla Faisal Al-Mubarak', first: 'Layla',  score: 8,  level: 'Normal', violations: 0, lastEvent: 'Camera offline',      time: '10:20:11', color: '#f97316', offline: true },
];

export const exams = [
  { id: 'EX-4821', name: 'CS-401 · Machine Learning Midterm', department: 'Computer Science', status: 'Live',      students: 142, schedule: '09:30 – 12:00' },
  { id: 'EX-4820', name: 'BUS-302 · Financial Management',    department: 'Business',         status: 'Live',      students: 98,  schedule: '09:00 – 11:30' },
  { id: 'EX-4819', name: 'ENG-201 · Technical Writing',       department: 'Engineering',      status: 'Scheduled', students: 67,  schedule: '13:00 – 15:00' },
  { id: 'EX-4818', name: 'MED-501 · Pharmacology Final',      department: 'Medicine',         status: 'Scheduled', students: 210, schedule: '14:00 – 17:00' },
  { id: 'EX-4817', name: 'PHY-101 · Classical Mechanics',     department: 'Physics',          status: 'Completed', students: 88,  schedule: '07:00 – 09:00' },
  { id: 'EX-4816', name: 'LAW-401 · Constitutional Law',      department: 'Law',              status: 'Completed', students: 55,  schedule: '07:00 – 10:00' },
];

export const alerts = [
  { title: 'Phone Detected',     level: 'High',   student: 'Ahmed Ali Hassan',        text: 'Mobile device detected in camera view',   time: '10:47:22', confidence: 94 },
  { title: 'Head Turn Detected', level: 'Review', student: 'Fatima Yusuf Al-Amri',    text: 'Repeated head movement away from screen', time: '10:49:05', confidence: 87 },
  { title: 'Voice Detected',     level: 'Review', student: 'Sara Mohammed Al-Rashid', text: 'Unexplained audio detected in room',      time: '10:45:10', confidence: 79 },
  { title: 'Multiple Persons',   level: 'High',   student: 'Yusuf Ali Al-Qahtan',     text: 'Additional person detected in background', time: '10:43:17', confidence: 91 },
  { title: 'Tab Switch',         level: 'Low',    student: 'Khalid Nasser Salim',     text: 'Browser tab changed during the exam',     time: '10:38:42', confidence: 99 },
];

export const timeline = [
  { time: '10:47:22', event: 'Phone Detected',  level: 'High',   confidence: '94%',  text: 'Mobile device detected in camera view — right hand' },
  { time: '10:43:11', event: 'Voice Detected',  level: 'Review', confidence: '81%',  text: 'Unexplained audio detected. Possible verbal communication.' },
  { time: '10:38:04', event: 'Head Turn',       level: 'Low',    confidence: '77%',  text: 'Student looked away from screen for 4+ seconds' },
  { time: '10:29:55', event: 'Face Disappeared', level: 'Review', confidence: '99%', text: 'Face not detected in frame for 8 seconds' },
  { time: '10:18:43', event: 'Multiple Persons', level: 'High',   confidence: '89%', text: 'Second face detected in background of frame' },
  { time: '10:12:30', event: 'Tab Switch',      level: 'Low',    confidence: '100%', text: 'Browser window lost focus — 2 occurrences' },
];

export const violationTypes = [
  ['Phone', 34], ['Voice', 28], ['Head Turn', 22], ['Multi-person', 18], ['Tab Switch', 45], ['Face Lost', 12],
];

export const riskDistribution = [
  { label: 'Normal (0–24)',  value: 42, color: '#22c88a' },
  { label: 'Low (25–49)',    value: 28, color: '#3b82f6' },
  { label: 'Medium (50–74)', value: 18, color: '#f0a30a' },
  { label: 'High (75–100)',  value: 12, color: '#dc3545' },
];

export const riskTrend = [30, 33, 32, 38, 36, 41, 39, 45, 43, 40, 35, 37];

export const questions = [
  { text: 'In the context of machine learning, which of the following best describes "overfitting"?',
    options: ['The model performs well on training data but poorly on unseen data', 'The model performs poorly on both training and test data', 'The model has too few parameters to capture the underlying pattern', 'The model generalizes well across all datasets'] },
  { text: 'What does the term "gradient descent" refer to in model optimization?',
    options: ['A technique for selecting relevant features', 'An iterative algorithm to minimize a loss function', 'A method for reducing overfitting', 'A clustering technique that groups similar data points'] },
  { text: 'What is the primary purpose of the activation function in a neural network?',
    options: ['To normalize input data before processing', 'To introduce non-linearity into the network output', 'To reduce the dimensionality of input features', 'To initialize weights during training'] },
  { text: 'Which metric is most useful for evaluating a classifier on imbalanced data?',
    options: ['Accuracy', 'F1 score', 'Mean squared error', 'R-squared'] },
  { text: 'What is a validation set used for?',
    options: ['Training the final model', 'Tuning hyperparameters without touching the test set', 'Increasing the dataset size', 'Removing outliers'] },
];

export const initials = (name) =>
  name.split(' ').slice(0, 2).map((word) => word[0]).join('');
