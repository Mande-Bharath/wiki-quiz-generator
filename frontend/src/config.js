// API configuration
// In production, this will use relative URLs (same domain)
// In development, it uses localhost:8000
const API_BASE_URL = import.meta.env.VITE_API_URL || 
  (import.meta.env.DEV ? 'http://localhost:8000' : '/api');

export default {
  API_BASE_URL
};
