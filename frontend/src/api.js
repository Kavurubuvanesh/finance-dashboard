import axios from 'axios';

// When on Vercel, we just look at "/api".
// When on localhost, we look at port 8000.
const api = axios.create({
  baseURL: import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000',
});

export default api;