import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  AppBar,
  Box,
  Button,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Chip,
  Container,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import Grid from "@mui/material/Grid2";
import { Link as RouterLink } from "react-router-dom";

import { api } from "../lib/api";

function formatDate(value: string | null): string {
  if (!value) return "";
  return new Date(value).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

export function HomePage() {
  const [category, setCategory] = useState<string | null>(null);

  const categoriesQuery = useQuery({
    queryKey: ["public-categories"],
    queryFn: () => api.getPublicCategories(),
  });

  const articlesQuery = useQuery({
    queryKey: ["public-articles", category],
    queryFn: () => {
      const params = new URLSearchParams();
      if (category) params.set("category", category);
      params.set("page_size", "24");
      return api.getPublicArticles(params);
    },
  });

  const articles = articlesQuery.data?.items ?? [];

  return (
    <Box sx={{ minHeight: "100vh", backgroundColor: "background.default" }}>
      <AppBar position="static" elevation={0} color="transparent" sx={{ borderBottom: "1px solid rgba(20,17,14,0.1)" }}>
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Typography variant="h4" component={RouterLink} to="/" sx={{ textDecoration: "none", color: "text.primary" }}>
            The NMPP Times
          </Typography>
          <Button component={RouterLink} to="/login" variant="outlined" color="inherit">
            Editorial sign in
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 5 }}>
        <Stack spacing={1} sx={{ mb: 4 }}>
          <Typography variant="overline" sx={{ letterSpacing: 3 }}>
            Latest coverage
          </Typography>
          <Typography variant="h2">Today's headlines</Typography>
          <Typography color="text.secondary">
            Independent reporting across technology, business, science, and culture.
          </Typography>
        </Stack>

        <Stack direction="row" spacing={1} sx={{ mb: 4, flexWrap: "wrap", gap: 1 }}>
          <Chip
            label="All"
            color={category === null ? "primary" : "default"}
            onClick={() => setCategory(null)}
          />
          {(categoriesQuery.data ?? []).map((item) => (
            <Chip
              key={item.id}
              label={item.name}
              color={category === item.slug ? "primary" : "default"}
              onClick={() => setCategory(item.slug)}
            />
          ))}
        </Stack>

        <Grid container spacing={3}>
          {articles.map((article) => (
            <Grid key={article.id} size={{ xs: 12, sm: 6, md: 4 }}>
              <Card sx={{ height: "100%", border: "1px solid rgba(20,17,14,0.08)" }}>
                <CardActionArea component={RouterLink} to={`/article/${article.slug}`} sx={{ height: "100%" }}>
                  {article.cover_image_url ? (
                    <CardMedia component="img" height="180" image={article.cover_image_url} alt={article.title} />
                  ) : (
                    <Box sx={{ height: 180, backgroundColor: "#E7E5E4" }} />
                  )}
                  <CardContent>
                    <Stack spacing={1}>
                      <Stack direction="row" spacing={1} alignItems="center">
                        {article.category_name ? <Chip size="small" label={article.category_name} /> : null}
                        <Typography variant="caption" color="text.secondary">
                          {formatDate(article.published_at)}
                        </Typography>
                      </Stack>
                      <Typography variant="h5">{article.title}</Typography>
                      <Typography color="text.secondary">{article.excerpt}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {article.author_name ? `By ${article.author_name}` : ""}
                      </Typography>
                    </Stack>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>

        {articles.length === 0 && !articlesQuery.isLoading ? (
          <Typography color="text.secondary" sx={{ mt: 4 }}>
            No published stories yet.
          </Typography>
        ) : null}
      </Container>
    </Box>
  );
}
