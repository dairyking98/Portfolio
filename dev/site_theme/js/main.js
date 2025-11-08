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

            // When closing the mobile nav, also close any open submenus
            if (!willOpen) {
                const openDropdowns = navList.querySelectorAll('.nav-dropdown.submenu-open');
                openDropdowns.forEach((item) => {
                    const btn = item.querySelector('.submenu-toggle');
                    if (btn) {
                        btn.setAttribute('aria-expanded', 'false');
                    }
                    item.classList.remove('submenu-open');
                });
            }
        };

        toggleButton.addEventListener('click', () => toggleNav());
    }

    // Mobile submenu toggle by clicking the Typewriters link (only on mobile)
    const mqMobile = window.matchMedia('(max-width: 768px)');
    const dropdownLinks = document.querySelectorAll('.nav-dropdown > a');
    dropdownLinks.forEach((anchor) => {
        const dropdownItem = anchor.closest('.nav-dropdown');
        if (!dropdownItem) return;
        anchor.addEventListener('click', (event) => {
            // If mobile viewport or the main nav is in mobile-open state, toggle submenu
            const navList = document.getElementById('primary-nav');
            const isMobile = mqMobile.matches || (navList && navList.classList.contains('open'));
            if (isMobile) {
                event.preventDefault();
                const isOpen = dropdownItem.classList.contains('submenu-open');
                dropdownItem.classList.toggle('submenu-open', !isOpen);
            }
        });
    });
});




