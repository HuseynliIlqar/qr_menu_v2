// modal.js — Yemək detay modal-ı idarə edir.
// openModal(item) — xaricdən çağırılır (grid.js-dən)
// closeModal()    — daxildən idarə olunur

import { buildTag } from './icons.js';

const modal = document.getElementById('modal');

// ── OPEN ──────────────────────────────────────────────────────
export function openModal(item) {
    const hasDiscount = item.origPrice && item.origPrice > item.price;

    // Şəkil
    const img = document.getElementById('m-img');
    img.src = item.img;
    img.alt = item.name;

    // Başlıq
    document.getElementById('m-title').textContent = item.name;

    // Uzun təsvir
    document.getElementById('m-desc').textContent = item.long;

    // Endirim badge-i
    const discEl = document.getElementById('m-discount');
    if (hasDiscount) {
        discEl.textContent = `Save $${(item.origPrice - item.price).toFixed(2)}`;
        discEl.style.display = 'block';
    } else {
        discEl.style.display = 'none';
    }

    // Taglar
    document.getElementById('m-tags').innerHTML = item.tags.map(buildTag).join('');

    // Qiymət
    document.getElementById('m-price').innerHTML = hasDiscount
        ? `<span class="modal-price-old">$${item.origPrice.toFixed(2)}</span>
           <span class="modal-price-now">$${item.price.toFixed(2)}</span>`
        : `<span class="modal-price-now" style="color:var(--dark)">$${item.price.toFixed(2)}</span>`;

    // İnqrediyentlər
    document.getElementById('m-ingredients').innerHTML =
        item.ingredients.map(i => `<li>${i}</li>`).join('');

    // Allergenlər
    const allerBox  = document.getElementById('m-allergens');
    const allerText = document.getElementById('m-allergens-text');
    if (item.allergens?.length) {
        allerText.textContent = 'Contains: ' + item.allergens.join(', ');
        allerBox.classList.add('show');
    } else {
        allerBox.classList.remove('show');
    }

    // Modalı aç
    modal.classList.add('open');
    document.body.style.overflow = 'hidden';
}

// ── CLOSE ─────────────────────────────────────────────────────
export function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
}

// ── EVENT LİSTENERS ───────────────────────────────────────────
export function initModal() {
    document.getElementById('m-close')
        ?.addEventListener('click', closeModal);

    modal?.addEventListener('click', e => {
        if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') closeModal();
    });
}
