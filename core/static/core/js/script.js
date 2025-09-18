document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const toggleBtn = document.querySelector(".btn-toggle");
  const closeBtn = document.querySelector(".btn-close");
  const overlay = document.getElementById("sidebar-overlay");

  // Open sidebar
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.add("open");
      overlay.style.display = "block";
      toggleBtn.style.display = "none";  // hide open button
      if (closeBtn) closeBtn.style.display = "block"; // show close button
    });
  }

  // Close sidebar
  function closeSidebar() {
    sidebar.classList.remove("open");
    overlay.style.display = "none";
    toggleBtn.style.display = "block";  // show open button
    if (closeBtn) closeBtn.style.display = "none"; // hide close button
  }

  if (closeBtn) closeBtn.addEventListener("click", closeSidebar);
  if (overlay) overlay.addEventListener("click", closeSidebar);

  // Dropdown toggle
  const dropdowns = document.querySelectorAll("#sidebar .has-dropdown > a");
  dropdowns.forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      this.parentElement.classList.toggle("open");
    });
  });
});
