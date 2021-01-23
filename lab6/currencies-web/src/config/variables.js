export const axiosBaseUrl = process.env.NODE_ENV === 'development'
    ? 'http://localhost:5000'
    : 'https://currencies-api-lab6.herokuapp.com'