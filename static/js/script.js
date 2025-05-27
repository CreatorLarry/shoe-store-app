document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarCollapse = document.querySelector(".navbar-collapse");
    const navbar = document.querySelector(".navbar");
    const scrollTopBtn = document.getElementById("scrollTopBtn");
    const priceRange = document.getElementById("priceRange");
    const priceValue = document.getElementById("priceValue");

    // Toggle navbar on link click
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", () => {
            if (navbarCollapse?.classList.contains("show")) {
                navbarToggler?.click();
            }
        });
    });

    // Close navbar when clicking outside
    document.addEventListener("click", function (event) {
        if (!navbarCollapse?.contains(event.target) && !navbarToggler?.contains(event.target)) {
            navbarCollapse?.classList.remove("show");
        }
    });

    // Scroll effects
    window.addEventListener("scroll", function () {
        if (window.scrollY > 50) {
            navbar?.classList.add("navbar-scrolled");
            scrollTopBtn?.classList.add("show");
        } else {
            navbar?.classList.remove("navbar-scrolled");
            scrollTopBtn?.classList.remove("show");
        }
    });

    // Scroll to top
    scrollTopBtn?.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Price range slider update
    priceRange?.addEventListener("input", function () {
        priceValue.textContent = `KSh ${this.value}`;
    });
});

// Thumbnail image swapper
function changeImage(element) {
    const mainImage = document.getElementById('mainImage');
    if (!mainImage || !element) return;
    mainImage.style.opacity = 0.5;
    setTimeout(() => {
        mainImage.src = element.src;
        mainImage.style.opacity = 1;
    }, 200);
}


