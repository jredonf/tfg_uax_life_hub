// Mensajes globales del sitio.
document.addEventListener("DOMContentLoaded", function () {
    const MESSAGE_AUTO_DISMISS_MS = 10000;

    const scheduleMessageAutoDismiss = function (message) {
        if (!message || message.dataset.autoDismissScheduled === "true") {
            return;
        }

        message.dataset.autoDismissScheduled = "true";
        window.setTimeout(function () {
            if (message.isConnected) {
                message.remove();
            }
        }, MESSAGE_AUTO_DISMISS_MS);
    };

    document.addEventListener("click", function (event) {
        const closeButton = event.target.closest("[data-message-close]");
        if (!closeButton) {
            return;
        }

        const message = closeButton.closest(".message");
        if (message) {
            message.remove();
        }
    });

    document.querySelectorAll(".message").forEach(scheduleMessageAutoDismiss);

    const messageObserver = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            mutation.addedNodes.forEach(function (node) {
                if (!(node instanceof Element)) {
                    return;
                }

                if (node.matches(".message")) {
                    scheduleMessageAutoDismiss(node);
                }

                node.querySelectorAll?.(".message").forEach(scheduleMessageAutoDismiss);
            });
        });
    });

    messageObserver.observe(document.body, {
        childList: true,
        subtree: true,
    });
});
