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

    // Mobile submenu toggle for Typewriters
    const submenuToggles = document.querySelectorAll('.submenu-toggle');
    submenuToggles.forEach((btn) => {
        const controlsId = btn.getAttribute('aria-controls');
        const dropdownItem = btn.closest('.nav-dropdown');
        if (!dropdownItem) return;
        btn.addEventListener('click', (event) => {
            event.preventDefault();
            const expanded = btn.getAttribute('aria-expanded') === 'true';
            const nextExpanded = !expanded;
            btn.setAttribute('aria-expanded', String(nextExpanded));
            dropdownItem.classList.toggle('submenu-open', nextExpanded);
        });
    });
});




