import axios from "axios";
import { Employee } from "./types";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
});

export async function fetchEmployees(search?: string): Promise<Employee[]> {
  const params: Record<string, string> = {};
  if (search && search.trim() !== "") {
    params.search = search.trim();
  }
  const response = await api.get<Employee[]>("/employees/", { params });
  return response.data;
}

export default api;
