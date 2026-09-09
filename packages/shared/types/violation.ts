export type ViolationType =
  | "phone"
  | "person"
  | "face_loss"
  | "head_turn"
  | "voice"
  | "noise"
  | "screen_leave";

export interface Violation {
  id: string;
  session_id: string;
  type: ViolationType;
  timestamp: string;
  risk_contribution: number;
  confidence: number;
  meta: Record<string, unknown>;
}
