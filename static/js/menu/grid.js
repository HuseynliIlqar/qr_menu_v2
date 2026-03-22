// grid.js — Yemək kartlarını render edir və kateqoriya filtrini idarə edir.

import { buildTag } from './icons.js';
import { openModal } from './modal.js';

let activeCat = 'all';

// ── RENDER ────────────────────────────────────────────────────
export function renderGrid(items) {
    const grid = document.getElementById('food-grid');
    if (!grid) return;

    grid.innerHTML = '';

    items.forEach((item, i) => {
        const card = createCard(item, i);
        grid.appendChild(card);

        // CSS transition üçün bir frame gözlə, sonra visible əlavə et
        requestAnimationFrame(() =>
            requestAnimationFrame(() => card.classList.add('visible'))
        );
    });
}

// ── CARD BUILDER ──────────────────────────────────────────────
function createCard(item, index) {
    const hasDiscount = item.origPrice && item.origPrice > item.price;
    const saved       = hasDiscount ? (item.origPrice - item.price).toFixed(2) : null;

    const card = document.createElement('div');
    card.className = 'food-card';
    card.style.transitionDelay = `${index * 40}ms`;

    card.innerHTML = `
        <div class="food-img-wrap">
            <img src="${item.img}" alt="${item.name}" loading="lazy">
            ${hasDiscount ? `<div class="food-discount">Save $${saved}</div>` : ''}
        </div>
        <div class="food-body">
            <div class="food-name">${item.name}</div>
            <div class="food-desc">${item.desc}</div>
            ${item.tags.length ? `<div class="food-tags">${item.tags.map(buildTag).join('')}</div>` : ''}
            <div class="food-footer">
                <div class="price-wrap">
                    ${hasDiscount
                        ? `<span class="price-old">$${item.origPrice.toFixed(2)}</span>
                           <span class="price-now">$${item.price.toFixed(2)}</span>`
                        : `<span class="price-regular">$${item.price.toFixed(2)}</span>`
                    }
                </div>
                <div class="view-btn">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </div>
            </div>
        </div>
    `;

    card.addEventListener('click', () => openModal(item));
    return card;
}

// ── CATEGORY FILTER ───────────────────────────────────────────
export function initCategoryFilter(allFoods) {
    document.querySelectorAll('.cat-chip').forEach(btn => {
        btn.addEventListener('click', () => {
            // Aktiv class-ı köçür
            document.querySelectorAll('.cat-chip').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            activeCat = btn.dataset.cat;
            const filtered = activeCat === 'all'
                ? allFoods
                : allFoods.filter(f => Array.isArray(f.cats) ? f.cats.includes(activeCat) : f.cat === activeCat);

            renderGrid(filtered);
        });
    });
}
