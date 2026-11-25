import { Button, MenuItem, Paper, Stack, TextField, Typography } from "@mui/material";
import Grid from "@mui/material/Grid2";
import { useForm } from "react-hook-form";

import { Article, Category } from "../types/models";

export type ArticleFormValues = {
  title: string;
  excerpt: string;
  body: string;
  category_id: string;
  tags: string;
  cover_image_url: string;
};

interface ArticleFormProps {
  categories: Category[];
  initial?: Article | null;
  onSubmit: (payload: ArticleFormValues) => Promise<void>;
  onCancel?: () => void;
}

export function ArticleForm({ categories, initial, onSubmit, onCancel }: ArticleFormProps) {
  const { handleSubmit, register, formState } = useForm<ArticleFormValues>({
    defaultValues: {
      title: initial?.title ?? "",
      excerpt: initial?.excerpt ?? "",
      body: initial?.body ?? "",
      category_id: initial?.category_id ?? categories[0]?.id ?? "",
      tags: initial?.tags?.join(", ") ?? "",
      cover_image_url: initial?.cover_image_url ?? "",
    },
  });

  return (
    <Paper sx={{ p: 3, border: "1px solid rgba(20,17,14,0.08)" }}>
      <Stack spacing={2}>
        <div>
          <Typography variant="h5">{initial ? "Edit article" : "New article"}</Typography>
          <Typography color="text.secondary">
            Draft your story, assign a category, and add tags before publishing.
          </Typography>
        </div>
        <Grid
          container
          spacing={2}
          component="form"
          onSubmit={handleSubmit(async (values) => {
            await onSubmit(values);
          })}
        >
          <Grid size={{ xs: 12, md: 8 }}>
            <TextField label="Title" fullWidth {...register("title", { required: true })} />
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <TextField
              label="Category"
              select
              fullWidth
              defaultValue={initial?.category_id ?? categories[0]?.id ?? ""}
              {...register("category_id", { required: true })}
            >
              {categories.map((category) => (
                <MenuItem key={category.id} value={category.id}>
                  {category.name}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid size={12}>
            <TextField label="Excerpt" fullWidth multiline minRows={2} {...register("excerpt")} />
          </Grid>
          <Grid size={12}>
            <TextField label="Body (Markdown)" fullWidth multiline minRows={6} {...register("body")} />
          </Grid>
          <Grid size={{ xs: 12, md: 8 }}>
            <TextField label="Cover image URL" fullWidth {...register("cover_image_url")} />
          </Grid>
          <Grid size={{ xs: 12, md: 4 }}>
            <TextField label="Tags (comma separated)" fullWidth {...register("tags")} />
          </Grid>
          <Grid size={12}>
            <Stack direction="row" spacing={2}>
              <Button type="submit" variant="contained" disabled={formState.isSubmitting}>
                {initial ? "Save changes" : "Create draft"}
              </Button>
              {onCancel ? (
                <Button variant="text" onClick={onCancel}>
                  Cancel
                </Button>
              ) : null}
            </Stack>
          </Grid>
        </Grid>
      </Stack>
    </Paper>
  );
}
