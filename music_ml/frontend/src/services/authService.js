import axios from 'axios';

// Configure axios defaults
axios.defaults.withCredentials = true;

export const authService = {
  async getLoginUrl() {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/auth/login", {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
      return response.data.auth_url;
    } catch (error) {
      console.error("Error getting login URL:", error.response?.data || error.message);
      throw error;
    }
  },

  async processCallback(code) {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/auth/callback?code=${code}`, {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error("Error processing callback:", error.response?.data || error.message);
      throw error;
    }
  },

  async checkAuthStatus() {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/auth/check-auth", {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
      return response.data.authenticated;
    } catch (error) {
      console.error("Error checking auth status:", error.response?.data || error.message);
      return false;
    }
  },

  async logout() {
    try {
      await axios.get("http://127.0.0.1:5000/api/auth/logout", {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
    } catch (error) {
      console.error("Error during logout:", error.response?.data || error.message);
      throw error;
    }
  },

  async getUserInfo() {
    try {
      const response = await axios.get("http://127.0.0.1:5000/api/auth/me", {
        headers: {
          'Content-Type': 'application/json',
        },
        withCredentials: true
      });
      return response.data;
    } catch (error) {
      console.error("Error getting user info:", error.response?.data || error.message);
      throw error;
    }
  }
}; 