# Website Northguard – www.northguardbv.nl

Statische website (HTML/CSS/JS) voor GitHub Pages. Geen server, database of build-tool nodig.

## Pagina's

| Bestand | Inhoud |
|---|---|
| `index.html` | Overzicht van de Northguard-bedrijven |
| `services.html` | Northguard Services B.V. – detachering, uitzenden, projectondersteuning, facility management |
| `inspection.html` | Northguard Inspection B.V. – keuringen, veiligheidskundig advies, trainingen, keuringsregister |
| `materieel.html` | Northguard Materieel B.V. – verhuur en in- en verkoop van materialen voor bouw en industrie |
| `mobility.html` | Northguard Mobility B.V. – verhuur van personenauto's en lichte bedrijfswagens |
| `privacy.html` | Privacyverklaring website |
| `404.html` | Foutpagina |

## Online zetten met GitHub Pages

1. Maak op GitHub een nieuwe repository aan, bijvoorbeeld `northguard-website` (openbaar).
2. Upload alle bestanden van deze map (niet de zip zelf) naar de hoofdmap van de repository:
   *Add file → Upload files*, selecteer alle bestanden en kies *Commit changes*.
   Deze versie heeft bewust geen submappen, zodat uploaden via de website altijd werkt.
3. Ga naar *Settings → Pages*:
   - *Source*: **Deploy from a branch**
   - *Branch*: **main**, map **/ (root)** → *Save*
4. Vul onder *Custom domain* in: `www.northguardbv.nl` en klik *Save*.
   (GitHub maakt dan zelf het bestand `CNAME` aan.)
5. Zodra de DNS goed staat (zie hieronder) en het certificaat is aangemaakt: vink **Enforce HTTPS** aan.

## DNS-instellingen bij uw domeinregistrar

Vervang `GEBRUIKERSNAAM` door de GitHub-gebruikers- of organisatienaam.

| Type | Naam / host | Waarde |
|---|---|---|
| CNAME | `www` | `GEBRUIKERSNAAM.github.io` |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

- Met de vier A-records stuurt `northguardbv.nl` (zonder www) automatisch door naar `www.northguardbv.nl`.
- **Laat de MX-records (e-mail) ongemoeid**, anders werkt `info@northguardbv.nl` niet meer.
- Verwijder eventuele oude A- of CNAME-records voor `@` en `www` van de vorige website.
- DNS-wijzigingen kunnen tot 24 uur duren. Controleer de actuele IP-adressen in de documentatie van GitHub Pages ("Managing a custom domain").
- Aanbevolen: verifieer het domein in GitHub (*Settings → Pages → Verified domains*) om misbruik van het domein te voorkomen.

## Teksten aanpassen

Teksten pas je direct aan in de `.html`-bestanden (op GitHub: open het bestand en klik op het potloodje). Kop, menu en voettekst staan op elke pagina; pas die bij een wijziging op alle pagina's aan.

Kleuren en vormgeving staan in `style.css` (bovenaan, onder `:root`). Elk bedrijf heeft een eigen accentkleur:
Services goud, Inspection groen, Materieel oranje, Mobility blauw.

## Foto's

De foto's komen van [Unsplash](https://unsplash.com) (gratis te gebruiken, ook commercieel, volgens de Unsplash-licentie) en worden rechtstreeks van Unsplash geladen. Laadt een foto niet, dan toont de pagina een donker vlak in de huisstijl.

Eigen foto's gebruiken (aanbevolen zodra beschikbaar):
1. Upload de foto naar de hoofdmap van de repository (liefst `.jpg`, ca. 1600–2000 px breed, < 400 kB).
2. Vervang in de HTML de `src` van de foto door de bestandsnaam, bijvoorbeeld `naam.jpg`.

Gebruik geen foto's van internet zonder toestemming van de maker.

## Contactformulier

GitHub Pages heeft geen server. Het formulier stelt daarom een e-mail op aan `info@northguardbv.nl` in het e-mailprogramma van de bezoeker. Wilt u dat aanvragen direct binnenkomen zonder e-mailprogramma, koppel dan later een formulierdienst (bijv. Formspree) en pas `main.js` aan.

## Privacy

Lettertypen staan op de eigen website (geen Google Fonts). Er worden geen trackingcookies gebruikt. Bij het laden van foto's van Unsplash ontvangt Unsplash het IP-adres van de bezoeker; dit staat in de privacyverklaring. Met eigen foto's in de repository vervalt dit.
