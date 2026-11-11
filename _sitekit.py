#!/usr/bin/env python3
"""Shared page templates for the PPCall referral sites (plain HTML output, no build step needed to host).
Each site's _build.py defines a CONFIG dict + page content and calls build()."""
import json
from pathlib import Path

PHONE_DISP = "{{PHONE}}"
PHONE_TEL = "{{PHONE_TEL}}"
CALL = f'<a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>'


def fill(text):
    """Swap the {CALL} token for an inline phone link (no f-string brace headaches)."""
    return text.replace("{CALL}", CALL)


class Site:
    def __init__(self, cfg, root):
        self.c = cfg
        self.root = Path(root)
        self.pages = {}       # filename -> html
        self.sitemap = []     # (loc, changefreq, priority)

    # ---------- chrome ----------
    def url(self, path=""):
        return f"https://{self.c['domain']}/{path}"

    def ld(self, obj):
        return ('  <script type="application/ld+json">\n'
                + json.dumps(obj, indent=2, ensure_ascii=False) + "\n  </script>\n")

    def head(self, title, desc, canonical, schemas=()):
        extra = "".join(self.ld(s) for s in schemas)
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{self.url(canonical)}">
  <meta name="robots" content="index, follow">
  <meta name="geo.region" content="{self.c['geo_region']}">
  <meta name="geo.placename" content="{self.c['city']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{self.url(canonical)}">
  <meta property="og:site_name" content="{self.c['brand']}">
  <meta property="og:locale" content="en_US">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="css/styles.css">
{extra}</head>
'''

    def nav(self, active):
        c = self.c
        def a(href, label, key):
            cur = ' aria-current="page"' if key == active else ""
            return f'<a href="{href}"{cur}>{label}</a>'
        svc_active = active in [s["file"] for s in c["services"]]
        cur_attr = ' aria-current="page"'
        drop = "\n              ".join(
            f'<a href="{s["file"]}"{cur_attr if s["file"] == active else ""}>{s["nav"]}</a>'
            for s in c["services"])
        return f'''{a("index.html", "Home", "index.html")}
          <div class="nav-drop">
            <a href="index.html#services" class="nav-drop-toggle{" is-active" if svc_active else ""}" aria-haspopup="true">Services ▾</a>
            <div class="drop-menu">
              {drop}
            </div>
          </div>
          {a("service-areas.html", "Service Areas", "service-areas.html")}
          {a("about.html", "About", "about.html")}
          {a("contact.html", "Contact", "contact.html")}'''

    def header(self, active):
        c = self.c
        return f'''<body>
  <div class="topbar">
    {c['topbar']} &nbsp;·&nbsp;
    <a href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
  </div>
  <header class="site-header">
    <div class="container header-inner">
      <a class="logo" href="index.html">
        <span class="logo-mark" aria-hidden="true">💧</span>
        <span>{c['brand']}<small>{c['logo_sub']}</small></span>
      </a>
      <nav class="nav" aria-label="Main">
          {self.nav(active)}
        <a class="btn btn-primary header-cta" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
      </nav>
    </div>
  </header>
'''

    def footer(self):
        c = self.c
        svc = "\n            ".join(f'<li><a href="{s["file"]}">{s["name"]}</a></li>' for s in c["services"])
        return f'''  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand">{c['brand']}</div>
          <p>{c['footer_blurb']}</p>
          <p><a class="phone-link" href="tel:{PHONE_TEL}" style="color:#5eead4">{PHONE_DISP}</a></p>
        </div>
        <div>
          <h3>Services</h3>
          <ul>
            {svc}
          </ul>
        </div>
        <div>
          <h3>Info</h3>
          <ul>
            <li><a href="service-areas.html">Service Areas</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="contact.html">Contact</a></li>
            <li><a href="privacy.html">Privacy Policy</a></li>
            <li><a href="terms.html">Terms of Use</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-disclosure">
        <strong>Important:</strong> This site is a free referral service. Calls may be forwarded to an independent, licensed service provider in your area. We do not perform restoration, mold, fire, or plumbing work ourselves, and we are not affiliated with any single contractor. Always confirm licensing, insurance, and pricing directly with the provider you speak with.
      </div>
      <div class="footer-bottom">
        <span>&copy; {c['year']} {c['brand']} Referral. All rights reserved.</span>
        <span><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></span>
      </div>
    </div>
  </footer>
  <div class="mobile-callbar" aria-label="Call now">
    <a href="tel:{PHONE_TEL}">📞 Call Now — {PHONE_DISP}</a>
  </div>
