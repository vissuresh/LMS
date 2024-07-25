// utils/storage.js

export const saveToStorage = (key, data) => {
    sessionStorage.setItem(key, JSON.stringify(data));
  };
  
  export const loadFromStorage = (key) => {
    const data = sessionStorage.getItem(key);
    return data ? JSON.parse(data) : null;
  };
  
  // Remove data from storage
  export const removeFromStorage = (key) => {
    sessionStorage.removeItem(key);
  };