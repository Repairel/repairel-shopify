function hamburger_menu_toggle() {
    var hamburger_button = document.getElementById("hamburger")
    var hamburger_menu = document.getElementById("hamburger_menu")
    var body_wrapper = document.getElementById("body_wrapper")

    if(!hamburger_menu.classList.contains("custom_hamburger_menu_active")) {
        hamburger_menu.classList.toggle("custom_hamburger_menu_active")
        hamburger_menu.animate({opacity: [0, 1], transform: ["translateX(-100%)", "translateX(0%)"]}, {duration: 200, easing: "ease-out"})
    }
    else {
        hamburger_menu.animate({opacity: [1, 0], transform: ["translateX(0%)", "translateX(-100%)"]}, {duration: 200, easing: "ease-in"}).onfinish = function() {
            hamburger_menu.classList.toggle("custom_hamburger_menu_active")
        }
    }
 
    hamburger_button.classList.toggle("custom_hamburger_active")
    body_wrapper.classList.toggle("custom_body_wrapper_active")
}