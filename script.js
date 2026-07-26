document.getElementById("year").textContent = new Date().getFullYear();

// respect an explicit theme choice if the user has one; otherwise follow the OS
const stored = localStorage.getItem("theme");
if (stored === "dark" || stored === "light") {
  document.documentElement.setAttribute("data-theme", stored);
}
