document.addEventListener('DOMContentLoaded', function () {
    const datasetSelect = document.getElementById('dataset-select');
    const datasetLabel = document.getElementById('dataset-label');
    const datasetDescription = document.getElementById('dataset-description');
    const form = document.getElementById('dataset-form');

    datasetSelect.addEventListener('change', function () {
        const selectedDataset = datasetSelect.value;

        if (!selectedDataset) {
            datasetLabel.textContent = 'Не выбрано';
            datasetDescription.textContent = 'Описание набора';
            return;
        }

        fetch('/update-dataset/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                dataset: selectedDataset,
            }),
        })
        .then(response => response.json())
        .then(data => {
            datasetLabel.textContent = data.name;
            datasetDescription.textContent = data.description;
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