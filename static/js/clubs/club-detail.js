// Interacciones del detalle de un club.
document.addEventListener("DOMContentLoaded", function () {
    // Elementos base de la vista.
    const leaveModal = document.querySelector("[data-leave-modal]");
    const leaveOpen = document.querySelector("[data-leave-open]");
    const leaveClosers = document.querySelectorAll("[data-leave-close]");
    const deleteEventModal = document.querySelector("[data-delete-event-modal]");
    const deleteEventClosers = document.querySelectorAll("[data-delete-event-close]");
    const deleteEventConfirm = document.querySelector("[data-delete-event-confirm]");
    const deleteEventName = document.querySelector("[data-delete-event-name]");
    const joinEventModal = document.querySelector("[data-join-event-modal]");
    const joinEventClosers = document.querySelectorAll("[data-join-event-close]");
    const joinEventConfirm = document.querySelector("[data-join-event-confirm]");
    const joinEventName = document.querySelector("[data-join-event-name]");
    const joinEventMessage = document.querySelector("[data-join-event-message]");
    const joinEventHeading = document.querySelector("[data-join-event-heading]");
    const joinEventCompanionsInput = document.querySelector("[data-join-event-companions]");
    const joinEventMinus = document.querySelector("[data-join-event-minus]");
    const joinEventPlus = document.querySelector("[data-join-event-plus]");
    const leaveEventModal = document.querySelector("[data-leave-event-modal]");
    const leaveEventClosers = document.querySelectorAll("[data-leave-event-close]");
    const leaveEventConfirm = document.querySelector("[data-leave-event-confirm]");
    const leaveEventName = document.querySelector("[data-leave-event-name]");
    let pendingJoinEventForm = null;
    let pendingJoinEventRequest = null;
    let pendingLeaveEventRequest = null;
    const deletePostModal = document.querySelector("[data-delete-post-modal]");
    const deletePostClosers = document.querySelectorAll("[data-delete-post-close]");
    const deletePostConfirm = document.querySelector("[data-delete-post-confirm]");
    const deletePostName = document.querySelector("[data-delete-post-name]");
    const removeMemberModal = document.querySelector("[data-remove-member-modal]");
    const removeMemberClosers = document.querySelectorAll("[data-remove-member-close]");
    const removeMemberName = document.querySelector("[data-remove-member-target-name]");
    const removeMemberForm = document.querySelector("[data-remove-member-form]");
    const removeMemberReason = document.querySelector("[data-remove-member-reason]");
    const removeMemberOther = document.querySelector("[data-remove-member-other]");
    const removeMemberOtherInput = document.querySelector("[data-remove-member-other-input]");
    const createNewsToggle = document.querySelector("[data-create-news-toggle]");
    const createNewsPanel = document.querySelector("[data-create-news-panel]");
    const createNewsClosers = document.querySelectorAll("[data-create-news-close]");
    const editGeneralToggle = document.querySelector("[data-edit-general-toggle]");
    const editGeneralPanel = document.querySelector("[data-edit-general-panel]");
    const editGeneralClosers = document.querySelectorAll("[data-edit-general-close]");
    const editContactToggle = document.querySelector("[data-edit-contact-toggle]");
    const editContactPanel = document.querySelector("[data-edit-contact-panel]");
    const editContactClosers = document.querySelectorAll("[data-edit-contact-close]");
    const createEventToggle = document.querySelector("[data-create-event-toggle]");
    const createEventPanel = document.querySelector("[data-create-event-panel]");
    const createEventClosers = document.querySelectorAll("[data-create-event-close]");
    const createPollToggle = document.querySelector("[data-create-poll-toggle]");
    const createPollPanel = document.querySelector("[data-create-poll-panel]");
    const createPollClosers = document.querySelectorAll("[data-create-poll-close]");
    const pollForm = createPollPanel ? createPollPanel.querySelector(".club-poll-form") : null;
    const pollAddOptionButton = document.querySelector("[data-poll-add-option]");
    const pollOptionalOptionRows = Array.from(document.querySelectorAll(
        "#id_option_3, #id_option_4, #id_option_5, #id_option_6, #id_option_7, #id_option_8"
    )).map(function (input) {
        return input.closest("p");
    }).filter(Boolean);
    const uploadResourceToggle = document.querySelector("[data-upload-resource-toggle]");
    const uploadResourcePanel = document.querySelector("[data-upload-resource-panel]");
    const uploadResourceClosers = document.querySelectorAll("[data-upload-resource-close]");
    const memberSearchInput = document.querySelector("[data-member-search]");
    const memberSortSelect = document.querySelector("[data-member-sort]");
    const memberRanking = document.querySelector("[data-member-ranking]");
    const memberRows = Array.from(document.querySelectorAll("[data-member-row]"));
    const memberSearchEmpty = document.querySelector("[data-member-search-empty]");
    const resourceGallery = document.querySelector("[data-resource-gallery]");
    const newsGallery = document.querySelector("[data-news-gallery]");
    const eventGallery = document.querySelector("[data-event-gallery]");
    const pollGallery = document.querySelector("[data-poll-gallery]");
    const eventMemberPanels = Array.from(document.querySelectorAll("[data-equal-height-panel='events-members']"));
    let eventTitleTooltip = null;
    let pendingDeleteEventForm = null;
    let pendingDeletePostForm = null;

    // Normaliza textos reutilizados en modales.
    const normalizeVisibleCopy = function () {
        const deleteEventDialog = document.querySelector("[data-delete-event-modal] .leave-club-modal__dialog");
        const deleteEventText = document.querySelector("[data-delete-event-name]");
        const deletePostDialog = document.querySelector("[data-delete-post-modal] .leave-club-modal__dialog");
        const deletePostText = document.querySelector("[data-delete-post-name]");
        const removeMemberDialog = document.querySelector("[data-remove-member-modal] .leave-club-modal__dialog");
        const removeMemberText = document.querySelector("[data-remove-member-target-name]");
        const removeMemberReasonLabel = document.querySelector("label[for='remove-member-reason']");
        const removeMemberOtherLabel = document.querySelector("label[for='remove-member-other']");
        const joinEventDialog = document.querySelector("[data-join-event-modal] .leave-club-modal__dialog");
        const joinEventCompanionsLabel = document.querySelector("label[for='join-event-companions']");
        const joinEventSmall = document.querySelector(".club-join-event-modal__companions small");
        const leaveEventDialog = document.querySelector("[data-leave-event-modal] .leave-club-modal__dialog");
        const leaveEventBack = document.querySelector("[data-leave-event-close].club-chip-button");

        if (deleteEventDialog) {
            deleteEventDialog.setAttribute("aria-label", "Confirmar eliminación del evento");
            const paragraph = deleteEventDialog.querySelector("p");
            if (paragraph) {
                paragraph.innerHTML = "¿Seguro que quieres eliminar <strong data-delete-event-name>este evento</strong>? Esta acción no se puede deshacer.";
            }
        }

        if (deletePostDialog) {
            deletePostDialog.setAttribute("aria-label", "Confirmar eliminación de la noticia");
            const paragraph = deletePostDialog.querySelector("p");
            if (paragraph) {
                paragraph.innerHTML = "¿Seguro que quieres eliminar <strong data-delete-post-name>esta noticia</strong>? Esta acción no se puede deshacer.";
            }
        }

        if (removeMemberDialog) {
            removeMemberDialog.setAttribute("aria-label", "Confirmar eliminación del miembro");
            const paragraph = removeMemberDialog.querySelector("p");
            if (paragraph) {
                paragraph.innerHTML = "¿Seguro que quieres eliminar a <strong data-remove-member-target-name>este miembro</strong> del club?";
            }
        }

        if (removeMemberReasonLabel) {
            removeMemberReasonLabel.textContent = "Causa de eliminación";
        }

        if (removeMemberOtherLabel) {
            removeMemberOtherLabel.textContent = "Motivo";
        }

        if (removeMemberOtherInput) {
            removeMemberOtherInput.setAttribute("placeholder", "Máx. 100 caracteres");
        }

        if (joinEventDialog) {
            joinEventDialog.setAttribute("aria-label", "Confirmar inscripción al evento");
        }

        if (joinEventHeading) {
            joinEventHeading.textContent = "Confirmar inscripción";
        }

        if (joinEventMessage) {
            joinEventMessage.innerHTML = "¿Quieres apuntarte a <strong data-join-event-name>este evento</strong>?";
        }

        if (joinEventCompanionsLabel) {
            joinEventCompanionsLabel.textContent = "Llevo acompañantes";
        }

        if (joinEventMinus) {
            joinEventMinus.setAttribute("aria-label", "Reducir acompañantes");
        }

        if (joinEventPlus) {
            joinEventPlus.setAttribute("aria-label", "Aumentar acompañantes");
        }

        if (joinEventSmall) {
            joinEventSmall.textContent = "Máximo 10 acompañantes.";
        }

        if (leaveEventDialog) {
            leaveEventDialog.setAttribute("aria-label", "Confirmar baja del evento");
            const paragraph = leaveEventDialog.querySelector("p");
            if (paragraph) {
                paragraph.innerHTML = "¿Seguro que quieres desapuntarte de <strong data-leave-event-name>este evento</strong>?";
            }
        }

        if (leaveEventBack) {
            leaveEventBack.textContent = "Atrás";
        }
    };

    normalizeVisibleCopy();
    // Ajusta la altura del feed de noticias.
    const syncNewsHeightToResources = function () {
        if (!resourceGallery || !newsGallery) {
            return;
        }

        const newsFeed = newsGallery.querySelector(".club-feed");
        const newsCards = Array.from(newsGallery.querySelectorAll("[data-news-card]"));

        if (!newsFeed || !newsCards.length) {
            return;
        }

        const newsPagination = newsGallery.querySelector("[data-news-pagination]");
        const newsGalleryStyles = window.getComputedStyle(newsGallery);
        const newsGalleryGap = parseFloat(newsGalleryStyles.rowGap || newsGalleryStyles.gap || 0) || 0;
        const newsPaginationHeight = newsPagination && !newsPagination.hidden
            ? Math.ceil(newsPagination.getBoundingClientRect().height) + newsGalleryGap
            : 0;
        const targetGalleryHeight = Math.max(Math.ceil(resourceGallery.getBoundingClientRect().height), 820);
        const resourcePageHeight = Math.max(targetGalleryHeight - newsPaginationHeight, 520);

        if (!resourcePageHeight) {
            return;
        }

        newsFeed.style.height = resourcePageHeight + "px";
        newsFeed.style.minHeight = resourcePageHeight + "px";
        document.documentElement.style.setProperty("--club-resource-page-height", resourcePageHeight + "px");
        newsCards.forEach(function (card) {
            card.style.height = resourcePageHeight + "px";
            card.style.maxHeight = resourcePageHeight + "px";
        });
    };

    // Iguala la altura de eventos y miembros.
    const syncEventMemberPanelHeights = function () {
        if (eventMemberPanels.length < 2) {
            return;
        }

        eventMemberPanels.forEach(function (panel) {
            panel.style.minHeight = "";
        });

        const firstPanelTop = Math.round(eventMemberPanels[0].getBoundingClientRect().top);
        const panelsShareRow = eventMemberPanels.every(function (panel) {
            return Math.abs(Math.round(panel.getBoundingClientRect().top) - firstPanelTop) <= 2;
        });

        if (!panelsShareRow) {
            return;
        }

        const layout = document.querySelector(".club-detail__layout");
        const layoutStyles = layout ? window.getComputedStyle(layout) : null;
        const defaultPanelHeight = layoutStyles
            ? parseFloat(layoutStyles.getPropertyValue("--club-event-member-panel-height")) || 0
            : 0;
        const targetHeight = Math.max.apply(
            null,
            [defaultPanelHeight].concat(eventMemberPanels.map(function (panel) {
                return Math.ceil(panel.getBoundingClientRect().height);
            }))
        );

        eventMemberPanels.forEach(function (panel) {
            panel.style.minHeight = targetHeight + "px";
        });
    };

    // Paginación reutilizable.
    const setupPagination = function (gallery, options) {
        const itemsPerPage = options.itemsPerPage || 6;
        const cards = Array.from(gallery.querySelectorAll(options.cardSelector));
        const linkedCards = options.linkedSelector
            ? Array.from(gallery.querySelectorAll(options.linkedSelector))
            : [];
        const pagination = gallery.querySelector(options.paginationSelector);
        const prevButton = gallery.querySelector(options.prevSelector);
        const nextButton = gallery.querySelector(options.nextSelector);
        const pageLabel = gallery.querySelector(options.pageSelector);
        let currentPage = 0;
        const getFilteredIndexes = function () {
            const indexes = [];
            cards.forEach(function (card, index) {
                if (!options.filterPredicate || options.filterPredicate(card, index)) {
                    indexes.push(index);
                }
            });
            return indexes;
        };

        const getTotalPages = function () {
            return Math.max(Math.ceil(getFilteredIndexes().length / itemsPerPage), 1);
        };

        const renderPage = function () {
            const filteredIndexes = getFilteredIndexes();
            const totalPages = getTotalPages();
            currentPage = Math.min(currentPage, totalPages - 1);
            const start = currentPage * itemsPerPage;
            const end = start + itemsPerPage;
            const visibleIndexes = new Set(filteredIndexes.slice(start, end));

            cards.forEach(function (card, index) {
                card.hidden = !visibleIndexes.has(index);
            });

            linkedCards.forEach(function (card, index) {
                card.hidden = !visibleIndexes.has(index);
            });

            if (pageLabel) {
                pageLabel.textContent = (currentPage + 1) + " / " + totalPages;
            }

            if (prevButton) {
                prevButton.disabled = currentPage === 0;
            }

            if (nextButton) {
                nextButton.disabled = currentPage === totalPages - 1;
            }

            if (pagination) {
                pagination.hidden = options.hideWhenSinglePage && filteredIndexes.length <= itemsPerPage;
            }

            if (typeof options.onRender === "function") {
                options.onRender({
                    filteredCount: filteredIndexes.length,
                    totalPages: totalPages,
                    currentPage: currentPage,
                });
            }
        };

        if (prevButton) {
            prevButton.addEventListener("click", function () {
                currentPage = Math.max(currentPage - 1, 0);
                renderPage();
            });
        }

        if (nextButton) {
            nextButton.addEventListener("click", function () {
                currentPage = Math.min(currentPage + 1, getTotalPages() - 1);
                renderPage();
            });
        }

        renderPage();
        return {
            render: renderPage,
            reset: function () {
                currentPage = 0;
                renderPage();
            },
        };
    };

    // Tooltip para textos truncados.
    const hideRichTooltip = function () {
        if (eventTitleTooltip) {
            eventTitleTooltip.remove();
            eventTitleTooltip = null;
        }
    };

    // Cuenta atrás de encuestas.
    const updatePollCountdowns = function () {
        document.querySelectorAll("[data-poll-countdown]").forEach(function (countdown) {
            const rawDate = countdown.dataset.pollClosesAt;
            if (!rawDate) {
                return;
            }

            const closesAt = new Date(rawDate);
            if (Number.isNaN(closesAt.getTime())) {
                countdown.textContent = "";
                return;
            }

            const diffMs = closesAt.getTime() - Date.now();
            if (diffMs <= 0) {
                countdown.textContent = "Encuesta cerrada";
                return;
            }

            const totalMinutes = Math.floor(diffMs / 60000);
            const days = Math.floor(totalMinutes / (60 * 24));
            const hours = Math.floor((totalMinutes % (60 * 24)) / 60);
            const minutes = totalMinutes % 60;

            countdown.textContent =
                "Cierra en " +
                days + " día" + (days !== 1 ? "s" : "") +
                " ? " +
                hours + " hora" + (hours !== 1 ? "s" : "") +
                " ? " +
                minutes + " min";
        });
    };

    // Cuenta atrás de eventos.
    const updateEventCountdowns = function () {
        document.querySelectorAll("[data-event-countdown]").forEach(function (countdown) {
            const rawDate = countdown.dataset.eventStartAt;
            const value = countdown.querySelector(".club-event-card__countdown-value");
            const alert = countdown.querySelector(".club-event-card__countdown-alert");
            const card = countdown.closest(".club-event-card");
            if (!rawDate || !value) {
                return;
            }

            const startAt = new Date(rawDate);
            if (Number.isNaN(startAt.getTime())) {
                countdown.classList.add("club-event-card__countdown--placeholder");
                return;
            }

            const diffMs = startAt.getTime() - Date.now();
            if (diffMs <= 0) {
                countdown.classList.add("club-event-card__countdown--placeholder");
                return;
            }

            const totalMinutes = Math.floor(diffMs / 60000);
            const days = Math.floor(totalMinutes / (60 * 24));
            const hours = Math.floor((totalMinutes % (60 * 24)) / 60);
            const minutes = totalMinutes % 60;
            const isStartingSoon = diffMs < 12 * 60 * 60 * 1000;

            if (days > 0) {
                value.textContent = days + "d " + hours + "h";
            } else {
                value.textContent = hours + "h " + minutes + "m";
            }

            if (alert) {
                alert.hidden = !isStartingSoon;
            }

            if (card) {
                card.classList.toggle("is-starting-soon", isStartingSoon);
            }

            countdown.classList.remove("club-event-card__countdown--placeholder");
        });
    };

    // Posiciona el tooltip cuando el texto se corta.
    const showRichTooltip = function (target) {
        const text = target.dataset.tooltip;
        if (!text) {
            return;
        }

        const hasOverflow =
            target.scrollWidth > target.clientWidth ||
            target.scrollHeight > target.clientHeight;
        const textChild = target.querySelector(".club-event-card__title-text");
        const childHasOverflow = textChild
            ? textChild.scrollWidth > textChild.clientWidth || textChild.scrollHeight > textChild.clientHeight
            : false;

        if (!hasOverflow && !childHasOverflow) {
            return;
        }

        hideRichTooltip();
        eventTitleTooltip = document.createElement("div");
        eventTitleTooltip.className = "club-event-title-tooltip";
        eventTitleTooltip.textContent = text;
        document.body.appendChild(eventTitleTooltip);

        const targetRect = target.getBoundingClientRect();
        const tooltipRect = eventTitleTooltip.getBoundingClientRect();
        const left = Math.min(
            Math.max(targetRect.left, 16),
            window.innerWidth - tooltipRect.width - 16
        );
        const topAbove = targetRect.top - tooltipRect.height - 10;
        const top = topAbove >= 16 ? topAbove : targetRect.bottom + 10;

        eventTitleTooltip.style.left = left + "px";
        eventTitleTooltip.style.top = top + "px";
    };

    // Abre y cierra tooltips.
    document.addEventListener("mouseover", function (event) {
        const tooltipTarget = event.target.closest("[data-tooltip]");
        if (tooltipTarget) {
            showRichTooltip(tooltipTarget);
        }
    });

    document.addEventListener("mouseout", function (event) {
        if (event.target.closest("[data-tooltip]")) {
            hideRichTooltip();
        }
    });

    document.addEventListener("focusin", function (event) {
        const tooltipTarget = event.target.closest("[data-tooltip]");
        if (tooltipTarget) {
            showRichTooltip(tooltipTarget);
        }
    });

    document.addEventListener("focusout", function (event) {
        if (event.target.closest("[data-tooltip]")) {
            hideRichTooltip();
        }
    });

    window.addEventListener("scroll", hideRichTooltip, true);
    window.addEventListener("resize", hideRichTooltip);

    if (memberRows.length) {
        // Ordena la lista de miembros.
        const sortMemberRows = function () {
            if (!memberRanking || !memberSortSelect) {
                return;
            }

            const sortMode = memberSortSelect.value;
            const sortedRows = memberRows.slice().sort(function (firstRow, secondRow) {
                if (sortMode === "name") {
                    return (firstRow.dataset.memberName || "").localeCompare(secondRow.dataset.memberName || "", "es", { sensitivity: "base" });
                }
                if (sortMode === "role") {
                    return (firstRow.dataset.memberRole || "").localeCompare(secondRow.dataset.memberRole || "", "es", { sensitivity: "base" });
                }
                return Number(firstRow.dataset.memberJoinedOrder || 0) - Number(secondRow.dataset.memberJoinedOrder || 0);
            });

            sortedRows.forEach(function (row) {
                memberRanking.appendChild(row);
            });
        };

        // Filtra miembros desde el buscador.
        const filterMemberRows = function () {
            const query = memberSearchInput ? memberSearchInput.value.trim().toLowerCase() : "";
            let visibleRows = 0;

            memberRows.forEach(function (row) {
                const searchableText = (row.dataset.memberSearchText || "").toLowerCase();
                const isVisible = !query || searchableText.includes(query);
                row.hidden = !isVisible;
                if (isVisible) {
                    visibleRows += 1;
                }
            });

            if (memberSearchEmpty) {
                memberSearchEmpty.hidden = visibleRows !== 0;
            }
            syncEventMemberPanelHeights();
        };

        if (memberSearchInput) {
            memberSearchInput.addEventListener("input", filterMemberRows);
        }

        if (memberSortSelect) {
            memberSortSelect.addEventListener("change", function () {
                sortMemberRows();
                filterMemberRows();
                syncEventMemberPanelHeights();
            });
        }
    }

    // Atajos del panel de gestión.
    document.querySelectorAll("[data-management-trigger]").forEach(function (button) {
        button.addEventListener("click", function () {
            const targetSelector = button.dataset.managementTrigger;
            const target = targetSelector ? document.querySelector(targetSelector) : null;
            if (target) {
                target.click();
            }
        });
    });

    // Utilidades comunes para modales.
    const openModal = function (modal) {
        if (!modal) {
            return;
        }

        modal.hidden = false;
        modal.classList.add("is-visible");
        document.body.classList.add("modal-open");
    };

    const closeModal = function (modal) {
        if (!modal) {
            return;
        }

        modal.classList.remove("is-visible");
        modal.hidden = true;
        document.body.classList.remove("modal-open");
    };

    // Limpia la validación del modal de eventos.
    const clearJoinEventValidationState = function () {
        if (joinEventCompanionsInput) {
            joinEventCompanionsInput.classList.remove("is-invalid");
        }
        if (joinEventConfirm) {
            joinEventConfirm.classList.remove("is-invalid");
        }
    };

    // Prepara el modal de inscripción a eventos.
    const openJoinEventModalForRequest = function (requestConfig) {
        pendingJoinEventRequest = requestConfig;
        clearJoinEventValidationState();
        const eventTitle = requestConfig.title || "este evento";
        const companionsCount = Number(requestConfig.companionsCount || 0);
        if (joinEventName) {
            joinEventName.textContent = eventTitle;
        }
        if (joinEventMessage) {
            joinEventMessage.innerHTML = "";
            if (requestConfig.mode === "edit") {
                const strong = document.createElement("strong");
                strong.textContent = eventTitle;
                joinEventMessage.append("Ya estás apuntado al evento ");
                joinEventMessage.append(strong);
                joinEventMessage.append(` y llevas ${companionsCount} acompañantes. ¿Deseas modificar el número de acompañantes?`);
            } else {
                const strong = document.createElement("strong");
                strong.textContent = eventTitle;
                joinEventMessage.append("¿Quieres apuntarte a ");
                joinEventMessage.append(strong);
                joinEventMessage.append("?");
            }
        }
        if (joinEventHeading) {
            joinEventHeading.textContent = requestConfig.mode === "edit" ? "Editar acompañantes" : "Confirmar inscripción";
        }
        if (joinEventConfirm) {
            joinEventConfirm.textContent = requestConfig.mode === "edit" ? "Guardar cambios" : "Confirmar";
        }
        if (joinEventCompanionsInput) {
            joinEventCompanionsInput.value = String(Number(requestConfig.companionsCount || 0));
        }
        openModal(joinEventModal);
    };

    // Abre y cierra modales de edición.
    if (createNewsToggle && createNewsPanel) {
        createNewsToggle.addEventListener("click", function () {
            createNewsPanel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = createNewsPanel.querySelector("input, textarea, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    }

    const closeCreateNewsModal = function () {
        if (!createNewsPanel) {
            return;
        }

        createNewsPanel.hidden = true;
        document.body.classList.remove("modal-open");
        if (createNewsToggle) {
            createNewsToggle.focus({ preventScroll: true });
        }
    };

    createNewsClosers.forEach(function (closer) {
        closer.addEventListener("click", closeCreateNewsModal);
    });

    if (editGeneralToggle && editGeneralPanel) {
        editGeneralToggle.addEventListener("click", function () {
            editGeneralPanel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = editGeneralPanel.querySelector("input, textarea, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    }

    const closeEditGeneralModal = function () {
        if (!editGeneralPanel) {
            return;
        }

        editGeneralPanel.hidden = true;
        document.body.classList.remove("modal-open");
        if (editGeneralToggle) {
            editGeneralToggle.focus({ preventScroll: true });
        }
    };

    editGeneralClosers.forEach(function (closer) {
        closer.addEventListener("click", closeEditGeneralModal);
    });

    if (editContactToggle && editContactPanel) {
        editContactToggle.addEventListener("click", function () {
            editContactPanel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = editContactPanel.querySelector("input, textarea, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    }

    const closeEditContactModal = function () {
        if (!editContactPanel) {
            return;
        }

        editContactPanel.hidden = true;
        document.body.classList.remove("modal-open");
        if (editContactToggle) {
            editContactToggle.focus({ preventScroll: true });
        }
    };

    editContactClosers.forEach(function (closer) {
        closer.addEventListener("click", closeEditContactModal);
    });

    if (createEventToggle && createEventPanel) {
        createEventToggle.addEventListener("click", function () {
            createEventPanel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = createEventPanel.querySelector("input, textarea, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    }

    const closeCreateEventModal = function () {
        if (!createEventPanel) {
            return;
        }

        createEventPanel.hidden = true;
        document.body.classList.remove("modal-open");
        if (createEventToggle) {
            createEventToggle.focus({ preventScroll: true });
        }
    };

    createEventClosers.forEach(function (closer) {
        closer.addEventListener("click", closeCreateEventModal);
    });

    if (createPollToggle && createPollPanel) {
        createPollToggle.addEventListener("click", function () {
            createPollPanel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = createPollPanel.querySelector("input, textarea, select, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    }

    const closeCreatePollModal = function () {
        if (!createPollPanel) {
            return;
        }

        createPollPanel.hidden = true;
        document.body.classList.remove("modal-open");
        if (createPollToggle) {
            createPollToggle.focus({ preventScroll: true });
        }
    };

    createPollClosers.forEach(function (closer) {
        closer.addEventListener("click", closeCreatePollModal);
    });

    // Gestiona opciones dinámicas de encuestas.
    const syncPollOptionRows = function () {
        if (!pollOptionalOptionRows.length || !pollAddOptionButton) {
            return;
        }

        pollOptionalOptionRows.forEach(function (row) {
            const input = row.querySelector("input");
            row.hidden = !input || !input.value.trim();
        });

        pollAddOptionButton.hidden = pollOptionalOptionRows.every(function (row) {
            return !row.hidden;
        });
    };

    if (pollAddOptionButton) {
        syncPollOptionRows();
        pollAddOptionButton.addEventListener("click", function () {
            const hiddenRows = pollOptionalOptionRows.filter(function (row) {
                return row.hidden;
            });
            const nextRow = hiddenRows[0];

            if (!nextRow) {
                pollAddOptionButton.hidden = true;
                return;
            }

            nextRow.hidden = false;
            const input = nextRow.querySelector("input");
            if (input) {
                input.focus({ preventScroll: true });
            }
            pollAddOptionButton.hidden = pollOptionalOptionRows.every(function (row) {
                return !row.hidden;
            });
        });
    }

    // Contadores de caracteres.
    const initMaxLengthCounters = function (root) {
        (root || document).querySelectorAll("input[maxlength], textarea[maxlength]").forEach(function (field) {
            const maxLength = Number(field.getAttribute("maxlength"));
            if (!maxLength || field.dataset.maxlengthCounterReady === "true") {
                return;
            }
            field.dataset.maxlengthCounterReady = "true";

            const wrapper = field.closest("p, .club-comment-form, .club-event-card__edit-body, .club-manager-form");
            if (!wrapper) {
                return;
            }

            const staticHint = wrapper.querySelector(".helptext, .club-comment-form__limit");
            const existingCounter = wrapper.querySelector("[data-char-count]");
            if (existingCounter) {
                return;
            }

            const meta = document.createElement("div");
            meta.className = "maxlength-counter__meta";

            if (staticHint) {
                staticHint.parentNode.insertBefore(meta, staticHint);
                meta.appendChild(staticHint);
            } else {
                field.insertAdjacentElement("afterend", meta);
            }

            const counter = document.createElement("span");
            counter.className = "maxlength-counter__value";
            counter.dataset.charCount = "true";
            meta.appendChild(counter);

            const renderCounter = function () {
                const currentLength = field.value.length;
                counter.textContent = currentLength + " / " + maxLength;
                counter.classList.toggle("is-near-limit", currentLength >= maxLength * 0.9 && currentLength < maxLength);
                counter.classList.toggle("is-at-limit", currentLength >= maxLength);
            };

            field.addEventListener("input", renderCounter);
            renderCounter();
        });
    };

    initMaxLengthCounters(document);

    // Gestiona el modal de recursos.
    if (uploadResourceToggle && uploadResourcePanel) {
        uploadResourceToggle.addEventListener("click", function () {
            uploadResourcePanel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = uploadResourcePanel.querySelector("input, textarea, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    }

    const closeUploadResourceModal = function () {
        if (!uploadResourcePanel) {
            return;
        }

        uploadResourcePanel.hidden = true;
        document.body.classList.remove("modal-open");
        if (uploadResourceToggle) {
            uploadResourceToggle.focus({ preventScroll: true });
        }
    };

    uploadResourceClosers.forEach(function (closer) {
        closer.addEventListener("click", closeUploadResourceModal);
    });

    // Gestiona el editor de noticias.
    const closePostEditModal = function (panel, toggle) {
        if (!panel) {
            return;
        }

        panel.hidden = true;
        document.body.classList.remove("modal-open");
        if (toggle) {
            toggle.focus({ preventScroll: true });
        }
    };

    document.querySelectorAll("[data-post-edit-toggle]").forEach(function (toggle) {
        const panelId = toggle.getAttribute("aria-controls");
        const panel = panelId ? document.getElementById(panelId) : null;

        toggle.addEventListener("click", function () {
            if (!panel) {
                return;
            }

            panel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = panel.querySelector("input, textarea, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    });

    document.querySelectorAll("[data-post-edit-close]").forEach(function (closer) {
        closer.addEventListener("click", function () {
            const panel = closer.closest("[data-post-edit-panel]");
            const toggle = panel && panel.id
                ? document.querySelector("[data-post-edit-toggle][aria-controls='" + panel.id + "']")
                : null;
            closePostEditModal(panel, toggle);
        });
    });

    // Gestiona el editor de eventos.
    const closeEventEditModal = function (panel, toggle) {
        if (!panel) {
            return;
        }

        panel.hidden = true;
        document.body.classList.remove("modal-open");
        if (toggle) {
            toggle.focus({ preventScroll: true });
        }
    };

    document.querySelectorAll("[data-event-edit-toggle]").forEach(function (toggle) {
        toggle.addEventListener("click", function () {
            const panel = toggle.getAttribute("aria-controls")
                ? document.getElementById(toggle.getAttribute("aria-controls"))
                : null;
            if (!panel) {
                return;
            }

            panel.hidden = false;
            document.body.classList.add("modal-open");
            const firstInput = panel.querySelector("input, textarea, select, button");
            window.requestAnimationFrame(function () {
                if (firstInput) {
                    firstInput.focus({ preventScroll: true });
                }
            });
        });
    });

    document.querySelectorAll("[data-event-edit-close]").forEach(function (closer) {
        closer.addEventListener("click", function () {
            const panel = closer.closest("[data-event-edit-panel]");
            const toggle = panel && panel.id
                ? document.querySelector("[data-event-edit-toggle][aria-controls='" + panel.id + "']")
                : null;
            closeEventEditModal(panel, toggle);
        });
    });

    // Inicializa las paginaciones.
    if (resourceGallery) {
        setupPagination(resourceGallery, {
            itemsPerPage: 4,
            cardSelector: "[data-resource-card]",
            paginationSelector: "[data-resource-pagination]",
            prevSelector: "[data-resource-prev]",
            nextSelector: "[data-resource-next]",
            pageSelector: "[data-resource-page]",
            hideWhenSinglePage: false,
        });
    }

    if (newsGallery) {
        setupPagination(newsGallery, {
            itemsPerPage: 1,
            cardSelector: "[data-news-card]",
            linkedSelector: "[data-news-management-card]",
            paginationSelector: "[data-news-pagination]",
            prevSelector: "[data-news-prev]",
            nextSelector: "[data-news-next]",
            pageSelector: "[data-news-page]",
            hideWhenSinglePage: false,
        });
    }

    if (eventGallery) {
        const activeFilterToggle = document.querySelector("[data-event-active-filter-toggle]");
        let showOnlyActiveEvents = false;

        const eventPagination = setupPagination(eventGallery, {
            itemsPerPage: 2,
            cardSelector: "[data-event-card]",
            paginationSelector: "[data-event-pagination]",
            prevSelector: "[data-event-prev]",
            nextSelector: "[data-event-next]",
            pageSelector: "[data-event-page]",
            hideWhenSinglePage: false,
            filterPredicate: function (card) {
                if (!showOnlyActiveEvents) {
                    return true;
                }

                return card.dataset.eventActiveStatus === "true";
            },
            onRender: function () {
                syncEventMemberPanelHeights();
            },
        });

        if (activeFilterToggle) {
            activeFilterToggle.addEventListener("click", function () {
                showOnlyActiveEvents = !showOnlyActiveEvents;
                activeFilterToggle.classList.toggle("is-active", showOnlyActiveEvents);
                activeFilterToggle.setAttribute("aria-pressed", showOnlyActiveEvents ? "true" : "false");
                eventPagination.reset();
            });
        }
    }

    if (pollGallery) {
        setupPagination(pollGallery, {
            itemsPerPage: 1,
            cardSelector: "[data-poll-card]",
            paginationSelector: "[data-poll-pagination]",
            prevSelector: "[data-poll-prev]",
            nextSelector: "[data-poll-next]",
            pageSelector: "[data-poll-page]",
            hideWhenSinglePage: false,
        });
    }

    // Sincroniza alturas y cuentas atrás.
    window.requestAnimationFrame(syncNewsHeightToResources);
    window.requestAnimationFrame(syncEventMemberPanelHeights);
    updatePollCountdowns();
    updateEventCountdowns();
    window.addEventListener("resize", syncNewsHeightToResources);
    window.addEventListener("resize", syncEventMemberPanelHeights);
    window.setInterval(updatePollCountdowns, 1000);
    window.setInterval(updateEventCountdowns, 1000);

    // Utilidades para mensajes flotantes.
    const ensureMessagesContainer = function () {
        let container = document.querySelector(".messages");
        if (!container) {
            container = document.createElement("div");
            container.className = "messages";
            container.setAttribute("aria-live", "polite");
            document.body.appendChild(container);
        }
        return container;
    };

    const showToast = function (message, type) {
        const toast = document.createElement("div");
        toast.className = "message " + (type || "error");

        const text = document.createElement("span");
        text.textContent = message;

        const close = document.createElement("button");
        close.type = "button";
        close.className = "message__close";
        close.setAttribute("aria-label", "Cerrar mensaje");
        close.textContent = "×";
        close.addEventListener("click", function () {
            toast.remove();
        });

        toast.append(text, close);
        ensureMessagesContainer().appendChild(toast);
    };

    // Sincroniza el editor rico antes de enviar.
    const syncRichEditor = function (editor) {
        const textarea = editor.previousElementSibling;
        const surface = editor.querySelector("[data-rich-editor-surface]");
        if (textarea && surface) {
            textarea.value = surface.innerHTML.trim();
        }
    };

    const countEditorWords = function (surface) {
        const text = surface.textContent.trim();
        return text ? text.split(/\s+/).length : 0;
    };

    // Ejecuta comandos del editor enriquecido.
    const execRichCommand = function (surface, editor, command, value) {
        surface.focus();
        document.execCommand(command, false, value || null);
        syncRichEditor(editor);
    };

    // Construye el editor enriquecido.
    const initRichEditor = function (textarea) {
        if (textarea.dataset.richEditorReady === "true") {
            return;
        }
        textarea.dataset.richEditorReady = "true";
        textarea.classList.add("rich-text-source");

        const editor = document.createElement("div");
        editor.className = "rich-text-editor";

        const toolbar = document.createElement("div");
        toolbar.className = "rich-text-editor__toolbar";
        toolbar.innerHTML = [
            "<label class='rich-text-editor__select'><span>Tipo</span><select data-rich-select='formatBlock'><option value='p'>Párrafo</option><option value='h2'>Encabezado</option><option value='h3'>Subtítulo</option></select></label>",
            "<label class='rich-text-editor__select'><span>Fuente</span><select data-rich-select='fontName'><option value='Arial'>Arial</option><option value='Georgia'>Georgia</option><option value='Verdana'>Verdana</option><option value='Trebuchet MS'>Trebuchet</option><option value='Courier New'>Courier</option></select></label>",
            "<label class='rich-text-editor__select'><span>Tamaño</span><select data-rich-select='fontSize'><option value='3'>Normal</option><option value='4'>Medio</option><option value='5'>Grande</option><option value='6'>Muy grande</option></select></label>",
            "<div class='rich-text-editor__buttons' data-rich-buttons></div>",
        ].join("");

        const buttonGroup = toolbar.querySelector("[data-rich-buttons]");

        const surface = document.createElement("div");
        surface.className = "rich-text-editor__surface";
        surface.contentEditable = "true";
        surface.dataset.richEditorSurface = "true";
        surface.dataset.placeholder = "Escribe aquí...";
        surface.innerHTML = textarea.value || "";

        const footer = document.createElement("div");
        footer.className = "rich-text-editor__footer";
        const wordCounter = document.createElement("span");
        wordCounter.className = "rich-text-editor__counter";
        footer.appendChild(wordCounter);

        const actions = [
            ["bold", "<strong>B</strong>", "Negrita"],
            ["italic", "<em>I</em>", "Cursiva"],
            ["underline", "<u>U</u>", "Subrayado"],
            ["insertUnorderedList", "• Lista", "Lista con puntos"],
            ["insertOrderedList", "1. Lista", "Lista numerada"],
            ["outdent", "←", "Reducir sangría"],
            ["indent", "→", "Aumentar sangría"],
            ["formatBlock", "<span>Cita</span>", "Cita", "blockquote"],
            ["formatBlock", "<span>Texto</span>", "Párrafo", "p"],
        ];
        actions.splice(
            3,
            6,
            ["strikeThrough", "<s>S</s>", "Tachado"],
            ["justifyLeft", "Izq", "Alinear izquierda"],
            ["justifyCenter", "Cen", "Alinear centro"],
            ["justifyRight", "Der", "Alinear derecha"],
            ["insertUnorderedList", "•", "Lista con viñetas"],
            ["insertOrderedList", "1.", "Lista numerada"],
        );

        // Refresca estado y contador del editor.
        const updateToolbarState = function () {
            toolbar.querySelectorAll("button[data-rich-command]").forEach(function (button) {
                const command = button.dataset.richCommand;
                if (["bold", "italic", "underline", "strikeThrough", "justifyLeft", "justifyCenter", "justifyRight"].includes(command)) {
                    button.classList.toggle("is-active", document.queryCommandState(command));
                }
            });
            wordCounter.textContent = countEditorWords(surface) + " palabra" + (countEditorWords(surface) === 1 ? "" : "s");
        };

        actions.forEach(function (action) {
            const button = document.createElement("button");
            button.type = "button";
            button.innerHTML = action[1];
            button.title = action[2];
            button.setAttribute("aria-label", action[2]);
            button.dataset.richCommand = action[0];
            button.addEventListener("click", function () {
                surface.focus();
                document.execCommand(action[0], false, action[3] || null);
                syncRichEditor(editor);
                updateToolbarState();
            });
            buttonGroup.appendChild(button);
        });

        toolbar.querySelector("[title='Lista con viñetas']").innerHTML = "<svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'><path d='M5 7a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm5-3h10v2H10V4ZM5 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm5-3h10v2H10v-2ZM5 21a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm5-3h10v2H10v-2Z'></path></svg>";
        toolbar.querySelector("[title='Lista numerada']").innerHTML = "<svg viewBox='0 0 24 24' aria-hidden='true' focusable='false'><path d='M4 5h2v1H3V4h1V3h2v1H4v1Zm-1 6h3v1H4v1h2v1H3v-3Zm0 6h3v4H3v-1h2v-.5H4v-1h1V18H3v-1Zm7-13h11v2H10V4Zm0 7h11v2H10v-2Zm0 7h11v2H10v-2Z'></path></svg>";

        toolbar.querySelectorAll("[data-rich-select]").forEach(function (select) {
            select.addEventListener("change", function () {
                surface.focus();
                document.execCommand(select.dataset.richSelect, false, select.value);
                syncRichEditor(editor);
                updateToolbarState();
            });
        });

        const linkButton = document.createElement("button");
        linkButton.type = "button";
        linkButton.textContent = "Link";
        linkButton.title = "Insertar enlace";
        linkButton.addEventListener("click", function () {
            const url = window.prompt("URL del enlace");
            if (url) {
                surface.focus();
                document.execCommand("createLink", false, url);
                syncRichEditor(editor);
            }
        });
        buttonGroup.appendChild(linkButton);

        const imageButton = document.createElement("button");
        imageButton.type = "button";
        imageButton.textContent = "Img";
        imageButton.title = "Insertar imagen";
        imageButton.addEventListener("click", function () {
            const url = window.prompt("URL de la imagen");
            if (url) {
                surface.focus();
                document.execCommand("insertImage", false, url);
                syncRichEditor(editor);
            }
        });
        buttonGroup.appendChild(imageButton);

        surface.addEventListener("input", function () {
            syncRichEditor(editor);
            updateToolbarState();
        });

        surface.addEventListener("blur", function () {
            syncRichEditor(editor);
        });

        surface.addEventListener("keyup", updateToolbarState);
        surface.addEventListener("mouseup", updateToolbarState);

        editor.append(toolbar, surface, footer);
        textarea.insertAdjacentElement("afterend", editor);
        updateToolbarState();
    };

    // Inicializa todos los editores enriquecidos.
    document.querySelectorAll("[data-rich-editor]").forEach(initRichEditor);

    // Copia el contenido enriquecido al enviar.
    document.addEventListener("submit", function (event) {
        event.target.querySelectorAll(".rich-text-editor").forEach(syncRichEditor);
    });

    // Utilidades de fecha y hora.
    const padDatePart = function (value) {
        return String(value).padStart(2, "0");
    };

    const formatDateTimeValue = function (date, time) {
        return date.getFullYear() + "-" + padDatePart(date.getMonth() + 1) + "-" + padDatePart(date.getDate()) + "T" + time;
    };

    const formatDateTimeLabel = function (date, time) {
        return padDatePart(date.getDate()) + "/" + padDatePart(date.getMonth() + 1) + "/" + date.getFullYear() + " a las " + time;
    };

    const parseDateTimeValue = function (value) {
        if (!value) {
            return null;
        }

        const parts = value.split("T");
        if (parts.length !== 2) {
            return null;
        }

        const dateParts = parts[0].split("-").map(Number);
        if (dateParts.length !== 3 || dateParts.some(Number.isNaN)) {
            return null;
        }

        return {
            date: new Date(dateParts[0], dateParts[1] - 1, dateParts[2]),
            time: parts[1].slice(0, 5),
        };
    };

    const buildTimeOptions = function (select) {
        for (let hour = 8; hour <= 22; hour += 1) {
            ["00", "30"].forEach(function (minutes) {
                const value = padDatePart(hour) + ":" + minutes;
                const option = document.createElement("option");
                option.value = value;
                option.textContent = value;
                select.appendChild(option);
            });
        }
    };

    const getScrollContainer = function (element) {
        let current = element.parentElement;
        while (current) {
            const styles = window.getComputedStyle(current);
            const overflowY = styles.overflowY;
            if ((overflowY === "auto" || overflowY === "scroll") && current.scrollHeight > current.clientHeight) {
                return current;
            }
            current = current.parentElement;
        }
        return document.scrollingElement || document.documentElement;
    };

    // Selector personalizado de fecha y hora.
    const initDateTimePicker = function (input) {
        const parsed = parseDateTimeValue(input.value);
        const required = input.required;
        let selectedDate = parsed ? parsed.date : null;
        let selectedTime = parsed ? parsed.time : "09:00";
        const today = new Date();
        let viewYear = selectedDate ? selectedDate.getFullYear() : today.getFullYear();
        let viewMonth = selectedDate ? selectedDate.getMonth() : today.getMonth();

        input.required = false;
        input.dataset.required = required ? "true" : "false";

        const wrapper = document.createElement("div");
        wrapper.className = "datetime-picker";
        wrapper.dataset.datetimePicker = "true";

        const trigger = document.createElement("button");
        trigger.type = "button";
        trigger.className = "datetime-picker__trigger";

        const valueBox = document.createElement("span");
        valueBox.className = "datetime-picker__value";

        const label = document.createElement("span");
        label.className = "datetime-picker__label";
        label.textContent = input.closest("p")?.querySelector("label")?.textContent || "Fecha y hora";

        const text = document.createElement("span");
        text.className = "datetime-picker__text";

        const icon = document.createElement("span");
        icon.className = "datetime-picker__icon";
        icon.setAttribute("aria-hidden", "true");
        icon.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 2a1 1 0 0 1 1 1v1h8V3a1 1 0 1 1 2 0v1h1.5A2.5 2.5 0 0 1 22 6.5v12A2.5 2.5 0 0 1 19.5 21h-15A2.5 2.5 0 0 1 2 18.5v-12A2.5 2.5 0 0 1 4.5 4H6V3a1 1 0 0 1 1-1Zm12.5 8h-15v8.5a.5.5 0 0 0 .5.5h14a.5.5 0 0 0 .5-.5V10ZM5 6a.5.5 0 0 0-.5.5V8h15V6.5A.5.5 0 0 0 19 6H5Zm2 6h3v3H7v-3Zm5 0h3v3h-3v-3Z"></path></svg>';

        valueBox.append(label, text);
        trigger.append(valueBox, icon);

        const panel = document.createElement("div");
        panel.className = "datetime-picker__panel";
        panel.hidden = true;

        const head = document.createElement("div");
        head.className = "datetime-picker__head";
        const prev = document.createElement("button");
        prev.type = "button";
        prev.className = "datetime-picker__nav";
        prev.textContent = "<";
        const monthLabel = document.createElement("span");
        monthLabel.className = "datetime-picker__month";
        const next = document.createElement("button");
        next.type = "button";
        next.className = "datetime-picker__nav";
        next.textContent = ">";
        head.append(prev, monthLabel, next);

        const week = document.createElement("div");
        week.className = "datetime-picker__week";
        ["L", "M", "X", "J", "V", "S", "D"].forEach(function (day) {
            const dayLabel = document.createElement("span");
            dayLabel.textContent = day;
            week.appendChild(dayLabel);
        });

        const days = document.createElement("div");
        days.className = "datetime-picker__days";

        const timeBox = document.createElement("div");
        timeBox.className = "datetime-picker__time";
        const timeLabel = document.createElement("label");
        timeLabel.textContent = "Hora";
        const timeSelect = document.createElement("select");
        buildTimeOptions(timeSelect);
        timeSelect.value = selectedTime;
        timeBox.append(timeLabel, timeSelect);

        const actions = document.createElement("div");
        actions.className = "datetime-picker__actions";
        const clear = document.createElement("button");
        clear.type = "button";
        clear.className = "datetime-picker__clear";
        clear.textContent = "Limpiar";
        const done = document.createElement("button");
        done.type = "button";
        done.className = "btn-primary datetime-picker__done";
        done.textContent = "Aplicar";
        actions.append(clear, done);

        panel.append(head, week, days, timeBox, actions);
        wrapper.append(trigger, panel);
        input.insertAdjacentElement("afterend", wrapper);

        const updateText = function () {
            text.textContent = selectedDate ? formatDateTimeLabel(selectedDate, selectedTime) : "Selecciona fecha y hora";
        };

        const updateInput = function () {
            input.value = selectedDate ? formatDateTimeValue(selectedDate, selectedTime) : "";
            input.dispatchEvent(new Event("change", { bubbles: true }));
            updateText();
        };

        const ensurePanelVisible = function () {
            if (panel.hidden) {
                return;
            }

            const scrollContainer = getScrollContainer(wrapper);
            const isDocumentScroller = scrollContainer === document.scrollingElement || scrollContainer === document.documentElement;
            const viewportPadding = 20;
            const containerRect = isDocumentScroller
                ? { top: 0, bottom: window.innerHeight }
                : scrollContainer.getBoundingClientRect();
            const popupContainer = wrapper.closest(".club-create-news-modal__dialog, .club-event-card__edit-popup");

            wrapper.classList.remove("datetime-picker--above");
            let panelRect = panel.getBoundingClientRect();
            const spaceBelow = (containerRect.bottom - viewportPadding) - panelRect.top;
            const spaceAbove = panelRect.top - (containerRect.top + viewportPadding);

            if (!popupContainer && panelRect.bottom > containerRect.bottom - viewportPadding && spaceAbove > spaceBelow) {
                wrapper.classList.add("datetime-picker--above");
                panelRect = panel.getBoundingClientRect();
            }

            const overflowBottom = panelRect.bottom - (containerRect.bottom - viewportPadding);
            const overflowTop = (containerRect.top + viewportPadding) - panelRect.top;

            if (overflowBottom > 0) {
                if (isDocumentScroller) {
                    window.scrollBy({ top: overflowBottom, behavior: "smooth" });
                } else {
                    scrollContainer.scrollBy({ top: overflowBottom, behavior: "smooth" });
                }
            } else if (overflowTop > 0) {
                if (isDocumentScroller) {
                    window.scrollBy({ top: -overflowTop, behavior: "smooth" });
                } else {
                    scrollContainer.scrollBy({ top: -overflowTop, behavior: "smooth" });
                }
            }

            if (popupContainer) {
                window.requestAnimationFrame(function () {
                    const refreshedRect = panel.getBoundingClientRect();
                    const popupRect = popupContainer.getBoundingClientRect();
                    const popupOverflowBottom = refreshedRect.bottom - (popupRect.bottom - viewportPadding);
                    const popupOverflowTop = (popupRect.top + viewportPadding) - refreshedRect.top;

                    if (popupOverflowBottom > 0) {
                        popupContainer.scrollBy({ top: popupOverflowBottom, behavior: "smooth" });
                    } else if (popupOverflowTop > 0) {
                        popupContainer.scrollBy({ top: -popupOverflowTop, behavior: "smooth" });
                    }
                });
            }
        };

        const renderDays = function () {
            days.innerHTML = "";
            monthLabel.textContent = new Intl.DateTimeFormat("es-ES", { month: "long", year: "numeric" }).format(new Date(viewYear, viewMonth, 1));

            const firstDay = new Date(viewYear, viewMonth, 1);
            const offset = (firstDay.getDay() + 6) % 7;
            const totalDays = new Date(viewYear, viewMonth + 1, 0).getDate();

            for (let index = 0; index < offset; index += 1) {
                const placeholder = document.createElement("span");
                placeholder.className = "datetime-picker__day is-placeholder";
                days.appendChild(placeholder);
            }

            for (let day = 1; day <= totalDays; day += 1) {
                const button = document.createElement("button");
                button.type = "button";
                button.className = "datetime-picker__day";
                button.textContent = day;
                if (
                    selectedDate
                    && selectedDate.getFullYear() === viewYear
                    && selectedDate.getMonth() === viewMonth
                    && selectedDate.getDate() === day
                ) {
                    button.classList.add("is-selected");
                }
                button.addEventListener("click", function () {
                    selectedDate = new Date(viewYear, viewMonth, day);
                    updateInput();
                    renderDays();
                });
                days.appendChild(button);
            }
        };

        trigger.addEventListener("click", function () {
            panel.hidden = !panel.hidden;
            if (!panel.hidden) {
                window.requestAnimationFrame(function () {
                    ensurePanelVisible();
                    const selectedDay = panel.querySelector(".datetime-picker__day.is-selected");
                    (selectedDay || timeSelect).focus({ preventScroll: true });
                });
            }
        });

        prev.addEventListener("click", function () {
            viewMonth -= 1;
            if (viewMonth < 0) {
                viewMonth = 11;
                viewYear -= 1;
            }
            renderDays();
            ensurePanelVisible();
        });

        next.addEventListener("click", function () {
            viewMonth += 1;
            if (viewMonth > 11) {
                viewMonth = 0;
                viewYear += 1;
            }
            renderDays();
            ensurePanelVisible();
        });

        timeSelect.addEventListener("change", function () {
            selectedTime = timeSelect.value;
            if (!selectedDate) {
                selectedDate = new Date(viewYear, viewMonth, today.getDate());
            }
            updateInput();
            renderDays();
            ensurePanelVisible();
        });

        clear.addEventListener("click", function () {
            selectedDate = null;
            input.value = "";
            updateText();
            renderDays();
            ensurePanelVisible();
        });

        done.addEventListener("click", function () {
            if (!selectedDate) {
                selectedDate = new Date(viewYear, viewMonth, today.getDate());
                updateInput();
                renderDays();
            }
            panel.hidden = true;
            trigger.focus({ preventScroll: true });
        });

        document.addEventListener("click", function (event) {
            if (!wrapper.contains(event.target)) {
                panel.hidden = true;
            }
        });

        updateText();
        renderDays();
    };

    // Utilidades para comentarios y contadores.
    const updateCommentsCount = function (card, commentsTotal) {
        const commentsCount = card ? card.querySelector("[data-comments-count]") : null;
        if (commentsCount) {
            commentsCount.textContent = commentsTotal + " comentario" + (commentsTotal === 1 ? "" : "s");
        }
    };

    const buildCommentDeleteButton = function (deleteUrl, csrfToken) {
        const form = document.createElement("form");
        form.method = "post";
        form.action = deleteUrl;
        form.setAttribute("data-delete-comment-form", "");

        const csrf = document.createElement("input");
        csrf.type = "hidden";
        csrf.name = "csrfmiddlewaretoken";
        csrf.value = csrfToken;

        const button = document.createElement("button");
        button.type = "submit";
        button.className = "club-resource-card__delete club-comment-row__delete";
        button.setAttribute("aria-label", "Eliminar comentario");
        button.title = "Eliminar comentario";

        const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        icon.setAttribute("viewBox", "0 0 24 24");
        icon.setAttribute("aria-hidden", "true");
        icon.setAttribute("focusable", "false");

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("d", "M9 3h6l1 2h4v2H4V5h4l1-2Zm1 6h2v9h-2V9Zm4 0h2v9h-2V9ZM7 9h2l1 11h4l1-11h2l-1.2 13H8.2L7 9Z");

        icon.appendChild(path);
        button.appendChild(icon);
        form.append(csrf, button);
        return form;
    };

    // Construye filas y acciones de asistencia.
    const buildTrashButton = function (label) {
        const button = document.createElement("button");
        button.type = "submit";
        button.className = "club-resource-card__delete club-event-attendees__delete";
        button.setAttribute("aria-label", label);
        button.title = label;

        const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        icon.setAttribute("viewBox", "0 0 24 24");
        icon.setAttribute("aria-hidden", "true");
        icon.setAttribute("focusable", "false");

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("d", "M9 3h6l1 2h4v2H4V5h4l1-2Zm1 6h2v9h-2V9Zm4 0h2v9h-2V9ZM7 9h2l1 11h4l1-11h2l-1.2 13H8.2L7 9Z");

        icon.appendChild(path);
        button.appendChild(icon);
        return button;
    };

    const updateEventAttendeesCount = function (card, attendeesTotal) {
        const counter = card ? card.querySelector("[data-event-attendees-count]") : null;
        if (counter) {
            counter.textContent = attendeesTotal;
        }
    };

    const removeEmptyEventAttendeesMessage = function (list) {
        if (!list) {
            return;
        }

        Array.from(list.children).forEach(function (item) {
            if (!item.hasAttribute("data-event-attendance-row")) {
                item.remove();
            }
        });
    };

    const ensureEmptyEventAttendeesMessage = function (list) {
        if (!list) {
            return;
        }

        const hasAttendanceRows = list.querySelector("[data-event-attendance-row]");
        if (hasAttendanceRows) {
            return;
        }

        removeEmptyEventAttendeesMessage(list);
        const emptyItem = document.createElement("li");
        emptyItem.textContent = "Aún no hay participantes.";
        list.appendChild(emptyItem);
    };

    const buildEventAttendanceRow = function (data, csrfToken) {
        const row = document.createElement("li");
        row.setAttribute("data-event-attendance-row", "");
        row.dataset.attendanceId = String(data.attendance_id);

        const name = document.createElement("span");
        const companionsCount = Number(data.companions_count || 0);
        name.textContent = data.user_display_name + (companionsCount > 0 ? " (+" + companionsCount + ")" : "");
        row.appendChild(name);

        if (data.delete_url) {
            const form = document.createElement("form");
            form.method = "post";
            form.action = data.delete_url;
            form.setAttribute("data-event-leave-form", "");
            form.dataset.ownAttendance = "true";

            const csrf = document.createElement("input");
            csrf.type = "hidden";
            csrf.name = "csrfmiddlewaretoken";
            csrf.value = csrfToken;

            form.append(csrf, buildTrashButton("Eliminar asistencia de " + data.user_display_name));
            row.appendChild(form);
        }

        return row;
    };

    const buildJoinEventForm = function (actionUrl, csrfToken) {
        const form = document.createElement("form");
        form.method = "post";
        form.action = actionUrl;
        form.className = "club-event-card__action-form";
        form.setAttribute("data-event-join-form", "");

        const csrf = document.createElement("input");
        csrf.type = "hidden";
        csrf.name = "csrfmiddlewaretoken";
        csrf.value = csrfToken;

        const button = document.createElement("button");
        button.type = "submit";
        button.className = "club-chip-button club-event-card__action";
        button.textContent = "Apuntarse";

        form.append(csrf, button);
        return form;
    };

    const buildJoinedEventBadge = function (title, updateUrl, companionsCount) {
        const badge = document.createElement("button");
        badge.type = "button";
        badge.className = "club-event-card__joined club-event-card__action";
        badge.setAttribute("data-event-edit-attendance-open", "");
        badge.dataset.eventTitle = title || "este evento";
        badge.dataset.updateUrl = updateUrl || "";
        badge.dataset.companionsCount = String(Number(companionsCount || 0));
        badge.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 17.25V21h3.75L18.8 9.95l-3.75-3.75L4 17.25Zm16.7-10.2a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83Z"></path></svg><span>Modificar</span>';
        return badge;
    };

    const buildLeaveEventAction = function (deleteUrl, attendanceId, csrfToken) {
        const form = document.createElement("form");
        form.method = "post";
        form.action = deleteUrl;
        form.className = "club-event-card__leave-action-form";
        form.setAttribute("data-event-leave-form", "");
        form.dataset.ownAttendance = "true";
        form.dataset.attendanceId = String(attendanceId);

        const csrf = document.createElement("input");
        csrf.type = "hidden";
        csrf.name = "csrfmiddlewaretoken";
        csrf.value = csrfToken;

        const button = document.createElement("button");
        button.type = "submit";
        button.className = "club-event-card__leave-action";
        button.setAttribute("aria-label", "Desapuntarse del evento");
        button.title = "Desapuntarse";
        button.textContent = "\u00d7";

        form.append(csrf, button);
        return form;
    };

    // Gestiona likes en noticias.
    document.querySelectorAll("[data-like-form]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const button = form.querySelector("[data-like-button]");
            if (button) {
                button.disabled = true;
            }

            fetch(form.action.split("#")[0], {
                method: "POST",
                body: new FormData(form),
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("No se pudo actualizar el like.");
                    }
                    return response.json();
                })
                .then(function (data) {
                    if (button) {
                        button.textContent = (data.liked ? "Quitar like" : "Like") + " \u00b7 " + data.likes_total;
                    }
                })
                .catch(function (error) {
                    showToast(error.message, "error");
                })
                .finally(function () {
                    if (button) {
                        button.disabled = false;
                        button.focus({ preventScroll: true });
                    }
                });
        });
    });

    // Activa el selector de fecha y hora.
    document.querySelectorAll("[data-datetime-smart]").forEach(initDateTimePicker);

    // Valida formularios de eventos.
    document.querySelectorAll("[data-event-form]").forEach(function (form) {
        const capacityInput = form.querySelector("[name='capacity']");
        const startDateTimeInput = form.querySelector("[name='start_datetime']");
        const endDateTimeInput = form.querySelector("[name='end_datetime']");
        const requiredDateTimeInputs = Array.from(form.querySelectorAll("[data-datetime-smart][data-required='true']"));

        if (!capacityInput) {
            return;
        }

        capacityInput.addEventListener("input", function () {
            capacityInput.setCustomValidity("");
        });

        if (startDateTimeInput && endDateTimeInput) {
            [startDateTimeInput, endDateTimeInput].forEach(function (input) {
                input.addEventListener("input", function () {
                    endDateTimeInput.setCustomValidity("");
                });
            });
        }

        form.addEventListener("submit", function (event) {
            const missingDateTimeInput = requiredDateTimeInputs.find(function (input) {
                return !input.value;
            });
            if (missingDateTimeInput) {
                event.preventDefault();
                showToast("Completa la fecha y hora de inicio.", "error");
                missingDateTimeInput.nextElementSibling?.querySelector(".datetime-picker__trigger")?.focus({ preventScroll: true });
                return;
            }

            if (
                startDateTimeInput &&
                endDateTimeInput &&
                startDateTimeInput.value &&
                endDateTimeInput.value &&
                new Date(startDateTimeInput.value) > new Date(endDateTimeInput.value)
            ) {
                event.preventDefault();
                endDateTimeInput.setCustomValidity("La fecha de fin no puede ser anterior a la fecha de inicio.");
                endDateTimeInput.reportValidity();
                endDateTimeInput.nextElementSibling?.querySelector(".datetime-picker__trigger")?.focus({ preventScroll: true });
                showToast("La fecha de fin no puede ser anterior a la fecha de inicio.", "error");
                return;
            }

            if (Number(capacityInput.value) >= 1) {
                return;
            }

            event.preventDefault();
            capacityInput.setCustomValidity("El aforo debe ser al menos 1.");
            capacityInput.reportValidity();
            capacityInput.focus({ preventScroll: true });
        showToast("El aforo debe ser al menos 1.", "error");
        });
    });

    // Abre la inscripción inicial a eventos.
    document.addEventListener("submit", function (event) {
        const form = event.target.closest("[data-event-join-form]");
        if (!form) {
            return;
        }

        event.preventDefault();

        pendingJoinEventForm = form;
        const card = form.closest("[data-event-card]");
        const title = card ? card.querySelector(".club-event-card__title-text")?.textContent?.trim() : "";
        const csrfToken = form.querySelector("[name='csrfmiddlewaretoken']")?.value || "";
        openJoinEventModalForRequest({
            mode: "join",
            title: title || "este evento",
            actionUrl: form.action,
            csrfToken: csrfToken,
            card: card,
            list: card ? card.querySelector("[data-event-attendees-list]") : null,
            joinForm: form,
            triggerButton: form.querySelector("button[type='submit']"),
            companionsCount: 0,
        });
    });

    // Ajusta el número de acompañantes.
    const syncJoinEventCompanions = function (value) {
        if (!joinEventCompanionsInput) {
            return 0;
        }

        const normalizedValue = Math.max(0, Math.min(10, Number(value) || 0));
        joinEventCompanionsInput.value = String(normalizedValue);
        return normalizedValue;
    };

    if (joinEventCompanionsInput) {
        joinEventCompanionsInput.addEventListener("input", function () {
            syncJoinEventCompanions(joinEventCompanionsInput.value);
            clearJoinEventValidationState();
        });
    }

    if (joinEventMinus) {
        joinEventMinus.addEventListener("click", function () {
            syncJoinEventCompanions((Number(joinEventCompanionsInput?.value || 0) - 1));
            clearJoinEventValidationState();
        });
    }

    if (joinEventPlus) {
        joinEventPlus.addEventListener("click", function () {
            syncJoinEventCompanions((Number(joinEventCompanionsInput?.value || 0) + 1));
            clearJoinEventValidationState();
        });
    }

    // Abre la edición de acompañantes.
    document.addEventListener("click", function (event) {
        const trigger = event.target.closest("[data-event-edit-attendance-open]");
        if (!trigger) {
            return;
        }

        const card = trigger.closest("[data-event-card]");
        const leaveForm = card ? card.querySelector(".club-event-card__leave-action-form[data-event-leave-form][data-own-attendance='true']") : null;
        const csrfToken = leaveForm ? leaveForm.querySelector("[name='csrfmiddlewaretoken']")?.value || "" : "";
        openJoinEventModalForRequest({
            mode: "edit",
            title: trigger.dataset.eventTitle || "este evento",
            actionUrl: trigger.dataset.updateUrl || "",
            csrfToken: csrfToken,
            card: card,
            list: card ? card.querySelector("[data-event-attendees-list]") : null,
            joinedBadge: trigger,
            companionsCount: Number(trigger.dataset.companionsCount || 0),
        });
    });

    // Cierra modales de eventos.
    joinEventClosers.forEach(function (closer) {
        closer.addEventListener("click", function () {
            pendingJoinEventForm = null;
            pendingJoinEventRequest = null;
            clearJoinEventValidationState();
            closeModal(joinEventModal);
        });
    });

    leaveEventClosers.forEach(function (closer) {
        closer.addEventListener("click", function () {
            pendingLeaveEventRequest = null;
            closeModal(leaveEventModal);
        });
    });

    if (leaveEventConfirm) {
        leaveEventConfirm.addEventListener("click", function () {
            if (!pendingLeaveEventRequest || !pendingLeaveEventRequest.form) {
                closeModal(leaveEventModal);
                return;
            }
            const form = pendingLeaveEventRequest.form;
            pendingLeaveEventRequest = null;
            closeModal(leaveEventModal);
            performEventLeave(form);
        });
    }

    // Envía la inscripción o actualización del evento.
    if (joinEventConfirm) {
        joinEventConfirm.addEventListener("click", function () {
            const requestConfig = pendingJoinEventRequest;
            if (!requestConfig || !requestConfig.actionUrl) {
                closeModal(joinEventModal);
                return;
            }

            pendingJoinEventForm = null;

            const card = requestConfig.card;
            const list = requestConfig.list;
            const button = requestConfig.triggerButton || requestConfig.joinedBadge || joinEventConfirm;
            const csrfToken = requestConfig.csrfToken;

            if (button) {
                button.disabled = true;
            }

            fetch(requestConfig.actionUrl, {
                method: "POST",
                body: (function () {
                    const formData = new FormData();
                    if (csrfToken) {
                        formData.set("csrfmiddlewaretoken", csrfToken);
                    }
                    formData.set("companions_count", String(syncJoinEventCompanions(joinEventCompanionsInput?.value || 0)));
                    return formData;
                })(),
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        if (!response.ok || !data.ok) {
                            throw new Error(data.error || "No se te pudo apuntar al evento.");
                        }
                        return data;
                    });
                })
                .then(function (data) {
                    closeModal(joinEventModal);
                    pendingJoinEventRequest = null;
                    updateEventAttendeesCount(card, data.attendees_total);

                    if (list && data.user_display_name && data.attendance_id && requestConfig.mode === "join") {
                        removeEmptyEventAttendeesMessage(list);
                        list.prepend(buildEventAttendanceRow(data, csrfToken));
                    }

                    if (requestConfig.mode === "join") {
                        const joinedBadge = buildJoinedEventBadge(
                            requestConfig.title,
                            data.update_url,
                            data.companions_count
                        );
                        requestConfig.joinForm.replaceWith(joinedBadge);
                        if (data.delete_url && data.attendance_id) {
                            joinedBadge.insertAdjacentElement(
                                "afterend",
                                buildLeaveEventAction(data.delete_url, data.attendance_id, csrfToken)
                            );
                        }
                    } else if (requestConfig.joinedBadge) {
                        requestConfig.joinedBadge.dataset.companionsCount = String(Number(data.companions_count || 0));
                        const ownRow = list
                            ? list.querySelector("[data-event-leave-form][data-own-attendance='true']")?.closest("[data-event-attendance-row]")?.querySelector("span")
                            : null;
                        if (ownRow) {
                            ownRow.textContent = data.user_display_name + (Number(data.companions_count || 0) > 0 ? " (+" + data.companions_count + ")" : "");
                        }
                    }
                })
                .catch(function (error) {
                    pendingJoinEventRequest = requestConfig;
                    pendingJoinEventForm = requestConfig.joinForm || null;
                    if (error.message && error.message.includes("No quedan plazas disponibles")) {
                        if (joinEventCompanionsInput) {
                            joinEventCompanionsInput.classList.add("is-invalid");
                        }
                        if (joinEventConfirm) {
                            joinEventConfirm.classList.add("is-invalid");
                        }
                    }
                    showToast(error.message, "error");
                    if (button) {
                        button.focus({ preventScroll: true });
                    }
                })
                .finally(function () {
                    if (button) {
                        button.disabled = false;
                    }
                });
        });
    }

    // Confirma borrados de eventos y noticias.
    const openDeleteEventModal = function (form) {
        if (!deleteEventModal) {
            form.submit();
            return;
        }

        pendingDeleteEventForm = form;
        if (deleteEventName) {
            deleteEventName.textContent = form.dataset.eventTitle || "este evento";
        }
        deleteEventModal.hidden = false;
        document.body.classList.add("modal-open");
        window.requestAnimationFrame(function () {
            deleteEventModal.classList.add("is-visible");
        });
    };

    const closeDeleteEventModal = function () {
        if (!deleteEventModal) {
            return;
        }

        deleteEventModal.classList.remove("is-visible");
        document.body.classList.remove("modal-open");
        window.setTimeout(function () {
            deleteEventModal.hidden = true;
            pendingDeleteEventForm = null;
        }, 180);
    };

    document.addEventListener("submit", function (event) {
        const form = event.target.closest("[data-delete-event-form]");
        if (!form) {
            return;
        }

        event.preventDefault();
        openDeleteEventModal(form);
    });

    deleteEventClosers.forEach(function (closer) {
        closer.addEventListener("click", closeDeleteEventModal);
    });

    if (deleteEventConfirm) {
        deleteEventConfirm.addEventListener("click", function () {
            if (pendingDeleteEventForm) {
                pendingDeleteEventForm.submit();
            }
        });
    }

    const openDeletePostModal = function (form) {
        if (!deletePostModal) {
            form.submit();
            return;
        }

        pendingDeletePostForm = form;
        if (deletePostName) {
            deletePostName.textContent = form.dataset.postTitle || "esta noticia";
        }

        deletePostModal.hidden = false;
        document.body.classList.add("modal-open");
        window.requestAnimationFrame(function () {
            deletePostModal.classList.add("is-visible");
            if (deletePostConfirm) {
                deletePostConfirm.focus({ preventScroll: true });
            }
        });
    };

    const closeDeletePostModal = function () {
        if (!deletePostModal) {
            return;
        }

        deletePostModal.classList.remove("is-visible");
        document.body.classList.remove("modal-open");
        window.setTimeout(function () {
            deletePostModal.hidden = true;
            pendingDeletePostForm = null;
        }, 180);
    };

    document.addEventListener("submit", function (event) {
        const form = event.target.closest("[data-delete-post-form]");
        if (!form) {
            return;
        }

        event.preventDefault();
        openDeletePostModal(form);
    });

    deletePostClosers.forEach(function (closer) {
        closer.addEventListener("click", closeDeletePostModal);
    });

    if (deletePostConfirm) {
        deletePostConfirm.addEventListener("click", function () {
            if (pendingDeletePostForm) {
                pendingDeletePostForm.submit();
            }
        });
    }

    // Gestiona el modal de miembros.
    const closeRemoveMemberModal = function () {
        if (!removeMemberModal) {
            return;
        }

        removeMemberModal.classList.remove("is-visible");
        document.body.classList.remove("modal-open");
        window.setTimeout(function () {
            removeMemberModal.hidden = true;
            if (removeMemberForm) {
                removeMemberForm.removeAttribute("action");
                removeMemberForm.reset();
            }
            if (removeMemberOther) {
                removeMemberOther.hidden = true;
            }
            if (removeMemberOtherInput) {
                removeMemberOtherInput.required = false;
            }
        }, 180);
    };

    document.querySelectorAll("[data-remove-member-open]").forEach(function (button) {
        button.addEventListener("click", function () {
            if (!removeMemberModal || !removeMemberForm) {
                return;
            }

            removeMemberForm.action = button.dataset.removeMemberAction || "";
            if (removeMemberName) {
                removeMemberName.textContent = button.dataset.removeMemberName || "este miembro";
            }

            removeMemberModal.hidden = false;
            document.body.classList.add("modal-open");
            window.requestAnimationFrame(function () {
                removeMemberModal.classList.add("is-visible");
                if (removeMemberReason) {
                    removeMemberReason.focus({ preventScroll: true });
                }
            });
        });
    });

    removeMemberClosers.forEach(function (closer) {
        closer.addEventListener("click", closeRemoveMemberModal);
    });

    if (removeMemberReason) {
        removeMemberReason.addEventListener("change", function () {
            const needsOtherReason = removeMemberReason.value === "other";
            if (removeMemberOther) {
                removeMemberOther.hidden = !needsOtherReason;
            }
            if (removeMemberOtherInput) {
                removeMemberOtherInput.required = needsOtherReason;
                if (!needsOtherReason) {
                    removeMemberOtherInput.value = "";
                }
            }
        });
    }

    if (removeMemberForm) {
        removeMemberForm.addEventListener("submit", function (event) {
            if (!removeMemberReason || !removeMemberReason.value) {
                event.preventDefault();
                removeMemberReason.setCustomValidity("Selecciona una causa para eliminar al miembro.");
                removeMemberReason.reportValidity();
                showToast("Selecciona una causa para eliminar al miembro.", "error");
                return;
            }

            removeMemberReason.setCustomValidity("");
            if (
                removeMemberReason.value === "other" &&
                removeMemberOtherInput &&
                !removeMemberOtherInput.value.trim()
            ) {
                event.preventDefault();
                removeMemberOtherInput.setCustomValidity("Indica el motivo de la eliminación.");
                removeMemberOtherInput.reportValidity();
                showToast("Indica el motivo de la eliminación.", "error");
                return;
            }

            if (removeMemberOtherInput) {
                removeMemberOtherInput.setCustomValidity("");
            }
        });
    }

    // Da de baja asistentes por AJAX.
    const performEventLeave = function (form) {
        const row = form.closest("[data-event-attendance-row]");
        const card = form.closest("[data-event-card]");
        const button = form.querySelector("button[type='submit']");
        const isOwnAttendance = form.dataset.ownAttendance === "true";
        const attendanceId = form.dataset.attendanceId;
        const joinedBadge = card ? card.querySelector(".club-event-card__joined") : null;
        const csrfToken = form.querySelector("[name='csrfmiddlewaretoken']").value;
        const joinAction = card ? card.dataset.eventJoinUrl : "";

        if (button) {
            button.disabled = true;
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
                        throw new Error(data.error || "No se pudo eliminar la asistencia.");
                    }
                    return data;
                });
            })
            .then(function (data) {
                updateEventAttendeesCount(card, data.attendees_total);
                const rowToRemove = row || (
                    card && attendanceId
                        ? card.querySelector('[data-event-attendance-row][data-attendance-id="' + attendanceId + '"]')
                        : null
                );
                if (rowToRemove) {
                    rowToRemove.remove();
                }

                const attendeesList = card ? card.querySelector("[data-event-attendees-list]") : null;
                ensureEmptyEventAttendeesMessage(attendeesList);

                if (isOwnAttendance && joinedBadge && joinAction) {
                    const actionLeaveForm = card
                        ? card.querySelector(".club-event-card__actions-row [data-event-leave-form][data-own-attendance='true']")
                        : null;
                    joinedBadge.replaceWith(buildJoinEventForm(joinAction, csrfToken));
                    if (actionLeaveForm) {
                        actionLeaveForm.remove();
                    }
                }
            })
            .catch(function (error) {
                showToast(error.message, "error");
            })
            .finally(function () {
                if (button) {
                    button.disabled = false;
                }
            });
    };

    // Decide si la baja del evento pide confirmación.
    document.addEventListener("submit", function (event) {
        const form = event.target.closest("[data-event-leave-form]");
        if (!form) {
            return;
        }

        event.preventDefault();

        const isOwnAttendance = form.dataset.ownAttendance === "true";
        const leaveButton = form.querySelector(".club-event-card__leave-action");
        if (isOwnAttendance && leaveButton) {
            const card = form.closest("[data-event-card]");
            const title = card ? card.querySelector(".club-event-card__title-text")?.textContent?.trim() : "este evento";
            pendingLeaveEventRequest = { form: form };
            if (leaveEventName) {
                leaveEventName.textContent = title || "este evento";
            }
            openModal(leaveEventModal);
            return;
        }

        performEventLeave(form);
    });

    // Publica comentarios en noticias.
    document.querySelectorAll("[data-comment-form]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();

            const card = form.closest("[data-news-card]");
            const textarea = form.querySelector("textarea[name='body']");
            const button = form.querySelector("button[type='submit']");

            if (button) {
                button.disabled = true;
            }

            fetch(form.action.split("#")[0], {
                method: "POST",
                body: new FormData(form),
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        if (!response.ok || !data.ok) {
                            throw new Error(data.error || "No se pudo publicar el comentario.");
                        }
                        return data;
                    });
                })
                .then(function (data) {
                    const commentsList = card ? card.querySelector("[data-comments-list]") : null;

                    if (commentsList) {
                        const row = document.createElement("div");
                        row.className = "club-comment-row";
                        row.setAttribute("data-comment-row", "");

                        const comment = document.createElement("p");
                        const author = document.createElement("strong");
                        author.textContent = data.author + ":";
                        comment.append(author, " " + data.body);
                        row.appendChild(comment);

                        if (data.delete_url) {
                            const csrfToken = form.querySelector("[name='csrfmiddlewaretoken']").value;
                            row.appendChild(buildCommentDeleteButton(data.delete_url, csrfToken));
                        }

                        commentsList.appendChild(row);
                    }

                    updateCommentsCount(card, data.comments_total);

                    if (textarea) {
                        textarea.value = "";
                        textarea.focus({ preventScroll: true });
                    }

                    syncNewsHeightToResources();
                })
                .catch(function (error) {
                    showToast(error.message, "error");
                    if (textarea) {
                        textarea.focus({ preventScroll: true });
                    }
                })
                .finally(function () {
                    if (button) {
                        button.disabled = false;
                    }
                });
        });
    });

    // Elimina comentarios por AJAX.
    document.addEventListener("submit", function (event) {
        const form = event.target.closest("[data-delete-comment-form]");
        if (!form) {
            return;
        }

        event.preventDefault();

        const row = form.closest("[data-comment-row]");
        const card = form.closest("[data-news-card]");
        const button = form.querySelector("button[type='submit']");

        if (button) {
            button.disabled = true;
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
                        throw new Error(data.error || "No se pudo eliminar el comentario.");
                    }
                    return data;
                });
            })
            .then(function (data) {
                if (row) {
                    row.remove();
                }
                updateCommentsCount(card, data.comments_total);
                syncNewsHeightToResources();
            })
            .catch(function (error) {
                showToast(error.message, "error");
            })
            .finally(function () {
                if (button) {
                    button.disabled = false;
                }
            });
    });

    // Gestiona la baja voluntaria del club.
    if (!leaveModal || !leaveOpen) {
        return;
    }

    leaveOpen.addEventListener("click", function () {
        leaveModal.hidden = false;
        document.body.classList.add("modal-open");
        window.requestAnimationFrame(function () {
            leaveModal.classList.add("is-visible");
        });
    });

    leaveClosers.forEach(function (closer) {
        closer.addEventListener("click", function () {
            leaveModal.classList.remove("is-visible");
            document.body.classList.remove("modal-open");
            window.setTimeout(function () {
                leaveModal.hidden = true;
            }, 180);
        });
    });
});
