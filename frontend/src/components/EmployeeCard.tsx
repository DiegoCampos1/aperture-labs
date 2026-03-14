import { Box, Typography, Card } from "@mui/material";
import { Employee } from "@/lib/types";

interface EmployeeCardProps {
  employee: Employee;
}

export default function EmployeeCard({ employee }: EmployeeCardProps) {
  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 2,
        borderLeft: "4px solid #C5D1E0",
        backgroundColor: "#FFFFFF",
        p: 2.5,
        display: "flex",
        flexDirection: "column",
        gap: 1.5,
        transition: "box-shadow 200ms ease, border-color 200ms ease",
        "&:hover": {
          boxShadow: "0 2px 8px rgba(27, 58, 92, 0.08)",
          borderLeftColor: "#1DBF73",
        },
      }}
    >
      {/* Employee name */}
      <Typography
        sx={{
          fontWeight: 700,
          fontSize: "0.938rem",
          color: "#1B3A5C",
          lineHeight: 1.4,
        }}
      >
        {employee.first_name}{employee.last_name ? ` ${employee.last_name}` : ""}
      </Typography>

      {/* Total hours */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Typography
          sx={{
            fontWeight: 600,
            fontSize: "0.813rem",
            color: "#1B3A5C",
          }}
        >
          Total hours
        </Typography>
        <Typography
          sx={{
            fontWeight: 700,
            fontSize: "0.938rem",
            color: "#1B3A5C",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {employee.total_hours}
        </Typography>
      </Box>
    </Card>
  );
}
