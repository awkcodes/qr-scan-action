import axios from 'axios';

export const getCSRFToken = async () => {
    const response = await axios.get('/offers/csrf/');
    return response.data.csrfToken;
};
