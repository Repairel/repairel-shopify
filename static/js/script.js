function set_cookie(name, value, days) {
    var expires = ""
    if (days) {
        var date = new Date()
        date.setTime(date.getTime() + (days*24*60*60*1000))
        expires = "; expires=" + date.toUTCString()
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/"
}

function get_cookie(name) {
    var nameEQ = name + "="
    var ca = document.cookie.split(';')
    for(var i=  0; i < ca.length; i++) {
        var c = ca[i]
        while (c.charAt(0)==' ') c = c.substring(1,c.length)
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length)
    }
    return null
}

function hamburger_menu_toggle() {
    var hamburger_button = document.getElementById("hamburger")
    var hamburger_menu = document.getElementById("hamburger_menu")
    var body_wrapper = document.getElementById("body_wrapper")
    var header_top_bar = document.getElementById("header_top_text")

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
    header_top_bar.classList.toggle("custom_header_top_text_hidden")
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
            pass &&= element.dataset.condition.includes(condition) || condition == "All Conditions"

        var size = get_option(".filter_option_Size")
        if(size)
            pass &&= element.dataset.size.includes(size) || size == "All Sizes"

        var brand = get_option(".filter_option_Brand")
        if(brand)
            pass &&= element.dataset.brand == brand || brand == "All Gender"
        var gender = get_option(".filter_option_Gender")
        if(gender)
            pass &&= element.dataset.gender == gender || gender == "All Genders"
        var group = get_option(".filter_option_Group")
        if(group)
            pass &&= element.dataset.group == group || group == "All Groups"
        var product_type = get_option(".filter_option_Type")
        if(product_type)
            pass &&= element.dataset.product_type == product_type || product_type == "All Types"
        var color = get_option(".filter_option_Colour")
        if(color)
            pass &&= element.dataset.color.includes(color) || color == "All Colours"
        var material = get_option(".filter_option_Material")
        if(material)
            pass &&= element.dataset.material == material || material == "All Materials"
        var shoe_or_other = get_option(".filter_option_Material")
        if(shoe_or_other)
            pass &&= element.dataset.shoe_or_other == shoe_or_other || shoe_or_other == "Shoe or Other"

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
        Size: ["All Sizes", "3", "3.5", "4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "11", "12", "13", "14"],
        Brand: ["All Brands", "Birdsong", "Dr Martens", "Will's Vegan Shoes"],
        Gender: ["All Genders", "Men", "Women", "Unisex"],
        Group: ["All Groups", "Kids", "Adults"],
        Type: ["All Types", "Brogues", "Flat Boots", "Heeled Boots", "High Heels", "Oxford Shoes", "Sandals", "Slip-ons", "Trainers", "Walking Boots"],
        Colour: ["All Colours", "Black", "Blue", "Brown", "Green", "Grey", "Multicolour", "Natural", "Pink", "Purple", "Red", "White", "Yellow"],
        Material: ["All Materials", "Leather", "Suede", "Textile", "Synthetic", "Vegan (Synthetic)"],
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

//shoe_balls is the parent object - the parent of the attribute and balls.
function show_shoe_balls_description(shoe_balls) {

    var only_close = shoe_balls.classList.contains("custom_shoe_balls_black")

    var mobile_view_cutoff = 700

    //check if shoe_balls_description existss
    var shoe_balls_description = document.getElementById("shoe_balls_description")
    if(shoe_balls_description) {
        shoe_balls_description.remove()
    }

    if(!only_close) {
        shoe_balls_description = document.createElement("div")
        shoe_balls_description.id = "shoe_balls_description"
        shoe_balls_description.classList = "custom_shoe_balls_description"
    
        
        if(window.innerWidth < mobile_view_cutoff) {
            shoe_balls.parentElement.insertBefore(shoe_balls_description, shoe_balls.nextSibling)
        }
        else {
            shoe_balls.parentElement.parentElement.insertBefore(shoe_balls_description, shoe_balls.parentElement.nextSibling)
        }
        shoe_balls_description = document.getElementById("shoe_balls_description")
        //clear the description
        shoe_balls_description.innerHTML = ""
    
        //now create the necessary elements
        var header = document.createElement("div")
        
        var image = document.createElement("img")
        image.src = shoe_balls.dataset.image
    
        var title = document.createElement("h3")
        title.innerHTML = shoe_balls.dataset.title
    
        var description = document.createElement("p")
        description.innerHTML = shoe_balls.dataset.description
        
    
        header.appendChild(image)
        header.appendChild(title)
    
        shoe_balls_description.appendChild(header)
        shoe_balls_description.appendChild(description)
    }

    //finally make the selected shoe_balls black
    var all_shoe_balls = document.querySelectorAll(".custom_shoe_balls")
    all_shoe_balls.forEach(function(element) {
        element.classList.remove("custom_shoe_balls_black")
    })

    if(!only_close) {
        if(shoe_balls.dataset.description == "" || shoe_balls.dataset.description == "None") {
            shoe_balls_description.innerHTML = ""
        }
        else {
            shoe_balls.classList.add("custom_shoe_balls_black")
        }
    }
}

function shoe_get_variant() {
    var selected_options = document.querySelectorAll(".shoe_option_active")
    var variants = document.querySelectorAll(".shoe_variants")

    for(var i = 0; i < variants.length; i++) {
        var variant = variants[i]
        var match = true
        for(var j = 0; j < selected_options.length; j++) {
            var option = selected_options[j]
            if(variant.dataset["option" + option.dataset.position] != option.dataset.value) {
                match = false
                break
            }
        }
        if(match) {
            return variant
        }
    }
    return null
}

function shoe_options_get_variant_id() {
    var variant = shoe_get_variant()
    if(!variant) return null

    return variant.dataset.id
}

function shoe_option_click(element) {
    var parent = element.parentElement
    for(var i = 0; i < parent.children.length; i++) {
        parent.children[i].classList.remove("shoe_option_active")
    }
    element.classList.toggle("shoe_option_active")

    //change the price
    var shoe_price = document.getElementById("shoe_price")
    var variant = shoe_get_variant()
    if(variant) {
        shoe_price.innerHTML = variant.dataset.price
    }
}

function shoe_add_to_cart(csrf_token) {
    var variant = shoe_options_get_variant_id()
    if(variant != null) {
        fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({variant_id: variant})
        }).then(function(response) {
            if(response.status == 200) {
                //success
                //TODO
                console.log("successfully added to cart")
                location.reload()
            }
            else {
                //failure
                console.log("failed to add to cart")
            }
        })
    }
    else {
        alert("There was an error adding this product to the cart")
        console.log("there was an error adding this product to the cart")
    }
}

function open_popup_window(url) {
    window.open(url,'popUpWindow','height=500, width=400, left=100, top=100, resizable=yes, scrollbars=yes, toolbar=yes, menubar=no, location=no, directories=no, status=yes');
}

function request_shoe_info(id) {
    return new Promise((resolve, reject) => {
        var url = local_api_url.replace("$request_type$", "product").replace("$argument$", id)
        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrf
            }
        }).then(function(response) {
            if(response.status == 200) {
                response.json().then(function(data) {
                    resolve(data)
                })
            }
            else {
                console.log("failed to get shoe info")
                reject()
            }
        })
    })
}

