document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector(".navbar-collapse");

    // Close navbar when a link is clicked
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            if (navbarCollapse.classList.contains("show")) {
                navbarToggler.click(); // Programmatically close the menu
            }
        });
    });

    // Close navbar when clicking outside
    document.addEventListener("click", function (event) {
        if (!navbarCollapse.contains(event.target) && !navbarToggler.contains(event.target)) {
            navbarCollapse.classList.remove("show");
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".navbar");
    const scrollTopBtn = document.getElementById("scrollTopBtn");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar.classList.add("navbar-scrolled");
            scrollTopBtn.classList.add("show");
        } else {
            navbar.classList.remove("navbar-scrolled");
            scrollTopBtn.classList.remove("show");
        }
    });

    // Scroll to top when button is clicked
    scrollTopBtn.addEventListener("click", function () {
        window.scrollTo({top: 0, behavior: "smooth"});
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar.classList.add("navbar-scrolled");
        } else {
            navbar.classList.remove("navbar-scrolled");
        }
    });
});

// Get slider and value display elements
const priceRange = document.getElementById("priceRange");
const priceValue = document.getElementById("priceValue");

// Update price value in real time
priceRange.addEventListener("input", function () {
    priceValue.textContent = `KSh ${this.value}`;
});


function changeImage(element) {
    let mainImage = document.getElementById('mainImage');
    mainImage.style.opacity = 0.5; // Smooth transition effect
    setTimeout(() => {
        mainImage.src = element.src;
        mainImage.style.opacity = 1;
    }, 200);
}

// card js
document.addEventListener("DOMContentLoaded", function () {
    function updateTotalPrice() {
        let total = 0;
        document.querySelectorAll(".cart-item").forEach((cartItem) => {
            let itemPrice = parseFloat(cartItem.querySelector(".price").getAttribute("data-price"));
            let itemQuantity = parseInt(cartItem.querySelector(".quantity-input").value);
            total += itemPrice * itemQuantity;
        });
        document.querySelector(".total-price").textContent = "$" + total.toFixed(2);
    }

    document.querySelectorAll(".cart-item").forEach((item) => {
        const decreaseBtn = item.querySelector(".decrease-btn");
        const increaseBtn = item.querySelector(".increase-btn");
        const quantityInput = item.querySelector(".quantity-input");
        const priceElement = item.querySelector(".price");
        const removeBtn = item.querySelector(".remove-btn");

        let unitPrice = parseFloat(priceElement.getAttribute("data-price"));

        // Increase quantity
        increaseBtn.addEventListener("click", function () {
            let quantity = parseInt(quantityInput.value);
            quantity++;
            quantityInput.value = quantity;
            priceElement.textContent = "$" + (unitPrice * quantity).toFixed(2);
            updateTotalPrice();
        });

        // Decrease quantity (minimum = 1)
        decreaseBtn.addEventListener("click", function () {
            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantity--;
                quantityInput.value = quantity;
                priceElement.textContent = "$" + (unitPrice * quantity).toFixed(2);
                updateTotalPrice();
            }
        });

        // Remove item from cart
        removeBtn.addEventListener("click", function () {
            item.remove();
            updateTotalPrice();
        });
    });

    // Initial total price calculation
    updateTotalPrice();
});

