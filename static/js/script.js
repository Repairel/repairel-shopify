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

function compute_filter() {
    var filter = document.getElementById("filter")
    if(filter.children.length == 0) return

    var price_direction = 0;
    var price_choice = filter.querySelector(".filter_option_Price").querySelector(".filter_option_active")
    if(price_choice)
        price_direction = price_choice.innerHTML.startsWith("H")? -1 : 1

    //reorder and filter products
    var products = [...document.querySelectorAll(".shoe_wrapper")]

    if(price_direction != 0) {
        var sort_price = function(a, b) {
            return (a.dataset.price - b.dataset.price) * price_direction
        }
        products.sort(sort_price)
    }
    var count = 0
    products.forEach(function(element) {
        var get_option = function(class_name) {
            var active = filter.querySelector(class_name).querySelector(".filter_option_active")
            if(active)
                return active.innerHTML
            else return null
        }

        var pass = true
        //here additionally filter the other things
        var condition = get_option(".filter_option_Condition")
        if(condition)
            pass &&= element.dataset.condition == condition || condition == "All Conditions"
        var size = get_option(".filter_option_Size")
        if(size)
            pass &&= element.dataset.size == size || size == "All Sizes"
        var brand = get_option(".filter_option_Brand")
        if(brand)
            pass &&= element.dataset.brand == brand || brand == "All Brands"
        if(pass) {
            element.style.display = "block"
            element.parentElement.appendChild(element)
            count++
        }
        else {
            element.style.display = "none"
        }
    })

    var no_shoe_text = document.getElementById("no_shoe_text")
    if(count == 0) {
        no_shoe_text.style.display = "block"
    }
    else {
        no_shoe_text.style.display = "none"
    }
}

function toggle_filter(filter_button) {
    var filter_options = {
        Price: ["High to Low", "Low to High"],
        Condition: ["All Conditions", "New", "Refurbished"],
        Size: ["All Sizes", "Kids", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
        Brand: ["All Brands", "Will's Vegan Store", "Refurbished Doc Martens", "Birdsong"]
    }
    
    var filter = document.getElementById("filter")
    if(filter_button.classList.contains("underline_thick")) {
        //turn off
        filter.innerHTML = ""
        compute_filter()
    }
    else {
        //turn on
        var filter_inner = document.createElement("div")
        filter_inner.classList.add("custom_filter_inner")

        for(var key in filter_options) {
            var filter_option = document.createElement("div")
            var filter_name = document.createElement("h4")
            filter_name.innerHTML = key
            filter_option.classList.add("custom_filter_option")
            filter_option.classList = "filter_option_" + key
            filter_option.appendChild(filter_name)

            var filter_content = document.createElement("div")
            filter_content.classList.add("custom_filter_content")
            for(var i = 0; i < filter_options[key].length; i++) {
                var filter_option_item = document.createElement("span")
                filter_option_item.onclick = function() {
                    //turn off all options in the same parent
                    var parent = this.parentElement
                    for(var i = 0; i < parent.children.length; i++) {
                        parent.children[i].classList.remove("filter_option_active")
                    }
                    this.classList.toggle("filter_option_active")
                    compute_filter()
                }.bind(filter_option_item)
                filter_option_item.innerHTML = filter_options[key][i]
                filter_content.appendChild(filter_option_item)
            }
            filter_option.appendChild(filter_content)
            filter_inner.appendChild(filter_option)
        }

        var no_shoe_text = document.createElement("p")
        no_shoe_text.innerHTML = "We're sorry, there are no products that match these filters. Please try again using different filters."
        no_shoe_text.id = "no_shoe_text"
        no_shoe_text.classList = "custom_no_shoe_text"
        no_shoe_text.style.display = "none"
        filter_inner.appendChild(no_shoe_text)

        var filter_clear_all = document.createElement("button")
        filter_clear_all.onclick = function() {
            //turn off all options in filter
            filter_inner.querySelectorAll(".filter_option_active").forEach(function(element) {
                element.classList.remove("filter_option_active")
            })
            compute_filter()
        }
        filter_clear_all.classList.add("button_white")
        filter_clear_all.innerHTML = "Clear all"
        filter_inner.appendChild(filter_clear_all)

        filter.appendChild(filter_inner)
    }
    filter_button.classList.toggle("underline_thick")
}