function open_compare(first_checkbox, second_checkbox) {
    var first_id = first_checkbox.dataset.id
    var second_id = second_checkbox.dataset.id

    var compare_popup_wrapper = document.getElementById("compare_popup_wrapper")
    if(compare_popup_wrapper) compare_popup.remove()

    
    compare_popup_wrapper = document.createElement("div")
    closed = false
    var close_compare = function() {
        closed = true
        compare_popup_wrapper.animate({opacity: [1, 0]}, {duration: 300}).onfinish = function() {
            compare_popup_wrapper.remove()
        }
        document.documentElement.classList.remove("html_stop_scroll")
    }
    compare_popup_wrapper.id = "compare_popup_wrapper"
    compare_popup_wrapper.classList = "custom_compare_popup_wrapper"
    compare_popup_wrapper.onclick = function(event) {
        if(event.target == compare_popup_wrapper) {
            close_compare()
        }
    }

    var compare_popup_outer = document.createElement("div")
    compare_popup_outer.classList = "custom_compare_popup_outer"
    compare_popup_wrapper.appendChild(compare_popup_outer)

    var compare_popup = document.createElement("div")
    compare_popup.classList = "custom_compare_popup"
    compare_popup_outer.appendChild(compare_popup)

    var compare_close = document.createElement("div")
    compare_close.classList = "custom_compare_close"
    compare_close.innerHTML = "x"
    compare_close.onclick = function() {
        close_compare()
    }
    compare_popup_outer.appendChild(compare_close)

    var loading = document.createElement("div")
    var animation_delay = 100
    loading.id = "compare_popup_loading"
    loading.classList = "custom_compare_loading div_loading"
    for(var i = 0; i < 3; i++) {
        var ball = document.createElement("div")
        ball.style.animationDelay = i * animation_delay + "ms"
        loading.appendChild(ball)
    }

    compare_popup.appendChild(loading)
    
    document.body.appendChild(compare_popup_wrapper)
    compare_popup_wrapper.animate({opacity: [0, 1]}, {duration: 300})
    document.documentElement.classList.add("html_stop_scroll")

    var construct_compare = function(first_shoe_info, second_shoe_info) {
        //remove loading
        loading.remove()
        
        //put the shoes side by side
        var shoe_container = document.createElement("div")
        shoe_container.classList = "custom_compare_poup_shoe_container"

        for(var shoe_info of [first_shoe_info, second_shoe_info]) {
            var shoe_container_entry = document.createElement("div")
            shoe_container_entry.classList = "custom_compare_popup_shoe_container_entry"
            shoe_container.appendChild(shoe_container_entry)
            //first the image
            var shoe_image_link = document.createElement("a")
            shoe_image_link.href = `/${shoe_info.id}/`
            shoe_container_entry.appendChild(shoe_image_link)

            var shoe_image = document.createElement("div")
            shoe_image.classList = "custom_compare_popup_shoe_image"
            shoe_image.style.backgroundImage = `url(${shoe_info.thumbnail})`
            shoe_image_link.appendChild(shoe_image)

            var text_block = document.createElement("div")
            text_block.classList = "custom_compare_popup_shoe_text_block"
            shoe_container_entry.appendChild(text_block)

            var shoe_name = document.createElement("h3")
            shoe_name.innerHTML = shoe_info.name
            text_block.appendChild(shoe_name)

            var shoe_description = document.createElement("p")
            shoe_description.innerHTML = shoe_info.tags
            text_block.appendChild(shoe_description)

            var shoe_price = document.createElement("h4")
            shoe_price.innerHTML = "&#163;" + shoe_info.price
            text_block.appendChild(shoe_price)
        }
        compare_popup.appendChild(shoe_container)

        //now create the environmental factors
        //this is just copy paste from the backend
        var attributes = {
            "design": {"title": "Design", "image": "data:image/svg+xml;base64,PHN2ZyBpZD0iQ2FwYV8xIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCA1MTAuMTMxIDUxMC4xMzEiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA1MTAuMTMxIDUxMC4xMzEiIHdpZHRoPSI0MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Zz48cGF0aCBkPSJtNDYxLjkxNCA1MDkuODYzIDQ4LjIxNy00OC4yMDgtMjcuOTExLTM0LjI0NyAyNy45MTEtMzQuMjUtMjcuOTExLTM0LjI1MSAyNy45MTEtMzQuMjU1LTI3LjkxMS0zNC4yNTYgMjcuOTExLTM0LjI1NS0yNy45MTEtMzQuMjU3IDI3LjkxMS0zNC4yNjItNDguMjA4LTQ4LjIxNy0zNC4yNDcgMjcuOTExLTM0LjI1LTI3LjkxMS0zNC4yNTEgMjcuOTExLTM0LjI1NS0yNy45MTEtMzQuMjU2IDI3LjkxMS0zNC4yNTUtMjcuOTExLTM0LjI1NyAyNy45MTEtMzQuMjYyLTI3LjkxMS00OC4yMTcgNDguMjA4IDI3LjkxMSAzNC4yNDctMjcuOTExIDM0LjI1IDI3LjkxMSAzNC4yNTEtMjcuOTExIDM0LjI1NSAyNy45MTEgMzQuMjU2LTI3LjkxMSAzNC4yNTUgNC40NjggNS40ODQgMjMuNDQzIDI4Ljc3My0yNy43MTggMzYuNTc3IDQ4LjAxNSA0NS45MDIgMzQuMjQ3LTI3LjkxMSAzNC4yNSAyNy45MTEgMzQuMjUxLTI3LjkxMSAzNC4yNTUgMjcuOTExIDM0LjI1Ni0yNy45MTEgMzQuMjU1IDI3LjkxMSAzNC4yNTctMjcuOTExem0tMjEyLjAxMy04MC4yM2gtMzB2LTMwaDMwem0wLTYwaC0zMHYtMzBoMzB6bTAtNjBoLTMwdi0zMGgzMHptMC02MGgtMzB2LTMwaDMwem02MCAxODBoLTMwdi0zMGgzMHptMC02MGgtMzB2LTMwaDMwem0wLTYwaC0zMHYtMzBoMzB6bTAtNjBoLTMwdi0zMGgzMHptNjAgMTgwaC0zMHYtMzBoMzB6bTAtNjBoLTMwdi0zMGgzMHptMC02MGgtMzB2LTMwaDMwem0wLTYwaC0zMHYtMzBoMzB6bTMwLTMwaDMwdjMwaC0zMHptMCA2MGgzMHYzMGgtMzB6bTAgNjBoMzB2MzBoLTMwem0wIDYwaDMwdjMwaC0zMHoiLz48cGF0aCBkPSJtMTI4Ljg4NiAzNTguODcxLTI3LjkxMS0zNC4yNTUgMjcuOTEtMzQuMjU0LTI3LjkxMi0zNC4yNTMgMjcuOTEtMzQuMjQ5LTI5LjU4Ni0zNi4zMDIgODYuNTM5LTg2LjUyMiAzNi4zMTQgMjkuNTg0IDM0LjI1OS0yNy45MTMgMzQuMjU1IDI3LjkxMSAzNC4yNTYtMjcuOTExIDM0LjI1NCAyNy45MSAyNC43NzMtMjAuMTg3LTIzLjg1NC0yMS40NTggMjkuMzQtMzYuMDE3LTUwLjY3Ny01MC42ODctMzYuMDAxIDI5LjM0MS0zNi4wMDQtMjkuMzQxLTM2LjAwNiAyOS4zNDEtMzYuMDEtMjkuMzQxLTM2LjAxIDI5LjM0MS0zNi4wMS0yOS4zNDEtMzYuMDExIDI5LjM0MS0zNi4wMTctMjkuMzQxLTUwLjY4NyA1MC42NzggMjkuMzQxIDM2LTI5LjM0MSAzNi4wMDUgMjkuMzQxIDM2LjAwNS0yOS4zNDEgMzYuMDEgMjkuMzQxIDM2LjAxMS0yOS4zNDEgMzYuMDA5IDI5LjM0MSAzNi4wMTItMjkuMTM4IDM4LjQ1MSA1MC40NzQgNDguMjUzIDM2LjAwMS0yOS4zNDEgMjIuNjUzIDIyLjUxMXoiLz48L2c+PC9zdmc+"},
            "raw_materials": {"title": "Raw Materials", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/PjwhRE9DVFlQRSBzdmcgIFBVQkxJQyAnLS8vVzNDLy9EVEQgU1ZHIDEuMS8vRU4nICAnaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkJz48c3ZnICBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAuMTA3IC05LjU2NyAxNDEuNzMyIDE0MS43MzIiIHdpZHRoPSc0MCcgaGVpZ2h0PSc0MCcgaWQ9IkxpdmVsbG9fMSIgdmVyc2lvbj0iMS4xIiB2aWV3Qm94PSIwLjEwNyAtOS41NjcgMTQxLjczMiAxNDEuNzMyIiAgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+PGcgaWQ9IkxpdmVsbG9fNTQiPjxwYXRoIGQ9Ik0yOS4xMTYsMTE1LjM4M2gxMy40Mzh2LTExLjk5NkgyOS4xMTZWMTE1LjM4M3ogTTk5LjM5MywxMTUuMzgzaDEzLjQzOHYtMTEuOTk2SDk5LjM5M1YxMTUuMzgzeiBNMTMuNDM4LDQ4LjE5aDYuNzU2ICAgTDQuNDgxLDcwLjY5NWgxMy4xNjhMMCw5Ny40NjVoMjkuMTE1djIuMjEzTDQ2LjY0LDcxLjUzMUgzMS44NGwxNy42NjItMjYuNzc0aC03LjU5NGw2Ljg4NS0xMS42NjJMMzUuODM0LDEyLjM1NkwxMy40MzgsNDguMTl6ICAgIE05My4xNTIsMzMuMDkybDYuODg1LDExLjY2MmgtNy41OTRsMTcuNjYyLDI2Ljc3NEg5NS4zMDNsMTcuNTI0LDI4LjE0NnYtMi4yMTNoMjkuMTE3bC0xNy42NS0yNi43NzFoMTMuMTcxTDEyMS43NTIsNDguMTloNi43NTYgICBsLTIyLjM5Ni0zNS44MzRMOTMuMTUyLDMzLjA5MnogTTQ1Ljk1LDQyLjY0M2g3LjU5MkwzNS44NzksNjkuNDJoMTQuODA2bC0xOS44MzYsMzEuODU0aDMyLjcyNXYyMS4zMjNoMTUuMTA0di0yMS4zMjNoMzIuNzI3ICAgTDkxLjU2MSw2OS40MmgxNC44MDNMODguNzAxLDQyLjY0M2g3LjU5Mkw3MS4xMjIsMEw0NS45NSw0Mi42NDN6Ii8+PC9nPjxnIGlkPSJMaXZlbGxvXzFfMV8iLz48L3N2Zz4="},
            "material_manufacturing": {"title": "Material Manufacturing", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTkuMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBoZWlnaHQ9IjQwIiB3aWR0aD0iNDAiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiBzdHlsZT0iZW5hYmxlLWJhY2tncm91bmQ6bmV3IDAgMCA1MTIgNTEyOyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+CjxnPgoJPGc+CgkJPHBhdGggZD0iTTI0NS4zMzMsNDQ4SDEwLjY2N0M0Ljc3OSw0NDgsMCw0NTIuNzc5LDAsNDU4LjY2N3Y0Mi42NjdDMCw1MDcuMjIxLDQuNzc5LDUxMiwxMC42NjcsNTEyaDIzNC42NjcKCQkJYzUuODg4LDAsMTAuNjY3LTQuNzc5LDEwLjY2Ny0xMC42Njd2LTQyLjY2N0MyNTYsNDUyLjc3OSwyNTEuMjIxLDQ0OCwyNDUuMzMzLDQ0OHoiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxjaXJjbGUgY3g9IjQ4MCIgY3k9IjIwMi42NjciIHI9IjMyIi8+Cgk8L2c+CjwvZz4KPGc+Cgk8Zz4KCQk8cGF0aCBkPSJNMjI0LDM0MS4zMzNoLTMyVjMyMGMwLTM1LjI4NS0yOC43MTUtNjQtNjQtNjRzLTY0LDI4LjcxNS02NCw2NHYyMS4zMzNIMzJjLTUuODg4LDAtMTAuNjY3LDQuNzc5LTEwLjY2NywxMC42Njd2NzQuNjY3CgkJCWgyMTMuMzMzVjM1MkMyMzQuNjY3LDM0Ni4xMTIsMjI5Ljg4OCwzNDEuMzMzLDIyNCwzNDEuMzMzeiBNODUuMzMzLDM5NC42NjdjMCw1Ljg4OC00Ljc3OSwxMC42NjctMTAuNjY3LDEwLjY2NwoJCQlTNjQsNDAwLjU1NSw2NCwzOTQuNjY3di0yMS4zMzNjMC01Ljg4OCw0Ljc3OS0xMC42NjcsMTAuNjY3LTEwLjY2N3MxMC42NjcsNC43NzksMTAuNjY3LDEwLjY2N1YzOTQuNjY3eiBNMTI4LDM5NC42NjcKCQkJYzAsNS44ODgtNC43NzksMTAuNjY3LTEwLjY2NywxMC42NjdzLTEwLjY2Ny00Ljc3OS0xMC42NjctMTAuNjY3di0yMS4zMzNjMC01Ljg4OCw0Ljc3OS0xMC42NjcsMTAuNjY3LTEwLjY2NwoJCQlTMTI4LDM2Ny40NDUsMTI4LDM3My4zMzNWMzk0LjY2N3oiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxwYXRoIGQ9Ik00NzYuODg1LDMxMi40NjlsLTE5LjI2NC0xOS4yNjRjMC40NDgtMS43MDcsMS4wNDUtMy4zNDksMS4wNDUtNS4yMDVjMC0xLjg5OS0wLjYxOS0zLjU4NC0xLjA4OC01LjMzM2wyMS4xNjMtMjYuNzk1CgkJCWMtMTYuNDkxLTAuMzg0LTMwLjk5Ny04LjM0MS00MC41MTItMjAuNDU5bC05LjQ3MiwzMy4xMzFjLTQuMDc1LDEuODEzLTcuMjExLDQuOTkyLTkuNDcyLDguNzg5aC0yNC42MTkKCQkJYy01Ljg4OCwwLTEwLjY2Nyw0Ljc3OS0xMC42NjcsMTAuNjY3djQyLjY2N2MwLDUuODg4LDQuNzc5LDEwLjY2NywxMC42NjcsMTAuNjY3czEwLjY2Ny00Ljc3OSwxMC42NjctMTAuNjY3di0zMmgxMy45NTIKCQkJYzMuNzMzLDYuMjUxLDEwLjI2MSwxMC42NjcsMTguMDQ4LDEwLjY2N2MxLjgzNSwwLDMuNDk5LTAuNjE5LDUuMjA1LTEuMDQ1TDQ1NC4yNTEsMzIwbC0yNC40NDgsMjQuNDQ4CgkJCWMtNC4xNiw0LjE2LTQuMTYsMTAuOTIzLDAsMTUuMDgzYzIuMDY5LDIuMDkxLDQuOCwzLjEzNiw3LjUzMSwzLjEzNmMyLjczMSwwLDUuNDYxLTEuMDQ1LDcuNTUyLTMuMTE1bDMyLTMyCgkJCUM0ODEuMDQ1LDMyMy4zOTIsNDgxLjA0NSwzMTYuNjI5LDQ3Ni44ODUsMzEyLjQ2OXoiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxwYXRoIGQ9Ik0yNjYuNjY3LDEyOGMtMjcuODQsMC01MS45MDQtMTUuNTA5LTY0LjcyNS0zOC4xNjVsLTkzLjA1NiwxNDcuMTc5YzYuMTY1LTEuNDI5LDEyLjUyMy0yLjM0NywxOS4xMTUtMi4zNDcKCQkJYzMzLjk4NCwwLDYzLjE0NywyMC4wOTYsNzYuODY0LDQ4LjkxN2w3MC4zNzktMTU2LjQ1OUMyNzIuMzg0LDEyNy40NjcsMjY5LjYxMSwxMjgsMjY2LjY2NywxMjh6Ii8+Cgk8L2c+CjwvZz4KPGc+Cgk8Zz4KCQk8Y2lyY2xlIGN4PSIyNjYuNjY3IiBjeT0iNTMuMzMzIiByPSI1My4zMzMiLz4KCTwvZz4KPC9nPgo8Zz4KCTxnPgoJCTxwYXRoIGQ9Ik0zNDAuMjI0LDY0LjM2M2MtMy40NTYsMjMuMDgzLTE3LjQwOCw0Mi41MzktMzYuOTQ5LDUzLjYzMmwxMjQuMDk2LDc3LjY1M2MyLjMwNC0xNy4xOTUsMTIuNzM2LTMxLjcyMywyNy40MTMtMzkuNjgKCQkJTDM0MC4yMjQsNjQuMzYzeiIvPgoJPC9nPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+CjxnPgo8L2c+Cjwvc3ZnPgo="},
            "footwear_manufacturing": {"title": "Footwear Manufacturing", "image": "data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNTEyIDUxMiIgaGVpZ2h0PSI0MCIgd2lkdGg9IjQwIiB2aWV3Qm94PSIwIDAgNTEyIDUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Zz48Zz48Zz48cGF0aCBkPSJtNTA1Ljg1NCAxNTAuMzM2Yy0zLjY5MS0xLjc0OS04LjE0OS0xLjE3My0xMS4zNDkgMS40NTFsLTExMC41MDcgOTIuMDk2di04My44ODNjMC00LjEzOS0yLjM4OS03LjkxNS02LjE0NC05LjY2NC0zLjcxMi0xLjc0OS04LjE0OS0xLjE3My0xMS4zNDkgMS40NTFsLTExMC41MDcgOTIuMDk2di04My44ODNjMC00LjIyNC0yLjQ5Ni04LjA2NC02LjM3OS05Ljc3MS0zLjg0LTEuNzQ5LTguMzg0LS45Ni0xMS40OTkgMS44OTlsLTY2Ljg1OSA2MS4yOTFjLTIuNDMyIDIuMjQtMy43MTIgNS40ODMtMy40MTMgOC43ODlsMjQuMDIxIDI3Ni4yNjcgMTAuNTgxLS4zNjMtMTAuNjY3IDMuMjIxYzAgNS44ODggNC43NzkgMTAuNjY3IDEwLjY2NyAxMC42NjdoMjk4Ljg4YzUuODg4IDAgMTAuNjY3LTQuNzc5IDEwLjY2Ny0xMC42Njd2LTM0MS4zMzNjLjAwMS00LjEzOS0yLjM4OC03LjkxNS02LjE0My05LjY2NHptLTE4NS44NTYgMjQ0LjMzMWMwIDUuODg4LTQuNzc5IDEwLjY2Ny0xMC42NjcgMTAuNjY3aC02NGMtNS44ODggMC0xMC42NjctNC43NzktMTAuNjY3LTEwLjY2N3YtNjRjMC01Ljg4OCA0Ljc3OS0xMC42NjcgMTAuNjY3LTEwLjY2N2g2NGM1Ljg4OCAwIDEwLjY2NyA0Ljc3OSAxMC42NjcgMTAuNjY3em0xMjggMGMwIDUuODg4LTQuNzc5IDEwLjY2Ny0xMC42NjcgMTAuNjY3aC02NGMtNS44ODggMC0xMC42NjctNC43NzktMTAuNjY3LTEwLjY2N3YtNjRjMC01Ljg4OCA0Ljc3OS0xMC42NjcgMTAuNjY3LTEwLjY2N2g2NGM1Ljg4OCAwIDEwLjY2NyA0Ljc3OSAxMC42NjcgMTAuNjY3eiIvPjxwYXRoIGQ9Im0xMjcuOTU2IDkuNzQ5Yy0uNDctNS41MjUtNS4wOTktOS43NDktMTAuNjI0LTkuNzQ5aC02NGMtNS41MjUgMC0xMC4xNTUgNC4yMjQtMTAuNjI0IDkuNzQ5bC00Mi42NjcgNDkwLjY2N2MtLjI1NiAyLjk4Ny43NDcgNS45MzEgMi43NTIgOC4xMjhzNC44ODUgMy40NTYgNy44NzIgMy40NTZoMTQ5LjMzM2MuMTI4IDAgLjI3Ny0uMDIxLjQyNyAwIDUuODg4IDAgMTAuNjY3LTQuNzc5IDEwLjY2Ny0xMC42NjcgMC0xLjM2NS0uMjU2LTIuNjY3LS43MjUtMy44NjF6Ii8+PC9nPjwvZz48L2c+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PGcvPjxnLz48Zy8+PC9zdmc+"},
            "retail": {"title": "Retail", "image": "data:image/svg+xml;base64,PHN2ZyBpZD0iQ2FwYV8xIiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCA0OTkgNDk5IiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgNDk5IDQ5OSIgd2lkdGg9IjQwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxnPjxwYXRoIGQ9Im0xOTIuNSA4N2MzLjEzOS03NS42MzMgMTEwLjg4NS03NS41ODMgMTE0IDB2MjdoMzB2LTI3YzAtNDcuOTctMzkuMDMtODctODctODdzLTg3IDM5LjAzLTg3IDg3djI3aDMweiIvPjxwYXRoIGQ9Im0yMTEuMzMgMzU5LjUyIDUwLjgxIDE4LjQ4aDc0LjM2di0zMC4xYy0yMS4zNC0zLjA3LTQ0LjU3LTEyLjUzLTY5LjI5LTI4LjI0LTE1LjI5LTkuNzEtMjcuMjQtMTkuNC0zMy4zOC0yNC42NmgtNzEuMzN2ODNoMzEuNXoiLz48cGF0aCBkPSJtMzM2LjUgMTE0djY5aC0zMGMwLTE4LjUyNSAwLTUwLjgwNyAwLTY5aC0xMTR2NjloLTMwYzAtMTguNTI1IDAtNTAuODA3IDAtNjloLTE2MXYzODVoNDk2di0zODV6bS05MS4xIDE1MWM0LjExNiAzLjQ0IDU0LjM5NiA1Mi42MiAxMDYuMSA1NC4wMDEgMC0uMDAxIDE1LS4wMDEgMTUtLjAwMXY4OWgtMTA5LjY0bC0zNy4xOS0xMy41Mi0xMi42NyAxMy41MmgtNzQuNXYtMTQzeiIvPjwvZz48L3N2Zz4="},
            "use": {"title": "Use", "image": "data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIC0xNiA1MTIgNTEyIiB3aWR0aD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0ibTkxIDQ1MC4wNTA3ODFoMTUwdjMwaC0xNTB6bTAgMCIvPjxwYXRoIGQ9Im0wIDM5MC4wNTA3ODFoMTUxdjMwaC0xNTF6bTAgMCIvPjxwYXRoIGQ9Im05Ny43NjU2MjUgMTMyLjY2NDA2MmMtNC45Njg3NS03LjQ5MjE4Ny0xMC44MzIwMzEtMTQuMTcxODc0LTE3LjQ0OTIxOS0yMC4wNDI5NjhsLTI5Ljc4OTA2MiA0MC44MTY0MDYgNjMuMTI4OTA2IDUwLjQ5MjE4OGMzLjQ1MzEyNS0yNC42ODM1OTQtMS44Nzg5MDYtNTAuMTQ4NDM4LTE1Ljg5MDYyNS03MS4yNjU2MjZ6bTAgMCIvPjxwYXRoIGQ9Im0xMjIuNzY5NTMxIDExNi4wODIwMzFjMjEuMjk2ODc1IDMyLjEwNTQ2OSAyNy4zMTI1IDcyLjAzNTE1NyAxNy4xNjc5NjkgMTA4Ljg3MTA5NGwyMDIuMzI4MTI1IDE2NS4wOTc2NTZoMTY4LjY5NTMxM2MtNC44NTU0NjktMzYuNTYyNS0yOC4yNDIxODgtNjguNDEwMTU2LTYxLjkyNTc4Mi04NS4yNTM5MDZsLTE1LjY4NzUtNy44NTE1NjNjLS40MTAxNTYtLjIwNzAzMS0uNzYxNzE4LS40ODgyODEtMS4xNjc5NjgtLjY5NTMxMmwtMjcuNzYxNzE5IDU1LjUwNzgxMi0yNi44MzU5MzgtMTMuNDE3OTY4IDI5LjQ3NjU2My01OC45NDE0MDZjLTMuNTExNzE5LTIuOTA2MjUtNi45MTc5NjktNS44ODI4MTMtMTAuMTA1NDY5LTkuMDkzNzVsLTQyLjE3OTY4NyA0Mi4xNzk2ODctMjEuMjEwOTM4LTIxLjIxMDkzNyA0NC41ODIwMzEtNDQuNTc4MTI2Yy0zLjIwNzAzMS01LjA3MDMxMi02LjAxNTYyNS0xMC4zMzk4NDMtOC41NDI5NjktMTUuNzg1MTU2bC02NC44MzU5MzcgMjUuMjIyNjU2LTEwLjg3MTA5NC0yNy45NDkyMTggNjUuOTc2NTYzLTI1LjY2Nzk2OWMtMi42MzY3MTktMTEuODk0NTMxLTMuOTM3NS0yNC4xOTUzMTMtMy4zMjQyMTktMzYuNzM0Mzc1bC43NjE3MTktMTUuNzMwNDY5aC0yMS40MDIzNDRjLTU1LjAxOTUzMSAwLTk3LjE1MjM0NC00MS4yMjI2NTYtMTAzLjQyMTg3NS05NS44OTA2MjUtMy42MTcxODctMzEuNTIzNDM3LTMxLjgzMjAzMS01NS41NjI1LTYyLjk0NTMxMy01NC4wOTc2NTZsLTcuMjY1NjI0LjI2NTYyNS02NC4yNjU2MjYgODguMDU0Njg3YzkuMzk0NTMyIDguMDAzOTA3IDE3Ljc3NzM0NCAxNy4xNzU3ODIgMjQuNzYxNzE5IDI3LjY5OTIxOXptMCAwIi8+PHBhdGggZD0ibTMzMS43NDYwOTQgNDIwLjA1MDc4MS0yOTguNDQ1MzEzLTI0MS45NjQ4NDMtMzMuMzAwNzgxIDUwLjA5NzY1NiAzMTAuNzQyMTg4IDI1MS44NjcxODdoMjAxLjI1NzgxMnYtNjB6bTAgMCIvPjwvc3ZnPg=="},
            "disposal": {"title": "Disposal", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pgo8IS0tIEdlbmVyYXRvcjogQWRvYmUgSWxsdXN0cmF0b3IgMTguMC4wLCBTVkcgRXhwb3J0IFBsdWctSW4gLiBTVkcgVmVyc2lvbjogNi4wMCBCdWlsZCAwKSAgLS0+CjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+CjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiBoZWlnaHQ9IjQwIiB3aWR0aD0iNDAiIHg9IjBweCIgeT0iMHB4IgoJIHZpZXdCb3g9IjAgMCAzMjQuNzI2IDMyNC43MjYiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDMyNC43MjYgMzI0LjcyNjsiIHhtbDpzcGFjZT0icHJlc2VydmUiPgo8Zz4KCTxwYXRoIGQ9Ik0xNTYuMzg2LDExNC43MzZsODUuNTUyLDEzLjYzMWwzMC4zOTktNzcuODczbC00LjE3MS04LjI1NmwtMTguMzkzLDguNjI0Yy0zLjU3Ny03LjkyNS05LjA1Ni0xOC41NjItMTcuMjY1LTI3LjY3MwoJCUMyMTcuMjcxLDYuMjc3LDE5OS4yNDUsNC44NjEsMTgzLjU0Myw0Ljg2MWMtMC4yMjMsMC02Ny42NjgtMC4wMjEtNjcuNjcxLTAuMDIxYy0xMC4yNzgsMC4wMDktMTguMTI0LDQuMzk4LTIzLjMxLDEzLjAyOAoJCUw1My4yNDcsODIuMDM0bDY5Ljc4MywzNi40MzZsMS4yMDMtMi4wNTRjNy44NjctMTMuNDE5LDE1Ljk0MS0yNy4wMTgsMjMuNzQ4LTQwLjE3YzIuMzc1LTQuMDAyLDQuNzUyLTguMDA0LDcuMTI1LTEyLjAwNwoJCWwxNy4xNzMsMzAuOTM2bC0yMS4wOTMsMTAuMTdMMTU2LjM4NiwxMTQuNzM2eiBNMTYzLjgxNyw0OS43MjRsMTYuODc1LTI5LjY4NmMxNS42OTIsMC4wMTcsMzAuNjI1LDEuMDcxLDQxLjE1NSwxMi43NTUKCQljNy43ODgsOC42NDYsMTIuNzIsMTguODk4LDE2LjUxNSwyNy43ODhsNC41MTIsOS4zNjVsNy45MS0zLjcwOGwtMTguMDA4LDQ2LjEzN2wtNDcuNDM2LTcuNTU4bDYuMjE5LTMuMDE2TDE2My44MTcsNDkuNzI0eiIvPgoJPHBhdGggZD0iTTMyMC42NTcsMTc2LjAzbC0zOC4zNDgtNjQuNzQ0bC02NC44MjgsNDQuNjYzbDEuMjUzLDIuMDI0YzcuOTAzLDEyLjc2NywxNS44NjgsMjUuNzkzLDIzLjU3MSwzOC4zOTEKCQljMi43MDksNC40MjksNS40MTYsOC44NTcsOC4xMjcsMTMuMjg0bC0zNS4zOTcsMC43MjJjMC4xNDctNC41NDcsMC40MjUtMTEuNjkzLDAuNTcxLTE1LjI3M2wwLjMyNC04LjEyNmwtMTAuNzQyLDAuMjA4CgkJbC01Mi4wMzUsNjkuMjYybDU0LjYzMyw2My4yNzFsOS4yNTEsMC4xNzNsMC45NzQtMjAuMjkzYzMuMzIsMC4yMDYsNi4zODEsMC4zMDcsOS4yOTcsMC4zMDdjOC42MDQsMCwxNi4yMDctMC44NjMsMjMuMjQtMi42MzYKCQljMjIuMDctNS41NjYsMzEuNzUtMjAuODQyLDM5LjA5NC0zNC43MzFjMC4yNjYtMC41MDYsMzEuMzIxLTU5LjIwOCwzMS42MzYtNTkuODAyQzMyNi4wNzcsMTkzLjY0NSwzMjUuODY0LDE4NC42NTUsMzIwLjY1NywxNzYuMDMKCQl6IE0yNDcuMDM4LDI4My4zNDljLTUuOSwxLjQ4OC0xMi4zMDYsMi4yMTItMTkuNTgyLDIuMjEyYy00LjkyNiwwLTkuNjA5LTAuMzQyLTEyLjcwMy0wLjU5OWwtMTAuMzkxLTAuMzg1bC0wLjQxOCw4LjcyMgoJCWwtMzIuMzY5LTM3LjQ4NGwyOC44NTItMzguMzk4bC0wLjI0Miw2Ljg5OWw1OS4wMS0wLjE4M2wxOC4zNTMsMjguNzkxQzI3MC4xOTksMjY2Ljc5LDI2Mi4yODgsMjc5LjUsMjQ3LjAzOCwyODMuMzQ5eiIvPgoJPHBhdGggZD0iTTc3LjU0NiwyMjEuMDgybDE3LjY0OC0zMC43MTljNC4zMDgsMi43ODUsMTEuMjI1LDcuMzMyLDEyLjc5Myw4LjM2NWw2Ljc5Miw0LjQ3MWw1LjM2NS05LjMxbC0zMi41MDEtODAuMzAzCgkJTDUuMjU2LDEyNy43NjFsLTQuOTIsNy44MzlsMTYuODg1LDExLjNjLTQuOTQ1LDcuMTY2LTExLjIzLDE3LjM1OC0xNC43ODUsMjkuMDcxYy02LjYxNywyMS43ODUsMS40OCwzNy45NTQsOS41NzYsNTEuMzc1CgkJYzAuMTEzLDAuMTkyLDI5LjEyMSw0OC4zMzEsMzQuOTM2LDU3Ljk4MmM1LjMwOSw4Ljc4NCwxMy4xMDIsMTMuMjM3LDIzLjIxMiwxMy4yMzdsNzIuMDc3LDAuMDE1bC0wLjAyNS03Ny42NzlMNzcuNTQ2LDIyMS4wODJ6CgkJIE02MC42MzUsMjIxLjA5N2wtMzQuMTM3LDAuODc3Yy04LjA5LTEzLjQ1Mi0xNC44OTktMjYuNzg3LTEwLjMzLTQxLjgzYzMuMzgxLTExLjEzMyw5LjYxNS0yMC42NTEsMTUuMjctMjguNDk1bDUuNjg2LTguNjk5CgkJbC03LjI1Ni00Ljg1OGw0OC44MS04LjQwMmwxOC4wMTcsNDQuNTIzbC01Ljc4OS0zLjc2OUw2MC42MzUsMjIxLjA5N3oiLz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8Zz4KPC9nPgo8L3N2Zz4K"},
            "governance": {"title": "Governance", "image": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iNDBweCIgaGVpZ2h0PSI0MHB4IiB2aWV3Qm94PSIwIDAgNDAgMzkiIHZlcnNpb249IjEuMSI+CjxkZWZzPgo8aW1hZ2UgaWQ9ImltYWdlNSIgd2lkdGg9IjUxMiIgaGVpZ2h0PSI1MTEiIHhsaW5rOmhyZWY9ImRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBZ0FBQUFIL0NBWUFBQUFoVkdXckFBQUFCbUpMUjBRQS93RC9BUCtndmFlVEFBQWdBRWxFUVZSNG5PM2RlZkJtVlozZjhYZi8yZ2Fhcldtd2RVRG9ibGtiY1FFMXlwUUxTQnhIVVFzaktJNldiSXBDU1RIT21Ja1pacHpTU3Bqb3hHUUd4eVZxR0ZwblRCRk54aWlJR2x3YVJVVlJZaFF4S2x1cnJialFDRFE3OUM5LzNQNUJMNy9sUHM5enovM2VjODc3VlhXS3NpeDR6dGFmZS9vKzkvbmVSVWdxd1hUUTV5NEsrbHhKRTVxSzdvQWtTZXFmQndCSmtpcmtBVUNTcEFwNUFKQWtxVUllQUNSSnFwQUhBRW1TS3VRQlFKS2tDbmtBa0NTcFFoNEFKRW1xa0FjQVNaSXE1QUZBa3FRS2VRQ1FKS2xDSGdBa1NhcVFCd0JKa2lya0FVQ1NwQXA1QUpBa3FVSWVBQ1JKcXBBSEFFbVNLdVFCUUpLa0Nua0FrQ1NwUWg0QUpFbXFrQWNBU1pJcTVBRkFrcVFLZVFDUUpLbENIZ0FrU2FxUUJ3QkpraXJrQVVDU3BBcDVBSkFrcVVJZUFDUkpxcEFIQUVtU0t1UUJRSktrQ25rQWtDU3BRaDRBSkVtcWtBY0FTWklxNUFGQWtxUUtlUUNRSktsQ0hnQWtTYXFRQndCSmtpcmtBVUNTcEFwNUFKQWtxVUllQUNSSnFwQUhBRW1TS3VRQlFKS2tDbmtBa0NTcFFoNEFKRW1xa0FjQVNaSXE1QUZBa3FRS2VRQ1FKS2xDSGdBa1NhcVFCd0JKa2lya0FVQ1NwQXA1QUpBa3FVSWVBQ1JKcXBBSEFFbVNLdVFCUUpLa0Nua0FrQ1NwUWg0QUpFbXFrQWNBU1pJcTVBRkFrcVFLZVFDUUpLbENIZ0FrU2FxUUJ3QkpraXJrQVVESzMvSktQMXVTcENvZERsd0FiQUttZzlxOXdFZUJJeE9QVlpLa3FrMEJKd05YRW5mUm42dDlGWGdsM2xtVUpLbFRSd05mSi81Q3YxRDdObkJNb2ptUUpLa2Fod0FmSi83Q1BtcTdIRGdpd1h4SWtsUzB4Y0RiZ1B1SnY1aVAyKzRIL21MTFdDUkowZ0pXQWxjUWZ3SHZxbjBET0xEVEdaSWtxVEFuQVJ1SnYyaDMzVzRIWHRQaFBFbVNWSVJGd051SnYxQ25iaGZnTHdVa1NRSmdKK0JqeEYrYysyci9DQ3pwWk9Za1NjclU3c0JuaWI4bzk5MitBT3pad2Z4SmtwU2RQWUJ2RVg4eGptcmZwRGtBU1pKVWpTWEE1NGkvQ0VlM0x3STdUemlYa2lSbFlSR3dsdmlMNzFEYWY5c3lKNUlrRmUzZHhGOTBoOWJlT2RHTVNwSTBjQ2NSZjdFZGF2dWpDZVpWa3FUQk9vQXlpL3gwMVc0RFZvMDl1NUlrRGRBVThHWGlMN0pEYjEvRmR3ZEl5Zm1IVE9yUDI0RFRvenVSZ1pVMEx4SDZhblJISkVtYTFHSGsvVmEvdnR2OXdLRmp6YlFrU1FQeUtlSXZxcm0xZng1cnBpVkpHb2hqaWIrWTV0cWVPL3AwUzVJVWJ3cjROdkVYMGx6Yk5mam1RRWxTaGs0bS9pS2FlenRwNUZtWEpDblkxNGkvZ09iZXZqTHlyRXVTRk9oSTRpK2VwYlNuampqM2toYmdkMnRTT3VkRWQ2QWdaMFYzUUNxTmI5K1MwdGdMMkFEc0d0MlJRdHdEN0U5VFJsbFNCNklQQU5QQm55OUowaEQwZmozMkt3QkpraXJrQVVDU3BBcDVBSkFrcVVJZUFDUkpxcEFIQUVtU0t1UUJRSktrQ25rQWtDU3BRaDRBSkVtcWtBY0FTWklxNUFGQWtxUUtlUUNRSktsQ0hnQWtTYXFRQndCSmtpcmtBVUNTcEFwNUFKQWtxVUllQUNSSnFwQUhBRW1TS3VRQlFKS2tDbmtBa0NTcFFoNEFKRW1xa0FjQVNaSXE1QUZBa3FRS2VRQ1FKS2xDSGdBa1NhcVFCd0JKa2lya0FVQ1NwQXA1QUpBa3FVSWVBQ1JKcXBBSEFFbVNKT0FTWURxemRtYVNtZEFrOWdJMkViODNTbWwzQVh1UHRBTHFnM21wWXF3RUhpUitnNDdhdnB0aU1qU3hEeEcvTjBwcEh4eHg3cFdlZWFtaW5FLzg1aHkzSFoxZ1BqU1pKeEsvTDBwcFR4NXg3cFdlZWFsaUxBRTJFTDh4eDIwZjZYNUsxSUd2RUw4M2NtOVhqRHpyU3MyOFZGRmVTZnltbktUZERlelQrYXhvVXE4Z2ZtL2szazRhZWRhVm1ubXBvbnlaK0UwNWFYdEw1N09pU1MwQ3ZrWDgzc2kxZlhQTEhHcFl6RXNWWXcyd21mZ05PV203SG4vYU9VUy9UeG43SzZJOVo0ejVWbHJtWlNHcUh2eFd6cUtNdjJVY0JEdy91aFBhd1RlQS94WGRpUXo5VCtDcjBaM1FEc3hMRldNcGNDdnhwOUd1MmllN25SNTE1RURnWHVMM1J5N3RQdUNRc1daYUtabVhLc29aeEcvQ0x0dUR3S3BPWjBoZCtVdmk5MGN1N2MvSG5HT2xaVjZxS0ZjVHZ3bTdidS9vZEliVWxTbmdTOFR2ajZHM3J3Q0x4NXhqcFdWZXFoaEhFci81VXJSZjBQeE9WOE96UDJYZFF1MjYzWVovSXhzcTg3SXd0VDhFZUU1MEJ4TFpGemdodWhPYTFjK0JOMFIzWXNET0J0WkhkMEt6TWk5VmpHV1UvYktXTDNZM1ZVcmdYY1R2a2FHMXY1NW9ScFdTZWFtaW5Fdjhwa3ZkbnREWmJLbHJpNENMaU44alEya2ZvNHlmbHBYS3ZGUlJ2ay84aGt2ZC9yYXoyVklLUzREUEVyOVBvdHNYZ1owbW5FdWxaVjZxR01jUXY5bjZhQnVCWFR1YU02V3hPMDI1MitpOUV0V3UyaklIR2k3elVrVzVtUGpOMWxjN282TTVVenE3QVpjUnYxZjZicGNEZTNZd2Ywckx2RlF4VmxCWFJiWnJ1cGsySmZZbzRNUEU3NWUrMmtlcDlLZFhtVEV2VlpRL0ozNlQ5ZDJlM3NuTUtiVkZ3TnVKM3krcDJ3WDR3Rjh1ekVzVll3cTRrZmdOMW5lN3NJdkpVMjlPcE14aVFiOERYdDNoUENrdDgxSkZlVEh4bXl1aTNRM3MzY0g4cVQ4SEFPdUkzenRkdGE4RGorOXlncFNjZWFtaVhFTDg1b3BxYis1Zy90U3Z4Y0JmMEx3Wkwzci9qTnZ1QTg3RDJ2NDVNaTlWakpVMGIzNkszbGhSN1NmNHZXdXVEZ0UrRG13bWZoK04waTRCRGs0d0gwclB2RFF2aTNJK3NSdnFLdUovNzMzY3hMT29TTThFdmtaOE9DN1VyZ2FlbTJnTzFBL3owcndzeGs3QUw0bmRUS2R1YVpGOStNU2tFNmx3aTRDVGFGNlpHN21YWm10WDBEekE2TitjOG1aZW1wZEZPWm5ZamZRYllCZGdaK0JYZ2YxNEFIamNoSE9wNFZoRDg1TzZ5SmUwM0V2em0vNm5KQjZyK21OZW1wZEYrUkt4Ry9wZFcvVWwraTF3ZnpYMkxHcW9saE8zbjViM01ENzF5N3cwTDR1eGh0aUhweDVpMjU4L3JTTDI0Wm9OV0lHdFJGSDdTV1V4THl2S3k2bm9EdlRnTEdLL2s3d011R21yLzcwZStGeFFYd0Qyby9sOXJ5UnR6N3pjbG5tWnNhWEVWMVI3MFN6OU9qNjRUNThmZFNJMWVGRjdTZVV3TDgzTG9weEI3TWE1bnRudnNpd0NmaHpZcjgzQW9TUE9wWVl0YWkrcEhPWmxaWGxaK2xjQVp3ZC8vZ2RvTnMvMnBvRVA5ZHlYclMwQzNoRDQrWktHeDd5Y25YbVpvU09KUGMzZURld3pULytXQTNjRjltOGpzR3ZMdWRUd1JlMGpsY0c4ckRBdlM3NERjRTd3NTE5TTgzM2FYRzZqS2U4YVpUbE5RUmxKTWkvbloxNW1aQm14eFZHbWFmZE82YU9DKy9pTkZuMVVIcUwya1BKblhwcVhSVG1YMkkxeTFRaDlqYTUzL2JRUitxcmhpdG8veXA5NWFWNFc1VnBpTjhrcEkvVDExT0MrUmo1Y28rNUU3Ui9sejd3MEw0dHhETEViWkthT2RWdlI5YTd2d25LdUpZamFQOHFiZVZseFhwYjRFR0QwVDFrdXBIbEJTbHYzQVd2VGRLV1ZYWUhYQkg2K3BEam01V2pNeXdGYlFiT1pvazZIMjlleGJtc1ZzZld1cjhOWHVPWXVhdThvWCthbGVWbVU4NGpiRk5QQUpSUDAvZExndmg4elFkOFZMMnJmS0YvbXBYbFpqQ25nUm1JM3hXeDFyTnVLcm5kOThRUjlWN3lvZmFNOG1aZm1aVkZlVE95R21LdU9kVnZSOWE3dnAzbnpsZklVdFcrVUovUFN2Q3pxSWNDemdqOS9yanJXYlUwVCt4T1RKY0JwZ1o4dnFUL201V1RNeXdGWlNleERJUXZWc1c0cnV0NzFlbUJ4QitOUS82TDJqUEpqWHBxWFFEbDNBTjVJN0VJc1ZNZTZyZWg2MXl0cHZsdVRWQzd6c2h2bTVRQXNBVFlRZHdxY3BsMGQ2N2FpNjExZjF1RlkxSitvL2FLOG1KZm1aVkZPSm5ZRGZEUEJtTDRWT0o3TndNRUp4cVMwb3ZhTDhtSmVtcGNQSytFcmdPaUhXZDZYeVgrenJVWEE2d00vWDFJNjVtVzN6TXRBYTJoT1lGR252OTh5V2gzcnRuWUdmaDA0cmxIcmN5dGUxRjVSUHN4TDgzSWJ1ZDhCT0p2WWtveWoxckZ1SzdyZTlhT0JFd00vWDFMM3pNczB6TXNBUzRHTnhKMzZ4cTFqM2RZcVluK3FjMlhDc2FsN1VmdEVlVEF2emN1aW5FSGNZazh6V1IzcnRxTHJYUitWZm9qcVNOUWVVUjdNUy9PeUtGY1R1OWlUMUxGdUs3cmU5ZnZURDFFZGlkb2p5b041YVY0V0kvcTNuNVBXc1c0cnV0NzFuY0NleVVlcExrVHRFUTJmZVdsZXppclhod0RmRlB6NS80WEo2bGkzTlExOHVJZlBtY3Z1d0dzQ1AxL1M1TXpMZnBpWFBWZ0diQ0x1bE5kVkhldTJvdXRkL3lEOUVOV0JxUDJoWVRNdnpjczU1WGdINEZSZ3Q4RFA3NnFPZFZ2UjlhNmZBRHdyOFBNbGpjKzg3SmQ1bWRpMXhKM3VwdW0yam5WYjBkL2gvVlA2SVdwQ1VYdER3MlplbXBmRk9JYlloVTFSeDdxdHlIclg5d0dQU1Q5RVRTQnFiMmk0ekV2emNsNjVmUVZ3ZHZEblI5YWNqdnpzbllEVEF6OWYwdWpNeXhqbVpRSXJhTXBJUnAzcVV0V3hiaXU2M3ZYTnhMNURYUE9MMmhjYUp2UFN2RnhRVG5jQXpxUloxQ2lwNmxpM0ZWM3ZlaFh3Z3NEUGw5U2VlV2xlRm1NS3VKRzQwMXpxT3RadHJTSzIzdlduMHc5Ulk0cmFFeG9lODdKaFhoYml4Y1F0NGpUOTFMRnVLN0xlOVVQQTZ1UWoxRGlpOW9TR3g3eDhoSGs1ajF5K0FvaCttR1ZJTlo0ait6SkZjMnRSMG5DWmw0OHdMek8za3RqYk9IM1ZzVzRydXQ3MXI0bjlibEd6aTlvUEdoYnpjbHZtNVR5R3RGQnplU094VDFQMlZjZTZyV2xpNjEydkFGNFcrUG1TNW1aZWJzdTh6TmdTWUFOeHA3ZSs2MWkzRlYzdmVsM3lFV3BVVVh0QncyRmV6czY4ek5USnhDM2FOUEFQNlljNHRvdUluWnNucGgraVJoQzFEelFjNXVYY3pNc01mWm5ZUmZzWDZZYzR0cWNTT3pkL24zNklHa0hVUHRCd21KZHpNeTh6czRibXU2U29CWXVzWTkxV1pMM3JPNEE5MGc5UkxVWHRBdzJEZWJrdzgzSTdRMzRJOEd5YUp6aWpET21uTEhPSjdPTWV3S3NDUDEvU0k4ekxoWm1YbVZnS2JDVHV0QlpkeDdxdDZIclgzMDAvUkxVVXRRY1V6N3hzeDd6Y3psRHZBUHdSelpPYlVhTHJXTGNWWGUvNktjRFJnWjh2eWJ4c3k3ek14TlhFbmRLR1VzZTZyVlhFRnY3NFNQb2hxb1dvOVZjODg3STk4M0xnamlKdWNhWnBha2ZuNWpQRXpkZTlOTVV1RkN0cS9SWEx2QnlkZWJuRkVMOENlRlB3NTc4ditQUEhFZG5ubllGVEFqOWZxcGw1T1RyemNxQ1dBWnVJTzUzZHdEQVBSUXVKcm5jOXRQcmZOWXBhZThVeEw4ZGpYbTR4aUU1czVWUmd0OERQL3dERHFtUGQxalN4OWE0UEFwNGYrUGxTamN6TDhaaVhBM1V0Y2FleW9kYXhiaXU2M3ZVbjB3OVI4NGhhZDhVeEw4ZG5YZzdNc2NRdHhqVERybVBkMWtYRXpkK0RORS9ZS2tiVXVpdkdzWmlYa3pJdkIrUmlZamYwa090WXR4VmQ3L29kNlllb09VU3R1V0tZbDVNekx3ZGlCYzNQSTZJV0lvYzYxbTFGMXJ2K0JjMHJTZFcvcURWWC84ekw3bFNkbDBONUNQQk1tcDlIUk1taGpuVmJrV1BaRnpnaDhQT2xHcGlYM1RFdmcwMEJOeEYzQ3N1bGpuVmIwZld1djVoK2lKcEYxSHFyWCtabHQ2ck95eUhjQVhnUnNEcnc4M09wWTkxV2RMM3I0NEFuQkg2K1ZETHpzbHZtWmJCTGlUdDk1VmJIdXExVnhOYTcvdHYwUTlSMm90WmEvVEl2dTJkZUJsbEo3TVRuV01lNnJjaDYxN2NSVzZDa1JsRnJyZjZZbCtsVW1aZlJYd0c4RVZnYytQazUxckZ1SzNKc2V3RW5CMzYrVkNMek1oM3pzbWRMZ0EzRW5icHlyV1BkVm5TOTYydlNEMUZiaVZwbjljTzhUS3ZLdkl4YzBKY0Qrd1YrZnE1MXJOdWFKcmJlOVZIQTB3TS9YeXFKZVptV2VkbXpMeE4zMnNxOWpuVmIwZld1TDB3L1JHMFJ0Y2JxaDNtWm5ublprelUwcDhtb2liNG8vUkFIWXkyeHdiRjM4aEVLNHRaWTZabVgvVm1MZVpuY0JjUk44alJsMUxGdUs3cmU5WnZURDFIRXJhL1NNeS83WTE0bXRoVFlTTndFbDFUSHVxM0lldGMvb1huQVJtbEZyYS9TTWkvN1YwMWVSandFK0dxYTcxcWlsRlRIdXEzSU1SOE1QQy93ODZXY21aZjlNeThUdXBxNDAxVnBkYXpiaXE1My9ZbjBRNnhlMU5vcUxmT3lmK1psSWtjUk42blR3THZTRDNHdy9vYTRlWDhBZUZ6NklWWXRhbTJWam5rWng3eE00RUxpSnZVaDRNRDBReHlzVmNTV0VmMnI5RU9zV3RTNktoM3pNbzU1MmJGbHdDYmlKclRrT3RadFJkYTcza0JUelV4cFJLMnIwakF2NDVtWEhUcVh1TW1jQm81UFA4VEJlekd4YS9DeTlFT3NWdFNhS2czek1wNTUyYUZyaVp2STB1dFl0eFZkNy9yejZZZFlyYWcxVlJybVpUenpzaVBIRWplSjA4Qy9UajdDZlB3WmNldXdHVGcwL1JDckZMV202dDZ4bUpkRFlWNTI0R0xpSnJHV090WnRSZGU3Zm5mNklWWXBhajNWUGZOeU9NekxDYTBBN2lWdUFpOUtQOFRzckNWdVBUWUN1eVlmWVgyaTFsUGRNaStIWnkzbTVkak9JMjd5cHFtcmpuVmIwZld1VDBrL3hPcEVyYVc2WlY0T2ozazVwaW5nSnVJbXJzWTYxbTFGMXJ2K1JnL2pxMDNVV3FvNzV1VndtWmRqaVA0WnhhbnBoNWl0MDRoZG02Y2xIMkZkb3RaUjNURXZoK3Mwek11UlhVcmNoTlZheDdxdDZIclhIMG8veEtwRXJhTzZZMTRPbDNrNW9wWEVsbEtzdVk1MVc1SDFydThpOWkxbnBZbGFSM1hEdkJ3KzgzSUU1eE0zV2JYWHNXNXJGYkdoYzA3NklWWWphZzNWRGZOeStNekxscGJRMURLT21panJXTGNYV2UvNk9wcHFXNXBjMUJwcWN1WmxQc3pMRms0bWJwS21zWTcxS0tJZlBEb20vUkNyRUxWK21weDVtUS96c29WMXhFMlFkYXhIRTEzdit1TDBRNnhDMVBwcGN1c3dMM05oWGk1Z0RVME40NmdKK3JQMFF5ek92eUZ1dmU0SDlrcy94T0pGclo4bVkxN214N3ljeHdYRVRjNjlOS1UwTlpwOWdIdUlXN2Z6MGcreGVGRnJwOG1ZbC9reEwrZXdsS1oyY2RURVhKUitpTVZhUzl5NnJRY1dKeDloMmFMV1R1TXpML08xRnZOeUI2OGpibEttc1k3MUpKNUI3TnE5TlAwUWl4YTFiaHFmZVprdjgzSVdWeE0zSWQvcFlYeWxpNngzZlZrUDR5dFoxTHBwZk9abDNzekxyUnhGM0dSTVl4M3JMcHhHM1BwdEJnNU9Qc0p5UmEyYnhtTmU1dTgwek11SFhVamNaR1QvenVTQldFcFRFenhxSGQrWmZvakZpbG96amNlOHpKOTV1Y1V5WUJOeEUvRTM2WWRZamY5STNEcitCbDlJTXE2b05kUG96TXR5bUpmQXVjUk53bWJna1BSRHJNYUJOTFhCbzliek5lbUhXS1NvOWRMb3pNdHltSmZBdGNSTmdIV3N1eGRaNy9yS0hzWlhvcWoxMHVqTXk3SlVuWmZIRWpmNGFheGpuVUowdmV1ajBnK3hPRkZycGRFY2kzbFptcXJ6OHVJNU90Vkh1NW1CRmtUSTNCUk5qZkNvZFgxLytpRVdKMnF0TkJyenNqelY1dVVLbW5LU1VRTzNqblU2a2ZXdTd3VDJURC9Fb2tTdGxkb3pMOHRWWlY2ZU4wWm51MnJXc1U0cnV0NzEyZW1IV0pTb2RWSjc1bVc1cXN2TEtlQ21Eam8rYnJzby9SQ3J0NWE0OWYxQit1RVZKV3FkMUk1NVdiNjFWSlNYTCttbzQrTTI2MWluRjEzditsbnBoMWlNcURWU08rWmwrYXJLeTBzVERhSk5zNDUxZnlMclhmOVREK01yUmRRYXFSM3pzZzVWNU9WSzRNRWVCalJYT3pYOUVMWEZhY1N0ODMzQVk1S1BzQXhSYTZTRm1aZjFPSTBLOHZMOGdNSE5OT3RZOXl1NjN2VmIwdyt4Q0ZIcm80V1psL1VvUGkrWEFCc0NCMmdkNi81RjFydStHWCs3M0ViVSttaCs1bVY5aXM3TGt3TUhaeDNyR05IMXJsK1Vmb2paaTFvYnpjKzhyRS9SZWJrdWNHRFdzWTRUV2UvNjB6Mk1MM2RSYTZQNXJjTzhyRkdSZWJtRzVsUVpOVERyV01lSnJIZjlFTEE2K1FqekZyVTJtcHQ1V2E4aTgvS0N3RUhkak44RlI1b0NiaVJ1L2M5UFA4U3NSYTJMNW1aZTFxdTR2RnhLODBScDFJQ3NZeDB2c3Q3MXI0R2Qwdzh4VzFIcm90bVpseW9xTDE4WE9CanJXQTlEZEwzcms5TVBNVnRSYTZMWm1aY3FLaSt2RGh6SVJWME9SQk5aUzl3K1dKZDhkUG1LV2hQTnpyd1VGSktYUndVT1locnJXQTlKZEwzcko2WWZZcGFpMWtNN01pODFvNGk4dkRCd0FOYXhIcDdJZXRkLzM4UDRjaFMxSHRxUmVhbXRaWjJYZXdHYkFnZHcycVFEVU9kT0oyNC8zQUhza1g2STJZbGFEMjNMdk5UMnNzN0xQdzdzdkhXc2h5bTYzdldaNlllWW5haTEwTGJNUzIwdjY3eThOckRqMXJFZXJzaDYxOS90WVh5NWlWb0xiY3U4MUd5eXpNdGpBenR0SGV0aGk2NTNmWFQ2SVdZbGFoMzBpR014THpXN0xQUHk0c0FPZjJhY0RxdFhseEczUHo3U3cvaHlFclVPZW9SNXFma01MaThYemRQWkZjRFBzUHFhaHVrKzRBRGdOOUVkR1lpb2kvRjhHVklUODFKRE5tdGVUczN6TDV5Sm0xbkR0VE53U25RbnBDM01TdzNackhrNTErbDlDcmdCMzhDbVlic0JPSlRtKzgvYWVRY2dqbm1wSE95UWwzUGRBVGdlTjdPRzd5RGcrZEdkVVBYTVMrVmdoN3ljNndCd1Z2cStTSjA0TzdvRHFwNTVxVnhzazVlejNiNWJTZk1lWTk4bHJSdzhSSE95WFIvZGtXQitCUkREdkZST3RzbkwyZTRBbklXYldmbFlESndSM1FsVnk3eFVUcmJKeSsxUDcwdG9UZ2I3OXRramFVSy9CRllCRDBSM0pKQjNBUHBuWGlwSEQrZmw5bmNBWG82YldmblpGemdodWhPcWpubXBIRDJjbDlzZkFIeWdTcmx5NzZwdjdqbmw2bXpZOXZiZDRjQVBxUHVXbnZKMkJIQmRkQ2VDK0JWQXY4eEw1ZTZJcmU4QW5JV2JXWG56TmNIcWkzbXAzSjA1czRHWEFodUE1WUdka1NiMU8yQi80SzdvamdUd0RrQi96RXVWNEhjemR3QmVqWnRaK2RzTE9EbTZFeXFlZWFrUzdEVnplcjhhZUhwa1Q2U08vQi9ncWRHZENPQWRnUDZZbHlyQ3pCL2VCN0dZaGNyd0VQQ282RTRFOEFEUUgvTlNSWmo1Q3VEKzBGNUkzYmt2dWdNcW5ubXBJbmdBVUdrOEFDZzE4MUpGbURrQUdKb3FoWHRacWJuSFZJU1pBOEFkb2IyUXVuTjdkQWRVUFBOU1JaZzVBUHcydEJkU2Q5ekxTczA5cGlMTUhBQnVEZTJGMUIzM3NsSnpqNmtJM2dGUWFReG5wV1plcWdnekI0Q2ZodlpDNnM3NjZBNm9lT2FsaWpCekFMZzVzaE5TaDI2SzdvQ0tkM04wQjZRdXpCd0FERTJWNHVib0RxaDQ1cVdLTUhNQXVDRzBGMUozM010S3pUMm1JaXphNnA4YmFkNm1KdVZxSTdCUGRDZUMrQzZBL3BpWEtzSEdtVHNBMDhEM0kzc2lkZUI3MFIxUUZjeExsZUI3VTF2L2o3QnVTTjF3RDZzdjdqWGxicHNEd0hmQ3VpRjE0NXJvRHFnYTVxVnlkODNXQjRDdmhYVkQ2c2FWMFIxUU5jeEw1ZTdLclIvZ1dRVGNBandtcURQU0pHNEI5bzN1UkNBZkF1eVhlYW1jM1FMc3UvVWRnR25nNjBHZGtTYmwzLzdWSi9OU09ic1NIcWtETU9NTEFSMlJ1bkI1ZEFkVUhmTlN1Ym9jZHJ4OTkzamd4djc3SWsxc05YVy9COEN2QVBwblhpcFhxNEgxMjk4QnVBbjRjZjk5a1NaeUhYVmYvQlhEdkZTT0hzN0w3UThBQUpmMDJ4ZHBZcGRHZDBEVk1pK1ZtNGZ6Y3JZRHdNZDc3SWpVaFl1ak82QnFtWmZLemNONU9kZjNkOWNEQi9YVEYya2lOd0FIUjNkaUFId0dJSTU1cVZ4c2s1ZXozUUVBK0IvOTlFV2FtSC83VnpUelVybllKaS9uT3IwZkJ2eHdudjlmR29KcG1yMzZrK2lPRElCM0FPS1lsOHJCRG5rNTF4MkFIMkZoRlEzZk9yejRLNTU1cVJ5c1k3dThuT3NBQVBEaHBGMlJKdmRmb3pzZ2JXRmVhdWgyeU12NWJsbnRRdk5iUVd0ZGE0aCtSVlBNNHQ3Z2ZneUZYd0hFTWk4MVpMUG01WHgzQU80RjNwK3dROUlrM29NWGZ3MkhlYWtobXpVdkZ6cTk3dzM4Rk5ndFJZK2tNZDBOckFSdWplN0lnSGdISUo1NXFTR2FNeS9udXdNQXNCSDRTSW9lU1JQNE1GNzhOVHptcFlab3pyeHNjM3JmajZiUXhkSXVleVNONlY2YVFoWWJvanN5TU40QkdBYnpVa015YjE0dWRBY0E0QmY0aEt1RzQ3MTQ4ZGR3bVpjYWtubnpzdTNwL2Zkb1RyVit0NlZJZDlLVVhQMU5kRWNHeURzQXcyRmVhZ2dXek1zMmR3QUFiZ0hlMVVXUHBBbWNqeGQvRFo5NXFTRllNQzlIT2IwdnBYbVA4T29KT2lTTjYwYmdDUHpwMzF5OEF6QXM1cVVpdGNyTHRuY0FBTzRCM2pwSmo2UUp2QVV2L3NxSGVhbElyZkp5bk5QN0pjQkx4dmozcEhGZEJydzR1aE1ENXgyQVlUSXYxYmZXZVRuT0g5NVZ3TFhBN21QOHU5S283cVM1bGZXejZJNE1uQWVBWVRJdjFhZVI4bktVcndCbXJBZitjb3gvVHhySGVYanhWNzdNUy9WcHBMd2M5L1ErQlZ3T0hEZm12eSsxY1FYTkh0c2MzWkVNZUFkZ3VNeEw5V0hrdkp6a0QrL2pnUDhMN0RQQmYwT2F5MjNBVS9Cdi8yMTVBQmcyODFJcGpaV1g0M3dGTUdNRGNQWUUvNzQwbDJuZ2RMejRxeHptcFZJWk95OG5PUUFBZklMbU5ZTlNsLzRUOEtub1RrZ2RNeStWd3RoNTJjWHR1MGNCWHdTZTI4Ri9TL295OEFMZ3dlaU9aTWF2QVBKZ1hxcExFK1ZsVjM5NGZ3LzROczMzWE5LNGZnWThIZmgxZEVjeTVBRWdIK2FsdWpCeFhrNzZGY0NNVzRBWEFyZDM5TjlUZmU0RVhvb1hmNVhQdk5Ta09zbkxyZzRBMEJTN2VCWGV1dFhvSGdCT29ubEtXcXFCZWFseGRaYVhYUjRBQUQ1SDg2UnIxTzFJNVdjYWVBUHd2Nk03SXZYTXZOU29zc2pMYzJrNmFyTXQxTjZDdWhDMWZwcWNlV2xyMjdMSnk3Y1JQMW0yWWJmelVGZWkxbERkTUM5dEM3WHM4dkt0eEUrYWJaanRuYWhMVWV1bzdwaVh0cmxhdG5uNUpwcmF4TkVUYUJ0RzJ3ejhDZXBhMUhxcVcrYWxiZXRXUkY2K251Ykp4ZWpKdE1XMisybEtWcXA3VVd1cTdwbVh0bWtLeThzL0FINUgvS1RhWXRxZHdQRW9sYWgxVlJybVpkMnR5THc4RXZnNThaTnI2N2Y5RkhneVNpbHFiWldPZVZsbkt6b3ZWd0JmSUg2U2JmMjBLMmhLbnlxdHFQVlZXdVpsWGEyS3ZId1V6Vk9OMFpOdFM5cytDQ3hCZlloYVk2Vm5YdGJScXN2TEU0RmJpWjk0VzdmdE44QUpxRTlSYTYzK21KZGx0cXJ6OHJIQVpjUXZncTJiOWdWOHkxbUVxUFZXdjh6THNwcDVTZk5PZ25OcG5ueU1YaERiZU8wTzRCeDhQV3lVcUhWWC84ekwvSnQ1T1l2OWdIOG1mbkZzbzdYUEFDdG5XVS8xSjJydEZjZTh6TE9abHdzNEViaVIrSVd5emQrdUIxNDJ4eHFxWDFGN1FQSE15enlhZVRtQ1hXaGVmdUJ0cnVHMU80Qi9DK3c4NStxcGIxRjdRY05nWGc2M21aY1RlRFROVDJEdUpuNGhhMi8zMHZ4VXBmamZxV1lvYWs5b1dNekw0VFR6c2tQN0FlOEJOaEcvc0xXMVRjRGY0VVllc3FpOW9XRXlMODNMSWkwRC9oaExaUGJSZmdXOEhkaW56Y0lvVk5RZTBiQ1psK1psa1hZQlhnT3N3OWRuZHRrMkExOENYbzNmV2VVa2FyOG9EK2FsZVZtc1E0SHphWjZ5ak40UXViYWZBUDhlT0hqRXVkY3dSTzBiNWNlOE5DK0JNb3NRUEIxNEpmQVM0UERndmd6ZGRjQ2x3TWVCN3dUM1JaT0p1aGlYbUNFMU1TL2JLeTR2Uy8vRHV4cDRJYzI3dFo5RlUwYXpacmNBVndLWEE1K2plZTJreXVBQlFKTmFqWG01dGVMenNyWS92SWZRYk95bkFVK2llZWZ5OHRBZXBYTWI4RDNnKzhDM2dhL1IzUEpUbVR3QXFHdm1aZUg4d3d2N0F3ZlJuSDRmRDZ5aWVZcHo2N2FZNWpXTnU4ZDA4V0YzQWc5dWFSdHAzZ3gySy9CYm10UHBUVnZhRGNDR29ENHFoZ2NBOWNHOExJaC9lS1V5ZUFDUU5KS3A2QTVJbXNoT3dMTURQLy9aVy9vZ0tUT2UzcVc4N0FvY0RUd1hPQVo0SnJBMHRFZHdEL0JONEFyZ0s4QlZOS1ZvSlVuU0JQWUNYZ0Y4bER4ZTluSVBjQWx3eXBhK1M1S2tsdllBWGdkOEZyaVArSXY2dU8wKzRETGdqQzFqa2lSSnN6aWM1bTF1RzRtL2VIZmQ3cUI1TzlwUm5jMldKRWtaMndrNEZmZ0c4UmZwdnRyWGFiNGlXTkxCL0VtU2xKVWxOQmZCbW11eXI2ZDVXOTB1RTg2bEpFbUR0eE5lK0QwSVNKS3E4aXFhaTEzMEJYZW9iVDNOeTJra1NTckNHdUR6eEY5Z2MybnJhR3JQUzVLVXBlWEFlNEVIaUwrbzV0WWVBTjZEdFFRa1NabDVBZkJ6NGkra3ViZGJhTjVYTDBuU29JSUYyODBBQUFlV1NVUkJWQzBGTGdBMkUzL3hMS1Z0cHFraEVQMkdPVW1TWnZWTTRFZkVYekJMYlRjQ3oybTlHcElrOWVBTndQM0VYeVJMYnc4Q2IyMjVKcElrSmJNTGNCSHhGOGJhMnNkbzNvNG9TVkx2OWdlK1JmekZzTloyRGJCNm9VV1NKS2xMUndPL0p2NGlXSHY3RmZDTUJkWktrcVJPUEkvbTdYYlJGejliMHpiUi9PeFNrcVJrVGdEdUlmNmlaOXUyM1FlOFlwNTFreVJwYktkZ1ZiOGh0d2VCTStkY1BVbVN4bkFtRnZmSm9XMEdYai9IR2txU05KS1gwL3p0TXZyaVptdlhIZ0pPbm5VbEpVbHE2UStBZTRtL3FObEdhL2NEeDgreW5wSWtMZWozYVo0d2o3NlkyY1pyZDJQcFlHbFdpNkk3SUEzWUlUUkZmbndkYmQ1dW82a1RjSDEwUjZRaG1ZcnVnRFJRZXdDZnhJdC9DWllEbndiMmpPNklOQ1FlQUtRZExRTCtBVGdpdWlQcXpPSEFSL0N1cC9Td3hkRWRrQWJvSGNEWjBaMVE1OWJRL0RyZ0s5RWRrU1FOend2eHQvNGx0NGRvZnRVaFZjL2JZZElqSGcxOEQ5ZzN1aU5LNmhmQWs0RmJvenNpUmZJWkFPa1I3OE9MZnczMkF6NFUzUWxKMGpDY1N2enRhVnUvN2RWSUZmTXJBQWxXMHR6Nlh4YmRFZlhxZDhBVGdRM1JIWkVpK0JXQUJQOFpMLzQxMmd0NGQzUW5KRWt4L2lYeHQ2SnRzZTA0cEFyNUZZQnE5aWpnR3VCSjBSMVJxT3VBSTRFSG9qc2k5Y2xDUUtyWm53Q3ZqZTZFd3EyZ2VWL0FWZEVka2Zya0hRRFZhaC9nUnF3UHI4YnR3RUZZRzBBVjhTRkExZW90ZVBIWEk1WUJiNDd1aE5Rbjd3Q29SdnNBTjlHODhVK2FjUWZ3ZUdCamRFZWtQbmdIUURYNlU3ejRhMGQ3NGwwQVZjUTdBS3JOM3NETmVBRFE3TzRBVnRNOEZDZ1Z6VHNBcXMyYjhPS3Z1ZTJKcjRKV0pid0RvSm9zQm00QVZrVjNSSVAyVStCQW1sY0hTOFh5RG9CcThoSzgrR3RoSzRFWFJYZENTczBEZ0dweVZuUUhsQTIvQmxEeC9BcEF0VGdRK0FrZWV0WE9adUJnbXArTFNrVXlERldMMDNHL3E3MHBtajBqRmNzN0FLckZENEUxMFoxUVZuNkVlMFlGODI5RXFzRVJHT1FhM1dIQTRkR2RrRkx4QUtBYW5CamRBV1hMdmFOaWVRQlFEUXh4amN1OW8yTDVESUJLZHlCTjhSOXBYQWZpcndGVUlPOEFxSFRIUlhkQTJYdGVkQWVrRkR3QXFIVFBpZTZBc3ZmYzZBNUlLWGdBVU9rTWIwM3FtT2dPU0NuNERJQkt0ai93cytoT3FBaXJhRjRTSkJYRE93QXEyYkhSSFZBeHZKTWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSWtTWklrU1pJa1NaSzBnMFhSSFZDVmxnQ0hBNGR1YVd1QWc0SGRnZDJBNVZ2K3VWTlVCNlVFN2dmdUFtN2I4czg3Z2V1Qkh3RS8zdkxQL3djOEVOVkIxY1VEZ1Bxd0dEZ1NlRGJ3TE9BRndMTFFIa25EZERmd2RlQnJ3SlhBRlhnZ1VDSWVBSlRTRWNCcmdkT0J4d1QzUmNyUmJjQW5nSCtrT1JCSW5mRUFvSzR0QTk0SW5FWnptMTlTTjM0SVhBUjhFTGdqdUM4cWdBY0FkZVhSd0RuQXVUVGY0VXRLNDA2YWc4Qi9BRzRKN291a2l1MEJ2QXZZQkV6YmJMYmUycDAwaDREZGthU2V2UlJZVDN3UTJtdzF0dzNBS1Vnajhpc0FqZVB4d0FlQVA0enVpS1NIZlE0NEc3ZzV1Qi9LaEFjQWplb0VtdThmL1o1ZkdwNDdnRE9CajBkM1JNTTNGZDBCWldObjRBTGdrM2p4bDRacVQrQy8wL3hTd0VKYW1wZDNBTlRHWTRCTGdHZEVkMFJTYTFmUlBLZnoyK2lPYUpnOEFHZ2hxNERQQTRkRmQwVFN5RzZnZVZibmh1aU9hSGo4Q2tEek9ZS20rcGdYZnlsUEJ3RmZCWjRTM1JFTmozY0FOSmNuMGRRaDkvdCtLWDhiZ1dPQWE2TTdvdUh3QUtEWkhFRHpNcElEb2pzaXFUTy9vSGtaMTgzQi9kQkErQldBdHZkbzRISzgrRXVsMlkvbXovWmpvenVpWWZBQW9LM3RESHdHdi9PWFNuVXd6VTk1L1ltZ1dCemRBUTNLM3dIL0tyb1RrcEk2Z09iOUFaK1A3b2hpK1F5QVpyd1UrQlR1Q2FrRzA4Q0pOSGNEVkNuRFh0RFU5cjhHMkN1Nkk1SjZjeHR3Rk0wTHZWUWhud0VRd0h2eDRpL1ZaamxOeVdCVnlnT0FYZ2tjSDkwSlNTSCtFSi83cVpaZkFkUnREK0NId09PaU95SXB6TStBSndDYm9qdWlmdmtyZ0xyOU8rQkYwWjJRRkdvWnpVT0JYNHJ1aVBybEhZQjY3VU5URVd6MzRINUlpbmNYc0JyZkhGZ1Zud0dvMTUvaXhWOVNZemZnbk9oT3FGL2VBYWpUbmpRLy9mSEpmMGt6YnFkNS9mZnQwUjFSUDd3RFVLZXo4T0l2YVZ2TGdET2pPNkgrZUFlZ1RqOEUxa1IzUXRMZ1hBY2NFZDBKOWNNN0FQVjVCbDc4SmMzdUNjQlRvenVoZm5nQXFNOXJvenNnYWRETWlFcjRGVUJkRmdPL0JGWkVkMFRTWVAwSzJBL1lITjBScGVVZGdMbzhEUy8ra3ViM1dPREk2RTRvUFE4QWRUa3V1Z09Tc21CV1ZNQURRRjJlRjkwQlNWa3dLeXJnTXdEMTJBbllTRlB4UzVMbXN3bllHM2dndWlOS3h6c0E5VGdNTC82UzJ0a2RPQ1M2RTByTEEwQTlEb3Z1Z0tTc21CbUY4d0JRRC84d1N4cUZtVkU0RHdEMThBK3pwRkdZR1lYekFGQ1BBNk03SUNrckIwVjNRR2w1QUtqSHN1Z09TTXFLbVZFNER3RDEyQ082QTVLeVltWVV6Z05BUGZ6RExHa1Vaa2JoUEFEVVkvZm9Ea2pLaWdlQXdsa0pzQjdUMFIyUWxCMnZFUVh6RG9Ba1NSWHlBQ0JKVW9VOEFFaVNWQ0VQQUpJa1ZjZ0RnQ1JKRmZJQUlFbFNoVHdBU0pKVUlROEFraVJWeUFPQUpFa1Y4Z0FnU1ZLRlBBQklrbFFoRHdDU0pGWElBNEFrU1JYeUFDQkpVb1grUDl4cTR3ODlFdDFFQUFBQUFFbEZUa1N1UW1DQyIvPgo8L2RlZnM+CjxnIGlkPSJzdXJmYWNlMiI+Cjx1c2UgeGxpbms6aHJlZj0iI2ltYWdlNSIgdHJhbnNmb3JtPSJtYXRyaXgoMC4wNzgwNzQsMCwwLDAuMDc2MzIwOSwwLjAxMzA0NjMsMCkiLz4KPC9nPgo8L3N2Zz4K"}
        }
        
        var environmental = document.createElement("div")
        environmental.classList = "custom_compare_attribute_wrapper"
        compare_popup.appendChild(environmental)

        for(var [attribute_key, attribute] of Object.entries(attributes)) {
            var attribute_div = document.createElement("div")
            attribute_div.classList = "custom_compare_attribute"
            environmental.appendChild(attribute_div)

            for(var shoe_info of [first_shoe_info, "middle_section", second_shoe_info]) {
                if(shoe_info == "middle_section") {
                    //construct middle section
                    var middle_section = document.createElement("div")
                    middle_section.classList = "custom_compare_attribute_middle_section"
                    attribute_div.appendChild(middle_section)

                    var icon = document.createElement("img")
                    icon.src = attribute.image
                    middle_section.appendChild(icon)

                    var title = document.createElement("h3")
                    title.innerHTML = attribute.title
                    middle_section.appendChild(title)

                    var arrow = document.createElement("div")
                    arrow.classList = "custom_compare_attribute_middle_section_arrow custom_shoe_expander compare_attribute_middle_section_arrow"
                    middle_section.appendChild(arrow)

                    middle_section.onclick = function() {
                        //turn all the arrows off
                        var all_arrows = document.querySelectorAll(".compare_attribute_middle_section_arrow")
                        for(var i = 0; i < all_arrows.length; i++) {
                            if(all_arrows[i] != this.arrow)
                                all_arrows[i].classList.remove("custom_shoe_expander_active")
                        }
                        this.arrow.classList.toggle("custom_shoe_expander_active")

                        var attribute_description = document.getElementById("compare_attribute_description")
                        if(attribute_description) attribute_description.remove()

                        attribute_description = document.createElement("div")
                        attribute_description.id = "compare_attribute_description"
                        attribute_description.classList = "custom_compare_attribute_description"
                        attribute_description.innerHTML = this.attribute_div.dataset.text
                        this.attribute_div.parentElement.insertBefore(attribute_description, this.attribute_div.nextSibling)


                    }.bind({attribute_div: attribute_div, middle_section: middle_section, arrow: arrow})
                }
                else {
                    var environmental_impact = shoe_info.extra_info.environmental_impact[attribute.title]
                    if(environmental_impact != null) {
                        //construct the balls
                        if(attribute_div.dataset.text == null)
                            attribute_div.dataset.text = ""
                        if(environmental_impact.text != null) {
                            attribute_div.dataset.text += `<h4>${shoe_info.name}</h4>`
                            attribute_div.dataset.text += `<p>${environmental_impact.text}</p>`
                        }
                        var ball_wrapper = document.createElement("div")
                        ball_wrapper.classList = "custom_scoring_balls custom_compare_scoring_balls"
                        attribute_div.appendChild(ball_wrapper)
                        var ball_inner = document.createElement("div")
                        ball_wrapper.appendChild(ball_inner)
                        if(environmental_impact.rating != null) {
                            var ball_count = parseInt(environmental_impact.rating)
                            if(shoe_info == second_shoe_info)
                                ball_wrapper.style.textAlign = "right"
                            //decide color
                            var color_base = "custom_scoring_balls_"
                            if(ball_count < 3) {
                                ball_inner.classList = color_base + "red"
                            }
                            else if(ball_count == 3) {
                                ball_inner.classList = color_base + "orange"
                            }
                            else {
                                ball_inner.classList = color_base + "green"
                            }
                            for(var i = 0; i < ball_count; i++) {
                                var ball = document.createElement("div")
                                ball_inner.appendChild(ball)
                            }
                        }
                    }
                }
            }


        }
    }

    request_shoe_info(first_id).then(function(first_shoe_info) {
        if(!closed) {
            request_shoe_info(second_id).then(function(second_shoe_info) {
                if(!closed) {
                    construct_compare(first_shoe_info, second_shoe_info)
                }
            })
        }
    })
}

function check_if_open_compare() {
    var all_check_boxes = document.querySelectorAll(".compare_checkbox")
    //find how many are checked and get the checked checkboxes
    var checked_check_boxes = []
    for(var i = 0; i < all_check_boxes.length; i++) {
        if(all_check_boxes[i].checked) {
            checked_check_boxes.push(all_check_boxes[i])
        }
    }
    if(checked_check_boxes.length >= 2) {
        open_compare(checked_check_boxes[0], checked_check_boxes[1])
        for(var i = 0; i < checked_check_boxes.length; i++) {
            all_check_boxes[i].checked = false
        }
    }
}

function toggle_compare() {
    var compare_info = document.getElementById("compare_info")
    compare_info.classList.toggle("custom_compare_info_visible")
    var on = compare_info.classList.contains("custom_compare_info_visible")


    var shoe_wrappers = document.querySelectorAll(".shoe_wrapper")
    for(var i = 0; i < shoe_wrappers.length; i++) {
        
        if(on) {
            var compare_shoe_button = document.createElement("div")
            compare_shoe_button.classList = "custom_compare_shoe_button compare_shoe_button"
            
            var toggle_input = document.createElement("input")
            toggle_input.classList = "compare_shoe_button_input"
            toggle_input.classList = "compare_checkbox"
            toggle_input.dataset.id = shoe_wrappers[i].dataset.id
            toggle_input.type = "checkbox"
            toggle_input.addEventListener("input", function() {
                check_if_open_compare()
            })
            compare_shoe_button.appendChild(toggle_input)

            var compare_shoe_button_label = document.createElement("label")
            compare_shoe_button_label.innerHTML = "Compare"
            compare_shoe_button.appendChild(compare_shoe_button_label)

            shoe_wrappers[i].appendChild(compare_shoe_button)

            compare_shoe_button.onclick = function(event) {
                var input_checked = event.target == this.toggle_input
                if(input_checked) return true
                else {
                    this.toggle_input.checked = !this.toggle_input.checked
                    check_if_open_compare()
                    return false
                }
            }.bind({toggle_input: toggle_input})
        }
        else {
            var compare_shoe_button = shoe_wrappers[i].querySelector(".compare_shoe_button")
            if(compare_shoe_button) {
                compare_shoe_button.remove()
            }
        }
    }
}

//returns array of dicts
function get_items_in_cart(all_products, cart) {
    var result = []
    for(var cart_item of cart) {
        var product_info = null
        var variant_info = null
        var found = false
        for(var product of all_products.products) {
            if(found) break
            var variants = product.variants
            for(var variant of variants) {
                if(variant.id == cart_item.variant_id) {
                    product_info = product
                    variant_info = variant
                    found = true
                    break
                }
            }
        }
        if(!found) {
            console.log("Could not find product for cart item: " + cart_item.variant_id)
        }
        else {
            result.push({
                product_info: product_info,
                variant_info: variant_info,
                quantity: cart_item.quantity
            })
        }
    }
    return result
}

var all_products_store = null
function open_shopping_cart(shopping_cart) {
    shopping_cart.innerHTML = ""

    //add loading
    var add_loading = function() {
        var loading = document.createElement("div")
        var animation_delay = 100
        loading.classList = "div_loading custom_shopping_cart_loading"
        for(var i = 0; i < 3; i++) {
            var ball = document.createElement("div")
            ball.style.animationDelay = i * animation_delay + "ms"
            loading.appendChild(ball)
        }
        shopping_cart.appendChild(loading)
        return loading
    }
    var loading = add_loading()

    var sending_update = false
    var construct_shopping_cart = function() {
        //remove the loading animation
        loading.remove()
        var encoded_cart = JSON.parse(cart.replaceAll("'", "\""))
        var items_in_cart = get_items_in_cart(all_products_store, encoded_cart)

        //create header
        var header = document.createElement("span")
        header.classList = "custom_shopping_cart_header"
        header.innerHTML = "Shopping cart"
        shopping_cart.appendChild(header)

        var cart_close = document.createElement("div")
        cart_close.classList = "custom_compare_close"
        cart_close.innerHTML = "x"
        cart_close.onclick = function() {
            toggle_shopping_cart()
        }
        shopping_cart.appendChild(cart_close)

        //loop over all items in cart and insert them
        var entries = document.createElement("div")
        entries.classList = "custom_shopping_cart_entry_wrapper"
        shopping_cart.appendChild(entries)

        cart_total_amount = 0
        for(var item_info of items_in_cart) {
            var entry = document.createElement("div")
            entry.classList = "custom_shopping_cart_entry"
            entries.appendChild(entry)

            var image_wrapper = document.createElement("a")
            image_wrapper.href = `/${item_info.product_info.id}/`
            entry.appendChild(image_wrapper)

            var image = document.createElement("img")
            image.src = item_info.product_info.thumbnail
            image_wrapper.appendChild(image)

            var text_block = document.createElement("div")
            text_block.classList = "custom_shopping_cart_text_block"
            entry.appendChild(text_block)

            var title = document.createElement("span")
            title.innerHTML = item_info.product_info.name
            text_block.appendChild(title)

            var bottom_text_wrapper = document.createElement("div")
            bottom_text_wrapper.classList = "custom_shopping_cart_bottom_text_wrapper"
            text_block.appendChild(bottom_text_wrapper)

            var description = document.createElement("span")
            description.innerHTML = item_info.variant_info.title
            bottom_text_wrapper.appendChild(description)

            var quantity_wrapper = document.createElement("div")
            quantity_wrapper.classList = "custom_shopping_cart_quantity_wrapper"
            bottom_text_wrapper.appendChild(quantity_wrapper)

            var quantity_text = document.createElement("span")
            quantity_text.innerHTML = "qty: "
            quantity_wrapper.appendChild(quantity_text)

            var quantity = document.createElement("input")
            quantity.classList = "custom_shopping_cart_text_bottom_quantity shopping_cart_text_bottom_quantity"
            quantity.type = "number"
            quantity.max = "9"
            quantity.min = "0"
            quantity.value = item_info.quantity
            quantity_wrapper.appendChild(quantity)

            quantity.oninput = function() {
                if(parseInt(this.value) > parseInt(this.max)) {
                    this.value = this.max
                }
                else if(parseInt(this.value) < parseInt(this.min)) {
                    this.value = this.min
                }
            }.bind(quantity)

            var remove_button = document.createElement("div")
            remove_button.classList = "custom_shopping_cart_remove_button"
            remove_button.innerHTML = "x"
            entry.appendChild(remove_button)

            cart_total_amount += item_info.quantity * item_info.variant_info.price

            var send_update = function() {
                if(!sending_update) {
                    sending_update = true
                    add_loading()
                    var all_inputs = document.querySelectorAll(".shopping_cart_text_bottom_quantity")
                    for(var input of all_inputs) {
                        input.disabled = true
                    }

                    var cart_update_data = {
                        quantity: parseInt(this.quantity.value),
                        variant_id: parseInt(this.item_info.variant_info.id)
                    }

                    fetch(cart_update_url, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": csrf
                        },
                        body: JSON.stringify(cart_update_data)
                    }).then(function(response) {
                        location.reload()
                    })
                }
            }.bind({quantity: quantity, item_info: item_info})

            quantity.oninput = send_update
            remove_button.onclick = function() {
                this.value = 0
                send_update()
            }.bind(quantity)
        }
        if(items_in_cart.length == 0) {
            var empty_text = document.createElement("span")
            empty_text.classList = "custom_shopping_cart_empty_text"
            empty_text.innerHTML = "Your cart is empty"
            shopping_cart.appendChild(empty_text)
        }

        var bottom_wrapper = document.createElement("div")
        bottom_wrapper.classList = "custom_shopping_cart_bottom_wrapper"
        shopping_cart.appendChild(bottom_wrapper)

        var total_amount = document.createElement("span")
        total_amount.classList = "custom_shopping_cart_total_amount"
        total_amount.innerHTML = `Total: <b>&#163;${parseFloat(cart_total_amount).toFixed(2)}</b>`
        bottom_wrapper.appendChild(total_amount)

        //add checkout button
        if(items_in_cart.length != 0) {
            var checkout_button = document.createElement("button")
            checkout_button.classList = "button_primary custom_shopping_cart_checkout_button"
            checkout_button.innerHTML = "Checkout"
            checkout_button.onclick = function() {
                open_popup_window(checkout_url)
            }
            bottom_wrapper.appendChild(checkout_button)
        }
    }


    if(all_products_store == null) {
        //request all products from the server
        var url = local_api_url.replace("$request_type$", "all_products").replace("/$argument$", "")
        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrf
            }
        }).then(function(response) {
            response.json().then(function(data) {
                all_products_store = data
                construct_shopping_cart()
            })
        })
    }
    else {
        construct_shopping_cart()
    }

}

