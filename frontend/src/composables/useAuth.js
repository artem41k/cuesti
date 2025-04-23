import { authorizeReq, getProfileReq, logoutReq } from "@/services/api";
import { ref } from "vue";

const user = ref(null);

export const useAuth = () => {
  const isAuthenticated = () => !!user.value;

  const fetchUser = async () => {
    try {
      const response = await getProfileReq();
      // TODO: make it better way
      if (response?.detail) {
        throw new Error('Failed to fetch user data');
      }
      user.value = response;
    } catch {
      user.value = null;
    }

  }
  const login = async (creds) => {
    try {
      await authorizeReq(creds);
    } catch (error) {
      return Promise.reject(error);
    }
    await fetchUser();
  }

  const logout = async () => {
    user.value = null;
    localStorage.removeItem('username');
    await logoutReq();
  }
  
  return { user, isAuthenticated, fetchUser, login, logout };
}