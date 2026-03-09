// icons.js — SVG ikonlar və label mapping.
// Yeni tag əlavə etmək istəsən sadəcə buraya əlavə et.

export const TAG_ICONS = {
    spicy: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"></path>
    </svg>`,

    vegan: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path>
        <path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path>
    </svg>`,

    popular: `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
        <polyline points="17 6 23 6 23 12"></polyline>
    </svg>`,

    'chef-special': `<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 13.87A4 4 0 0 1 7.41 6a5.11 5.11 0 0 1 1.05-1.54 5 5 0 0 1 7.08 0A5.11 5.11 0 0 1 16.59 6 4 4 0 0 1 18 13.87V21H6Z"></path>
        <line x1="6" y1="17" x2="18" y2="17"></line>
    </svg>`,
};

export const TAG_LABELS = {
    spicy: 'Spicy',
    vegan: 'Vegan',
    popular: 'Popular',
    'chef-special': 'Chef Special',
};

// Tag HTML-i yaratmaq üçün helper
export function buildTag(tagKey) {
    return `<span class="tag tag-${tagKey}">${TAG_ICONS[tagKey]} ${TAG_LABELS[tagKey]}</span>`;
}
