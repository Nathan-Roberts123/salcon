let subMenu = document.getElementById("subMenu")

function toogleMenu() {
    subMenu.classList.toggle("open-menu")
}

var cart_count = document.getElementById("cart-count")
var box_container = document.getElementById("checkout-product-box-id")

var cookieValue = Cookies.get("items")
var formsInfo = document.getElementsByClassName("form-info")

function addAddress() {

    const address = {}

    for (let i = 0; i < formsInfo.length; i++) {
        address[formsInfo[i].id] = formsInfo[i].value
        console.log(address)
    }

    let seri_address = JSON.stringify(address)
    document.cookie = 'address = ' + seri_address + ";domain=;path=/"

    window.location.href = "/payment/"
}

if (!cookieValue) {
    console.log("creating cart")
    var items = {}
    document.cookie = 'items = ' + JSON.stringify(items)  + ";domain=;path=/"
} 

else {
    var cuu = cookieValue
    var items = JSON.parse(cuu)
    //document.cookie = 'items = ' + JSON.stringify(items)
    //console.log(items)
}


var CartBtn = document.getElementsByClassName("cart-btn")


for (var i = 0; i < CartBtn.length; i++) {

    CartBtn[i].addEventListener('click', function() {
        var product_name = this.dataset.product
        var action = this.dataset.action

        if (user === "AnonymousUser") {
            addToCookies(product_name, action)
    
        } else {
            console.log("you are logged in")
            addToCart(product_name, action)
        }
    })
}


function addToCart(product_name, action_name) {

    fetch("/add-to-cart/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFTOKEN": csrftoken},
        body: JSON.stringify({product: product_name, action: action_name})
    }).then((res)=>res.json())
    .then((data)=>{ location.reload() })

}


function addToCookies(product_name, action) {

    if (action == "create") {
        if (items[product_name] == undefined) {
            items[product_name] = {"quantity":1}
        } else {
            items[product_name]["quantity"] += 1
        }
    } 

    else if (action == "add") {
        console.log("adding")
        items[product_name]["quantity"] += 1
    }

    else if (action == "remove") {
        console.log("removing")
        items[product_name]["quantity"] -= 1

        if (items[product_name]["quantity"] == 0) {
            delete items[product_name]
        }
    }

    const keys = Object.keys(items)

    for (let i = 0; i < keys.length; i++) {
        const key = keys[i]
        if (key === null || key == "undefined" || key == ' ' || key == false || key == '') {
            delete items[key]
        }
    }

    document.cookie = 'items = ' + JSON.stringify(items)  + ";domain=;path=/"

    location.reload()

    /*
    items.unshift(product_name)
    var filtered = items.filter(elm => elm)

    document.cookie = 'items = ' + JSON.stringify(filtered)  + ";domain=;path=/"
    location.reload()
 
    //console.log(Cookies.get("items"))

    //var cookieValue = Cookies.get("list")

    */

    /*
    var cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)total_items\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    console.log(cookieValue)
    document.cookie = "total_items=" + 1
    */

}