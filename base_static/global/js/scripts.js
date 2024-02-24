function confirmDeletion() {
    const forms = document.querySelectorAll(".form-delete");

    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            
            const confirmed = confirm("Are you sure");

            if (confirmed) form.submit();
            
        })
    })
}
confirmDeletion()

function handleMenu() {
    
    function menuHandler() {
        buttonShowMenu.classList.toggle(buttonActiveClass);
        menuContainer.classList.toggle(menuHiddenClass);
        
        buttonShowMenuIcon.classList.toggle('fa-bars')
        buttonShowMenuIcon.classList.toggle('fa-xmark')
    }
    
    const menuContainer = document.querySelector(".menu-container");

    const buttonShowMenu = document.querySelector(".button-show-menu");
    const buttonShowMenuIcon = buttonShowMenu.firstElementChild

    const buttonActiveClass = "button-active";
    const menuHiddenClass = "menu-hidden";

    if (buttonShowMenu) {
        buttonShowMenu.removeEventListener("click", menuHandler);
        buttonShowMenu.addEventListener("click", menuHandler);
    }
}
handleMenu();

function handleLogout() {
    const authorsLogoutLinks = document.querySelectorAll(".authors-logout-link");
    const formLogout = document.querySelector(".form-logout");

    authorsLogoutLinks.forEach((link) => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            formLogout.submit();
        })
    })
}
handleLogout();