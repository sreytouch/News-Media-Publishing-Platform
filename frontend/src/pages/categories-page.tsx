import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Button,
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

import { api } from "../lib/api";
import { useAuthStore } from "../store/auth-store";
import { Category } from "../types/models";

export function CategoriesPage() {
  const token = useAuthStore((state) => state.accessToken) ?? "";
  const queryClient = useQueryClient();
  const [name, setName] = useState("");
  const [editing, setEditing] = useState<Category | null>(null);
  const [editName, setEditName] = useState("");

  const categoriesQuery = useQuery({
    queryKey: ["categories"],
    queryFn: () => api.getCategories(token),
  });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: ["categories"] });

  const createMutation = useMutation({
    mutationFn: () => api.createCategory(token, { name }),
    onSuccess: () => {
      setName("");
      invalidate();
    },
  });

  const updateMutation = useMutation({
    mutationFn: (category: Category) => api.updateCategory(token, category.id, { name: editName }),
    onSuccess: () => {
      setEditing(null);
      setEditName("");
      invalidate();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => api.deleteCategory(token, id),
    onSuccess: invalidate,
  });

  const createError = createMutation.error instanceof Error ? createMutation.error.message : null;

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="overline" sx={{ letterSpacing: 2 }}>
          Taxonomy
        </Typography>
        <Typography variant="h3">Categories</Typography>
      </div>

      <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
        <Stack direction="row" spacing={2} alignItems="center" component="form"
          onSubmit={(event) => {
            event.preventDefault();
            if (name.trim()) createMutation.mutate();
          }}
        >
          <TextField
            label="New category name"
            size="small"
            value={name}
            onChange={(event) => setName(event.target.value)}
            sx={{ flexGrow: 1 }}
          />
          <Button type="submit" variant="contained" disabled={createMutation.isPending}>
            Add
          </Button>
        </Stack>
        {createError ? (
          <Typography color="error" sx={{ mt: 1 }}>
            {createError}
          </Typography>
        ) : null}
      </Paper>

      <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Slug</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {(categoriesQuery.data ?? []).map((category) => (
              <TableRow key={category.id} hover>
                <TableCell>
                  {editing?.id === category.id ? (
                    <TextField
                      size="small"
                      value={editName}
                      onChange={(event) => setEditName(event.target.value)}
                    />
                  ) : (
                    category.name
                  )}
                </TableCell>
                <TableCell>{category.slug}</TableCell>
                <TableCell align="right">
                  <Stack direction="row" spacing={1} justifyContent="flex-end">
                    {editing?.id === category.id ? (
                      <>
                        <Button size="small" onClick={() => updateMutation.mutate(category)}>
                          Save
                        </Button>
                        <Button size="small" onClick={() => setEditing(null)}>
                          Cancel
                        </Button>
                      </>
                    ) : (
                      <Button
                        size="small"
                        onClick={() => {
                          setEditing(category);
                          setEditName(category.name);
                        }}
                      >
                        Edit
                      </Button>
                    )}
                    <Button size="small" color="error" onClick={() => deleteMutation.mutate(category.id)}>
                      Delete
                    </Button>
                  </Stack>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Stack>
  );
}
