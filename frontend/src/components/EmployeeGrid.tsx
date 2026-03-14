"use client";

import { useState, useCallback } from "react";
import { Box, Typography } from "@mui/material";
import FilterInput from "./FilterInput";
import EmployeeCard from "./EmployeeCard";
import EmployeeCardSkeleton from "./EmployeeCardSkeleton";
import { useEmployees } from "@/hooks/useEmployees";

export default function EmployeeGrid() {
  const [search, setSearch] = useState("");
  const { data: employees, isLoading } = useEmployees(search);

  const handleFilterChange = useCallback((value: string) => {
    setSearch(value);
  }, []);

  const showSkeleton = isLoading && !employees;
  const showEmpty = !isLoading && employees && employees.length === 0;
  const showCards = employees && employees.length > 0;

  return (
    <Box sx={{ px: { xs: 2, sm: 3, lg: 4 }, pb: 4, pt: 2 }}>
      {/* Filter input */}
      <Box sx={{ mb: 3 }}>
        <FilterInput onFilterChange={handleFilterChange} />
      </Box>

      {/* Skeleton loading state */}
      {showSkeleton && (
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "1fr",
              md: "repeat(2, 1fr)",
              lg: "repeat(4, 1fr)",
              xl: "repeat(4, 1fr)",
            },
            gap: 2.5,
          }}
          role="status"
          aria-label="Loading employees"
        >
          {Array.from({ length: 4 }).map((_, i) => (
            <EmployeeCardSkeleton key={i} />
          ))}
        </Box>
      )}

      {/* Empty state */}
      {showEmpty && (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            minHeight: 200,
          }}
        >
          <Typography
            sx={{
              fontWeight: 700,
              fontSize: "1.125rem",
              color: "#1B3A5C",
            }}
          >
            No employees match!
          </Typography>
        </Box>
      )}

      {/* Employee cards grid */}
      {showCards && (
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "1fr",
              md: "repeat(2, 1fr)",
              lg: "repeat(4, 1fr)",
              xl: "repeat(4, 1fr)",
            },
            gap: 2.5,
          }}
        >
          {employees.map((employee) => (
            <EmployeeCard key={employee.id} employee={employee} />
          ))}
        </Box>
      )}
    </Box>
  );
}
