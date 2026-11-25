import { ArcElement, BarElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, Tooltip } from "chart.js";
import Grid from "@mui/material/Grid2";
import { useQuery } from "@tanstack/react-query";
import { Bar, Doughnut } from "react-chartjs-2";
import { List, ListItem, ListItemText, Paper, Stack, Typography } from "@mui/material";

import { StatCard } from "../components/stat-card";
import { api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";

ChartJS.register(ArcElement, BarElement, CategoryScale, LinearScale, Legend, Tooltip);

export function DashboardPage() {
  const token = useAuthStore((state) => state.accessToken);
  const dashboardQuery = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => api.getDashboard(token ?? ""),
    enabled: Boolean(token),
  });

  const data = dashboardQuery.data;

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="overline" sx={{ letterSpacing: 2 }}>
          Editorial Overview
        </Typography>
        <Typography variant="h3">Newsroom at a glance</Typography>
        <Typography color="text.secondary">
          Track your publishing pipeline, category coverage, and most-read stories.
        </Typography>
      </div>

      <Grid container spacing={2}>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Total" value={`${data?.total_articles ?? 0}`} helper="All articles" />
        </Grid>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Published" value={`${data?.published ?? 0}`} helper="Live on the site" />
        </Grid>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Drafts" value={`${data?.drafts ?? 0}`} helper="In the pipeline" />
        </Grid>
        <Grid size={{ xs: 6, md: 3 }}>
          <StatCard eyebrow="Archived" value={`${data?.archived ?? 0}`} helper="Retired stories" />
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid size={{ xs: 12, lg: 7 }}>
          <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
            <Typography variant="h5" sx={{ mb: 2 }}>
              Articles by Category
            </Typography>
            <Bar
              data={{
                labels: (data?.by_category ?? []).map((row) => row.category),
                datasets: [
                  {
                    label: "Articles",
                    data: (data?.by_category ?? []).map((row) => row.count),
                    backgroundColor: "#1F2937",
                    borderRadius: 8,
                  },
                ],
              }}
              options={{ responsive: true, plugins: { legend: { display: false } } }}
            />
          </Paper>
        </Grid>
        <Grid size={{ xs: 12, lg: 5 }}>
          <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
            <Typography variant="h5" sx={{ mb: 2 }}>
              Status Breakdown
            </Typography>
            <Doughnut
              data={{
                labels: ["Published", "Drafts", "Archived"],
                datasets: [
                  {
                    data: [data?.published ?? 0, data?.drafts ?? 0, data?.archived ?? 0],
                    backgroundColor: ["#1F2937", "#B91C1C", "#A8A29E"],
                    borderWidth: 0,
                  },
                ],
              }}
            />
          </Paper>
        </Grid>
      </Grid>

      <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
        <Typography variant="h5" sx={{ mb: 1 }}>
          Top viewed
        </Typography>
        <List>
          {(data?.top_viewed ?? []).map((row) => (
            <ListItem key={row.slug} divider disableGutters>
              <ListItemText primary={row.title} secondary={`${row.view_count} views`} />
            </ListItem>
          ))}
          {(data?.top_viewed ?? []).length === 0 ? (
            <Typography color="text.secondary">No articles yet.</Typography>
          ) : null}
        </List>
      </Paper>
    </Stack>
  );
}
