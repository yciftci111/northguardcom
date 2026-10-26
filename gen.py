#!/usr/bin/env python3
"""Generates the static Northguard website (GitHub Pages). Run: python3 build/gen.py"""
import os, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = 'https://www.northguardbv.nl'
TEL, TEL_HREF = '+31 10 313 89 10', '+31103138910'
MOB, MOB_HREF = '+31 6 45 20 50 52', '+31645205052'
MAIL = 'info@northguardbv.nl'
ADDR = ('Hongkongstraat 47', '3047 BR Rotterdam')

DIVS = {
    'services':   dict(name='Services',   entity='Northguard Services B.V.',   kvk='98596403', color='#C8901A', file='services.html',
                       short='Detachering, uitzenden en projectondersteuning'),
    'inspection': dict(name='Inspection', entity='Northguard Inspection B.V.', kvk='42164007', color='#1E8A6E', file='inspection.html',
                       short='Keuringen, veiligheidsadvies en trainingen'),
    'materieel':  dict(name='Materieel',  entity='Northguard Materieel B.V.',  kvk='98527819', color='#D8641E', file='materieel.html',
                       short='Verhuur en verkoop van materialen voor bouw en industrie'),
    'mobility':   dict(name='Mobility',   entity='Northguard Mobility B.V.',   kvk='93289286', color='#2F6DB5', file='mobility.html',
                       short='Verhuur van personenauto\'s en lichte bedrijfswagens'),
}

def img(pid, alt, w=1400, eager=False, cls=''):
    src = f'https://images.unsplash.com/photo-{pid}?auto=format&fit=crop&w={w}&q=70'
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{src}" alt="{html.escape(alt)}" {load} decoding="async" onerror="this.remove()"{" class=" + chr(34) + cls + chr(34) if cls else ""}>'

def fig(pid, alt, cap=None, w=1200):
    c = f'<figcaption>{html.escape(cap)}</figcaption>' if cap else ''
    return f'<figure class="figure">{img(pid, alt, w)}{c}</figure>'

def header(active):
    tabs = ''.join(f'<li><a class="t-{k}" href="{d["file"]}"{" aria-current=" + chr(34) + "page" + chr(34) if k == active else ""}>{d["name"]}</a></li>' for k, d in DIVS.items())
    return f'''<a class="skip" href="#main">Naar de inhoud</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="Northguard – home">
      <img src="assets/img/shield.png" alt="" width="41" height="44">
      <span class="brand-name">Northguard<small>{"Group" if not active else DIVS[active]["name"]}</small></span>
    </a>
    <button class="menu-btn" aria-expanded="false" aria-controls="tabs">Menu</button>
    <ul class="tabs" id="tabs">{tabs}<li><a href="{"#contact"}">Contact</a></li></ul>
  </div>
</header>'''

def footer(active):
    links = ''.join(f'<li><a href="{d["file"]}">Northguard {d["name"]}</a></li>' for d in DIVS.values())
    ent = DIVS[active] if active else None
    legal = (f'<span>{ent["entity"]} &nbsp;·&nbsp; <span class="mono">KvK {ent["kvk"]}</span></span>' if ent else
             '<span>' + ' &nbsp;·&nbsp; '.join(f'{d["entity"]} <span class="mono">KvK {d["kvk"]}</span>' for d in DIVS.values()) + '</span>')
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <div class="fbrand"><img src="assets/img/shield.png" alt="" width="43" height="46"><span class="brand-name">Northguard<small>Group</small></span></div>
        <p>Industriële dienstverlening, inspectie, materieel en mobiliteit vanuit Rotterdam. Eén aanspreekpunt voor uw project.</p>
      </div>
      <div><h4>Bedrijven</h4><ul>{links}</ul></div>
      <div><h4>Contact</h4><ul>
        <li>{ADDR[0]}<br>{ADDR[1]}</li>
        <li><a href="tel:{TEL_HREF}">{TEL}</a></li>
        <li><a href="mailto:{MAIL}">{MAIL}</a></li>
      </ul></div>
      <div><h4>24/7 bereikbaar</h4><ul>
        <li><a href="tel:{MOB_HREF}">{MOB}</a></li>
        <li>Voor spoedaanvragen, ziekmeldingen en incidenten</li>
        <li><a href="privacy.html">Privacyverklaring</a></li>
      </ul></div>
    </div>
    <div class="legal">{legal}<span>© <span id="year">2026</span> Northguard</span></div>
  </div>
