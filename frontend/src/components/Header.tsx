import { Box, Typography, Avatar } from "@mui/material";

export default function Header() {
  const userName = "John Smith";
  const userEmail = "johnsmith@gmail.com";
  const initials = "JS";

  return (
    <Box
      component="header"
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        py: 3,
        px: { xs: 2, sm: 3, lg: 4 },
        backgroundColor: "#FFFFFF",
        borderColor: "#E5E7EB",
        borderBottomWidth: 1,
        borderBottomStyle: "solid",
      }}
    >
      {/* Page title */}
      <Typography
        variant="h4"
        component="h1"
        sx={{
          fontSize: { xs: "1.5rem", sm: "1.75rem" },
          fontWeight: 700,
          color: "#1B3A5C",
        }}
      >
        Employees
      </Typography>

      {/* User info */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
        }}
      >
        <Avatar
          sx={{
            bgcolor: "#6BB8C4",
            width: 40,
            height: 40,
            fontSize: "0.875rem",
            fontWeight: 600,
          }}
          aria-label={`User avatar for ${userName}`}
        >
          {initials}
        </Avatar>
        <Box sx={{ display: { xs: "none", sm: "block" } }}>
          <Typography
            sx={{
              fontWeight: 600,
              fontSize: "0.875rem",
              color: "#1B3A5C",
              lineHeight: 1.3,
            }}
          >
            {userName}
          </Typography>
          <Typography
            sx={{
              fontSize: "0.75rem",
              color: "#6B7280",
              lineHeight: 1.3,
            }}
          >
            {userEmail}
          </Typography>
        </Box>
      </Box>
    </Box>
  );
}
