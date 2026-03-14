import { useQuery } from "@tanstack/react-query";
import { fetchEmployees } from "@/lib/api";

export function useEmployees(search: string) {
  return useQuery({
    queryKey: ["employees", search],
    queryFn: () => fetchEmployees(search),
    placeholderData: (previousData) => previousData,
    staleTime: 30_000,
  });
}
