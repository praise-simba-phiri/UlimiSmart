document.addEventListener('DOMContentLoaded', function() {
  // Initialize Alpine.js components
  document.querySelectorAll('[x-data]').forEach(el => {
    Alpine.initializeComponent(el);
  });

  // Profile picture upload preview
  const profilePicInput = document.getElementById('id_profile_picture');
  if (profilePicInput) {
    profilePicInput.addEventListener('change', function(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
          let preview = document.getElementById('profile-picture-preview');
          const defaultIcon = document.getElementById('profile-picture-default');
          const avatarUpload = document.querySelector('.avatar-upload');
          
          if (!preview) {
            preview = document.createElement('img');
            preview.id = 'profile-picture-preview';
            preview.className = 'avatar-image animate-fade-in';
            preview.src = e.target.result;
            avatarUpload.insertBefore(preview, avatarUpload.firstChild);
            
            if (defaultIcon) {
              defaultIcon.classList.add('animate-fade-in');
              setTimeout(() => {
                defaultIcon.remove();
              }, 300);
            }
          } else {
            preview.classList.add('animate-fade-in');
            preview.src = e.target.result;
          }
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Add floating animation to cards on hover
  const cards = document.querySelectorAll('.glass-card');
  cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.classList.add('animate-float');
    });
    card.addEventListener('mouseleave', () => {
      card.classList.remove('animate-float');
    });
  });

  // Form input animations
  const inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(input => {
    input.addEventListener('focus', () => {
      input.parentElement.classList.add('animate-fade-in');
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Toast notifications
  const messages = document.querySelectorAll('.messages');
  messages.forEach(messageContainer => {
    if (messageContainer.children.length > 0) {
      messageContainer.classList.add('animate-fade-in');
      setTimeout(() => {
        messageContainer.classList.remove('animate-fade-in');
        messageContainer.classList.add('animate-fade-out');
        setTimeout(() => {
          messageContainer.remove();
        }, 300);
      }, 5000);
    }
  });
});

// Alpine.js components
document.addEventListener('alpine:init', () => {
  Alpine.data('dropdown', () => ({
    open: false,
    toggle() {
      this.open = !this.open;
    },
    close() {
      this.open = false;
    }
  }));

  Alpine.data('tabs', () => ({
    activeTab: 0,
    changeTab(index) {
      this.activeTab = index;
    }
  }));
});

// Utility functions
const UlimiSmart = {
  animateElement: (element, animation, duration = 300) => {
    element.classList.add(animation);
    setTimeout(() => {
      element.classList.remove(animation);
    }, duration);
  },

  debounce: (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  loadMore: (container, url) => {
    // Implement infinite scroll or pagination
  }
};