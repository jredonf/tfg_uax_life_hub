// Interacciones del explorador de categorías y clubes.
document.addEventListener("DOMContentLoaded", function () {
    // Modal principal de categorías y clubes.
    const clubsModal = document.querySelector("[data-clubs-modal]");

    if (!clubsModal) {
        return;
    }

    // Elementos del modal y del acceso asociado.
    const authModal = document.querySelector("[data-auth-modal]");
    const panels = Array.from(clubsModal.querySelectorAll("[data-modal-panel]"));
    const dialog = clubsModal.querySelector(".clubs-modal__dialog");
    const scrollArea = clubsModal.querySelector(".clubs-modal__scroll-area");
    const openers = Array.from(document.querySelectorAll("[data-modal-open]"));
    const closers = Array.from(document.querySelectorAll("[data-modal-close]"));
    const scrollTopButtons = Array.from(clubsModal.querySelectorAll("[data-modal-scroll-top]"));
    const joinButtonsSelector = "[data-club-join]";
    const authClosers = authModal ? Array.from(authModal.querySelectorAll("[data-auth-close]")) : [];
    const authDialog = authModal ? authModal.querySelector(".clubs-auth-modal__dialog") : null;
    const authForm = authModal ? authModal.querySelector("[data-auth-form]") : null;
    const authErrors = authModal ? authModal.querySelector("[data-auth-errors]") : null;
    const authClubName = authModal ? authModal.querySelector("[data-auth-club-name]") : null;
    let userIsAuthenticated = document.body.dataset.userAuthenticated === "true";
    let lastActiveTrigger = null;
    let pendingJoinButton = null;
    const restoreModalKey = "uaxClubsModalCategory";

    // Lee cookies para enviar el CSRF.
    const getCookie = function (name) {
        const cookieValue = document.cookie
            .split(";")
            .map(function (cookie) {
                return cookie.trim();
            })
            .find(function (cookie) {
                return cookie.startsWith(name + "=");
            });

        return cookieValue ? decodeURIComponent(cookieValue.split("=").slice(1).join("=")) : "";
    };

    // Muestra la categoría activa.
    const showPanel = function (slug) {
        panels.forEach(function (panel) {
            panel.hidden = panel.dataset.modalPanel !== slug;
        });
    };

    // Devuelve la categoría visible.
    const getActiveCategorySlug = function () {
        const activePanel = panels.find(function (panel) {
            return !panel.hidden;
        });

        return activePanel ? activePanel.dataset.modalPanel : "";
    };

    // Abre el modal en la categoría elegida.
    const openClubsModal = function (slug, trigger) {
        showPanel(slug);
        clubsModal.hidden = false;
        document.body.classList.add("modal-open");
        lastActiveTrigger = trigger || null;
        scrollArea.scrollTop = 0;
        window.requestAnimationFrame(function () {
            clubsModal.classList.add("is-visible");
        });
    };

    // Cierra el modal principal.
    const closeClubsModal = function () {
        clubsModal.classList.remove("is-visible");
        if (!authModal || authModal.hidden) {
            document.body.classList.remove("modal-open");
        }
        window.setTimeout(function () {
            clubsModal.hidden = true;
            if (lastActiveTrigger) {
                lastActiveTrigger.focus();
            }
        }, 220);
    };

    // Abre el acceso cuando el usuario no tiene sesión.
    const openAuthModal = function (button) {
        if (!authModal || !authForm) {
            window.location.href = "/accounts/login/";
            return;
        }

        pendingJoinButton = button;
        authForm.reset();
        authErrors.hidden = true;
        authErrors.textContent = "";
        authClubName.textContent = button.dataset.clubName || "este club";
        authModal.hidden = false;
        document.body.classList.add("modal-open");

        window.requestAnimationFrame(function () {
            authModal.classList.add("is-visible");
            const usernameInput = authForm.querySelector('input[name="username"]');
            if (usernameInput) {
                usernameInput.focus();
            }
        });
    };

    // Cierra el modal de acceso.
    const closeAuthModal = function () {
        if (!authModal) {
            return;
        }

        authModal.classList.remove("is-visible");
        if (clubsModal.hidden) {
            document.body.classList.remove("modal-open");
        }
        window.setTimeout(function () {
            authModal.hidden = true;
        }, 220);
    };

    // Actualiza el contador de miembros.
    const updateMembersChip = function (card, membersCount) {
        if (!card) {
            return;
        }

        const chip = card.querySelector(".club-modal-card__members-chip");
        if (!chip) {
            return;
        }

        chip.textContent = membersCount + " miembro" + (membersCount === 1 ? "" : "s");
    };

    // Reordena las tarjetas tras una unión.
    const reorderPanelCards = function (card) {
        const panel = card ? card.closest("[data-modal-panel]") : null;
        const grid = panel ? panel.querySelector(".clubs-modal__grid") : null;

        if (!grid) {
            return;
        }

        const cards = Array.from(grid.querySelectorAll("[data-club-card]"));
        cards.sort(function (leftCard, rightCard) {
            const leftMemberPriority = leftCard.dataset.isMember === "true" ? 0 : 1;
            const rightMemberPriority = rightCard.dataset.isMember === "true" ? 0 : 1;

            if (leftMemberPriority !== rightMemberPriority) {
                return leftMemberPriority - rightMemberPriority;
            }

            const leftMembersCount = Number(leftCard.dataset.membersCount || "0");
            const rightMembersCount = Number(rightCard.dataset.membersCount || "0");

            if (leftMembersCount !== rightMembersCount) {
                return rightMembersCount - leftMembersCount;
            }

            return (leftCard.dataset.clubName || "").localeCompare(rightCard.dataset.clubName || "", "es");
        });

        cards.forEach(function (sortedCard) {
            grid.appendChild(sortedCard);
        });
    };

    // Sustituye el botón por el estado de miembro.
    const replaceWithMemberLink = function (button, detailUrl, label) {
        const memberBadge = document.createElement("span");
        memberBadge.className = "club-modal-card__action is-member";
        memberBadge.textContent = label || "Ya eres miembro";
        button.replaceWith(memberBadge);
        return memberBadge;
    };

    // Guarda la categoría para volver a abrirla.
    const storeCategoryForReturn = function (slug) {
        if (!slug) {
            return;
        }
        sessionStorage.setItem(restoreModalKey, slug);
    };

    // Restaura la categoría al volver.
    const restoreCategoryModal = function () {
        const categoryToRestore = sessionStorage.getItem(restoreModalKey);
        if (!categoryToRestore) {
            return;
        }

        sessionStorage.removeItem(restoreModalKey);
        const opener = document.querySelector('[data-modal-open="' + CSS.escape(categoryToRestore) + '"]');
        openClubsModal(categoryToRestore, opener);

        window.requestAnimationFrame(function () {
            const panel = panels.find(function (candidate) {
                return candidate.dataset.modalPanel === categoryToRestore;
            });
            const eyebrow = panel ? panel.querySelector(".eyebrow") : null;
            if (eyebrow) {
                eyebrow.focus({ preventScroll: true });
            }
        });
    };

    // Recarga la página conservando la categoría.
    const reloadPage = function () {
        const activeSlug = getActiveCategorySlug();
        if (activeSlug) {
            storeCategoryForReturn(activeSlug);
        }

        window.setTimeout(function () {
            window.location.reload();
        }, 180);
    };

    // Envía la unión al club y sincroniza la UI.
    const sendJoinRequest = function (button, options) {
        if (!button || button.dataset.loading === "true") {
            return;
        }

        const shouldReload = options && options.reloadOnSuccess;
        const card = button.closest(".club-modal-card");

        button.dataset.loading = "true";
        button.disabled = true;
        button.classList.add("is-loading");
        button.textContent = "Uniendote...";

        fetch(button.dataset.joinUrl, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then(function (response) {
                if (response.status === 401) {
                    openAuthModal(button);
                    throw new Error("requires_login");
                }
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok || !result.data.ok) {
                    throw new Error("join_failed");
                }

                if (shouldReload) {
                    reloadPage();
                    return;
                }

                replaceWithMemberLink(
                    button,
                    result.data.detail_url || button.dataset.detailUrl,
                    result.data.button_label || "Ya eres miembro"
                );
                if (card) {
                    card.dataset.isMember = "true";
                    card.dataset.membersCount = String(result.data.members_count);
                }
                updateMembersChip(card, result.data.members_count);
                reorderPanelCards(card);

            })
            .catch(function (error) {
                if (error.message === "requires_login") {
                    return;
                }

                button.disabled = false;
                button.dataset.loading = "false";
                button.classList.remove("is-loading");
                button.textContent = "Unirse";
            });
    };

    // Disparadores de apertura del modal.
    openers.forEach(function (opener) {
        opener.addEventListener("click", function (event) {
            if (opener.tagName === "BUTTON") {
                event.stopPropagation();
            }
            openClubsModal(opener.dataset.modalOpen, opener);
        });

        opener.addEventListener("keydown", function (event) {
            if (opener.tagName !== "ARTICLE") {
                return;
            }
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                openClubsModal(opener.dataset.modalOpen, opener);
            }
        });
    });

    // Cierra el modal desde sus botones.
    closers.forEach(function (closer) {
        closer.addEventListener("click", closeClubsModal);
    });

    // Cierra el modal al pulsar fuera.
    clubsModal.addEventListener("click", function (event) {
        if (!dialog.contains(event.target)) {
            closeClubsModal();
        }
    });

    // Vuelve al inicio del panel activo.
    scrollTopButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const panel = button.closest("[data-modal-panel]");
            const eyebrow = panel ? panel.querySelector(".eyebrow") : null;

            if (eyebrow) {
                const scrollTarget =
                    eyebrow.offsetTop -
                    12;

                scrollArea.scrollTo({
                    top: Math.max(scrollTarget, 0),
                    behavior: "smooth",
                });

                window.setTimeout(function () {
                    eyebrow.focus({ preventScroll: true });
                }, 260);
                return;
            }

            scrollArea.scrollTo({ top: 0, behavior: "smooth" });
        });
    });

    // Gestiona detalle y unión dentro del modal.
    clubsModal.addEventListener("click", function (event) {
        const detailLink = event.target.closest("[data-restore-category]");
        if (detailLink) {
            storeCategoryForReturn(detailLink.dataset.restoreCategory);
            return;
        }

        const joinButton = event.target.closest(joinButtonsSelector);
        if (!joinButton) {
            return;
        }

        event.preventDefault();

        if (!userIsAuthenticated) {
            openAuthModal(joinButton);
            return;
        }

        sendJoinRequest(joinButton, { reloadOnSuccess: true });
    });

    // Cierres del modal de acceso.
    if (authModal) {
        authClosers.forEach(function (closer) {
            closer.addEventListener("click", closeAuthModal);
        });

        authModal.addEventListener("click", function (event) {
            if (!authDialog.contains(event.target)) {
                closeAuthModal();
            }
        });
    }

    // Cierra acceso o modal con Escape.
    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") {
            return;
        }

        if (authModal && !authModal.hidden) {
            closeAuthModal();
            return;
        }

        if (!clubsModal.hidden) {
            closeClubsModal();
        }
    });

    // Envía el acceso por AJAX y retoma la unión.
    if (authForm) {
        authForm.addEventListener("submit", function (event) {
            event.preventDefault();

            authErrors.hidden = true;
            authErrors.textContent = "";

            const submitButton = authForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = "Entrando...";

            fetch(authForm.action, {
                method: "POST",
                body: new FormData(authForm),
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (!result.ok || !result.data.ok) {
                        throw result.data;
                    }

                    userIsAuthenticated = true;
                    document.body.dataset.userAuthenticated = "true";
                    closeAuthModal();

                    if (pendingJoinButton) {
                        const buttonToJoin = pendingJoinButton;
                        pendingJoinButton = null;
                        sendJoinRequest(buttonToJoin, { reloadOnSuccess: true });
                        return;
                    }

                    reloadPage();
                })
                .catch(function (errorData) {
                    const errors = errorData && errorData.errors ? errorData.errors : ["No se pudo iniciar sesión."];
                    authErrors.innerHTML = errors
                        .map(function (error) {
                            return "<p>" + error + "</p>";
                        })
                        .join("");
                    authErrors.hidden = false;
                })
                .finally(function () {
                    submitButton.disabled = false;
                    submitButton.textContent = "Iniciar sesión";
                });
        });
    }

    // Restaura el modal al volver con el navegador.
    restoreCategoryModal();
    window.addEventListener("pageshow", restoreCategoryModal);
});
