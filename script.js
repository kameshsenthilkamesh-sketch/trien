let cart = JSON.parse(localStorage.getItem("cart")) || [];


// ADD FOOD TO CART

function addToCart(name, price) {

    let existingItem = cart.find(item => item.name === name);

    if (existingItem) {

        existingItem.quantity++;

    } else {

        cart.push({
            name: name,
            price: price,
            quantity: 1
        });

    }

    localStorage.setItem("cart", JSON.stringify(cart));

    updateCartCount();

    alert(name + " added to cart!");
}


// UPDATE CART COUNT

function updateCartCount() {

    let count = 0;

    cart.forEach(item => {
        count += item.quantity;
    });

    let element = document.getElementById("cartCount");

    if (element) {
        element.innerText = count;
    }
}


// GO TO CART

function goToCart() {

    window.location.href = "/cart.html";

}


// INITIAL UPDATE

updateCartCount();