</body>
</html>
'''

    # ---------- schema helpers ----------
    def org(self):
        c = self.c
        return {
            "@type": "Organization",
            "name": c["brand"],
            "url": self.url(),
            "description": "Free referral service connecting callers with independent restoration providers. Not a contractor.",
        }

    def area_served(self):
        c = self.c
        out = [{"@type": "City", "name": c["city"],
                "containedInPlace": {"@type": "State", "name": c["state"]}}]
        out += [{"@type": "City", "name": n} for n in c["schema_areas"]]
        return out

    def breadcrumb(self, name, file):
        return {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": self.url()},
                {"@type": "ListItem", "position": 2, "name": name, "item": self.url(file)},
            ],
        }

    def faq_schema(self, faqs):
        return {
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
        }

    def faq_html(self, faqs):
        return "\n".join(
            f'''          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''' for q, a in faqs)

    # ---------- page builders ----------
    def add(self, file, html, freq="monthly", prio="0.8"):
        self.pages[file] = html
        self.sitemap.append((file if file != "index.html" else "", freq, prio))

    def related(self, current):
        items = [s for s in self.c["services"] if s["file"] != current]
        cards = "\n".join(
            f'''          <a class="related-link" href="{s["file"]}"><span aria-hidden="true">{s["icon"]}</span> {s["name"]}</a>'''
            for s in items)
        return f'''    <section class="section section-alt">
      <div class="container">
        <div class="section-head">
          <h2>Other problems we can refer you for in {self.c['city']}</h2>
          <p>One call covers all of these. Describe what happened and we will try to match you with the right type of provider.</p>
        </div>
        <div class="related-grid">
{cards}
        </div>
      </div>
    </section>
'''

    def service_page(self, s):
        """s: dict with file,title,meta,h1,crumb,lead,body,schema_name,schema_desc,service_type,faqs(optional)"""
        c = self.c
        schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": s["schema_name"],
            "serviceType": s["service_type"],
            "description": s["schema_desc"],
            "provider": self.org(),
            "areaServed": self.area_served(),
            "url": self.url(s["file"]),
        }
        schemas = [schema, self.breadcrumb(s["crumb"], s["file"])]
        faqs = s.get("faqs") or []
        if faqs:
            schemas.append(self.faq_schema(faqs))
        faq_block = ""
        if faqs:
            faq_block = f'''          <h2>Quick answers</h2>
          <div class="faq">
{self.faq_html(faqs)}
          </div>
'''
        html = (self.head(s["title"], s["meta"], s["file"], schemas)
                + self.header(s["file"])
                + f'''  <main>
    <section class="page-hero">
      <div class="container">
        <p class="breadcrumb"><a href="index.html">Home</a> / {s["crumb"]}</p>
        <h1>{s["h1"]}</h1>
        <p class="lead">{s["lead"]}</p>
      </div>
    </section>
    <section class="section">
      <div class="container content-split">
        <article class="prose">
{fill(s["body"])}
{faq_block}          <div class="notice">
            <strong>Referral disclosure:</strong> This site does not perform restoration, cleanup, mold, fire, or plumbing work. We connect callers with independent providers. Confirm licensing, insurance, scope, and pricing directly with any company you hire.
          </div>
        </article>
        <aside>
          <div class="sidebar-card">
            <h2>{s.get("side_h", "Need help now?")}</h2>
            <p>{s.get("side_p", "Call our free referral line for " + c["city"] + " and nearby communities.")}</p>
            <div class="phone-display"><a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a></div>
            <a class="btn btn-primary btn-block" href="tel:{PHONE_TEL}">Call Now</a>
            <p class="muted" style="margin-top:1rem;margin-bottom:0;font-size:0.85rem;">No charge to call. Work pricing is set by the provider.</p>
          </div>
        </aside>
      </div>
    </section>
{self.related(s["file"])}    <section class="cta-band">
      <div class="container">
        <h2>{s.get("cta_h", "Talk with a local provider about your situation")}</h2>
        <p>{s.get("cta_p", "Describe what happened. We will help connect you.")}</p>
        <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
      </div>
    </section>
  </main>
