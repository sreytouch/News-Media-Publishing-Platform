import ArticleRounded from "@mui/icons-material/ArticleRounded";
import CategoryRounded from "@mui/icons-material/CategoryRounded";
import DashboardRounded from "@mui/icons-material/DashboardRounded";
import LogoutRounded from "@mui/icons-material/LogoutRounded";
import PublicRounded from "@mui/icons-material/PublicRounded";
import {
  AppBar,
  Box,
  Button,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Stack,
  Toolbar,
  Typography,
} from "@mui/material";
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuthStore } from "../store/auth-store";

const drawerWidth = 260;

const navigation = [
  { label: "Dashboard", icon: <DashboardRounded />, to: "/admin", end: true },
  { label: "Articles", icon: <ArticleRounded />, to: "/admin/articles", end: false },
  { label: "Categories", icon: <CategoryRounded />, to: "/admin/categories", end: false },
];

export function AppShell() {
  const user = useAuthStore((state) => state.user);
  const signOut = useAuthStore((state) => state.signOut);
  const navigate = useNavigate();

  const handleSignOut = () => {
    signOut();
    navigate("/login");
  };

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", backgroundColor: "background.default" }}>
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          ml: { md: `${drawerWidth}px` },
          width: { md: `calc(100% - ${drawerWidth}px)` },
          backgroundColor: "rgba(255,255,255,0.9)",
          backdropFilter: "blur(12px)",
          borderBottom: "1px solid rgba(20,17,14,0.1)",
          color: "text.primary",
        }}
      >
        <Toolbar sx={{ justifyContent: "space-between" }}>
          <div>
            <Typography variant="overline" sx={{ letterSpacing: 2 }}>
              Editorial Desk
            </Typography>
            <Typography variant="h6">Publish news your readers trust</Typography>
          </div>
          <Stack direction="row" spacing={2} alignItems="center">
            <Button component={NavLink} to="/" startIcon={<PublicRounded />} color="inherit">
              View site
            </Button>
            <Typography color="text.secondary">{user?.fullName ?? "Editor"}</Typography>
            <Button variant="outlined" color="inherit" endIcon={<LogoutRounded />} onClick={handleSignOut}>
              Sign out
            </Button>
          </Stack>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", md: "block" },
          width: drawerWidth,
          [`& .MuiDrawer-paper`]: {
            width: drawerWidth,
            boxSizing: "border-box",
            borderRight: "1px solid rgba(20,17,14,0.1)",
            background: "linear-gradient(180deg, #14110E 0%, #1F2937 100%)",
            color: "#FFFFFF",
          },
        }}
      >
        <Toolbar />
        <Stack sx={{ px: 3, py: 4, gap: 3, height: "100%" }}>
          <Stack direction="row" spacing={1.5} alignItems="center">
            <ArticleRounded />
            <div>
              <Typography variant="h6">NMPP</Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                News Media Publishing
              </Typography>
            </div>
          </Stack>
          <List sx={{ p: 0 }}>
            {navigation.map((item) => (
              <ListItemButton
                key={item.to}
                component={NavLink}
                to={item.to}
                end={item.end}
                sx={{
                  borderRadius: 2,
                  mb: 1,
                  color: "inherit",
                  "&.active": {
                    backgroundColor: "rgba(255,255,255,0.14)",
                  },
                }}
              >
                <ListItemIcon sx={{ color: "inherit", minWidth: 40 }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.label} />
              </ListItemButton>
            ))}
          </List>
        </Stack>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 4 }, mt: 10, ml: { md: `${drawerWidth}px` } }}>
        <Outlet />
      </Box>
    </Box>
  );
}
