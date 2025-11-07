// Global site JS: mobile navigation toggle and small accessibility helpers

document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.nav-toggle');
    const navList = document.getElementById('primary-nav');

    if (toggleButton && navList) {
        const closeOnEscape = (event) => {
            if (event.key === 'Escape' && navList.classList.contains('open')) {
                toggleNav(false);
                toggleButton.focus();
            }
        };

        const toggleNav = (forceOpen) => {
            const willOpen = typeof forceOpen === 'boolean' ? forceOpen : !navList.classList.contains('open');
            navList.classList.toggle('open', willOpen);
            toggleButton.setAttribute('aria-expanded', String(willOpen));
            document.removeEventListener('keydown', closeOnEscape);
            if (willOpen) {
                document.addEventListener('keydown', closeOnEscape);
            }
        };

        toggleButton.addEventListener('click', () => toggleNav());
    }
});



