import { useQuery } from "@tanstack/react-query";
import {
  AppBar,
  Box,
  Button,
  Chip,
  Container,
  Divider,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import { Link as RouterLink, useParams } from "react-router-dom";

import { api } from "../lib/api";

function formatDate(value: string | null): string {
  if (!value) return "";
  return new Date(value).toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric" });
}

export function ArticleDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const articleQuery = useQuery({
    queryKey: ["public-article", slug],
    queryFn: () => api.getPublicArticle(slug ?? ""),
    enabled: Boolean(slug),
  });

  const article = articleQuery.data;

  return (
    <Box sx={{ minHeight: "100vh", backgroundColor: "background.default" }}>
      <AppBar position="static" elevation={0} color="transparent" sx={{ borderBottom: "1px solid rgba(20,17,14,0.1)" }}>
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <Typography variant="h4" component={RouterLink} to="/" sx={{ textDecoration: "none", color: "text.primary" }}>
            The NMPP Times
          </Typography>
          <Button component={RouterLink} to="/" variant="text" color="inherit">
            Back to headlines
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 5 }}>
        {articleQuery.isError ? (
          <Typography color="error">This article could not be found.</Typography>
        ) : null}

        {article ? (
          <Stack spacing={2}>
            <Stack direction="row" spacing={1} alignItems="center">
              {article.category_name ? <Chip size="small" label={article.category_name} /> : null}
              <Typography variant="caption" color="text.secondary">
                {formatDate(article.published_at)} · {article.view_count} views
              </Typography>
            </Stack>
            <Typography variant="h1" sx={{ fontSize: { xs: "2.2rem", md: "3rem" } }}>
              {article.title}
            </Typography>
            <Typography variant="h6" color="text.secondary">
              {article.excerpt}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {article.author_name ? `By ${article.author_name}` : ""}
            </Typography>
            {article.cover_image_url ? (
              <Box
                component="img"
                src={article.cover_image_url}
                alt={article.title}
                sx={{ width: "100%", borderRadius: 2, my: 2 }}
              />
            ) : null}
            <Divider />
            <Typography component="div" sx={{ whiteSpace: "pre-wrap", lineHeight: 1.8, fontSize: "1.05rem", py: 2 }}>
              {article.body}
            </Typography>
            <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
              {article.tags.map((tag) => (
                <Chip key={tag} size="small" variant="outlined" label={`#${tag}`} />
              ))}
            </Stack>
          </Stack>
        ) : null}
      </Container>
    </Box>
  );
}
