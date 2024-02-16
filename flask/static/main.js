document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('theme-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const darkModeOn = !getDarkModeState();
            setDarkModeState(darkModeOn);
        });
    }

    if (getDarkModeState()) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
});

function setDarkModeState(state) {
    localStorage.setItem('darkMode', state ? 'on' : 'off');
    document.body.classList.toggle('dark-mode', state);
}

function getDarkModeState() {
    return localStorage.getItem('darkMode') === 'on';
}