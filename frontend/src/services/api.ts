import axios from 'axios';

// Create an Axios instance with base configuration
const api = axios.create({
    baseURL: 'https://api.example.com', // Replace with your API base URL
    timeout: 1000, // Set a timeout for requests
    headers: {'X-Custom-Header': 'foobar'}, // Custom headers, if needed
});

export default api;