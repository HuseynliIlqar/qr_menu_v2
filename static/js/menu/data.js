// data.js — Menu məlumatları Django admin-dən gəlir (window.MENU_DATA).

export const foods = (typeof window !== 'undefined' && window.MENU_DATA) ? window.MENU_DATA : [];
