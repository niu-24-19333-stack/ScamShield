/**
 * ScamShield Pro - Mobile Navigation & Interactions
 * Handles responsive navigation, gestures, and mobile-specific features
 */

(function() {
  'use strict';
  
  // ========================================
  // MOBILE NAVIGATION
  // ========================================
  
  function initMobileNavigation() {
    const nav = document.querySelector('.nav');
    if (!nav) return;
    
    // Create mobile menu toggle button
    const mobileToggle = document.createElement('button');
    mobileToggle.className = 'mobile-menu-toggle';
    mobileToggle.setAttribute('aria-label', 'Toggle mobile menu');
    mobileToggle.innerHTML = `
      <div class="hamburger-icon">
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
        <span class="hamburger-line"></span>
      </div>
    `;
    
    // Create backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'mobile-menu-backdrop';
    
    // Insert elements
    const navButtons = nav.querySelector('.nav-buttons');
    if (navButtons) {
      navButtons.before(mobileToggle);
    } else {
      nav.appendChild(mobileToggle);
    }
    document.body.appendChild(backdrop);
    
    // Get nav links
    const navLinks = nav.querySelector('.nav-links');
    
    // Toggle menu
    function toggleMenu() {
      const isActive = navLinks.classList.contains('active');
      
      if (isActive) {
        closeMenu();
      } else {
        openMenu();
      }
    }
    
    function openMenu() {
      navLinks.classList.add('active');
      backdrop.classList.add('active');
      mobileToggle.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
    
    function closeMenu() {
      navLinks.classList.remove('active');
      backdrop.classList.remove('active');
      mobileToggle.classList.remove('active');
      document.body.style.overflow = '';
    }
    
    // Event listeners
    mobileToggle.addEventListener('click', toggleMenu);
    backdrop.addEventListener('click', closeMenu);
    
    // Close on link click
    if (navLinks) {
      navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeMenu);
      });
    }
    
    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeMenu();
    });
    
    // Close on window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (window.innerWidth > 1024) {
          closeMenu();
        }
      }, 250);
    });
  }
  
  // ========================================
  // DASHBOARD MOBILE SIDEBAR
  // ========================================
  
  function initDashboardMobileSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const protectionBar = document.querySelector('.protection-bar');
    
    if (!sidebar || !protectionBar) return;
    
    // Create mobile sidebar toggle
    const sidebarToggle = document.createElement('button');
    sidebarToggle.className = 'mobile-sidebar-toggle';
    sidebarToggle.setAttribute('aria-label', 'Toggle sidebar');
    sidebarToggle.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="24" height="24">
        <line x1="3" y1="12" x2="21" y2="12"/>
        <line x1="3" y1="6" x2="21" y2="6"/>
        <line x1="3" y1="18" x2="21" y2="18"/>
      </svg>
    `;
    
    // Insert toggle button
    protectionBar.insertBefore(sidebarToggle, protectionBar.firstChild);
    
    // Create backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'mobile-menu-backdrop';
    document.body.appendChild(backdrop);
    
    // Toggle sidebar
    function toggleSidebar() {
      const isActive = sidebar.classList.contains('active');
      
      if (isActive) {
        closeSidebar();
      } else {
        openSidebar();
      }
    }
    
    function openSidebar() {
      sidebar.classList.add('active');
      backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
    
    function closeSidebar() {
      sidebar.classList.remove('active');
      backdrop.classList.remove('active');
      document.body.style.overflow = '';
    }
    
    // Event listeners
    sidebarToggle.addEventListener('click', toggleSidebar);
    backdrop.addEventListener('click', closeSidebar);
    
    // Close on link click
    sidebar.querySelectorAll('.sidebar-link').forEach(link => {
      link.addEventListener('click', closeSidebar);
    });
    
    // Close on escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSidebar();
    });
    
    // Close on resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (window.innerWidth > 1024) {
          closeSidebar();
        }
      }, 250);
    });
  }
  
  // ========================================
  // TOUCH GESTURES
  // ========================================
  
  function initTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;
    
    // Swipe detection
    function handleTouchStart(e) {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }
    
    function handleTouchEnd(e) {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;
      handleSwipe();
    }
    
    function handleSwipe() {
      const diffX = touchEndX - touchStartX;
      const diffY = touchEndY - touchStartY;
      const threshold = 50;
      
      // Horizontal swipe
      if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > threshold) {
        if (diffX > 0) {
          // Swipe right - open sidebar/menu
          const sidebar = document.querySelector('.sidebar');
          if (sidebar && touchStartX < 50) {
            sidebar.classList.add('active');
            document.querySelector('.mobile-menu-backdrop')?.classList.add('active');
          }
        } else {
          // Swipe left - close sidebar/menu
          const sidebar = document.querySelector('.sidebar');
          const navLinks = document.querySelector('.nav-links');
          
          if (sidebar?.classList.contains('active')) {
            sidebar.classList.remove('active');
            document.querySelector('.mobile-menu-backdrop')?.classList.remove('active');
          }
          
          if (navLinks?.classList.contains('active')) {
            navLinks.classList.remove('active');
            document.querySelector('.mobile-menu-backdrop')?.classList.remove('active');
            document.querySelector('.mobile-menu-toggle')?.classList.remove('active');
          }
        }
      }
    }
    
    // Add touch listeners
    document.addEventListener('touchstart', handleTouchStart, { passive: true });
    document.addEventListener('touchend', handleTouchEnd, { passive: true });
  }
  
  // ========================================
  // SCROLL ENHANCEMENTS
  // ========================================
  
  function initScrollEnhancements() {
    let lastScrollY = window.scrollY;
    const protectionBar = document.querySelector('.protection-bar');
    const nav = document.querySelector('.nav');
    
    // Hide/show navigation on scroll (mobile only)
    function handleScroll() {
      if (window.innerWidth > 768) return;
      
      const currentScrollY = window.scrollY;
      
      if (currentScrollY > lastScrollY && currentScrollY > 100) {
        // Scrolling down
        nav?.classList.add('nav-hidden');
        protectionBar?.classList.add('nav-hidden');
      } else {
        // Scrolling up
        nav?.classList.remove('nav-hidden');
        protectionBar?.classList.remove('nav-hidden');
      }
      
      lastScrollY = currentScrollY;
    }
    
    let scrollTimer;
    window.addEventListener('scroll', () => {
      clearTimeout(scrollTimer);
      scrollTimer = setTimeout(handleScroll, 10);
    }, { passive: true });
  }
  
  // ========================================
  // ORIENTATION CHANGE
  // ========================================
  
  function handleOrientationChange() {
    // Close all menus on orientation change
    document.querySelectorAll('.nav-links.active, .sidebar.active').forEach(el => {
      el.classList.remove('active');
    });
    
    document.querySelectorAll('.mobile-menu-backdrop.active').forEach(el => {
      el.classList.remove('active');
    });
    
    document.body.style.overflow = '';
  }
  
  // ========================================
  // VIEWPORT HEIGHT FIX (Mobile browsers)
  // ========================================
  
  function setVHProperty() {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  }
  
  // ========================================
  // PREVENT ZOOM ON INPUT FOCUS (iOS)
  // ========================================
  
  function preventIOSZoom() {
    if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
      const viewport = document.querySelector('meta[name=viewport]');
      if (viewport) {
        const content = viewport.getAttribute('content');
        viewport.setAttribute('content', content + ', maximum-scale=1.0');
      }
    }
  }
  
  // ========================================
  // INITIALIZE
  // ========================================
  
  function init() {
    // Check if mobile
    const isMobile = window.innerWidth <= 1024;
    
    if (isMobile) {
      // Initialize mobile features
      initMobileNavigation();
      initDashboardMobileSidebar();
      initTouchGestures();
      initScrollEnhancements();
      setVHProperty();
      preventIOSZoom();
      
      // Update VH on resize and orientation change
      window.addEventListener('resize', setVHProperty);
      window.addEventListener('orientationchange', () => {
        setVHProperty();
        handleOrientationChange();
      });
    }
    
    // Re-initialize on window resize
    let resizeTimer;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        const nowMobile = window.innerWidth <= 1024;
        if (nowMobile && !isMobile) {
          location.reload(); // Reload to initialize mobile features
        }
      }, 500);
    });
  }
  
  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
})();
