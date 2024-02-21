function confirm_deletion() {
    const forms = document.querySelectorAll('.form-delete');

    forms.forEach((form) => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            
            const confirmed = confirm('Are you sure');

            if (confirmed) form.submit();
            
        })
    })
}
confirm_deletion()