export type UserRole = "student" | "proctor" | "admin";

export type SessionStatus = "pending" | "active" | "ended";

export interface ExamSession {
  id: string;
  student_id: string;
  exam_id: string;
  start_time: string;
  status: SessionStatus;
  created_at: string;
}
