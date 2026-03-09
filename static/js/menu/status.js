// status.js — Rəstoran açıq/bağlı badge-ini real vaxtla idarə edir.
// Açılış/bağlanış saatlarını buradan dəyiş.

const OPEN_HOUR  = 10; // 10:00
const CLOSE_HOUR = 22; // 22:00

export function initStatus() {
    const badge = document.getElementById('status-badge');
    const text  = document.getElementById('status-text');
    if (!badge || !text) return;

    function update() {
        const hour   = new Date().getHours();
        const isOpen = hour >= OPEN_HOUR && hour < CLOSE_HOUR;

        badge.className  = `status-badge ${isOpen ? 'open' : 'closed'}`;
        text.textContent = isOpen ? 'Open Now' : 'Closed';
    }

    update();

    // Hər dəqiqə yenilə (saatın dəyişməsini tutmaq üçün)
    setInterval(update, 60_000);
}
