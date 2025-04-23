import axios from "axios";
import router from "@/router";
import { eventBus } from "./eventBus";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
})

api.interceptors.response.use(
    response => response,
    error => {
        if (error?.response.status === 401) {
            if (eventBus.onLogout) {
                eventBus.onLogout();
            }
            if (router.currentRoute.value !== '/login') {
                router.push('/login');
            }
            return error.response;
        } else if (error?.response.status === 404) {
            if (router.currentRoute.value !== '/404') {
                router.push('/404');
            }
        }
        return Promise.reject(error);
    }
)

// Auth

export const authorizeReq = async (creds) => {
    const response = await api.post('/token', creds);
    return response.data;
}

export const registerUserReq = async (creds) => {
    const response = await api.post('/register', creds);
    return response.data;
}

export const logoutReq = async () => {
    const response = await api.post('/logout');
    return response.data;
}

// Form manager

export const getProfileReq = async () => {
    const response = await api.get('/profile');
    return response.data;
}

export const getManagedFormsReq = async () => {
    const response = await api.get('/manage/forms');
    return response.data;
}

export const createFormReq = async (form) => {
    const response = await api.post('/manage/forms', form);
    return response.data;
}

export const getManagedFormReq = async (id) => {
    const response = await api.get(`/manage/forms/${id}`);
    return response.data
}

export const getFormQuestionsWithAnswersReq = async (id) => {
    const response = await api.get(`/manage/forms/${id}/answers`);
    return response.data
}

export const getFormSubmissionsReq = async (id) => {
    const response = await api.get(`/manage/forms/${id}/submissions`);
    return response.data
}

export const deleteFormReq = async (id) => {
    const response = await api.delete(`/manage/forms/${id}`);
    return response.data
}

// User

export const getFormReq = async (id) => {
    const response = await api.get(`/forms/${id}`);
    return response.data
}

export const submitFormReq = async (id, data) => {
    const response = await api.post(`/forms/${id}/submit`, data);
    return response.data
}
