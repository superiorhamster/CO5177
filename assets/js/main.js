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

// Initialize Modern Minimalist Yellowish Wallpaper immediately
(function initWallpaper() {
  const savedWallpaper = localStorage.getItem('wallpaper-style') || 'organic';
  const savedIntensity = localStorage.getItem('wallpaper-intensity') || 'balanced';
  document.documentElement.setAttribute('data-wallpaper', savedWallpaper);
  document.documentElement.setAttribute('data-wallpaper-intensity', savedIntensity);
})();

document.addEventListener('DOMContentLoaded', () => {
  setupThemeToggle();
  setupWallpaperSystem();
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
 * Modern Minimalist Yellowish Wallpaper Engine & Modal Controller
 */
function setupWallpaperSystem() {
  // 1. Inject or find Wallpaper Button in Header
  const themeToggle = document.getElementById('theme-toggle');
  let wallpaperBtn = document.getElementById('wallpaper-toggle');

  if (!wallpaperBtn && themeToggle && themeToggle.parentNode) {
    wallpaperBtn = document.createElement('button');
    wallpaperBtn.id = 'wallpaper-toggle';
    wallpaperBtn.type = 'button';
    wallpaperBtn.setAttribute('aria-label', 'Tùy chỉnh Hình nền');
    wallpaperBtn.setAttribute('title', 'Tùy biến Hình nền (Modern Minimalist Yellowish)');
    wallpaperBtn.className = 'p-2 rounded-lg text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 hover:bg-amber-100/60 dark:hover:bg-amber-950/40 transition-colors flex items-center justify-center';
    wallpaperBtn.innerHTML = `
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
        <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.563-2.512 5.563-5.563C22 6.5 17.5 2 12 2z"/>
      </svg>
    `;
    themeToggle.parentNode.insertBefore(wallpaperBtn, themeToggle);
  }

  // 2. Also inject into mobile drawer if exists
  const themeToggleMobile = document.getElementById('theme-toggle-mobile');
  if (themeToggleMobile && themeToggleMobile.parentNode && !document.getElementById('wallpaper-toggle-mobile')) {
    const mobileBtn = document.createElement('button');
    mobileBtn.id = 'wallpaper-toggle-mobile';
    mobileBtn.type = 'button';
    mobileBtn.className = 'p-2 rounded-lg bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-300 text-xs font-semibold flex items-center space-x-1.5';
    mobileBtn.innerHTML = `
      <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>
      <span>Hình nền</span>
    `;
    themeToggleMobile.parentNode.insertBefore(mobileBtn, themeToggleMobile);
    mobileBtn.addEventListener('click', () => openModal());
  }

  // 3. Create & inject Wallpaper Modal if not already present
  let modalBackdrop = document.getElementById('wallpaper-modal');
  if (!modalBackdrop) {
    modalBackdrop = document.createElement('div');
    modalBackdrop.id = 'wallpaper-modal';
    modalBackdrop.className = 'wallpaper-modal-backdrop';
    modalBackdrop.innerHTML = `
      <div class="wallpaper-modal-card p-6 sm:p-7 flex flex-col gap-5 text-slate-800 dark:text-slate-100">
        <!-- Header -->
        <div class="flex items-start justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 dark:bg-amber-900/60 dark:text-amber-300 flex items-center justify-center font-bold shadow-inner">
              <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.563-2.512 5.563-5.563C22 6.5 17.5 2 12 2z"/></svg>
            </div>
            <div>
              <h3 class="text-base font-bold text-slate-900 dark:text-white">Hình Nền Tối Giản Tông Vàng</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400">Modern Minimalist Yellowish Wallpaper Engine</p>
            </div>
          </div>
          <button id="wallpaper-modal-close" type="button" aria-label="Đóng" class="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors">
            <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Section: Wallpaper Styles -->
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 block mb-2.5">1. Chọn phong cách hình nền</span>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5" id="wallpaper-style-grid">
            
            <button type="button" data-style="organic" class="wallpaper-opt-btn flex flex-col p-2.5 rounded-xl border text-left transition-all">
              <div class="w-full h-14 rounded-lg bg-cover bg-center mb-2 border border-slate-200 dark:border-slate-700 shadow-sm" style="background-image: url('./assets/images/wallpapers/wallpaper-light.jpg')"></div>
              <span class="text-xs font-bold leading-tight">Organic Dunes</span>
              <span class="text-[10px] text-slate-500 dark:text-slate-400">Đường cong tự nhiên</span>
            </button>

            <button type="button" data-style="geometric" class="wallpaper-opt-btn flex flex-col p-2.5 rounded-xl border text-left transition-all">
              <div class="w-full h-14 rounded-lg bg-cover bg-center mb-2 border border-slate-200 dark:border-slate-700 shadow-sm" style="background-image: url('./assets/images/wallpapers/wallpaper-geometric.jpg')"></div>
              <span class="text-xs font-bold leading-tight">Architectural Geo</span>
              <span class="text-[10px] text-slate-500 dark:text-slate-400">Khối phẳng tối giản</span>
            </button>

            <button type="button" data-style="ambient" class="wallpaper-opt-btn flex flex-col p-2.5 rounded-xl border text-left transition-all">
              <div class="w-full h-14 rounded-lg mb-2 border border-slate-200 dark:border-slate-700 shadow-sm" style="background: radial-gradient(circle at 30% 30%, #fef08a 0%, #fde047 50%, #f59e0b 100%)"></div>
              <span class="text-xs font-bold leading-tight">Ambient Glow</span>
              <span class="text-[10px] text-slate-500 dark:text-slate-400">Lưới gradient ánh vàng</span>
            </button>

            <button type="button" data-style="none" class="wallpaper-opt-btn flex flex-col p-2.5 rounded-xl border text-left transition-all">
              <div class="w-full h-14 rounded-lg mb-2 border border-slate-200 dark:border-slate-700 bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-[11px] text-slate-400">Tắt</div>
              <span class="text-xs font-bold leading-tight">Plain Slate</span>
              <span class="text-[10px] text-slate-500 dark:text-slate-400">Đơn sắc truyền thống</span>
            </button>

          </div>
        </div>

        <!-- Section: Intensity -->
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-amber-600 dark:text-amber-400 block mb-2">2. Cường độ hiển thị (Opacity)</span>
          <div class="grid grid-cols-3 gap-2" id="wallpaper-intensity-grid">
            <button type="button" data-intensity="subtle" class="intensity-opt-btn py-2 px-3 rounded-xl text-xs font-semibold border text-center transition-all">
              Dịu nhẹ (18%)
            </button>
            <button type="button" data-intensity="balanced" class="intensity-opt-btn py-2 px-3 rounded-xl text-xs font-semibold border text-center transition-all">
              Tiêu chuẩn (35%)
            </button>
            <button type="button" data-intensity="vivid" class="intensity-opt-btn py-2 px-3 rounded-xl text-xs font-semibold border text-center transition-all">
              Rõ nét (58%)
            </button>
          </div>
        </div>

        <!-- Section: Download HD Wallpapers -->
        <div class="pt-3 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <span class="text-slate-500 dark:text-slate-400 font-medium">Tải wallpaper 16:9 gốc về máy:</span>
          <div class="flex items-center flex-wrap gap-2">
            <a href="./assets/images/wallpapers/wallpaper-light.jpg" target="_blank" download="modern-minimalist-yellow-light.jpg" class="inline-flex items-center px-2.5 py-1 rounded-lg bg-amber-50 dark:bg-amber-950/60 border border-amber-200/80 dark:border-amber-800/80 text-amber-800 dark:text-amber-300 font-semibold hover:bg-amber-100 transition-colors">
              Light Dunes
            </a>
            <a href="./assets/images/wallpapers/wallpaper-geometric.jpg" target="_blank" download="modern-minimalist-yellow-geometric.jpg" class="inline-flex items-center px-2.5 py-1 rounded-lg bg-amber-50 dark:bg-amber-950/60 border border-amber-200/80 dark:border-amber-800/80 text-amber-800 dark:text-amber-300 font-semibold hover:bg-amber-100 transition-colors">
              Geometric
            </a>
            <a href="./assets/images/wallpapers/wallpaper-dark.jpg" target="_blank" download="modern-minimalist-yellow-dark.jpg" class="inline-flex items-center px-2.5 py-1 rounded-lg bg-amber-50 dark:bg-amber-950/60 border border-amber-200/80 dark:border-amber-800/80 text-amber-800 dark:text-amber-300 font-semibold hover:bg-amber-100 transition-colors">
              Dark Wave
            </a>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modalBackdrop);
  }

  // Helper functions for modal state and selection
  function openModal() {
    modalBackdrop.classList.add('active');
    document.body.classList.add('overflow-hidden');
    refreshUIState();
  }

  function closeModal() {
    modalBackdrop.classList.remove('active');
    document.body.classList.remove('overflow-hidden');
  }

  function setWallpaper(style) {
    document.documentElement.setAttribute('data-wallpaper', style);
    localStorage.setItem('wallpaper-style', style);
    refreshUIState();
    window.dispatchEvent(new CustomEvent('wallpaperChanged', { detail: { style } }));
  }

  function setIntensity(intensity) {
    document.documentElement.setAttribute('data-wallpaper-intensity', intensity);
    localStorage.setItem('wallpaper-intensity', intensity);
    refreshUIState();
  }

  function refreshUIState() {
    const curStyle = document.documentElement.getAttribute('data-wallpaper') || 'organic';
    const curIntensity = document.documentElement.getAttribute('data-wallpaper-intensity') || 'balanced';

    // Update style buttons
    modalBackdrop.querySelectorAll('.wallpaper-opt-btn').forEach(btn => {
      const match = btn.getAttribute('data-style') === curStyle;
      if (match) {
        btn.className = 'wallpaper-opt-btn flex flex-col p-2.5 rounded-xl border border-amber-500 bg-amber-50/80 dark:bg-amber-950/50 dark:border-amber-500 ring-2 ring-amber-500/25 text-left transition-all shadow-sm';
      } else {
        btn.className = 'wallpaper-opt-btn flex flex-col p-2.5 rounded-xl border border-slate-200 dark:border-slate-800 hover:border-amber-300 dark:hover:border-amber-700 bg-white/60 dark:bg-slate-900/60 text-left transition-all';
      }
    });

    // Update intensity buttons
    modalBackdrop.querySelectorAll('.intensity-opt-btn').forEach(btn => {
      const match = btn.getAttribute('data-intensity') === curIntensity;
      if (match) {
        btn.className = 'intensity-opt-btn py-2 px-3 rounded-xl text-xs font-bold border border-amber-500 bg-amber-500 text-white shadow-sm transition-all';
      } else {
        btn.className = 'intensity-opt-btn py-2 px-3 rounded-xl text-xs font-semibold border border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white/60 dark:bg-slate-900/60 text-slate-700 dark:text-slate-300 transition-all';
      }
    });

    // Also update any inline showcase buttons on the page
    document.querySelectorAll('[data-action="apply-wallpaper"]').forEach(btn => {
      const style = btn.getAttribute('data-target-style');
      if (style === curStyle) {
        btn.innerHTML = '<svg class="w-4 h-4 mr-1.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg><span>Đang áp dụng</span>';
        btn.className = 'w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl text-xs font-bold bg-amber-500 text-white shadow-sm transition-all';
      } else {
        btn.innerHTML = '<span>Áp dụng hình nền</span>';
        btn.className = 'w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl text-xs font-semibold bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 hover:border-amber-400 hover:text-amber-600 dark:hover:text-amber-400 shadow-sm transition-all';
      }
    });
  }

  // Event Listeners
  if (wallpaperBtn) wallpaperBtn.addEventListener('click', openModal);

  const closeBtn = document.getElementById('wallpaper-modal-close');
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('active')) {
      closeModal();
    }
  });

  // Style buttons click
  modalBackdrop.querySelectorAll('.wallpaper-opt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const style = btn.getAttribute('data-style');
      if (style) setWallpaper(style);
    });
  });

  // Intensity buttons click
  modalBackdrop.querySelectorAll('.intensity-opt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const intensity = btn.getAttribute('data-intensity');
      if (intensity) setIntensity(intensity);
    });
  });

  // Page inline showcase triggers (e.g. on index.html)
  document.querySelectorAll('[data-action="apply-wallpaper"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const style = btn.getAttribute('data-target-style');
      if (style) {
        setWallpaper(style);
      }
    });
  });

  refreshUIState();
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
