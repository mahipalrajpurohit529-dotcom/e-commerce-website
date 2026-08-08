// Auto-dismiss flash messages
document.querySelectorAll('.flash').forEach(el => {
    setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity .5s'; setTimeout(() => el.remove(), 500); }, 3000);
});

// Payment option toggle
document.querySelectorAll('.payment-option').forEach(opt => {
    opt.addEventListener('click', () => {
        document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('active'));
        opt.classList.add('active');
    });
});

// Size/color selections persist visually
document.querySelectorAll('.size-btn input, .color-btn input').forEach(input => {
    input.addEventListener('change', () => {
        const parent = input.closest('.size-options, .color-options');
        parent.querySelectorAll('span').forEach(s => s.style.borderColor = '');
        input.nextElementSibling.style.borderColor = 'var(--accent)';
    });
});

// Smooth navbar scroll effect
let lastY = 0;
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    const currentY = window.scrollY;
    navbar.style.transform = currentY > lastY && currentY > 100 ? 'translateY(-100%)' : 'translateY(0)';
    navbar.style.transition = 'transform .3s ease';
    lastY = currentY;
});