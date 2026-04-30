const root=document.documentElement;const saved=localStorage.getItem("theme");if(saved){root.dataset.theme=saved}document.querySelectorAll("[data-theme-toggle]").forEach(btn=>btn.addEventListener("click",()=>{const next=root.dataset.theme==="dark"?"light":"dark";root.dataset.theme=next;localStorage.setItem("theme",next)}));
document.querySelectorAll(".message").forEach(item=>setTimeout(()=>item.remove(),5000));

// Mobile Menu Toggle
const menuToggle = document.querySelector('[data-menu-toggle]');
const menuContent = document.querySelector('[data-menu-content]');
if (menuToggle && menuContent) {
  menuToggle.addEventListener('click', () => {
    menuContent.classList.toggle('active');
    menuToggle.classList.toggle('active');
  });
  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!menuContent.contains(e.target) && !menuToggle.contains(e.target) && menuContent.classList.contains('active')) {
      menuContent.classList.remove('active');
      menuToggle.classList.remove('active');
    }
  });
}

