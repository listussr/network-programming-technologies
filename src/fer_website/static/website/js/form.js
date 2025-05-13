document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const imageUpload = document.getElementById('fileInput');

    function onChangeHandler(event) {
        event.preventDefault();
        console.log("Event");
        const formData = new FormData(form);
        fetch('/upload-image/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                return response.text();
              } else {
                throw new Error('Ошибка при отправке файла.');
              }
        })
        .then(html => {
            document.body.innerHTML = html;
        })
        .catch(error => console.error('Ошибка: ', error));
        
    }

    imageUpload.addEventListener('input', onChangeHandler, false);

    /*imageUpload.addEventListener('change', function(event) {
        event.preventDefault();
        console.log("Event");
        const formData = new FormData(form);
        fetch('/upload-image/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                return response.text();
              } else {
                throw new Error('Ошибка при отправке файла.');
              }
        })
        .then(html => {
            document.body.innerHTML = html;
            //window.location.reload();
            document.form.reset();
        })
        .catch(error => console.error('Ошибка: ', error));
    });*/

    // Функция для получения CSRF-токена из cookie
    function getCookie(name) {
        let cookie = {};
        document.cookie.split(';').forEach(function(el) {
            let [key,value] = el.split('=');
            cookie[key.trim()] = value;
        })
        return cookie[name];
    }
});