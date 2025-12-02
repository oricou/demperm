import axios from 'axios';
import Theme from '@/types/theme';


const SOCIAL_API_BASE_URL = 'http://localhost:8000/api/v1'; 
const ACCESS_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY0NDQzMTM1LCJpYXQiOjE3NjQ0Mzk1MzUsImp0aSI6IjcwMTM1NTVmMmU1MjRlYzBhODkyNGE5YmIzZTkwOTkyIiwidXNlcl9pZCI6ImQyYTViMmU4LWJmYjEtNDJmOS1iMzRiLTM5OWZiYTYzOTg5ZCJ9.wEo8LXI6v2KebIyjVY1Y7RNVvwWzO4msrG1qrHbxHV4';

const socialApi = axios.create({
  baseURL: SOCIAL_API_BASE_URL, 
  headers: {
    'Content-Type': 'application/json',
  },
});

socialApi.interceptors.request.use(
    (config:any) => {
        if (ACCESS_TOKEN) {
            // Le format standard pour les tokens JWT est 'Bearer <token>'
            config.headers.Authorization = `Bearer ${ACCESS_TOKEN}`;
        }
        return config;
    },
    (error: any) => {
        return Promise.reject(error);
    }
);

export default socialApi;

const get_forums = async (): Promise<Theme[]> => {
  try {
    // Call the /forums/ endpoint (returns all forums). Normalize the response so callers always
    // receive an array of Theme objects regardless of wrapper shape.
    const response = await socialApi.get('/forums/');
    const data = response?.data;
    const list: Theme[] = Array.isArray(data)
      ? data
      : data?.results ?? data?.items ?? data ?? [];
    return list;
  } catch (error) {
    console.error('Error fetching forums:', error);
    return [];
  }
};

export { get_forums };