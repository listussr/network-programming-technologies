document.addEventListener('DOMContentLoaded', function () {
    const modelSelect = document.getElementById('model-select');
    const modelLabel = document.getElementById('model-label');
    const modelDescription = document.getElementById('model-description');
    const form = document.getElementById('model-form');

    modelSelect.addEventListener('change', function () {
        const selectedModel = modelSelect.value;
        
        if (!selectedModel) {
            modelLabel.textContent = 'Не выбрано';
            modelDescription.textContent = 'Описание модели';
            return;
        }

        fetch('/update-model/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                model: selectedModel,
            }),
        })
        .then(response => response.json())
        .then(data => {
            
            modelLabel.textContent = data.name;
            modelDescription.textContent = data.description;
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