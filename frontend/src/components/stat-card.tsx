import { Paper, Stack, Typography } from "@mui/material";

interface StatCardProps {
  eyebrow: string;
  value: string;
  helper: string;
}

export function StatCard({ eyebrow, value, helper }: StatCardProps) {
  return (
    <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)", height: "100%" }}>
      <Stack spacing={1}>
        <Typography variant="overline" sx={{ letterSpacing: 2 }} color="text.secondary">
          {eyebrow}
        </Typography>
        <Typography variant="h3">{value}</Typography>
        <Typography color="text.secondary">{helper}</Typography>
      </Stack>
    </Paper>
  );
}
