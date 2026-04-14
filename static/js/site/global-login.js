// Modal global de acceso y login por AJAX.
document.addEventListener("DOMContentLoaded", function () {
    const getGlobalLoginElements = function () {
        const modal = document.querySelector("[data-global-login-modal]");
        return {
            modal,
            form: modal ? modal.querySelector("[data-global-login-form]") : null,
            errors: modal ? modal.querySelector("[data-global-login-errors]") : null,
            submit: modal ? modal.querySelector(".clubs-auth-form__submit") : null,
        };
    };

    const openGlobalLoginModal = function () {
        const elements = getGlobalLoginElements();
        if (!elements.modal) {
            window.location.href = "/accounts/login/";
            return;
        }

        elements.modal.hidden = false;
        document.body.classList.add("modal-open");
        window.requestAnimationFrame(function () {
            elements.modal.classList.add("is-visible");
            const usernameInput = elements.modal.querySelector("[name='username']");
            if (usernameInput) {
                usernameInput.focus({ preventScroll: true });
            }
        });
    };

    const closeGlobalLoginModal = function () {
        const elements = getGlobalLoginElements();
        if (!elements.modal) {
            return;
        }

        elements.modal.classList.remove("is-visible");
        document.body.classList.remove("modal-open");
        window.setTimeout(function () {
            elements.modal.hidden = true;
            if (elements.errors) {
                elements.errors.hidden = true;
                elements.errors.textContent = "";
            }
        }, 180);
    };

    document.addEventListener("click", function (event) {
        const loginTrigger = event.target.closest("[data-global-login-open]");
        if (!loginTrigger) {
            return;
        }

        event.preventDefault();
        document.dispatchEvent(new CustomEvent("uax:close-navigation"));
        openGlobalLoginModal();
    });

    document.addEventListener("click", function (event) {
        if (!event.target.closest("[data-global-login-close]")) {
            return;
        }

        closeGlobalLoginModal();
    });

    document.addEventListener("submit", function (event) {
        const form = event.target.closest("[data-global-login-form]");
        if (!form) {
            return;
        }

        event.preventDefault();
        const elements = getGlobalLoginElements();
        if (elements.errors) {
            elements.errors.hidden = true;
            elements.errors.textContent = "";
        }
        if (elements.submit) {
            elements.submit.disabled = true;
            elements.submit.textContent = "Entrando...";
        }

        fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then(function (response) {
                return response.json().then(function (data) {
                    if (!response.ok || !data.ok) {
                        throw data;
                    }
                    return data;
                });
            })
            .then(function (data) {
                if (document.querySelector(".club-detail")) {
                    window.location.reload();
                    return;
                }

                if (data.header_html) {
                    const currentHeader = document.querySelector(".header");
                    const wrapper = document.createElement("div");
                    wrapper.innerHTML = data.header_html.trim();
                    const newHeader = wrapper.firstElementChild;
                    if (currentHeader && newHeader) {
                        currentHeader.replaceWith(newHeader);
                    }
                }

                document.body.dataset.userAuthenticated = "true";
                closeGlobalLoginModal();
                document.dispatchEvent(new CustomEvent("uax:header-updated"));
            })
            .catch(function (error) {
                const errorMessages = error && error.errors && error.errors.length
                    ? error.errors
                    : ["No se pudo iniciar sesión. Revisa tus credenciales."];
                if (elements.errors) {
                    elements.errors.textContent = errorMessages.join(" ");
                    elements.errors.hidden = false;
                }
            })
            .finally(function () {
                if (elements.submit) {
                    elements.submit.disabled = false;
                    elements.submit.textContent = "Iniciar sesión";
                }
            });
    });

    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") {
            return;
        }

        closeGlobalLoginModal();
    });
});