function toggle_shopping_cart() {
    var shopping_cart = document.getElementById("shopping_cart")
    if(shopping_cart.style.display == "flex") {
        shopping_cart.animate({transform: ["", "translateX(100%)"]}, {duration: 300, easing: "ease-out"}).onfinish = function() {
            shopping_cart.style.display = "none"
            shopping_cart.innerHTML = ""
            set_cookie("shopping_cart_open", "false", 1)
        }
    }
    else {
        shopping_cart.style.display = "flex"
        shopping_cart.animate({transform: ["translateX(100%)", "translateX(0px)"]}, {duration: 300, easing: "ease-out"})

        open_shopping_cart(shopping_cart)
        set_cookie("shopping_cart_open", "true", 1)
    }
}

window.onload = function() {
    if(get_cookie("shopping_cart_open") == "true") {
        var shopping_cart = document.getElementById("shopping_cart")
        shopping_cart.style.display = "flex"
        open_shopping_cart(shopping_cart)
    }
}

//returns array of dicts
function get_items_in_cart(all_products, cart) {
    var result = []
    for(var cart_item of cart) {
        var product_info = null
        var variant_info = null
        var found = false
        for(var product of all_products.products) {
            if(found) break
            var variants = product.variants
            for(var variant of variants) {
                if(variant.id == cart_item.variant_id) {
                    product_info = product
                    variant_info = variant
                    found = true
                    break
                }
            }
        }
        if(!found) {
            console.log("Could not find product for cart item: " + cart_item.variant_id)
        }
        else {
            result.push({
                product_info: product_info,
                variant_info: variant_info,
                quantity: cart_item.quantity
            })
        }
    }
    return result
}

