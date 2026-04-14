// Cabecera principal y navegación del sitio.
document.addEventListener("DOMContentLoaded", function () {
    const getHeaderElements = function () {
        return {
            menuToggle: document.querySelector(".menu-toggle"),
            nav: document.querySelector(".site-nav"),
            accountMenu: document.querySelector("[data-account-menu]"),
            accountToggle: document.querySelector("[data-account-toggle]"),
            accountDropdown: document.querySelector("[data-account-dropdown]"),
        };
    };

    const closeMenu = function () {
        const elements = getHeaderElements();
        if (!elements.nav || !elements.menuToggle) {
            return;
        }

        elements.nav.classList.remove("active");
        elements.menuToggle.setAttribute("aria-expanded", "false");
    };

    const closeAccountMenu = function () {
        const elements = getHeaderElements();
        if (!elements.accountMenu || !elements.accountToggle || !elements.accountDropdown) {
            return;
        }

        elements.accountMenu.classList.remove("is-open");
        elements.accountDropdown.hidden = true;
        elements.accountToggle.setAttribute("aria-expanded", "false");
    };

    document.addEventListener("click", function (event) {
        const menuToggle = event.target.closest(".menu-toggle");
        if (!menuToggle) {
            return;
        }

        const elements = getHeaderElements();
        if (!elements.nav) {
            return;
        }

        const isOpen = elements.nav.classList.toggle("active");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
        if (isOpen) {
            closeAccountMenu();
        }
    });

    document.addEventListener("click", function (event) {
        const accountToggle = event.target.closest("[data-account-toggle]");
        if (!accountToggle) {
            return;
        }

        const accountMenu = accountToggle.closest("[data-account-menu]");
        const accountDropdown = accountMenu
            ? accountMenu.querySelector("[data-account-dropdown]")
            : null;

        if (!accountMenu || !accountDropdown) {
            return;
        }

        const isOpen = accountMenu.classList.toggle("is-open");
        accountDropdown.hidden = !isOpen;
        accountToggle.setAttribute("aria-expanded", String(isOpen));
        if (isOpen) {
            closeMenu();
        }
    });

    document.addEventListener("click", function (event) {
        const elements = getHeaderElements();

        if (event.target.closest(".menu a")) {
            closeMenu();
        }

        if (elements.accountMenu && !elements.accountMenu.contains(event.target)) {
            closeAccountMenu();
        }
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 900) {
            closeMenu();
        }
        closeAccountMenu();
    });

    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") {
            return;
        }

        closeMenu();
        closeAccountMenu();
    });

    document.addEventListener("uax:close-navigation", function () {
        closeMenu();
        closeAccountMenu();
    });

    document.addEventListener("uax:header-updated", function () {
        closeMenu();
        closeAccountMenu();
    });
});
