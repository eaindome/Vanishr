import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
import Dashboard from "../pages/Dashboard.vue";
import Brokers from "../pages/Brokers.vue";
import Requests from "../pages/Requests.vue";
import Settings from "../pages/Settings.vue";
import Login from "../pages/Login.vue";
import { useUserStore } from "../store/user";

const routes: Array<RouteRecordRaw> = [
  { path: "/login", name: "Login", component: Login },
  {
    path: "/",
    component: () => import("../layouts/MainLayout.vue"),
    children: [
      { path: "", name: "Dashboard", component: Dashboard },
      { path: "brokers", name: "Brokers", component: Brokers },
      { path: "requests", name: "Requests", component: Requests },
      { path: "settings", name: "Settings", component: Settings },
    ],
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Auth Guard
router.beforeEach((to, _, next) => {
  const userStore = useUserStore();

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next({ name: "Login" });
  } else {
    next();
  }
});

export default router;
