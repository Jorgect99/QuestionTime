import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Question from "../views/Question.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/question/:slug",
    name: "question",
    component: Question,
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
