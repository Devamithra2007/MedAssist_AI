const TOKEN_KEY = "token";
const ROLE_KEY = "role";

export const authStorage = {
  saveToken(token: string) {
    localStorage.setItem(TOKEN_KEY, token);
  },

  getToken() {
    return localStorage.getItem(TOKEN_KEY);
  },

  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },

  saveRole(role: string) {
    localStorage.setItem(ROLE_KEY, role);
  },

  getRole() {
    return localStorage.getItem(ROLE_KEY);
  },

  clear() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(ROLE_KEY);
  },

  isLoggedIn() {
    return !!localStorage.getItem(TOKEN_KEY);
  },
};