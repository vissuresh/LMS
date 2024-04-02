import axios from 'axios';
import store from '@/store';

export async function userLoadData(){
    try{
        const response = await axios.get('books/user');
        store.commit('setUserBooks', response.data.books);
        
    } catch (error) {
        console.error('Error:', error);
    }


    try{
        const response = await axios.get('requests/user');
        store.commit('setUserRequests', response.data.requests);
        
    } catch (error) {
        console.error('Error:', error);
    }
}