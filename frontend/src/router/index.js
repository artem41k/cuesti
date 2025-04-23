import CreateFormView from "@/views/CreateFormView.vue";
import FormView from "@/views/FormView.vue";
import LandingView from "@/views/LandingView.vue";
import LoginView from "@/views/LoginView.vue";
import ManageFormView from "@/views/ManageFormView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import ProfileView from "@/views/ProfileView.vue";
import RegisterView from "@/views/RegisterView.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
    { path: '/', component: LandingView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/profile', component: ProfileView },
    { path: '/manage/forms/create', component: CreateFormView },
    { path: '/manage/forms/:id', component: ManageFormView },
    { path: '/f/:id', component: FormView },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundView },
]


const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;