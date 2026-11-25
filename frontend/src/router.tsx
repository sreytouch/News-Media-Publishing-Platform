import { CssBaseline, ThemeProvider } from "@mui/material";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Navigate, RouterProvider, createBrowserRouter } from "react-router-dom";

import { AppShell } from "./layouts/app-shell";
import { useAuthStore } from "./store/auth-store";
import { theme } from "./theme";
import { ArticleDetailPage } from "./pages/article-detail-page";
import { ArticlesPage } from "./pages/articles-page";
import { CategoriesPage } from "./pages/categories-page";
import { DashboardPage } from "./pages/dashboard-page";
import { HomePage } from "./pages/home-page";
import { LoginPage } from "./pages/login-page";

const queryClient = new QueryClient();

function ProtectedRoute() {
  const token = useAuthStore((state) => state.accessToken);
  return token ? <AppShell /> : <Navigate to="/login" replace />;
}

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/article/:slug",
    element: <ArticleDetailPage />,
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/admin",
    element: <ProtectedRoute />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "articles", element: <ArticlesPage /> },
      { path: "categories", element: <CategoriesPage /> },
    ],
  },
]);

export function AppRouter() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
      </QueryClientProvider>
    </ThemeProvider>
  );
}