</footer>
<script src="assets/js/main.js" defer></script>'''

def contact(active, topics):
    opts = ''.join(f'<option>{html.escape(t)}</option>' for t in topics)
    ent = DIVS[active]['entity'] if active else 'Northguard'
    return f'''<section class="band dark" id="contact">
  <div class="wrap cta">
    <div>
      <span class="eyebrow">Contact</span>
      <h2 style="margin-top:14px">Vertel ons wat u nodig heeft</h2>
      <p class="lead" style="margin-top:14px">U krijgt binnen één werkdag reactie van {html.escape(ent)}. Voor spoed zijn wij dag en nacht telefonisch bereikbaar.</p>
      <ul class="contact-list">
        <li><span>Kantoor</span><a href="tel:{TEL_HREF}">{TEL}</a></li>
        <li><span>24/7</span><a href="tel:{MOB_HREF}">{MOB}</a></li>
        <li><span>E-mail</span><a href="mailto:{MAIL}">{MAIL}</a></li>
        <li><span>Adres</span><div>{ADDR[0]}, {ADDR[1]}</div></li>
      </ul>
    </div>
    <form class="quote" id="quote" novalidate>
      <h3>Aanvraag of offerte</h3>
      <div class="row2">
        <div class="fld"><label for="naam">Naam</label><input id="naam" name="naam" autocomplete="name" required></div>
        <div class="fld"><label for="bedrijf">Bedrijf</label><input id="bedrijf" name="bedrijf" autocomplete="organization"></div>
      </div>
      <div class="row2">
        <div class="fld"><label for="email">E-mail</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        <div class="fld"><label for="telefoon">Telefoon</label><input id="telefoon" name="telefoon" type="tel" autocomplete="tel"></div>
      </div>
      <div class="fld"><label for="onderwerp">Onderwerp</label><select id="onderwerp" name="onderwerp">{opts}</select></div>
      <div class="fld"><label for="bericht">Bericht</label><textarea id="bericht" name="bericht" required placeholder="Wat, waar, wanneer en hoeveel?"></textarea></div>
      <button class="btn btn-acc" type="submit">Aanvraag versturen <span class="arr">→</span></button>
      <p class="form-msg" aria-live="polite"></p>
      <p class="form-note">Uw aanvraag wordt als e-mail verstuurd. Wij gebruiken uw gegevens alleen om uw aanvraag te behandelen (zie <a href="privacy.html">privacyverklaring</a>).</p>
    </form>
  </div>
</section>'''

def page(fname, title, desc, active, body, topics, hero_img=None):
    cls = f'div-{active}' if active else 'div-home'
    og = f'https://images.unsplash.com/photo-{hero_img}?auto=format&fit=crop&w=1200&h=630&q=70' if hero_img else ''
    ld = {"@context": "https://schema.org", "@type": "Organization",
          "name": DIVS[active]['entity'] if active else 'Northguard', "url": f'{DOMAIN}/{fname}',
          "logo": f'{DOMAIN}/assets/img/logo.png', "email": MAIL, "telephone": TEL,
          "address": {"@type": "PostalAddress", "streetAddress": ADDR[0], "postalCode": "3047 BR", "addressLocality": "Rotterdam", "addressCountry": "NL"}}
    out = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{DOMAIN}/{'' if fname == 'index.html' else fname}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{DOMAIN}/{'' if fname == 'index.html' else fname}">
{f'<meta property="og:image" content="{og}">' if og else ''}
<meta name="theme-color" content="#141B1F">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/barlow-condensed-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="{cls}">
{header(active) if topics else header(active).replace('href="#contact"', 'href="index.html#contact"')}
<main id="main">
{body}
{contact(active, topics) if topics else ''}
</main>
{footer(active)}
</body>
</html>
'''
    with open(os.path.join(ROOT, fname), 'w', encoding='utf-8') as fh:
        fh.write(out)
    print('wrote', fname)

def hero(active, eyebrow, h1, lead, pid, alt, cta2=None):
    a2 = f'<a class="btn btn-ghost" href="{cta2[1]}">{cta2[0]}</a>' if cta2 else ''
    return f'''<section class="hero">
  <div class="photo">{img(pid, alt, 2000, eager=True)}</div>
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="actions"><a class="btn btn-acc" href="#contact">Neem contact op <span class="arr">→</span></a>{a2}</div>
  </div>
</section>'''

def plate(items):
    return '<dl class="plate"><div class="wrap">' + ''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in items) + '</div></dl>'

def cards(items, cols=''):
    out = []
    for code, title, text, bullets in items:
        ul = ('<ul>' + ''.join(f'<li>{b}</li>' for b in bullets) + '</ul>') if bullets else ''
        out.append(f'<article class="card"><span class="code">{code}</span><h3>{title}</h3><p>{text}</p>{ul}</article>')
    return f'<div class="grid {cols}">' + ''.join(out) + '</div>'

def steps(items):
    return '<ol class="steps">' + ''.join(f'<li><h3>{t}</h3><p>{p}</p></li>' for t, p in items) + '</ol>'

