/* ZAKO Land Partners — site behaviour (no third-party scripts) */
{
  const root = document.documentElement;
  const hdr = document.querySelector('.hdr');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header turns solid once the opening photograph scrolls away
  const solidAt = () => (document.body.classList.contains('over') ? 60 : 0);
  const setSolid = () => hdr && hdr.classList.toggle('solid', window.scrollY > solidAt() || nav?.classList.contains('open'));
  const nav = document.getElementById('nav');
  if (hdr && document.body.classList.contains('over')) {
    setSolid();
    window.addEventListener('scroll', setSolid, { passive: true });
  }

  // Mobile menu
  const menu = document.querySelector('.menu');
  if (menu && nav) {
    const close = () => { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); menu.textContent = 'Menu'; setSolid(); };
    menu.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
      menu.textContent = open ? 'Close' : 'Menu';
      setSolid();
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('open')) { close(); menu.focus(); } });
    window.matchMedia('(min-width: 821px)').addEventListener('change', (m) => { if (m.matches) close(); });
  }

  // Reveal on scroll: each element animates once, the first time it enters the viewport
  const items = document.querySelectorAll('[data-r]');
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('in'));
  } else {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    items.forEach((el) => io.observe(el));
    // Anything already on screen at load (or reached by an anchor link) shows without waiting
    window.addEventListener('load', () => items.forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('in');
    }));
  }

  // Preview notice
  const px = document.querySelector('.preview button');
  if (px) px.addEventListener('click', () => px.parentElement.remove());

  for (const el of document.querySelectorAll('[data-year]')) el.textContent = new Date().getFullYear();

  // Forms post to the form's action (Formspree) only when <html data-forms="live">.
  // In preview nothing is sent and the visitor is told so.
  const live = root.dataset.forms === 'live';
  for (const form of document.querySelectorAll('form[data-zako-form]')) {
    const status = form.querySelector('.status');
    const btn = form.querySelector('button[type=submit]');
    const label = btn.textContent;
    const show = (msg, ok) => {
      status.textContent = msg;
      status.className = 'status show' + (ok ? ' ok' : '');
      status.focus();
    };
    form.addEventListener('input', (e) => { if (e.target.validity?.valid) e.target.removeAttribute('aria-invalid'); });
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      form.querySelectorAll('[aria-invalid]').forEach((el) => el.removeAttribute('aria-invalid'));
      const invalid = [...form.querySelectorAll('input,select,textarea')].filter((el) => !el.checkValidity());
      if (invalid.length) {
        invalid.forEach((el) => el.setAttribute('aria-invalid', 'true'));
        const first = invalid[0];
        const name = first.type === 'checkbox' ? 'the agreement checkbox' : (form.querySelector(`label[for="${first.id}"]`)?.firstChild?.textContent.trim() || 'a required field');
        show(first.type === 'email' && first.value ? 'Please enter a valid email address.' : `Please complete ${name}.`, false);
        first.focus({ preventScroll: false });
        return;
      }
      const group = form.querySelector('[data-require-one]');
      if (group && !group.querySelector('input:checked')) { show('Please choose at least one market.', false); return; }
      if (form.querySelector('.hp input')?.value) return; // spam trap
      if (!live) { show('Preview only: this form is not connected yet, so nothing was sent.', false); return; }
      btn.disabled = true; btn.textContent = 'Sending';
      try {
        const res = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error(String(res.status));
        form.reset();
        show('Thank you. Your message reached us, and we will be in touch.', true);
      } catch (err) {
        show('Something went wrong and your message was not sent. Please try again, or email team@zakoland.com.', false);
      } finally {
        btn.disabled = false; btn.textContent = label;
      }
    });
  }
}
