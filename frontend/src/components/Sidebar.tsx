"use client";

import { Box, Typography, List, ListItemButton, ListItemText } from "@mui/material";
import Image from "next/image";

const navItems = [
  { label: "Employees", active: true },
  { label: "Scheduler", active: false },
  { label: "Timetracking", active: false },
];

export default function Sidebar() {
  return (
    <Box
      component="nav"
      aria-label="Main navigation"
      sx={{
        width: 260,
        minHeight: "100vh",
        backgroundColor: "#FFFFFF",
        borderRight: "1px solid #E5E7EB",
        display: { xs: "none", lg: "flex" },
        flexDirection: "column",
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 40,
      }}
    >
      {/* Logo section */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1.5,
          px: 3,
          py: 3,
        }}
      >
        <Image
          src="/logo.svg"
          alt="Aperture Labs logo"
          width={30}
          height={30}
        />
        <Typography
          sx={{
            fontWeight: 700,
            fontSize: "1.25rem",
            color: "#1B3A5C",
            letterSpacing: "-0.01em",
          }}
        >
          Push
        </Typography>
      </Box>

      {/* Navigation */}
      <List sx={{ px: 1.5, mt: 1 }}>
        {navItems.map((item) => (
          <ListItemButton
            key={item.label}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              py: 1.2,
              px: 2,
              cursor: "pointer",
              transition: "background-color 200ms ease",
              backgroundColor: item.active ? "#F0F1F3" : "transparent",
              "&:hover": {
                backgroundColor: item.active ? "#E8E9EB" : "rgba(27, 58, 92, 0.04)",
              },
            }}
            aria-current={item.active ? "page" : undefined}
          >
            <ListItemText
              primary={item.label}
              primaryTypographyProps={{
                sx: {
                  fontWeight: item.active ? 600 : 500,
                  fontSize: "0.938rem",
                  color: "#1B3A5C",
                },
              }}
            />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );
}
