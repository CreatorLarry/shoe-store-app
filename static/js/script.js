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
