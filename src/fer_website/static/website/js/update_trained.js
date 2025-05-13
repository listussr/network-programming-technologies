document.addEventListener('DOMContentLoaded', function () {
    const confirmButton = document.querySelector('.button-submit');
    const confSelect = document.getElementById("conf-select")
    const modelSelect = document.getElementById('conf-select');

    confSelect.addEventListener('change', function () {
        event.preventDefault();

        const selectedConf = modelSelect.value;

        if (!selectedConf) {
            alert('Пожалуйста, выберите модель и набор данных.');
            return;
        }

        console.log(selectedConf);
        

        fetch('/update-trained/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                conf: selectedConf,
            }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('model-label').textContent = data.model;
            document.getElementById('dataset-label').textContent = data.dataset;
            document.getElementById('accuracy-label').textContent = data.accuracy;
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