def head(eyebrow, title, lead=''):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="head"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{l}</div>'

def split(eyebrow, title, paras, checks, pid, alt, cap, reverse=False):
    ps = ''.join(f'<p>{p}</p>' for p in paras)
    ck = ('<ul class="checks">' + ''.join(f'<li>{c}</li>' for c in checks) + '</ul>') if checks else ''
    copy = f'<div class="copy"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{ps}{ck}</div>'
    f = fig(pid, alt, cap)
    return f'<div class="split">{f + copy if reverse else copy + f}</div>'

# =====================================================================
# HOME
# =====================================================================
P = dict(  # photo ids (Unsplash, free licence)
    refinery_dusk='1777915627530-fc3decb749cf', refinery_river='1787668803983-bc4fb4516a89', plant_night='1768128834332-7d3479c8d634',
    workers_vests='1787321280637-81ce957b60e7', two_workers='1760161306014-e2dcc13cbdf8', welder='1455165814004-1126a7199f9b',
    foreman='1774599730788-edc1fe2489b2', man_factory='1735494032948-14ef288fc9d3', hardhat_hook='1582489853490-cd3a53eb4530',
    electrician='1758101755915-462eddc23f57', caliper='1758873263563-5ba4aa330799', clipboard='1700727448575-6f1680cd7d75',
    hardhat_rack='1552879890-3a06dd3a06c2', valves='1690973692388-239878450c7b', hv_sign='1566417108845-5ba9c2f9ea1b',
    lab='1764835711461-117d67799a7d',
    scaffold_sky='1762248576542-f98e883f3fbd', scaffold_assemble='1758798349125-5c297b18b8b2', crane='1599707254554-027aeb4deacd',
    grinder='1694522362256-6c907336af43', vests_wall='1662309376159-b95fb193d96b', racks='1519143009590-e3800b9df468',
    vans_row='1587813369290-091c9d432daf', sprinter='1535655685871-dc8158ff167e', cars_row='1630165356623-266076eaceb6',
    car_road='1665521032636-e8d2f6927053', pickup='1612966808160-87a819e0af82', van_road='1624355761500-f00bb5cfb5a1',
)
ALL_TOPICS = ['Personeel / detachering', 'Keuring of inspectie', 'Training of advies', 'Materieel huren of kopen', 'Voertuig huren', 'Anders']

home_cards = ''.join(f'''<a class="div-card" href="{d['file']}" style="--c:{d['color']}">
  <div class="ph">{img(pid, alt, 900)}</div>
  <div class="body"><span class="tag">{d['entity']}</span><h3>{d['name']}</h3><p>{d['short']}.</p><span class="more">Bekijk {d['name']} <span>→</span></span></div>
</a>''' for (k, d), (pid, alt) in zip(DIVS.items(), [
    (P['workers_vests'], 'Vier werknemers in oranje veiligheidsvesten in een industriële hal'),
    (P['electrician'], 'Elektricien test een schakelkast met een multimeter'),
    (P['scaffold_sky'], 'Aluminium steigers tegen een blauwe lucht'),
    (P['vans_row'], 'Rij witte bestelbussen op een parkeerterrein')]))

rows = ''.join(f'<tr><td><span class="dot" style="background:{d["color"]}"></span>{d["entity"]}</td><td class="mono">{d["kvk"]}</td><td>{d["short"]}</td><td><a href="{d["file"]}">{d["name"]} →</a></td></tr>' for d in DIVS.values())

home = f'''{hero(None, 'Northguard Group · Rotterdam', 'Veilig werk voor <em>industrie</em> en bouw',
  'Personeel, inspecties, materieel en vervoer voor projecten in de (petro)chemie, de industrie en de bouw. Vier gespecialiseerde bedrijven, één aanspreekpunt.',
  P['refinery_dusk'], 'Raffinaderij in de schemering met binnenvaartschepen aan de kade', ('Onze bedrijven', '#bedrijven'))}
{plate([('Vestiging', 'Hongkongstraat 47, Rotterdam'), ('Werkgebied', 'Nederland & België'), ('Bereikbaar', '24/7 · ' + MOB), ('Contact', MAIL)])}
<section class="band paper" id="bedrijven">
  <div class="wrap">
    {head('Onze bedrijven', 'Vier disciplines, één team', 'Elk bedrijf heeft zijn eigen vakgebied. Samen ontzorgen we een project van personeel tot materieel en vervoer.')}
    <div class="grid four">{home_cards}</div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {split('Werkwijze', 'Veiligheid is de basis van elke opdracht',
      ['Onze mensen werken op locaties waar fouten grote gevolgen hebben. Daarom leggen we bij elke aanvraag vast welke risico\'s er zijn, welke opleidingen en beschermingsmiddelen nodig zijn en wie waarvoor verantwoordelijk is.',
       'Ons veiligheids- en gezondheidsbeleid is ingericht volgens de VG Checklist Uitzendorganisaties (VCU). Zo weet u vooraf wat u van ons kunt verwachten.'],
      ['VCA-gediplomeerd personeel voor risicovolle omgevingen', 'Gekeurd materieel met registratie per item', 'Eén contactpersoon die uw project kent', 'Dag en nacht bereikbaar bij spoed en incidenten'],
      P['foreman'], 'Voorman geeft instructies via een portofoon aan bouwvakkers', 'Werkinstructie op locatie')}
  </div>
</section>
<section class="band paper">
  <div class="wrap">
    {head('Bedrijfsgegevens', 'De Northguard-bedrijven')}
    <div class="table-wrap"><table class="entities"><thead><tr><th>Bedrijf</th><th>KvK-nummer</th><th>Activiteit</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>'''
