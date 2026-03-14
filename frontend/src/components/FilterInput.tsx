"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { TextField, InputAdornment } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

interface FilterInputProps {
  onFilterChange: (value: string) => void;
}

export default function FilterInput({ onFilterChange }: FilterInputProps) {
  const [inputValue, setInputValue] = useState("");
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const debouncedChange = useCallback(
    (value: string) => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
      debounceTimerRef.current = setTimeout(() => {
        onFilterChange(value);
      }, 300);
    },
    [onFilterChange],
  );

  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInputValue(value);
    debouncedChange(value);
  };

  return (
    <TextField
      value={inputValue}
      onChange={handleChange}
      placeholder="Filter employees by name"
      variant="outlined"
      fullWidth
      aria-label="Filter employees by name"
      slotProps={{
        input: {
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon sx={{ color: "#9CA3AF", fontSize: 20 }} />
            </InputAdornment>
          ),
        },
      }}
      sx={{
        maxWidth: { xs: "100%", md: "60%" },
        "& .MuiOutlinedInput-root": {
          backgroundColor: "#FFFFFF",
          borderRadius: 0,
          fontSize: "0.875rem",
          height: 44,
          "& fieldset": {
            borderColor: "#D0D5DD",
          },
          "&:hover fieldset": {
            borderColor: "#9CA3AF",
          },
          "&.Mui-focused fieldset": {
            borderColor: "#1DBF73",
            borderWidth: 2,
          },
        },
        "& .MuiOutlinedInput-input": {
          padding: "10px 14px 10px 0",
          "&::placeholder": {
            color: "#9CA3AF",
            opacity: 1,
          },
        },
      }}
    />
  );
}
