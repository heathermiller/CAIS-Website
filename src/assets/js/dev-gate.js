/**
 * CAIS Development Password Gate
 * 
 * TO REMOVE AT LAUNCH:
 * Delete the <script src="...dev-gate.js"></script> line from each HTML file:
 *   - index.html
 *   - pages/cfp.html
 *   - pages/accessibility.html
 *   - pages/codeofconduct.html
 *   - pages/inclusion.html
 *   - pages/recording-media.html
 * 
 * Then delete this file.
 */

(function() {
    'use strict';
    
    const DEV_PASSWORD = 'ratatoskr';
    const SESSION_KEY = 'cais_dev_access';
    
    // Check if already authenticated this session
    if (sessionStorage.getItem(SESSION_KEY) === 'granted') {
        return; // Already authenticated, show page normally
    }
    
    // Hide page content immediately
    document.documentElement.style.visibility = 'hidden';
    document.documentElement.style.overflow = 'hidden';
    
    // Create and inject the gate overlay when DOM is ready
    function createGate() {
        const overlay = document.createElement('div');
        overlay.id = 'dev-gate-overlay';
        overlay.innerHTML = `
            <style>
                #dev-gate-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 999999;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }
                #dev-gate-box {
                    background: rgba(255, 255, 255, 0.95);
                    padding: 3rem;
                    border-radius: 12px;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
                    text-align: center;
                    max-width: 400px;
                    width: 90%;
                }
                #dev-gate-box h2 {
                    margin: 0 0 0.5rem 0;
                    color: #1a1a2e;
                    font-size: 1.5rem;
                    font-weight: 600;
                }
                #dev-gate-box p {
                    margin: 0 0 1.5rem 0;
                    color: #666;
                    font-size: 0.95rem;
                }
                #dev-gate-input {
                    width: 100%;
                    padding: 0.875rem 1rem;
                    font-size: 1rem;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    margin-bottom: 1rem;
                    box-sizing: border-box;
                    transition: border-color 0.2s;
                }
                #dev-gate-input:focus {
                    outline: none;
                    border-color: #0f3460;
                }
                #dev-gate-input.error {
                    border-color: #e74c3c;
                    animation: shake 0.4s ease-in-out;
                }
                @keyframes shake {
                    0%, 100% { transform: translateX(0); }
                    25% { transform: translateX(-8px); }
                    75% { transform: translateX(8px); }
                }
                #dev-gate-btn {
                    width: 100%;
                    padding: 0.875rem 1rem;
                    font-size: 1rem;
                    font-weight: 600;
                    color: #fff;
                    background: #0f3460;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: background 0.2s;
                }
                #dev-gate-btn:hover {
                    background: #1a1a2e;
                }
                #dev-gate-error {
                    color: #e74c3c;
                    font-size: 0.875rem;
                    margin-top: 0.75rem;
                    min-height: 1.25rem;
                }
            </style>
            <div id="dev-gate-box">
                <h2>Development Preview</h2>
                <p>This site is under development. Please enter the access password to continue.</p>
                <form id="dev-gate-form">
                    <input type="password" id="dev-gate-input" placeholder="Enter password" autocomplete="off" autofocus />
                    <button type="submit" id="dev-gate-btn">Access Site</button>
                </form>
                <div id="dev-gate-error"></div>
            </div>
        `;
        
        document.body.insertBefore(overlay, document.body.firstChild);
        
        // Make overlay visible while keeping page hidden
        overlay.style.visibility = 'visible';
        
        const form = document.getElementById('dev-gate-form');
        const input = document.getElementById('dev-gate-input');
        const errorMsg = document.getElementById('dev-gate-error');
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (input.value === DEV_PASSWORD) {
                sessionStorage.setItem(SESSION_KEY, 'granted');
                overlay.remove();
                document.documentElement.style.visibility = '';
                document.documentElement.style.overflow = '';
            } else {
                input.classList.add('error');
                errorMsg.textContent = 'Incorrect password. Please try again.';
                input.value = '';
                input.focus();
                
                setTimeout(function() {
                    input.classList.remove('error');
                }, 400);
            }
        });
        
        input.focus();
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createGate);
    } else {
        createGate();
    }
})();