'''
                + self.footer())
        self.add(s["file"], html, "monthly", s.get("prio", "0.8"))

    def simple_page(self, file, title, desc, crumb, h1, lead, inner, active=None,
                    freq="yearly", prio="0.5", schemas=(), with_side=False, side_h="", side_p=""):
        if with_side:
            body = f'''    <section class="section">
      <div class="container content-split">
        <article class="prose">
{fill(inner)}
        </article>
        <aside>
          <div class="sidebar-card">
            <h2>{side_h}</h2>
            <p>{side_p}</p>
            <div class="phone-display"><a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a></div>
            <a class="btn btn-primary btn-block" href="tel:{PHONE_TEL}">Call Now</a>
          </div>
        </aside>
      </div>
    </section>
'''
        else:
            body = f'''    <section class="section">
      <div class="container prose{" legal" if file in ("privacy.html", "terms.html") else ""}">
{fill(inner)}
      </div>
    </section>
'''
        html = (self.head(title, desc, file, list(schemas) + [self.breadcrumb(crumb, file)])
                + self.header(active if active is not None else file)
                + f'''  <main>
    <section class="page-hero">
      <div class="container">
        <p class="breadcrumb"><a href="index.html">Home</a> / {crumb}</p>
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>
      </div>
    </section>
{body}  </main>
'''
                + self.footer())
        self.add(file, html, freq, prio)

    def raw_page(self, file, html, freq="monthly", prio="1.0"):
        self.add(file, fill(html), freq, prio)

    # ---------- shared legal pages ----------
    def legal_pages(self, updated):
        c = self.c
        d = c["domain"]
        b = c["brand"]
        privacy = f'''        <p>This Privacy Policy describes how the {b} website (“this site,” “we,” “us”) handles information when you visit {d} or call the phone number published on this site.</p>

        <h2>1. Who we are</h2>
        <p>This site is a free referral service that may connect callers with independent service providers. We are not those providers. This policy covers the website and the referral phone experience we control, not the privacy practices of third-party contractors you may later hire.</p>

        <h2>2. Information we may collect</h2>
        <h3>Website browsing</h3>
        <p>Our hosting provider may automatically receive standard technical data such as IP address, browser type, device type, referring URL, pages requested, and timestamps. As configured, this site does not run third-party advertising or analytics trackers.</p>
        <h3>Phone calls</h3>
        <p>If you call the number on this site, your telephone number and call details (such as time and duration) may be processed by our telephony provider and, when a referral is made, shared as needed with an independent provider to complete the connection. Calls may be recorded depending on the telephony or network tools in use; if recording applies, listen for a notice at the start of the call.</p>
        <h3>Information you volunteer</h3>
        <p>During a call you may describe your property, the water, mold, fire, or sewage problem, and your location so a provider can decide whether they can help. Share only what you are comfortable providing.</p>

        <h2>3. How information is used</h2>
        <ul>
          <li>To operate and secure the website</li>
          <li>To connect you with an independent provider when you request help by phone</li>
          <li>To troubleshoot call quality or misuse of the phone line</li>
          <li>To comply with law when required</li>
        </ul>

        <h2>4. Sharing of information</h2>
        <p>We may share call-related information with telephony platforms, call-tracking tools, pay-per-call or referral networks, and independent service providers only to complete a referral you started. We do not sell personal information as a standalone data product. Providers you speak with have their own privacy practices once you are connected.</p>

        <h2>5. Cookies</h2>
        <p>This static website has no accounts and is not intentionally configured with advertising cookies. Your browser may still cache files for performance.</p>

        <h2>6. Data retention</h2>
        <p>Technical logs and call records are kept only as long as needed for operations, billing reconciliation with networks, dispute resolution, and legal obligations, then deleted or anonymized according to our vendors’ practices.</p>

        <h2>7. Children’s privacy</h2>
        <p>This site is intended for adults making decisions about property damage. We do not knowingly collect information from children under 13.</p>

        <h2>8. Security</h2>
        <p>No method of transmission or storage is 100% secure. We use reputable hosting and telephony vendors and limit access to call-related tools to what is needed to run the referral service.</p>

        <h2>9. Your choices</h2>
        <p>You may choose not to call, and you may end a call at any time. For requests about call data held by a telephony vendor or network, contact us through the phone number on this site and we will point you to the right channel when we can.</p>

        <h2>10. Changes</h2>
        <p>We may update this Privacy Policy by posting a new version on this page with a revised “Last updated” date.</p>

        <h2>11. Contact</h2>
        <p>Questions about this policy: call {{CALL}} and say your question is about privacy (not an emergency referral).</p>'''
        terms = f'''        <p>These Terms of Use (“Terms”) govern your use of {d} and its phone referral line. By using the site or calling the published number, you agree to these Terms.</p>

        <h2>1. Nature of the service</h2>
        <p><strong>This site is a free referral / lead-connection service.</strong> We do not perform water damage restoration, flooded basement cleanup, sewage cleanup, mold remediation, fire or smoke restoration, roofing, plumbing, construction, or insurance adjusting. Calls may be forwarded or connected to an independent, licensed service provider in your area. Those providers are not our employees or joint-venture partners unless a separate written agreement says so.</p>

        <h2>2. No professional advice</h2>
        <p>Content on this website is general information only. It is not a substitute for inspection by a qualified professional, or for legal, insurance, or medical advice. Always confirm facts about your home with appropriate licensed trades and your insurer.</p>

        <h2>3. No guarantees</h2>
        <p>We do not guarantee that a provider will answer, serve your exact neighborhood, be available at a particular hour (including nights, weekends, or holidays), offer a particular price, or be the right fit for your job. We do not guarantee insurance outcomes. Any warranties or service commitments are solely those offered (if any) by the independent provider you hire.</p>

        <h2>4. Your responsibilities</h2>
        <ul>
          <li>Give accurate location and situation details when requesting a referral</li>
          <li>Verify licensing, insurance, scope, and pricing with any provider before authorizing work</li>
          <li>Use your own judgment about safety (electrical hazards, contaminated water, smoke, structural risk)</li>
          <li>Do not use the phone line for harassment, fraud, or unlawful purposes</li>
        </ul>

        <h2>5. Third-party providers</h2>
        <p>If you hire a provider, your contract is with them. We are not a party to that contract and are not responsible for their workmanship, billing, conduct, or omissions. Raise disputes about services directly with that provider.</p>

        <h2>6. Intellectual property</h2>
        <p>Website text, design, and branding are owned by the site operator or used with permission. You may not copy substantial portions for commercial reuse without permission.</p>

        <h2>7. Limitation of liability</h2>
        <p>To the fullest extent permitted by law, the site operator is not liable for indirect, incidental, special, consequential, or punitive damages, or for any loss arising from your use of the website, reliance on its content, or dealings with third-party providers reached through the referral line. Our total liability for claims relating to the site or referral service shall not exceed one hundred U.S. dollars (USD $100).</p>

        <h2>8. Indemnity</h2>
        <p>You agree to indemnify and hold harmless the site operator from claims arising out of your misuse of the site, your breach of these Terms, or your agreements with third-party providers.</p>

        <h2>9. Changes and availability</h2>
        <p>We may change the website, phone routing, or these Terms at any time. Continued use after changes means you accept the updated Terms. We may pause the referral line for maintenance or operational reasons.</p>

        <h2>10. Governing law</h2>
        <p>These Terms are governed by the laws of the State of {c['law_state']}, without regard to conflict-of-law rules, unless applicable law requires otherwise.</p>

        <h2>11. Contact</h2>
        <p>Questions about these Terms: call {{CALL}} and say your call is about website terms.</p>'''
        self.simple_page("privacy.html", f"Privacy Policy | {b}", f"Privacy Policy for the {b} referral website.",
                         "Privacy Policy", "Privacy Policy", f"Last updated: {updated}", privacy, active="", prio="0.3")
        self.simple_page("terms.html", f"Terms of Use | {b}", f"Terms of Use for the {b} referral website.",
                         "Terms of Use", "Terms of Use", f"Last updated: {updated}", terms, active="", prio="0.3")

    # ---------- output ----------
    def write(self):
        for name, html in self.pages.items():
            (self.root / name).write_text(html, encoding="utf-8")
            print(f"Wrote {name} ({len(html)} bytes)")
        order = sorted(self.sitemap, key=lambda t: -float(t[2]))
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for loc, freq, prio in order:
            lines.append(f'  <url><loc>{self.url(loc)}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>')
        lines.append("</urlset>")
        (self.root / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (self.root / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\n\nSitemap: {self.url('sitemap.xml')}\n", encoding="utf-8")
        (self.root / "CNAME").write_text(self.c["domain"] + "\n", encoding="utf-8")
        print("Done", len(self.pages), "pages + sitemap.xml, robots.txt, CNAME")