page('index.html', 'Northguard – Services, Inspection, Materieel & Mobility', 'Northguard uit Rotterdam: detachering en uitzenden, keuringen en veiligheidsadvies, verhuur van materieel en bedrijfsvoertuigen voor industrie en bouw.', None, home, ALL_TOPICS, P['refinery_dusk'])

# =====================================================================
# SERVICES
# =====================================================================
d = DIVS['services']
services = f'''{hero('services', 'Northguard Services', 'Vakmensen die <em>veilig</em> aan de slag gaan',
  'Detachering en uitzenden van gekwalificeerd personeel voor industrie, petrochemie en bouw. Van brandwacht tot projectondersteuning bij stops en onderhoud.',
  P['two_workers'], 'Twee bouwvakkers met helm en veiligheidsvest op een bouwplaats', ('Onze diensten', '#diensten'))}
{plate([('Bedrijf', d['entity']), ('KvK-nummer', d['kvk']), ('Activiteit', 'Detachering, uitzenden, facility'), ('24/7 inzet', MOB)])}
<section class="band paper" id="diensten">
  <div class="wrap">
    {head('Diensten', 'Wat wij voor u regelen', 'Wij leveren mensen die passen bij de risico\'s van uw werkplek, met de juiste diploma\'s, ervaring en instructie.')}
    {cards([
      ('Detachering & uitzenden', 'Veiligheidspersoneel', 'Gediplomeerde wachten voor werk met verhoogd risico.', ['Brandwachten en heetwerkwachten', 'Mangatwachten en buitenwachten', 'Gasmeten (indien vereist)']),
      ('Detachering & uitzenden', 'Technisch en operationeel personeel', 'Vakmensen en ondersteuning voor productie, onderhoud en bouw.', ['Monteurs en technische ondersteuning', 'Operators en productiemedewerkers', 'Algemeen medewerkers']),
      ('Projectondersteuning', 'Stops & onderhoud', 'Extra capaciteit bij shutdowns, turnarounds en onderhoudsprojecten, snel op te schalen.', ['Planning en bezetting per ploeg', 'Eén aanspreekpunt op locatie', 'Afgetekende urenregistratie']),
      ('Facility management', 'Facilitaire diensten', 'Ondersteuning van de dagelijkse bedrijfsvoering op uw locatie.', ['Facilitaire ondersteuning', 'Interieurverzorging', 'Logistieke ondersteuning']),
      ('Veiligheid', 'Voorbereid op de werkplek', 'Iedere medewerker krijgt vooraf informatie over risico\'s, beschermingsmiddelen en de meldprocedure.', ['VCA Basis of VOL waar vereist', 'PBM-afspraken per opdracht', 'Medische geschiktheid waar nodig']),
      ('Begeleiding', 'Controle tijdens de inzet', 'Wij bezoeken de werkplek, evalueren met u en de medewerker en lossen knelpunten snel op.', ['Werkplekbezoeken', 'Evaluatie na afloop', 'Opvolging van verbeterpunten']),
    ])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {head('Zo werken wij', 'Van aanvraag tot inzet', 'Een vaste route, zodat niets wordt vergeten en u weet wat u kunt verwachten.')}
    {steps([
      ('Aanvraag', 'We leggen de functie, werkplek, risico\'s, PBM en vereiste opleidingen met u vast.'),
      ('Selectie', 'We selecteren kandidaten die aan alle eisen voldoen en bespreken eventuele afwijkingen vooraf met u.'),
      ('Instructie', 'De medewerker krijgt informatie over de risico\'s, de PBM en de meldprocedure en tekent hiervoor.'),
      ('Begeleiding', 'Tijdens de inzet controleren we de afspraken en evalueren we de samenwerking.'),
    ])}
  </div>
</section>
<section class="band paper">
  <div class="wrap">
    {split('Sectoren', 'Thuis in risicovolle omgevingen',
      ['Onze medewerkers zijn gewend aan de regels en de cultuur van industriële locaties: werkvergunningen, toolboxmeetings en strikte huisregels.'],
      [], P['refinery_river'], 'Raffinaderij aan een rivier onder een bewolkte lucht', 'Petrochemie & industrie')}
    <ul class="chips" style="margin-top:28px"><li>Petrochemie</li><li>Chemie</li><li>Industrie & productie</li><li>Haven & logistiek</li><li>Bouw & infra</li><li>Energie</li></ul>
  </div>
</section>
<section class="band">
  <div class="wrap strip">
    {fig(P['welder'], 'Lasser met beschermkap en handschoenen bij rondvliegende vonken', 'Heetwerk')}
    {fig(P['man_factory'], 'Medewerker met helm in een fabriekshal')}
    {fig(P['hardhat_hook'], 'Witte veiligheidshelm aan een haak in een industriële hal')}
  </div>
</section>'''
page('services.html', 'Northguard Services – Detachering & projectondersteuning', 'Northguard Services B.V.: detachering en uitzenden van brandwachten, heetwerkwachten en technisch personeel, projectondersteuning en facility management.', 'services', services,
     ['Personeel / detachering', 'Projectondersteuning (stop/onderhoud)', 'Facility management', 'Anders'], P['two_workers'])

