export interface Job {
  id: number;
  company?: string;
  position_title?: string;
  position_generalized?: string;
  url?: string;
  location?: string;
  expected_salary?: number;
  given_salary?: number;
  flexibility?: string;
  status?: string;
  application_date?: string;
  rejection_date?: string;
  saved_date?: string;
  declined_date?: string;
  rejected_reason?: string;
  cv_path?: string;
  cover_letter_path?: string;
  notes?: string;
}
