import { Box, Card, Skeleton } from "@mui/material";

export default function EmployeeCardSkeleton() {
  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 2,
        borderLeft: "4px solid #E5E7EB",
        backgroundColor: "#FFFFFF",
        p: 2.5,
        display: "flex",
        flexDirection: "column",
        gap: 1.5,
      }}
    >
      {/* Name skeleton */}
      <Skeleton
        variant="text"
        width="65%"
        height={22}
        animation="pulse"
        sx={{ borderRadius: 1 }}
      />

      {/* Total hours row skeleton */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <Skeleton
          variant="text"
          width="40%"
          height={18}
          animation="pulse"
          sx={{ borderRadius: 1 }}
        />
        <Skeleton
          variant="text"
          width="15%"
          height={22}
          animation="pulse"
          sx={{ borderRadius: 1 }}
        />
      </Box>
    </Card>
  );
}
