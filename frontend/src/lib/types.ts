export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  total_hours: number;
}

export interface EmployeesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Employee[];
}
