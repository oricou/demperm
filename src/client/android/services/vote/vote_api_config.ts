import axios from 'axios';

const VOTE_API_BASE_URL = 'http://localhost:8080/api/v1'; 

const voteApi = axios.create({
  baseURL: VOTE_API_BASE_URL, 
  headers: {
    'Content-Type': 'application/json',
  },
});

export default voteApi;