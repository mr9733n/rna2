function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

const toggleButton = document.getElementById('theme-toggle');
toggleButton.addEventListener('click', () => {
    const darkModeOn = document.body.classList.toggle('dark-mode');
    setCookie('darkMode', darkModeOn ? 'on' : 'off', 7); // Сохраняем состояние темы на 7 дней
});
