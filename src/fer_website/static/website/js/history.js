document.addEventListener('DOMContentLoaded', function() {
    const listItems = document.querySelectorAll('.li-item-history a');

    listItems.forEach(item => {
        item.addEventListener('click', function(event) {
            event.preventDefault();

            const itemId = this.id;
            
            console.log('Нажат элемент с id:', itemId);
        });
    });
});