/**
 * Academic Course Showcase - Main JavaScript
 * Handles Theme Toggling (Dark/Light), Mobile Navigation, and Utilities
 */

// Initialize Theme immediately to prevent flash of wrong theme
(function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
})();

document.addEventListener('DOMContentLoaded', () => {
  setupThemeToggle();
  setupMobileMenu();
  setupSmoothScroll();
});

/**
 * Configure Dark / Light mode toggle with localStorage persistence
 */
function setupThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  const toggleBtnMobile = document.getElementById('theme-toggle-mobile');

  function updateIcons(isDark) {
    document.querySelectorAll('.theme-icon-light').forEach(el => {
      el.classList.toggle('hidden', !isDark);
    });
    document.querySelectorAll('.theme-icon-dark').forEach(el => {
      el.classList.toggle('hidden', isDark);
    });
  }

  const isInitiallyDark = document.documentElement.classList.contains('dark');
  updateIcons(isInitiallyDark);

  function toggleTheme() {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateIcons(isDark);
    
    // Dispatch custom event to notify Chart.js instances to update theme colors
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { isDark } }));
  }

  if (toggleBtn) toggleBtn.addEventListener('click', toggleTheme);
  if (toggleBtnMobile) toggleBtnMobile.addEventListener('click', toggleTheme);
}

/**
 * Mobile Navigation Menu Drawer toggle
 */
function setupMobileMenu() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const menuDrawer = document.getElementById('mobile-menu');
  const menuCloseBtn = document.getElementById('mobile-menu-close');
  
  if (!menuBtn || !menuDrawer) return;

  function openMenu() {
    menuDrawer.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  function closeMenu() {
    menuDrawer.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  menuBtn.addEventListener('click', openMenu);
  if (menuCloseBtn) menuCloseBtn.addEventListener('click', closeMenu);

  // Close when clicking outside or clicking any link inside
  menuDrawer.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !menuDrawer.classList.contains('hidden')) {
      closeMenu();
    }
  });
}

/**
 * Smooth scrolling for internal anchor links
 */
function setupSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#' || targetId === '') return;
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
}