var all_products_store = null
function open_shopping_cart(shopping_cart) {
    shopping_cart.innerHTML = ""

    //add loading
    var loading = document.createElement("div")
    var animation_delay = 100
    loading.classList = "div_loading custom_shopping_cart_loading"
    for(var i = 0; i < 3; i++) {
        var ball = document.createElement("div")
        ball.style.animationDelay = i * animation_delay + "ms"
        loading.appendChild(ball)
    }
    shopping_cart.appendChild(loading)


    var construct_shopping_cart = function() {
        //remove the loading animation
        loading.remove()
        var encoded_cart = JSON.parse(cart.replaceAll("'", "\""))
        var items_in_cart = get_items_in_cart(all_products_store, encoded_cart)
        console.log(items_in_cart)
    }


    if(all_products_store == null) {
        //request all products from the server
        var url = local_api_url.replace("$request_type$", "all_products").replace("/$argument$", "")
        fetch(url, {
            method: "POST",
            headers: {
                'X-CSRFToken': csrf
            }
        }).then(function(response) {
            response.json().then(function(data) {
                all_products_store = data
                construct_shopping_cart()
            })
        })
    }
    else {
        construct_shopping_cart()
    }

}

function toggle_shopping_cart() {
    var shopping_cart = document.getElementById("shopping_cart")
    if(shopping_cart.style.display == "flex") {
        shopping_cart.animate({transform: ["", "translateX(100%)"]}, {duration: 300, easing: "ease-out"}).onfinish = function() {
            shopping_cart.style.display = "none"
            shopping_cart.innerHTML = ""
        }
    }
    else {
        shopping_cart.style.display = "flex"
        shopping_cart.animate({transform: ["translateX(100%)", "translateX(0px)"]}, {duration: 300, easing: "ease-out"})

        open_shopping_cart(shopping_cart)
    }
}