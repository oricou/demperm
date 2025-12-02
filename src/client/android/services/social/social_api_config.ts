import axios from 'axios';

const SOCIAL_API_BASE_URL = 'http://localhost:8000/api/v1'; 

const ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NjIzNjI1LCJpYXQiOjE3NjQ2MjAwMjUsImp0aSI6IjkxYjUwNzNhMGNkYTRjODE4M2MyZGMyMzllMTJlNmEwIiwidXNlcl9pZCI6ImU0NTk3YmM5LTk2MGMtNGQ0Zi04MTJiLWM1MTUwNDAwNDAwNSJ9.Sh1C0VkkKx2sn_5Ms6jaVyAA3f_vBBYOaim46mtsjdU';

const socialApi = axios.create({
  baseURL: SOCIAL_API_BASE_URL, 
  headers: {
    'Content-Type': 'application/json',
  },
});

socialApi.interceptors.request.use(
    (config) => {
        if (ACCESS_TOKEN) {
            config.headers.Authorization = `Bearer ${ACCESS_TOKEN}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default socialApi;