# =====================================================================
# INSPECTION
# =====================================================================
d = DIVS['inspection']
label = '''<div class="label-demo"><div class="klabel" aria-label="Voorbeeld van een keuringslabel">
  <div class="top">Gekeurd <span>NG-INSPECTION</span></div>
  <dl><dt>Object</dt><dd>Rolsteiger RS-04</dd><dt>Registratienr.</dt><dd>NGI-2026-0148</dd><dt>Gekeurd op</dt><dd>14-10-2026</dd><dt>Volgende keuring</dt><dd>10-2027</dd><dt>Keurmeester</dt><dd>Paraaf</dd></dl>
  <div class="months" aria-hidden="true"><i>J</i><i>F</i><i>M</i><i>A</i><i>M</i><i>J</i><i>J</i><i>A</i><i>S</i><i class="on">O</i><i>N</i><i>D</i></div>
</div></div>'''
inspection = f'''{hero('inspection', 'Northguard Inspection', 'Gekeurd, <em>geregistreerd</em> en aantoonbaar veilig',
  'Inspecties en keuringen van arbeidsmiddelen en veiligheidsmiddelen, veiligheidskundig advies en trainingen. Met een digitale registratie die u altijd kunt laten zien.',
  P['electrician'], 'Elektricien test een schakelkast met een multimeter', ('Keuringen', '#keuringen'))}
{plate([('Bedrijf', d['entity']), ('KvK-nummer', d['kvk']), ('Activiteit', 'Keuren, adviseren, trainen'), ('Registratie', 'Digitaal keuringsregister')])}
<section class="band paper" id="keuringen">
  <div class="wrap">
    {head('Diensten', 'Inspectie, advies en training', 'Wij keuren volgens de geldende normen en de eisen van de Arbeidsomstandighedenwet, en leggen elk resultaat vast.')}
    {cards([
      ('Keuren', 'Elektrisch gereedschap', 'Keuring van handgereedschap, verlengkabels en verdeelkasten.', ['Visuele inspectie en meting', 'Volgens NEN 3140', 'Label en rapport per item']),
      ('Keuren', 'Klimmaterieel', 'Ladders, trappen en rolsteigers worden gecontroleerd op gebreken en slijtage.', ['Ladders en trappen', 'Rolsteigers', 'Afkeur en herstel-advies']),
      ('Keuren', 'Hijs- en hefmiddelen & PBM', 'Keuring van hulpmiddelen waar levens van afhangen.', ['Hijsbanden, kettingen en sluitingen', 'Valbeveiliging en harnassen', 'Overige veiligheidsmiddelen']),
      ('Adviseren', 'Veiligheidskundig advies', 'Praktisch advies om risico\'s te beheersen en aan wet- en regelgeving te voldoen.', ['RI&E en plan van aanpak', 'V&G-plannen en werkinstructies', 'Ondersteuning bij VCA/VCU']),
      ('Trainen', 'Opleidingen & trainingen', 'Trainingen op het gebied van arbeidsveiligheid, op locatie of bij ons.', ['Toolboxmeetings', 'Veilig werken met arbeidsmiddelen', 'PBM-instructie']),
      ('Registreren', 'Keuringsregister', 'Alle keuringen digitaal vastgelegd, met tijdige herinnering voor de volgende keuring.', ['Overzicht per locatie en object', 'Certificaten en rapporten', 'Herkeuringsplanning']),
    ])}
  </div>
</section>
<section class="band">
  <div class="wrap split">
    <div class="copy">
      <span class="eyebrow">Registratie</span>
      <h2>Elk object een eigen keuringsbewijs</h2>
      <p>Na een goedgekeurde keuring krijgt elk object een label met registratienummer, keuringsdatum en de maand van de volgende keuring. Dezelfde gegevens staan in uw digitale register, met het rapport erbij.</p>
      <ul class="checks"><li>Direct zichtbaar of materieel gebruikt mag worden</li><li>Afgekeurde items worden apart geregistreerd met reden</li><li>Herinnering vóór de volgende keuring</li></ul>
    </div>
    {label}
  </div>
</section>
<section class="band paper">
  <div class="wrap">
    {head('Werkwijze', 'Zo verloopt een keuring')}
    {steps([
      ('Inventarisatie', 'We brengen samen met u in kaart welke middelen gekeurd moeten worden en met welke frequentie.'),
      ('Keuring', 'Onze keurmeester inspecteert en meet op uw locatie, met zo min mogelijk verstoring van het werk.'),
      ('Label & rapport', 'Goedgekeurde items krijgen een label; u ontvangt een rapport met de bevindingen.'),
      ('Herkeuring', 'Wij plannen de volgende keuring en sturen tijdig een herinnering.'),
    ])}
  </div>
</section>
<section class="band">
  <div class="wrap strip">
    {fig(P['caliper'], 'Handen meten een metalen onderdeel met een digitale schuifmaat', 'Meten')}
    {fig(P['clipboard'], 'Man met klembord tijdens een controle')}
    {fig(P['hardhat_rack'], 'Rek met gele veiligheidshelmen')}
  </div>
</section>'''
page('inspection.html', 'Northguard Inspection – Keuringen & veiligheidsadvies', 'Northguard Inspection B.V.: keuringen van arbeidsmiddelen en veiligheidsmiddelen, veiligheidskundig advies, trainingen en een digitaal keuringsregister.', 'inspection', inspection,
     ['Keuring of inspectie', 'Veiligheidskundig advies', 'Training of opleiding', 'Keuringsregister', 'Anders'], P['electrician'])

