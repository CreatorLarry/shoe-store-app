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
        window.scrollTo({top: 0, behavior: "smooth"});
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


// Auto-dismiss after 4.5 seconds
setTimeout(() => {
    document.querySelectorAll('.flash-message').forEach(el => {
        el.remove();
    });
}, 4500);

// Loader control
function showLoader() {
    const loader = document.getElementById('loader-overlay');
    if (loader) {
        loader.style.display = 'flex';
    }
}

function hideLoader() {
    const loader = document.getElementById('loader-overlay');
    if (loader) {
        loader.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Hide loader on initial load
    hideLoader();

    // Attach loader to all form submissions
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            showLoader();
        });
    });

    // Attach loader to all internal <a> links (except anchor jumps and targets)
    document.querySelectorAll("a[href]:not([href^='#'])").forEach(link => {
        link.addEventListener("click", function (e) {
            const target = link.getAttribute('target');
            const href = link.getAttribute('href');

            // Only show loader if navigating within the same tab
            if (!target || target === "_self") {
                // Prevent loader on external links
                const isExternal = /^https?:\/\//i.test(href) && !href.includes(window.location.hostname);
                if (!isExternal) {
                    showLoader();
                }
            }
        });
    });

    // Reset loader if page is loaded from cache (like back button)
    window.addEventListener("pageshow", function (event) {
        hideLoader();
    });
});


