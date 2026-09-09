const menuBtn = document.getElementById("menuBtn");
const nav = document.getElementById("mainNav");

if (menuBtn && nav) {
    menuBtn.addEventListener("click", () => nav.classList.toggle("open"));
}

document.querySelectorAll(".flash").forEach((item) => {
    setTimeout(() => {
        item.style.opacity = "0";
        item.style.transform = "translateY(-5px)";
        item.style.transition = "all .3s ease";
        setTimeout(() => item.remove(), 300);
    }, 4500);
});

const dateInput = document.querySelector('input[name="food_date"]');
if (dateInput && !dateInput.value) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.min = today;
}
