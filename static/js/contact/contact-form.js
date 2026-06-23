// Sincroniza el segundo desplegable según el tipo de consulta elegido.
document.addEventListener("DOMContentLoaded", function () {
    const queryTypeSelect = document.querySelector("[data-query-type-select]");
    const queryTopicSelect = document.querySelector("[data-query-topic-select]");
    const groupsScript = document.getElementById("contact-query-topic-groups");

    if (!queryTypeSelect || !queryTopicSelect || !groupsScript) {
        return;
    }

    let queryTopicGroups = {};
    try {
        queryTopicGroups = JSON.parse(groupsScript.textContent);
    } catch (_error) {
        queryTopicGroups = {};
    }

    const buildPlaceholderOption = function () {
        const option = document.createElement("option");
        option.value = "";
        option.textContent = "Selecciona una opción";
        return option;
    };

    const syncQueryTopicOptions = function () {
        const currentType = queryTypeSelect.value;
        const currentValue = queryTopicSelect.value;
        const options = queryTopicGroups[currentType] || [];

        queryTopicSelect.innerHTML = "";
        queryTopicSelect.appendChild(buildPlaceholderOption());

        options.forEach(function (optionData) {
            const option = document.createElement("option");
            option.value = optionData[0];
            option.textContent = optionData[1];
            queryTopicSelect.appendChild(option);
        });

        const hasCurrentValue = options.some(function (optionData) {
            return optionData[0] === currentValue;
        });
        queryTopicSelect.value = hasCurrentValue ? currentValue : "";
        queryTopicSelect.disabled = !options.length;
    };

    queryTypeSelect.addEventListener("change", syncQueryTopicOptions);
    syncQueryTopicOptions();
});
