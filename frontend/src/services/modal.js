import Modal from 'bootstrap/js/dist/modal';

export const createInfoModal = (title, body) => {
    const modalElement = document.getElementById('infoModal');
    const modal = new Modal(modalElement);
    
    const modalTitle = document.querySelector('#infoModal .modal-title');
    modalTitle.textContent = title;

    const modalBody = document.querySelector('#infoModal .modal-body');
    modalBody.textContent = body;

    return modal;
};



export const createCSVModal = (title, link) => {

    const modalElement = document.getElementById('csvModal');
    const modal = new Modal(modalElement);
    
    const modalTitle = document.querySelector('#csvModal .modal-title');
    modalTitle.textContent = title;

    const modalLink = document.querySelector('#csvModal .modal-body .csv-modal-link');
    modalLink.href = link;
   
    return modal;
}