# =====================================================================
# MATERIEEL
# =====================================================================
d = DIVS['materieel']
materieel = f'''{hero('materieel', 'Northguard Materieel', 'Het juiste <em>materieel</em>, op tijd op de bouwplaats',
  'Verhuur en verkoop van materialen voor bouw en industrie. Gekeurd geleverd, met heldere afspraken over levering, gebruik en retour.',
  P['scaffold_assemble'], 'Werklieden zetten steigers op tegen een blauwe lucht', ('Assortiment', '#assortiment'))}
{plate([('Bedrijf', d['entity']), ('KvK-nummer', d['kvk']), ('Activiteit', 'Verhuur, in- en verkoop'), ('Levering', 'Op locatie of afhalen')])}
<section class="band paper" id="assortiment">
  <div class="wrap">
    {head('Assortiment', 'Huren of kopen', 'Ons aanbod is afgestemd op werk in de bouw en de industrie. Staat wat u zoekt er niet bij? Vraag het ons; we regelen het.')}
    {cards([
      ('Huur & koop', 'Steigers & klimmaterieel', 'Voor veilig werken op hoogte.', ['Rolsteigers', 'Ladders en trappen', 'Werkplatforms']),
      ('Huur & koop', 'Afzetting & signalering', 'Voor een veilige en overzichtelijke werkplek.', ['Bouwhekken en dranghekken', 'Afzetlint en kegels', 'Waarschuwingsborden']),
      ('Huur & koop', 'Gereedschap & machines', 'Professioneel gereedschap voor bouw en onderhoud.', ['Elektrisch handgereedschap', 'Slijp- en boormachines', 'Meet- en lasapparatuur']),
      ('Koop', 'PBM & veiligheidsmiddelen', 'Persoonlijke beschermingsmiddelen voor uw team.', ['Helmen, brillen en handschoenen', 'Gehoorbescherming', 'Werkkleding en vesten']),
      ('Huur', 'Verlichting & energie', 'Voor werk in het donker of op locaties zonder stroom.', ['Bouwlampen en lichtmasten', 'Aggregaten', 'Kabels en verdeelkasten']),
      ('Huur & koop', 'Bouw- en industriematerialen', 'Verbruiksmaterialen en onderdelen op aanvraag.', ['Bevestigingsmaterialen', 'Afdekmaterialen', 'Levering op projectbasis']),
    ])}
  </div>
</section>
<section class="band">
  <div class="wrap">
    {split('Kwaliteit', 'Gekeurd geleverd',
      ['Verhuurmaterieel dat keuringsplichtig is, wordt gecontroleerd voordat het de deur uitgaat. Dat doen we samen met Northguard Inspection, zodat u bij elk item kunt zien wanneer het voor het laatst is gekeurd.'],
      ['Keuringslabel op keuringsplichtig materieel', 'Controle bij retour', 'Vervanging bij defecten'],
      P['grinder'], 'Man slijpt een stuk beton met een haakse slijper', 'Gereedschap & machines', reverse=True)}
  </div>
</section>
<section class="band paper">
  <div class="wrap">
    {head('Werkwijze', 'Van aanvraag tot retour')}
    {steps([
      ('Aanvraag', 'U geeft door wat u nodig heeft, voor welke periode en op welke locatie.'),
      ('Offerte', 'U ontvangt een duidelijke offerte met huurprijs, borg en leverkosten.'),
      ('Levering', 'Wij leveren op locatie of u haalt het materieel af, gekeurd en gebruiksklaar.'),
      ('Retour', 'Bij retour controleren we het materieel en ronden we de huur af.'),
    ])}
  </div>
</section>
<section class="band">
  <div class="wrap strip">
    {fig(P['scaffold_sky'], 'Aluminium steigers tegen een blauwe lucht', 'Steigers')}
    {fig(P['crane'], 'Gele bouwkraan naast een gebouw')}
    {fig(P['vests_wall'], 'Oranje helmen en gele veiligheidsvesten aan een wand')}
  </div>
</section>'''
page('materieel.html', 'Northguard Materieel – Verhuur & verkoop bouwmaterieel', 'Northguard Materieel B.V.: verhuur en in- en verkoop van materialen voor bouw en industrie, zoals steigers, afzetting, gereedschap en PBM.', 'materieel', materieel,
     ['Materieel huren', 'Materieel kopen', 'Levering op locatie', 'Anders'], P['scaffold_assemble'])

