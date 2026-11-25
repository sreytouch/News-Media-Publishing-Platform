import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Button,
  Chip,
  MenuItem,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";

import { ArticleForm, ArticleFormValues } from "../components/article-form";
import { api, ArticlePayload } from "../lib/api";
import { useAuthStore } from "../store/auth-store";
import { Article } from "../types/models";

const statusColor: Record<Article["status"], "default" | "success" | "warning"> = {
  draft: "warning",
  published: "success",
  archived: "default",
};

function toPayload(values: ArticleFormValues): ArticlePayload {
  return {
    title: values.title,
    excerpt: values.excerpt,
    body: values.body,
    category_id: values.category_id,
    cover_image_url: values.cover_image_url.trim() || null,
    tags: values.tags
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean),
  };
}

export function ArticlesPage() {
  const token = useAuthStore((state) => state.accessToken) ?? "";
  const queryClient = useQueryClient();
  const [statusFilter, setStatusFilter] = useState("");
  const [search, setSearch] = useState("");
  const [editing, setEditing] = useState<Article | null>(null);
  const [showForm, setShowForm] = useState(false);

  const categoriesQuery = useQuery({
    queryKey: ["categories"],
    queryFn: () => api.getCategories(token),
  });

  const articlesQuery = useQuery({
    queryKey: ["articles", statusFilter, search],
    queryFn: () => {
      const params = new URLSearchParams();
      if (statusFilter) params.set("status", statusFilter);
      if (search) params.set("search", search);
      return api.getArticles(token, params);
    },
  });

  const invalidate = () => {
    queryClient.invalidateQueries({ queryKey: ["articles"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard"] });
  };

  const saveMutation = useMutation({
    mutationFn: async (values: ArticleFormValues) => {
      const payload = toPayload(values);
      if (editing) {
        return api.updateArticle(token, editing.id, payload);
      }
      return api.createArticle(token, payload);
    },
    onSuccess: () => {
      invalidate();
      setShowForm(false);
      setEditing(null);
    },
  });

  const publishMutation = useMutation({
    mutationFn: (article: Article) =>
      article.status === "published"
        ? api.unpublishArticle(token, article.id)
        : api.publishArticle(token, article.id),
    onSuccess: invalidate,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.deleteArticle(token, id),
    onSuccess: invalidate,
  });

  const categories = categoriesQuery.data ?? [];
  const categoryName = (id: string) => categories.find((category) => category.id === id)?.name ?? "—";

  return (
    <Stack spacing={3}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={2}>
        <div>
          <Typography variant="overline" sx={{ letterSpacing: 2 }}>
            Content
          </Typography>
          <Typography variant="h3">Articles</Typography>
        </div>
        <Button
          variant="contained"
          onClick={() => {
            setEditing(null);
            setShowForm((value) => !value);
          }}
        >
          {showForm && !editing ? "Close" : "New article"}
        </Button>
      </Stack>

      {showForm ? (
        <ArticleForm
          categories={categories}
          initial={editing}
          onSubmit={async (values) => {
            await saveMutation.mutateAsync(values);
          }}
          onCancel={() => {
            setShowForm(false);
            setEditing(null);
          }}
        />
      ) : null}

      <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
        <Stack direction="row" spacing={2} sx={{ mb: 2 }} flexWrap="wrap">
          <TextField
            label="Status"
            select
            size="small"
            sx={{ minWidth: 160 }}
            value={statusFilter}
            onChange={(event) => setStatusFilter(event.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="draft">Draft</MenuItem>
            <MenuItem value="published">Published</MenuItem>
            <MenuItem value="archived">Archived</MenuItem>
          </TextField>
          <TextField
            label="Search"
            size="small"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </Stack>

        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right">Views</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {(articlesQuery.data ?? []).map((article) => (
              <TableRow key={article.id} hover>
                <TableCell>{article.title}</TableCell>
                <TableCell>{categoryName(article.category_id)}</TableCell>
                <TableCell>
                  <Chip size="small" label={article.status} color={statusColor[article.status]} />
                </TableCell>
                <TableCell align="right">{article.view_count}</TableCell>
                <TableCell align="right">
                  <Stack direction="row" spacing={1} justifyContent="flex-end">
                    <Button
                      size="small"
                      onClick={() => {
                        setEditing(article);
                        setShowForm(true);
                      }}
                    >
                      Edit
                    </Button>
                    <Button size="small" onClick={() => publishMutation.mutate(article)}>
                      {article.status === "published" ? "Unpublish" : "Publish"}
                    </Button>
                    <Button size="small" color="error" onClick={() => deleteMutation.mutate(article.id)}>
                      Delete
                    </Button>
                  </Stack>
                </TableCell>
              </TableRow>
            ))}
            {(articlesQuery.data ?? []).length === 0 ? (
              <TableRow>
                <TableCell colSpan={5}>
                  <Typography color="text.secondary" sx={{ py: 2 }}>
                    No articles match these filters.
                  </Typography>
                </TableCell>
              </TableRow>
            ) : null}
          </TableBody>
        </Table>
      </Paper>
    </Stack>
  );
}
