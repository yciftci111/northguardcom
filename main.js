(function () {
  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  var tabs = document.getElementById('tabs');
  if (btn && tabs) {
    btn.addEventListener('click', function () {
      var open = tabs.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Current year in footer
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Contact form: compose an e-mail (static hosting has no server)
  var form = document.getElementById('quote');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = form.elements;
      var msg = form.querySelector('.form-msg');
      if (!f.naam.value.trim() || !f.email.value.trim() || !f.bericht.value.trim()) {
        msg.textContent = 'Vul uw naam, e-mailadres en bericht in.';
        return;
      }
      var subject = 'Aanvraag ' + (f.onderwerp.value || 'Northguard') + ' – ' + f.naam.value.trim();
      var body = [
        'Naam: ' + f.naam.value.trim(),
        'Bedrijf: ' + (f.bedrijf.value.trim() || '-'),
        'E-mail: ' + f.email.value.trim(),
        'Telefoon: ' + (f.telefoon.value.trim() || '-'),
        'Onderwerp: ' + (f.onderwerp.value || '-'),
        '',
        f.bericht.value.trim()
      ].join('\n');
      window.location.href = 'mailto:info@northguardbv.nl?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      msg.textContent = 'Uw e-mailprogramma wordt geopend met uw aanvraag. Opent er niets? Mail dan naar info@northguardbv.nl.';
    });
  }
})();
