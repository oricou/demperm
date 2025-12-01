import axios from 'axios';

const SOCIAL_API_BASE_URL = 'http://localhost:8000/api/v1'; 

const ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NTQ1Njk3LCJpYXQiOjE3NjQ1NDIwOTcsImp0aSI6IjEyYzY3YjBiNzVhYjQ5MWFhYTYzYTExM2IxYzkzYmQwIiwidXNlcl9pZCI6Ijc2NzA2MDFiLTAwYjItNGIxYi1hOTM4LTYwNzRlYzIxMjY1MSJ9.5C-NbagG9L4gmPv9WEduTdwvdUe0aPB1ioMr7PTJ43U';

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