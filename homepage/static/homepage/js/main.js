/**
 * Клиентский скрипт проекта Invento.
 */
document.addEventListener("DOMContentLoaded", () => {
    const yearElement = document.getElementById("current-year");
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
});
