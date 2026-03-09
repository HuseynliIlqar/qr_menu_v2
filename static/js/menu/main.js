// main.js — Giriş nöqtəsi. Bütün modulları buradan başladırıq.
// HTML-də belə bağla:  <script type="module" src="{% static 'js/menu/main.js' %}"></script>

import { foods }               from './data.js';
import { initSlider }          from './slider.js';
import { renderGrid, initCategoryFilter } from './grid.js';
import { initModal }           from './modal.js';
import { initStatus }          from './status.js';

document.addEventListener('DOMContentLoaded', () => {
    initSlider();
    initStatus();
    initModal();
    initCategoryFilter(foods);
    renderGrid(foods);
});
