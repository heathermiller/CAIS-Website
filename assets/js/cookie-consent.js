/**
 * CAIS 2026 - Cookie Consent Manager
 * GDPR-compliant consent for Google Analytics
 */

(function() {
  'use strict';

  const CONSENT_KEY = 'cais_cookie_consent';
  const CONSENT_VERSION = '1'; // Increment if policy changes significantly

  // Check if user has already consented
  function getConsent() {
    try {
      const stored = localStorage.getItem(CONSENT_KEY);
      if (stored) {
        const data = JSON.parse(stored);
        if (data.version === CONSENT_VERSION) {
          return data.consent;
        }
      }
    } catch (e) {
      // localStorage not available or parse error
    }
    return null;
  }

  // Store consent choice
  function setConsent(consent) {
    try {
      localStorage.setItem(CONSENT_KEY, JSON.stringify({
        consent: consent,
        version: CONSENT_VERSION,
        timestamp: new Date().toISOString()
      }));
    } catch (e) {
      // localStorage not available
    }
  }

  // Update gtag consent state
  function updateGtagConsent(granted) {
    if (typeof gtag === 'function') {
      gtag('consent', 'update', {
        'analytics_storage': granted ? 'granted' : 'denied'
      });
    }
  }

  // Remove the banner
  function removeBanner() {
    const banner = document.getElementById('cookie-consent-banner');
    if (banner) {
      banner.style.opacity = '0';
      banner.style.transform = 'translateY(100%)';
      setTimeout(function() {
        banner.remove();
      }, 300);
    }
  }

  // Handle accept
  function acceptCookies() {
    setConsent(true);
    updateGtagConsent(true);
    removeBanner();
  }

  // Handle decline
  function declineCookies() {
    setConsent(false);
    updateGtagConsent(false);
    removeBanner();
  }

  // Create and show the banner
  function showBanner() {
    // Don't show if already decided
    if (getConsent() !== null) {
      return;
    }

    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Cookie consent');
    banner.innerHTML = `
      <style>
        #cookie-consent-banner {
          position: fixed;
          bottom: 0;
          left: 0;
          right: 0;
          background: #252523;
          color: #FAFAF8;
          padding: 1rem 1.5rem;
          z-index: 99999;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          font-size: 0.9rem;
          box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
          transform: translateY(100%);
          opacity: 0;
          transition: transform 0.3s ease, opacity 0.3s ease;
        }
        #cookie-consent-banner.visible {
          transform: translateY(0);
          opacity: 1;
        }
        #cookie-consent-banner .consent-container {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
        }
        #cookie-consent-banner .consent-text {
          flex: 1;
          min-width: 280px;
          line-height: 1.5;
        }
        #cookie-consent-banner .consent-text a {
          color: #D89380;
          text-decoration: underline;
        }
        #cookie-consent-banner .consent-text a:hover {
          color: #FAFAF8;
        }
        #cookie-consent-banner .consent-buttons {
          display: flex;
          gap: 0.75rem;
          flex-shrink: 0;
        }
        #cookie-consent-banner button {
          padding: 0.5rem 1.25rem;
          border-radius: 4px;
          font-size: 0.85rem;
          font-weight: 600;
          cursor: pointer;
          transition: background-color 0.2s, border-color 0.2s, color 0.2s;
          border: 2px solid transparent;
        }
        #cookie-consent-banner .btn-accept {
          background: #B8593E;
          color: #FAFAF8;
          border-color: #B8593E;
        }
        #cookie-consent-banner .btn-accept:hover {
          background: #C4735A;
          border-color: #C4735A;
        }
        #cookie-consent-banner .btn-decline {
          background: transparent;
          color: #FAFAF8;
          border-color: #C7C6C5;
        }
        #cookie-consent-banner .btn-decline:hover {
          border-color: #FAFAF8;
        }
        @media (max-width: 600px) {
          #cookie-consent-banner {
            padding: 1rem;
          }
          #cookie-consent-banner .consent-buttons {
            width: 100%;
            justify-content: stretch;
          }
          #cookie-consent-banner button {
            flex: 1;
          }
        }
      </style>
      <div class="consent-container">
        <div class="consent-text">
          We use cookies to analyze site traffic and improve your experience. 
          See our <a href="${getPrivacyPolicyPath()}">Privacy Policy</a> for details.
        </div>
        <div class="consent-buttons">
          <button type="button" class="btn-decline" id="cookie-decline">Decline</button>
          <button type="button" class="btn-accept" id="cookie-accept">Accept</button>
        </div>
      </div>
    `;

    document.body.appendChild(banner);

    // Trigger animation
    requestAnimationFrame(function() {
      requestAnimationFrame(function() {
        banner.classList.add('visible');
      });
    });

    // Attach event listeners
    document.getElementById('cookie-accept').addEventListener('click', acceptCookies);
    document.getElementById('cookie-decline').addEventListener('click', declineCookies);
  }

  // Get correct path to privacy policy based on current page location
  function getPrivacyPolicyPath() {
    const path = window.location.pathname;
    if (path.includes('/pages/')) {
      return './privacy.html';
    }
    return './pages/privacy.html';
  }

  // Initialize on DOM ready
  function init() {
    const consent = getConsent();
    
    if (consent === true) {
      // User previously accepted - grant consent
      updateGtagConsent(true);
    } else if (consent === false) {
      // User previously declined - keep denied
      updateGtagConsent(false);
    } else {
      // No decision yet - show banner
      showBanner();
    }
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
