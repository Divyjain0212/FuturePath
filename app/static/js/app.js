/* FuturePath — shared client helpers. */

const FP = (() => {
  let mode = 'register';

  async function api(path, options = {}) {
    const res = await fetch(path, {
      headers: { 'Content-Type': 'application/json' },
      credentials: 'same-origin',
      ...options,
    });
    let data = null;
    try { data = await res.json(); } catch (e) { /* empty body */ }
    if (!res.ok) throw new Error((data && data.error) || `request failed (${res.status})`);
    return data;
  }

  function toast(msg) {
    const el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._t);
    el._t = setTimeout(() => el.classList.remove('show'), 2600);
  }

  function openAuth(which = 'register') { authTab(which); document.getElementById('authBack').classList.add('open'); }
  function closeAuth() { document.getElementById('authBack').classList.remove('open'); document.getElementById('authErr').textContent = ''; }
  function authTab(which) {
    mode = which;
    const isReg = which === 'register';
    document.getElementById('tabRegister').classList.toggle('active', isReg);
    document.getElementById('tabLogin').classList.toggle('active', !isReg);
    document.getElementById('registerFields').style.display = isReg ? 'block' : 'none';
    document.getElementById('authTitle').textContent = isReg ? 'Create your account' : 'Welcome back';
    document.getElementById('authSub').textContent = isReg
      ? 'Your assessment, results and roadmap are saved to this account.'
      : 'Sign in to continue where you left off.';
    document.getElementById('authGo').textContent = isReg ? 'Create account' : 'Sign in';
    document.getElementById('authErr').textContent = '';
  }

  async function submitAuth() {
    const errEl = document.getElementById('authErr');
    errEl.textContent = '';
    const payload = {
      username: document.getElementById('authUser').value.trim(),
      password: document.getElementById('authPass').value,
    };
    if (mode === 'register') {
      payload.display_name = document.getElementById('regName').value.trim() || payload.username;
      payload.class_level = document.getElementById('regClass').value;
      payload.board = document.getElementById('regBoard').value;
      payload.state = document.getElementById('regState').value.trim();
      payload.city = document.getElementById('regCity').value.trim();
    }
    try {
      await api(mode === 'register' ? '/api/register' : '/api/login',
        { method: 'POST', body: JSON.stringify(payload) });
      toast(mode === 'register' ? 'Account created' : 'Signed in');
      setTimeout(() => { location.href = mode === 'register' ? '/assessment' : '/results'; }, 400);
    } catch (e) {
      errEl.textContent = e.message;
    }
  }

  async function logout() {
    try { await api('/api/logout', { method: 'POST' }); } catch (e) { /* ignore */ }
    location.href = '/';
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && document.getElementById('authBack')?.classList.contains('open')) submitAuth();
    if (e.key === 'Escape') closeAuth();
  });

  // Mobile navigation. On desktop the toggle is hidden and the menu is always
  // visible, so this only ever runs on small screens.
  function toggleNav() {
    const nav = document.getElementById('mainNav');
    const btn = document.getElementById('navToggle');
    if (!nav) return;
    const open = nav.classList.toggle('nav-open');
    if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('nav-locked', open);
  }
  function closeNav() {
    const nav = document.getElementById('mainNav');
    const btn = document.getElementById('navToggle');
    if (nav) nav.classList.remove('nav-open');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-locked');
  }
  // Tapping a link on mobile should close the menu.
  document.addEventListener('click', (e) => {
    if (e.target.closest('#mainNav a') && window.innerWidth <= 940) closeNav();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeNav(); });

  // ------------------------------------------------------------------ theme
  function currentTheme() {
    return document.documentElement.getAttribute('data-theme') || 'light';
  }
  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('fp-theme', theme); } catch (e) { /* ignore */ }
    const meta = document.getElementById('themeColorMeta');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#14171c' : '#fbfaf8');
  }
  function toggleTheme() {
    applyTheme(currentTheme() === 'dark' ? 'light' : 'dark');
  }
  // If the user has never chosen explicitly, follow the operating system when
  // it changes mid-session.
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    let saved = null;
    try { saved = localStorage.getItem('fp-theme'); } catch (err) { /* ignore */ }
    if (!saved) applyTheme(e.matches ? 'dark' : 'light');
  });

  return { api, toast, openAuth, closeAuth, authTab, submitAuth, logout,
           toggleNav, closeNav, toggleTheme, currentTheme, applyTheme };
})();
