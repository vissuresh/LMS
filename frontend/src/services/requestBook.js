import axios from 'axios';
import  createInfoModal  from './modal';


export const requestBook = async (bookId) => {
    let modal = null;

    try {
        const response = await axios.post(`/requests/${bookId}`);
        modal = createInfoModal('Request', 'Request successful!');

    } catch (error) {
        modal = createInfoModal('Request', error.response.data.message);
    }
    modal.show();
}
