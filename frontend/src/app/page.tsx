"use client";

import { Box } from "@mui/material";
import Sidebar from "@/components/Sidebar";
import Header from "@/components/Header";
import EmployeeGrid from "@/components/EmployeeGrid";

export default function Home() {
  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          ml: { xs: 0, lg: "260px" },
          backgroundColor: "#F5F6FA",
          minHeight: "100vh",
        }}
      >
        <Header />
        <EmployeeGrid />
      </Box>
    </Box>
  );
}