# =====================================================================
# MOBILITY
# =====================================================================
d = DIVS['mobility']
fleet = ''.join(f'''<article class="vclass"><span class="cat">{cat}</span><h3>{t}</h3><p>{p}</p><dl>{''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in spec)}</dl></article>''' for cat, t, p, spec in [
    ('Categorie A', 'Personenauto', 'Voor dienstreizen en vervoer van leidinggevenden en specialisten.', [('Zitplaatsen', '5'), ('Rijbewijs', 'B'), ('Huur', 'Dag – maand')]),
    ('Categorie B', 'Personenbus', 'Voor groepsvervoer van ploegen naar de werklocatie.', [('Zitplaatsen', '8 + bestuurder'), ('Rijbewijs', 'B'), ('Huur', 'Week – project')]),
    ('Categorie C', 'Bestelbus compact', 'Voor gereedschap en kleine leveringen in de stad en op het terrein.', [('Laadruimte', 'Compact'), ('Rijbewijs', 'B'), ('Huur', 'Dag – maand')]),
    ('Categorie D', 'Bestelbus groot', 'Voor materieel en grotere volumes naar de bouwplaats.', [('Laadruimte', 'Groot'), ('Rijbewijs', 'B'), ('Huur', 'Dag – lange termijn')]),
])
mobility = f'''{hero('mobility', 'Northguard Mobility', 'Mobiel voor elk <em>project</em>',
  'Verhuur van personenauto\'s en lichte bedrijfswagens. Per dag, per week of voor de hele looptijd van uw project.',
  P['vans_row'], 'Rij witte bestelbussen op een parkeerterrein', ('Wagenpark', '#wagenpark'))}
{plate([('Bedrijf', d['entity']), ('KvK-nummer', d['kvk']), ('Activiteit', 'Verhuur personen- en bedrijfsauto\'s'), ('Huurduur', 'Dag · week · maand · project')])}
<section class="band paper" id="wagenpark">
  <div class="wrap">
    {head('Wagenpark', 'Kies het voertuig dat bij uw werk past', 'Alle voertuigen zijn te besturen met rijbewijs B. Beschikbaarheid en tarieven ontvangt u op aanvraag.')}
    <div class="fleet">{fleet}</div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    {split('Zakelijke verhuur', 'Vervoer geregeld, u focust op het werk',
      ['Bij projecten met wisselende ploegen of locaties is vervoer vaak een puzzel. Wij stemmen het aantal en type voertuigen af op uw planning en schalen mee als het project groeit.'],
      ['Korte en lange termijn', 'Voertuigen voor projectpersoneel van Northguard Services', 'Eén factuur per project', 'Vervangend vervoer bij uitval'],
      P['sprinter'], 'Witte bestelbus op een open terrein', 'Lichte bedrijfswagen', reverse=True)}
  </div>
</section>
<section class="band paper">
  <div class="wrap">
    {head('Werkwijze', 'Zo huurt u een voertuig')}
    {steps([
      ('Reserveren', 'Geef het type voertuig, de periode en de ophaal- of afleverlocatie door.'),
      ('Bevestiging', 'U ontvangt de bevestiging met de huurvoorwaarden, het tarief en de borg.'),
      ('Ophalen', 'Bij ophalen controleren we samen het rijbewijs en de staat van het voertuig.'),
      ('Inleveren', 'Na inlevering controleren we het voertuig en sluiten we de huur af.'),
    ])}
    <p class="form-note" style="margin-top:22px">Voorwaarden zoals minimumleeftijd, rijervaring, borg, kilometerbundel en eigen risico staan in de huurvoorwaarden die u bij de bevestiging ontvangt.</p>
  </div>
</section>
<section class="band">
  <div class="wrap strip">
    {fig(P['van_road'], 'Witte bestelbus op een betonnen weg', 'Bedrijfswagens')}
    {fig(P['cars_row'], 'Rij geparkeerde personenauto\'s')}
    {fig(P['car_road'], 'Witte auto op de weg')}
  </div>
</section>'''
page('mobility.html', 'Northguard Mobility – Verhuur auto\'s & bedrijfswagens', 'Northguard Mobility B.V.: verhuur van personenauto\'s, personenbussen en lichte bedrijfswagens per dag, week, maand of project.', 'mobility', mobility,
     ['Voertuig huren', 'Lange termijn / project', 'Anders'], P['vans_row'])

