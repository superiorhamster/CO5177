(() => {
  const sidebar = document.querySelector(".dashboard-sidebar");
  const dialog = document.createElement("dialog");
  if (!sidebar || typeof dialog.showModal !== "function") return;

  const desktop = matchMedia("(min-width: 80rem)");
  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "navigation-toggle";
  toggle.textContent = "Mở điều hướng";
  toggle.hidden = true;
  toggle.setAttribute("aria-controls", "navigation-drawer");
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-haspopup", "dialog");

  dialog.id = "navigation-drawer";
  dialog.className = "navigation-dialog";
  dialog.setAttribute("aria-label", "Điều hướng trang");
  const close = document.createElement("button");
  close.type = "button";
  close.className = "navigation-close";
  close.textContent = "Đóng điều hướng";
  close.autofocus = true;
  dialog.append(close);
  sidebar.before(toggle, dialog);
  let printing = false;

  function restoreSidebar() {
    if (dialog.open) dialog.close();
    if (sidebar.parentElement === dialog) dialog.after(sidebar);
    toggle.setAttribute("aria-expanded", "false");
  }

  function syncLayout() {
    if (printing) return;
    const focusInNavigation = sidebar.contains(document.activeElement)
      || dialog.contains(document.activeElement);
    const focusOnToggle = document.activeElement === toggle;
    restoreSidebar();
    sidebar.hidden = !desktop.matches;
    toggle.hidden = desktop.matches;
    if (desktop.matches && (focusInNavigation || focusOnToggle)) {
      sidebar.querySelector('[aria-current="page"]').focus();
    } else if (!desktop.matches && focusInNavigation) {
      toggle.focus();
    }
  }

  function dismiss(returnFocus = true) {
    restoreSidebar();
    sidebar.hidden = !desktop.matches;
    if (returnFocus) toggle.focus();
  }

  toggle.addEventListener("click", () => {
    dialog.append(sidebar);
    sidebar.hidden = false;
    dialog.showModal();
    toggle.setAttribute("aria-expanded", "true");
  });
  close.addEventListener("click", () => dismiss());
  dialog.addEventListener("cancel", (event) => {
    event.preventDefault();
    dismiss();
  });

  function isBackdrop(event) {
    if (event.target !== dialog) return false;
    const bounds = dialog.getBoundingClientRect();
    return event.clientX < bounds.left || event.clientX >= bounds.right
      || event.clientY < bounds.top || event.clientY >= bounds.bottom;
  }

  let pressedBackdrop = false;
  dialog.addEventListener("pointerdown", (event) => {
    pressedBackdrop = isBackdrop(event);
  });
  dialog.addEventListener("click", (event) => {
    if (pressedBackdrop && isBackdrop(event)) dismiss();
    pressedBackdrop = false;
  });

  sidebar.addEventListener("click", (event) => {
    if (!dialog.open || event.defaultPrevented || event.button !== 0
        || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const link = event.target.closest('.report-toc a[href^="#"]');
    if (!link) return;
    const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
    if (!target) return;

    const heading = document.getElementById(target.getAttribute("aria-labelledby"))
      || (target.matches("h1, h2, h3, h4, h5, h6") ? target : target.querySelector("h2, h3"))
      || target;
    dismiss(false);
    // Let the browser commit the fragment and history before focusing the heading.
    requestAnimationFrame(() => {
      if (!heading.hasAttribute("tabindex")) heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    });
  });

  desktop.addEventListener("change", syncLayout);
  addEventListener("beforeprint", () => {
    printing = true;
    restoreSidebar();
    sidebar.hidden = false;
  });
  addEventListener("afterprint", () => {
    printing = false;
    syncLayout();
  });
  syncLayout();
})();
