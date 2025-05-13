document.addEventListener('DOMContentLoaded', function () {
    const confirmButton = document.querySelector('.button-submit');
    const modelSelect = document.getElementById('model-select');
    const datasetSelect = document.getElementById('dataset-select');

    confirmButton.addEventListener('click', function (event) {
        event.preventDefault();

        const selectedModel = modelSelect.value;
        const selectedDataset = datasetSelect.value;

        if (!selectedModel || !selectedDataset) {
            alert('Пожалуйста, выберите модель и набор данных.');
            return;
        }

        fetch('/update-selection/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                model: selectedModel,
                dataset: selectedDataset,
            }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('selected-model').textContent = data.model;
            document.getElementById('selected-dataset').textContent = data.dataset;
            document.getElementById('accuracy').textContent = data.accuracy;
        })
        .catch(error => console.error('Ошибка:', error));
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});