# =====================================================================
# PRIVACY
# =====================================================================
privacy = f'''<section class="band">
  <div class="wrap prose">
    <span class="eyebrow">Privacy</span>
    <h1 style="font-size:clamp(2.2rem,5vw,3.4rem)">Privacyverklaring website</h1>
    <p>Deze verklaring geldt voor de website www.northguardbv.nl van de Northguard-bedrijven: {', '.join(d['entity'] for d in DIVS.values())}. Contact: {MAIL}, {ADDR[0]}, {ADDR[1]}.</p>
    <h2>Welke gegevens</h2>
    <p>Via het aanvraagformulier stelt u een e-mail op met uw naam, bedrijf, e-mailadres, telefoonnummer en bericht. Die e-mail verstuurt u zelf vanuit uw e-mailprogramma. Wij gebruiken deze gegevens alleen om uw aanvraag te behandelen en contact met u op te nemen.</p>
    <h2>Bewaartermijn</h2>
    <p>Wij bewaren aanvragen niet langer dan nodig is om ze af te handelen, tenzij er een overeenkomst uit voortvloeit. Dan gelden de wettelijke bewaartermijnen.</p>
    <h2>Cookies en externe diensten</h2>
    <p>Deze website plaatst geen tracking- of advertentiecookies. Lettertypen staan op onze eigen server. Foto's worden geladen via Unsplash (images.unsplash.com); daarbij ontvangt Unsplash technische gegevens zoals uw IP-adres. De website wordt gehost via GitHub Pages.</p>
    <h2>Uw rechten</h2>
    <p>U kunt ons vragen uw gegevens in te zien, te corrigeren of te verwijderen. Stuur hiervoor een e-mail naar {MAIL}. Bent u het niet eens met hoe wij met uw gegevens omgaan, dan kunt u een klacht indienen bij de Autoriteit Persoonsgegevens.</p>
    <p class="form-note">Laatst bijgewerkt: oktober 2026.</p>
  </div>
</section>'''
page('privacy.html', 'Privacyverklaring – Northguard', 'Privacyverklaring van de website van de Northguard-bedrijven.', None, privacy, None)

# 404
nf = f'''<section class="hero"><div class="photo">{img(P['plant_night'], 'Industrieel complex bij nacht', 2000, eager=True)}</div>
<div class="wrap"><span class="eyebrow">404</span><h1>Deze pagina bestaat niet</h1><p class="lead">De pagina is verplaatst of het adres is onjuist.</p>
<div class="actions"><a class="btn btn-acc" href="index.html">Naar de homepage <span class="arr">→</span></a></div></div></section>'''
page('404.html', 'Pagina niet gevonden – Northguard', 'Deze pagina bestaat niet.', None, nf, None)

# sitemap / robots / CNAME
urls = ['', 'services.html', 'inspection.html', 'materieel.html', 'mobility.html', 'privacy.html']
with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
with open(os.path.join(ROOT, 'robots.txt'), 'w') as fh:
    fh.write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
with open(os.path.join(ROOT, 'CNAME'), 'w') as fh:
    fh.write('www.northguardbv.nl\n')
open(os.path.join(ROOT, '.nojekyll'), 'w').close()
print('done')
