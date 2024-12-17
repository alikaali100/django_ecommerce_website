document.addEventListener('DOMContentLoaded', function() {
    fetch('http://localhost:8000/api/products/')
        .then(response => response.json())
        .then(data => {
            const productList = document.querySelector('.grid');

            // تابع برای تبدیل اعداد انگلیسی به فارسی
            function convertToPersian(num) {
                const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
                return num.toString().replace(/\d/g, function(match) {
                    return persianDigits[parseInt(match)];
                });
            }

            data.forEach(product => {
                const productCard = document.createElement('div');
                productCard.className = 'bg-white shadow rounded-lg p-4';
                productCard.innerHTML = `
            <div class="p-4 flex flex-col h-full">
                <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover">
                <div class="p-4 flex-grow">
                    <h2 class="text-xl font-semibold text-gray-800">${product.name}</h2>
                    <p class="text-gray-600">${product.description}</p>
                    <p class="text-lg font-bold text-gray-900 mt-2">${convertToPersian(product.price.toLocaleString())} تومان</p>
                </div>
                <button class="bg-blue-500 text-white px-4 py-2 mt-4 rounded-lg hover:bg-blue-600 text-sm mt-auto">
                    افزودن به سبد خرید
                </button>
            </div>
                `;
                productList.appendChild(productCard);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
});
document.getElementById('mobile-menu-btn').addEventListener('click', function () {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
});
document.addEventListener("DOMContentLoaded", () => {
    const searchIcon = document.getElementById("search-icon");
    const searchBar = document.getElementById("search-bar");

    searchIcon.addEventListener("click", () => {
        searchBar.classList.toggle("hidden");
        searchBar.classList.toggle("flex"); // نمایش به صورت flex
    });
});
