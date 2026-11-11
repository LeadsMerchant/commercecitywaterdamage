#!/usr/bin/env python3
"""Generate the static site pages for commercecitywaterdamage.com
Run:  python3 _build.py   (then ./replace_phone.sh once the tracking number exists)"""
from pathlib import Path
from _sitekit import Site, PHONE_DISP, PHONE_TEL, CALL

ROOT = Path(__file__).resolve().parent

CONFIG = {
    "domain": "commercecitywaterdamage.com",
    "brand": "Commerce City Water Damage",
    "logo_sub": "Local referral connection",
    "city": "Commerce City",
    "state": "Colorado",
    "geo_region": "US-CO",
    "topbar": "Free referral line for Commerce City &amp; north metro Denver homeowners",
    "footer_blurb": "A free referral service that helps homeowners in Commerce City and nearby north metro Denver communities connect with independent, licensed water damage, mold, fire, and sewage cleanup providers.",
    "schema_areas": ["Brighton", "Thornton", "Henderson", "Northglenn", "Denver"],
    "law_state": "New Mexico",
    "year": 2026,
    "services": [
        {"file": "water-damage-restoration.html", "name": "Water Damage Restoration", "nav": "Water Damage Restoration", "icon": "🌊"},
        {"file": "burst-frozen-pipes.html", "name": "Burst &amp; Frozen Pipes", "nav": "Burst &amp; Frozen Pipes", "icon": "🧊"},
        {"file": "storm-roof-leak-damage.html", "name": "Hail, Storm &amp; Roof Leaks", "nav": "Hail, Storm &amp; Roof Leaks", "icon": "⛈️"},
        {"file": "flooded-basement-cleanup.html", "name": "Flooded Basement &amp; Sump Pump", "nav": "Flooded Basement &amp; Sump", "icon": "🏚️"},
        {"file": "sewage-backup-cleanup.html", "name": "Sewage Backup Cleanup", "nav": "Sewage Backup Cleanup", "icon": "🚽"},
        {"file": "mold-remediation.html", "name": "Mold Remediation", "nav": "Mold Remediation", "icon": "🦠"},
        {"file": "fire-smoke-damage.html", "name": "Fire &amp; Smoke Damage", "nav": "Fire &amp; Smoke Damage", "icon": "🔥"},
    ],
}

site = Site(CONFIG, ROOT)
C = CONFIG["city"]

# ======================= HOME =======================
home_faqs = [
    ("Is this a restoration company?",
     "No. This website is a free referral service. When you call, we try to connect you with an independent, licensed provider who handles the kind of damage you have, whether that is water, mold, sewage, or fire and smoke."),
    ("Can I call at night or on a weekend?",
     "Yes, you can call any time. Many restoration companies offer emergency response outside business hours, and we will try to connect you with one. We cannot promise a provider is available at every hour."),
    ("What parts of the north metro do you cover?",
     "We focus on Commerce City (ZIP codes 80022 and 80640, plus the parts of 80601 and 80603 inside city limits) and nearby Brighton, Thornton, Henderson, Northglenn, and northeast Denver. Coverage depends on the providers available when you call."),
    ("What kinds of problems can I call about?",
     "Common calls include burst or frozen pipes, hail or wind damage that let water in, flooded basements, sump pump failures, sewage backups, mold after a leak, and fire or smoke damage, including the water left behind after a fire is put out."),
    ("Is there a charge to call?",
     "There is no charge to call this referral line. Any inspection or restoration fees are between you and the independent provider you choose to hire."),
    ("Should I call my insurance company too?",
     "If the damage may be covered, it is usually wise to photograph everything and contact your insurer. A restoration provider can explain the documentation that is typically requested for your type of loss."),
]

svc_cards = [
    ("🌊", "Water Damage Restoration", "Extraction, drying, and cleanup after leaks, appliance failures, and other indoor water.", "water-damage-restoration.html"),
    ("🧊", "Burst &amp; Frozen Pipes", "Colorado cold fronts can freeze pipes fast. Get help drying out after the break.", "burst-frozen-pipes.html"),
    ("⛈️", "Hail, Storm &amp; Roof Leaks", "Hail-cracked shingles, wind damage, and storm water coming through ceilings.", "storm-roof-leak-damage.html"),
    ("🏚️", "Flooded Basement &amp; Sump", "Water on the basement floor from a failed sump pump, window well, or heavy rain.", "flooded-basement-cleanup.html"),
    ("🚽", "Sewage Backup Cleanup", "Floor drain or toilet backups need special handling. Don’t clean it up yourself.", "sewage-backup-cleanup.html"),
    ("🦠", "Mold Remediation", "Musty smell or visible growth after a leak that never fully dried out.", "mold-remediation.html"),
    ("🔥", "Fire &amp; Smoke Damage", "Soot, smoke odor, and the water left behind by firefighting.", "fire-smoke-damage.html"),
]
cards_html = "\n".join(f'''          <article class="card">
            <div class="icon" aria-hidden="true">{i}</div>
            <h3>{t}</h3>
            <p>{d}</p>
            <a class="more" href="{h}">Learn more →</a>
          </article>''' for i, t, d, h in svc_cards)

home_schema_site = {
    "@context": "https://schema.org", "@type": "WebSite",
    "name": CONFIG["brand"], "url": site.url(),
    "description": "Free referral service connecting Commerce City, CO homeowners with independent water damage, mold, sewage, and fire restoration providers.",
}
home_schema_org = {
    "@context": "https://schema.org",
    **site.org(),
    "areaServed": site.area_served(),
    "knowsAbout": ["Water damage restoration", "Frozen pipe water damage", "Hail and roof leak water damage",
                   "Flooded basement cleanup", "Sewage backup cleanup", "Mold remediation", "Fire and smoke damage restoration"],
    "hasOfferCatalog": {
        "@type": "OfferCatalog", "name": "Referral services",
        "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"].replace("&amp;", "&"), "url": site.url(s["file"])}} for s in CONFIG["services"]],
    },
}

home = (site.head("Commerce City Water Damage Help | Emergency Referral, Call Any Time",
                  "Water damage, burst pipes, flooded basement, sewage, mold, or fire damage in Commerce City, CO? Call free to reach independent local restoration pros.",
                  "", [home_schema_site, home_schema_org, site.faq_schema(home_faqs)])
        + site.header("index.html")
        + f'''  <main>
    <section class="hero">
      <div class="container hero-grid">
        <div>
          <div class="hero-badge">Commerce City · Reunion · Brighton · Thornton · NE Denver</div>
          <h1>Water damage in Commerce City? One call to reach local help.</h1>
          <p class="lead">Burst pipe after a cold snap, hail-damaged roof leaking into the ceiling, or a basement full of water? We are a free referral line that connects you with an independent, licensed restoration provider in the north metro.</p>
          <div class="hero-actions">
            <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">📞 Call {PHONE_DISP}</a>
            <a class="btn btn-secondary btn-lg" href="#services">See what we cover</a>
          </div>
          <p class="hero-note">No charge to call, day or night. Which providers can respond depends on the hour and your location. We do not perform restoration work ourselves.</p>
        </div>
        <aside class="hero-card" aria-label="Common reasons to call">
          <h2>Why Commerce City homeowners call</h2>
          <ul>
            <li>Pipe burst after an arctic cold front</li>
            <li>Hail or wind damage and now the ceiling is wet</li>
            <li>Water on the basement floor after a storm</li>
            <li>Floor drain or toilet backing up sewage</li>
            <li>Musty smell or mold after an old leak</li>
            <li>Soot, smoke odor, or water after a fire</li>
          </ul>
        </aside>
      </div>
    </section>

    <section class="emergency-band" aria-label="Emergency help">
      <div class="container emergency-inner">
        <div>
          <h2>Water coming in right now? Call any time, day or night.</h2>
          <p>If it is safe, shut off the main water valve and stay away from wet outlets. Then call. Many restoration companies run 24/7 emergency crews, and we will try to connect you with one that serves your address.</p>
        </div>
        <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">🚨 Emergency: {PHONE_DISP}</a>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <h2>How the referral works</h2>
          <p>Three steps, no forms, no obligation.</p>
        </div>
        <div class="steps">
          <div class="step">
            <h3>Tell us what happened</h3>
            <p>Water, sewage, mold, or fire. Give a cross street or ZIP code in or near Commerce City.</p>
          </div>
          <div class="step">
            <h3>We connect you</h3>
            <p>Your call goes to an independent provider who handles that type of damage in the north metro, when one is available.</p>
          </div>
          <div class="step">
            <h3>You decide</h3>
            <p>Ask about inspection, drying, cleanup, and insurance paperwork. Whether you hire them, and at what price, is up to you.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section section-alt" id="services">
      <div class="container">
        <div class="section-head">
          <h2>Problems we can refer you for</h2>
          <p>One number covers water, sewage, mold, and fire damage for Commerce City-area homes.</p>
        </div>
        <div class="card-grid card-grid-3">
{cards_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <h2>What makes water damage common here</h2>
          <p>Colorado is dry most of the year, but the Front Range has its own set of water risks.</p>
        </div>
        <div class="card-grid card-grid-3">
          <div class="card">
            <h3>Hail Alley</h3>
            <p>The Rocky Mountain Insurance Information Association says the Front Range sits in the heart of “Hail Alley,” with damaging hail season running from mid-April to mid-September. Cracked shingles and torn flashing let the next rain in.</p>
          </div>
          <div class="card">
            <h3>Sudden arctic fronts</h3>
            <p>On December 21, 2022, the National Weather Service recorded a 37°F drop in one hour at Denver International Airport, just northeast of Commerce City. Swings like that catch pipes in garages and outside walls.</p>
          </div>
          <div class="card">
            <h3>Sprinkler and hose bib freezes</h3>
            <p>Irrigation lines, backflow preventers, and outdoor faucets with a hose still attached can split in the first hard freeze and leak inside the wall.</p>
          </div>
          <div class="card">
            <h3>Basements</h3>
            <p>Many north metro homes have basements. A failed sump pump, a clogged window well, or an overwhelmed drain can put water on finished floors fast.</p>
          </div>
          <div class="card">
            <h3>Creeks and the South Platte</h3>
            <p>Sand Creek, First Creek, and Second Creek all drain through Commerce City toward the South Platte River. Homes near them can check their flood zone on the Mile High Flood District or FEMA maps.</p>
          </div>
          <div class="card">
            <h3>Leaks that linger</h3>
            <p>Dry air helps surfaces look dry quickly, but water trapped in carpet pad, framing, and drywall can still turn into odor and mold.</p>
          </div>
        </div>
        <p class="source-note">Sources: Rocky Mountain Insurance Information Association (hail season); NWS Boulder December 2022 climate summary (temperature drop); Mile High Flood District and city drainage studies (creeks).</p>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <div class="section-head">
          <h2>Areas we focus on</h2>
          <p>Commerce City and nearby Adams County and northeast Denver communities.</p>
        </div>
        <ul class="area-list">
          <li>Commerce City</li>
          <li>Reunion</li>
          <li>Turnberry</li>
          <li>Belle Creek</li>
          <li>Buffalo Run</li>
          <li>Brighton</li>
          <li>Thornton</li>
          <li>Henderson</li>
          <li>Northglenn</li>
          <li>Northeast Denver</li>
        </ul>
        <p><a href="service-areas.html">Full service area details →</a></p>
      </div>
    </section>

    <section class="section" id="faq">
      <div class="container">
        <div class="section-head">
          <h2>Frequently asked questions</h2>
        </div>
        <div class="faq">
{site.faq_html(home_faqs)}
        </div>
      </div>
    </section>

    <section class="cta-band">
      <div class="container">
        <h2>Talk with someone about your damage today</h2>
        <p>Call the free Commerce City referral line. We will try to connect you with an independent local provider.</p>
        <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
      </div>
    </section>
  </main>
'''
        + site.footer())
site.raw_page("index.html", home, "monthly", "1.0")

# ======================= SERVICE PAGES =======================
site.service_page({
    "file": "water-damage-restoration.html",
    "title": "Water Damage Restoration Referral | Commerce City, CO",
    "meta": "Leak or standing water in your Commerce City home? Call free to connect with independent water damage restoration providers in the north metro.",
    "crumb": "Water Damage Restoration",
    "h1": "Water Damage Restoration in Commerce City",
    "lead": "The first day after a leak decides how much of your floor, drywall, and cabinets can be saved. Our free line connects Commerce City homeowners with independent restoration providers who extract water and dry the structure.",
    "schema_name": "Water Damage Restoration Referral",
    "service_type": "Water damage restoration",
    "schema_desc": "Free referral connecting Commerce City, Colorado homeowners with independent water damage restoration providers.",
    "prio": "0.9",
    "body": '''          <p>Most water damage in Commerce City does not come from a river. It comes from a washing machine hose that let go, a water heater that finally rusted through in the basement, an ice maker line behind the fridge, or a toilet supply line under a bathroom vanity. Water from those sources is usually clean when it starts, but it travels under baseboards and into the subfloor faster than most people expect.</p>

          <h2>What a restoration provider usually does</h2>
          <p>Independent restoration companies generally follow the same order of work, adjusted to your home:</p>
          <ol>
            <li><strong>Stop and assess.</strong> Confirm the source is off and map where moisture went using meters and, often, thermal cameras.</li>
            <li><strong>Extract.</strong> Pull standing water out of carpet, pad, and hard floors.</li>
            <li><strong>Remove what can’t be saved.</strong> Wet carpet pad, swollen particleboard, and the bottom of soaked drywall are common cuts.</li>
            <li><strong>Dry.</strong> Set air movers and dehumidifiers and take readings until materials reach normal moisture levels.</li>
            <li><strong>Document.</strong> Photos and moisture logs that insurers commonly ask for.</li>
          </ol>

          <h2>Why “looks dry” is not the same as dry</h2>
          <p>Colorado air is dry, so carpet and painted walls can feel normal within a day or two. The water underneath, in pad, tack strip, bottom plates, and wall cavities, takes much longer. That hidden moisture is what leads to odor, warped floors, and <a href="mold-remediation.html">mold</a> weeks later. It is fair to ask any provider how they will measure dryness and when they will remove the equipment.</p>

          <h2>Clean water, gray water, and black water</h2>
          <p>Providers sort water by contamination. A supply line break is usually clean. Dishwasher or washing machine discharge is “gray.” Anything that came up through a floor drain or toilet is treated as contaminated and needs a different process; see our <a href="sewage-backup-cleanup.html">sewage backup cleanup</a> page. Tell the person you talk to where the water came from so they can plan correctly.</p>

          <h2>Homes across the city</h2>
          <p>Whether you are in an older home in the south end near Derby and Rose Hill or a newer build in Reunion, Turnberry, or Belle Creek, the first steps are the same: stop the water, keep people away from wet electrical, take photos, and get the drying started.</p>

          <h2>What you can do right now</h2>
          <ul>
            <li>Shut off the fixture valve or the main shutoff, often in the basement or near the water heater.</li>
            <li>Turn off breakers to wet areas if you can reach the panel without standing in water.</li>
            <li>Lift furniture onto foil or blocks and move rugs, papers, and electronics out.</li>
            <li>Photograph everything before anything is thrown away.</li>
            <li>Call {CALL} for a free referral to a provider who can come assess it.</li>
          </ul>
          <p>Water came from a pipe that froze? See <a href="burst-frozen-pipes.html">burst and frozen pipes</a>. Came through the roof during a storm? See <a href="storm-roof-leak-damage.html">hail, storm, and roof leaks</a>.</p>
''',
    "faqs": [
        ("How fast should drying start?",
         "As soon as possible. Many providers aim to start extraction and drying the same day because materials that stay wet longer are more likely to need replacement."),
        ("Do you fix the pipe too?",
         "No. Restoration companies handle the water damage. A licensed plumber usually repairs the pipe or appliance connection. Ask who handles each part of the job."),
    ],
})

site.service_page({
    "file": "burst-frozen-pipes.html",
    "title": "Burst & Frozen Pipe Water Damage | Commerce City Referral",
    "meta": "Pipe froze and burst in your Commerce City home? Get a free referral to independent providers who dry out walls, floors, and basements after a pipe break.",
    "crumb": "Burst &amp; Frozen Pipes",
    "h1": "Burst &amp; Frozen Pipe Water Damage",
    "lead": "Front Range cold fronts can arrive in minutes. When a frozen pipe splits, it usually leaks inside a wall or ceiling. We connect Commerce City homeowners with independent providers who handle the cleanup and drying.",
    "schema_name": "Burst and Frozen Pipe Water Damage Referral",
    "service_type": "Frozen and burst pipe water damage restoration",
    "schema_desc": "Free referral for burst and frozen pipe water damage help in Commerce City, Colorado.",
    "side_h": "Pipe just burst?",
    "side_p": "Shut off the main water valve first, then call.",
    "body": '''          <p>Denver-area winters can be mild one day and brutal the next. On December 21, 2022, an arctic front dropped the temperature at Denver International Airport, just northeast of Commerce City, by 37 degrees in a single hour, according to the National Weather Service in Boulder. Pipes that were fine at lunch can freeze by dinner when that happens.</p>

          <h2>Where pipes freeze in north metro homes</h2>
          <ul>
            <li><strong>Outdoor faucets (hose bibs).</strong> A “frost-free” faucet can still split inside the wall if a hose is left connected and water can’t drain out.</li>
            <li><strong>Sprinkler systems.</strong> Backflow preventers and lines that were not blown out before the first hard freeze often crack.</li>
            <li><strong>Garages and exterior walls.</strong> Pipes running to a garage sink, laundry, or a kitchen on an outside wall.</li>
            <li><strong>Crawl spaces and unheated basements</strong>, especially near rim joists where cold air leaks in.</li>
            <li><strong>Vacant or vacation homes</strong> where the heat was turned down too far.</li>
          </ul>

          <h2>Why the leak often shows up later</h2>
          <p>Ice in a pipe can hold back the water. The real flood often starts when temperatures rise and the ice melts, sometimes days after the cold snap. If you notice low water pressure during a freeze, a hissing sound, a wet ceiling stain, or water at the base of a wall, shut off the main and look for the break before it thaws fully.</p>

          <h2>First steps after a pipe bursts</h2>
          <ol>
            <li>Close the main shutoff. In many homes here it is in the basement, crawl space, or near the water heater.</li>
            <li>Open a faucet at the lowest point of the house to drain the lines.</li>
            <li>Keep away from water near outlets, the electrical panel, or ceiling lights.</li>
            <li>Take photos and video of the damage and the broken pipe if you can see it.</li>
            <li>Call a plumber for the repair, and call {CALL} for a referral to a provider who handles the water damage side.</li>
          </ol>

          <h2>What the cleanup usually involves</h2>
          <p>Burst pipes often soak areas you can’t see: the inside of walls, the top of a ceiling below a bathroom, or the subfloor under laminate. Restoration providers typically open small sections of drywall to let cavities dry, extract water from flooring, and set drying equipment with daily moisture readings. Ask how they plan to dry inside walls without tearing out more than needed.</p>

          <h2>Prevention for next winter</h2>
          <ul>
            <li>Disconnect hoses and have the sprinkler system blown out before the first freeze.</li>
            <li>Open cabinet doors under sinks on outside walls during cold snaps.</li>
            <li>Let a faucet drip on the coldest nights.</li>
            <li>Keep the heat on (many people use 55°F or higher) if you travel.</li>
            <li>Seal drafts near pipes in the garage and rim joists.</li>
          </ul>
          <p class="source-note">Source: National Weather Service Boulder, December 2022 climate summary.</p>
          <p>Related: <a href="water-damage-restoration.html">water damage restoration</a>, <a href="flooded-basement-cleanup.html">flooded basement cleanup</a>, and <a href="mold-remediation.html">mold remediation</a> if the leak went unnoticed for a while.</p>
''',
    "faqs": [
        ("Is a burst pipe usually covered by homeowners insurance?",
         "Policies vary. Sudden pipe bursts are often treated differently than slow leaks or damage from a home left without heat. Check your own policy and talk to your insurer."),
        ("Should I use a hair dryer on a frozen pipe?",
         "If you can reach the pipe safely and there is no standing water, gentle heat is a common approach. Never use an open flame. If you are unsure, call a plumber."),
    ],
})

site.service_page({
    "file": "storm-roof-leak-damage.html",
    "title": "Hail & Roof Leak Water Damage Help | Commerce City, CO",
    "meta": "Hail or wind damaged your roof and now water is coming in? Commerce City homeowners can call free to reach independent storm water damage providers.",
    "crumb": "Hail, Storm &amp; Roof Leaks",
    "h1": "Hail, Storm &amp; Roof Leak Water Damage",
    "lead": "Hail rarely floods a house by itself. The damage shows up when the next storm finds the cracked shingle or torn flashing. We connect Commerce City homeowners with independent providers who dry out ceilings, attics, and walls after storm leaks.",
    "schema_name": "Storm and Roof Leak Water Damage Referral",
    "service_type": "Storm and roof leak water damage restoration",
    "schema_desc": "Free referral for hail, storm, and roof leak water damage help in Commerce City, Colorado.",
    "side_h": "Ceiling leaking?",
    "side_p": "Catch the drip, keep clear of light fixtures, then call.",
    "body": '''          <p>According to the Rocky Mountain Insurance Information Association, Colorado’s Front Range sits in the heart of “Hail Alley,” and the damaging hail season runs from about mid-April to mid-September. Afternoon thunderstorms in the north metro can bring hail, strong wind, and heavy rain in the same short burst.</p>

          <h2>How storm water gets inside</h2>
          <ul>
            <li>Hail-cracked or bruised shingles and broken ridge caps</li>
            <li>Lifted flashing around chimneys, vents, and skylights</li>
            <li>Wind-blown rain pushed past window and door seals</li>
            <li>Gutters packed with hail and debris that overflow against the fascia</li>
            <li>Broken skylights or vent caps</li>
            <li>Downspouts dumping next to the foundation and into window wells (see <a href="flooded-basement-cleanup.html">flooded basements</a>)</li>
          </ul>

          <h2>Signs of a roof leak</h2>
          <p>Brown rings on the ceiling, bubbling paint, a sagging spot in the drywall, damp attic insulation, or a drip from a light fixture or smoke detector. In attics, wet insulation loses its value and can hold moisture against the drywall below.</p>

          <h2>Two different jobs: the roof and the inside</h2>
          <p>A roofer stops the water from getting in. A restoration provider deals with what already got in: wet insulation, ceiling drywall, framing, and anything below. Many homeowners need both. If a tarp is needed before the roof can be repaired, ask who will install it and how quickly.</p>

          <h2>What to do during and after a storm</h2>
          <ol>
            <li>Put a bucket under drips. If a ceiling is bulging with water, keep people out from under it.</li>
            <li>Turn off power to any light fixture or fan that is leaking.</li>
            <li>Photograph the ceiling, attic, and outside of the home (hail on the ground, dented gutters) for your records.</li>
            <li>Watch out for storm-chasing contractors who knock on doors right after a hailstorm. Verify any company before signing.</li>
            <li>Call {CALL} to get connected with a provider for the interior water damage.</li>
          </ol>

          <h2>Insurance tips after hail</h2>
          <p>Hail and wind claims are common in Colorado. Insurers generally expect you to take reasonable steps to prevent further damage, like tarping and drying, so do not wait on the inside cleanup while the roof claim is sorted out. Keep receipts and photos. Your own policy and adjuster have the final word on coverage.</p>
          <p class="source-note">Source: Rocky Mountain Insurance Information Association, hail statistics.</p>
          <p>Related: <a href="water-damage-restoration.html">water damage restoration</a> and <a href="mold-remediation.html">mold remediation</a> if attic or ceiling materials stayed wet.</p>
''',
    "faqs": [
        ("Do you do roof repairs?",
         "No. We are a referral service focused on the water damage inside your home. You will need a roofer for the roof itself."),
        ("Can a small ceiling stain wait?",
         "A stain means water reached the drywall. It is worth having someone check the attic and insulation before the next storm adds more."),
    ],
})

site.service_page({
    "file": "flooded-basement-cleanup.html",
    "title": "Flooded Basement & Sump Pump Cleanup | Commerce City Referral",
    "meta": "Water in your Commerce City basement from a sump pump failure, window well, or storm? Call free to connect with independent flooded basement cleanup providers.",
    "crumb": "Flooded Basement &amp; Sump Pump",
    "h1": "Flooded Basement &amp; Sump Pump Failure Cleanup",
    "lead": "Basements are where water ends up. Whether it came from a failed sump pump, a filled window well, or a water heater, we can connect you with an independent provider who pumps it out and dries the space.",
    "schema_name": "Flooded Basement and Sump Pump Failure Cleanup Referral",
    "service_type": "Flooded basement water removal and cleanup",
    "schema_desc": "Free referral for flooded basement and sump pump failure cleanup in Commerce City, Colorado.",
    "side_h": "Water on the basement floor?",
    "side_p": "Stay out if outlets or the panel are near the water. Call us.",
    "body": '''          <p>A lot of Commerce City homes, from older ranches to newer two-stories in the northern subdivisions, have basements, and many of those basements are finished with carpet, drywall, and a bedroom or family room. That makes basement water expensive: it soaks the carpet pad, wicks up the drywall, and reaches the furnace and water heater.</p>

          <h2>Common reasons basements flood here</h2>
          <ul>
            <li><strong>Sump pump failure.</strong> A worn-out pump, a stuck float switch, or a power outage during a summer thunderstorm.</li>
            <li><strong>Window wells.</strong> Uncovered wells fill with hail, leaves, and rain, then leak through the window.</li>
            <li><strong>Downspouts and grading.</strong> Roof water dumped next to the foundation, or soil that settled and now slopes toward the house.</li>
            <li><strong>Water heaters and softeners.</strong> Usually in the basement, so a tank failure goes straight to the floor.</li>
            <li><strong>Frozen pipe bursts</strong> in a basement ceiling or rim joist. See <a href="burst-frozen-pipes.html">burst and frozen pipes</a>.</li>
            <li><strong>Floor drain backups.</strong> If the water came up through the floor drain, treat it as sewage; see <a href="sewage-backup-cleanup.html">sewage backup cleanup</a>.</li>
          </ul>

          <h2>Safety before anything else</h2>
          <p>Do not walk into a basement with standing water if outlets, extension cords, the furnace, or the electrical panel are wet or close to the water. If you cannot reach the main breaker without stepping in water, wait for a professional or your utility. Gas appliances that were submerged should be checked before they are used again.</p>

          <h2>What basement cleanup usually involves</h2>
          <ul>
            <li>Pumping out standing water and extracting carpet</li>
            <li>Pulling wet carpet pad (it rarely dries well in place)</li>
            <li>Cutting the bottom of wet drywall and removing wet insulation</li>
            <li>Drying the concrete, framing, and any remaining materials with dehumidifiers</li>
            <li>Checking the sump pit, pump, and check valve, and recommending a plumber or waterproofer if needed</li>
          </ul>

          <h2>Keep your sump pump ready</h2>
          <p>Pour a bucket of water into the pit every few months to make sure the pump turns on and shuts off. Pumps wear out, so many homeowners plan on replacing theirs every several years and add a battery backup and a high-water alarm. Make sure the discharge line is clear, points away from the house, and is not frozen in winter.</p>

          <h2>Near Sand Creek, First Creek, or Second Creek?</h2>
          <p>If your home is near one of the creeks that drain through Commerce City toward the South Platte River, you can look up your flood zone on the Mile High Flood District floodplain viewer or FEMA’s Flood Map Service Center. Standard homeowners policies typically do not cover flooding from outside water; that usually requires separate flood insurance.</p>

          <h2>Get a referral</h2>
          <p>Call {CALL}. Tell us where the water came from, how deep it is, and whether the basement is finished. We will try to connect you with an independent provider who serves your area.</p>
''',
    "faqs": [
        ("Can I just use a shop vac?",
         "For a small amount of clean water on concrete, maybe. Once carpet, pad, or drywall is wet, professional drying equipment is usually needed to prevent odor and mold."),
        ("Does insurance cover a sump pump failure?",
         "Many policies only cover sump or drain backup if you added that endorsement. Check your policy or ask your agent."),
    ],
})

site.service_page({
    "file": "sewage-backup-cleanup.html",
    "title": "Sewage Backup Cleanup Referral | Commerce City, CO",
    "meta": "Sewage backing up through a floor drain, toilet, or tub in Commerce City? Call free to connect with independent sewage cleanup and sanitizing providers.",
    "crumb": "Sewage Backup Cleanup",
    "h1": "Sewage Backup Cleanup in Commerce City",
    "lead": "Sewage is the one kind of water damage you should not clean up yourself. We connect Commerce City homeowners with independent providers equipped to remove contaminated water and sanitize the area.",
    "schema_name": "Sewage Backup Cleanup Referral",
    "service_type": "Sewage backup cleanup and sanitization",
    "schema_desc": "Free referral for sewage backup cleanup in Commerce City, Colorado.",
    "side_h": "Sewage on the floor?",
    "side_p": "Stop using water in the house, keep kids and pets away, and call.",
    "body": '''          <p>A sewage backup usually shows up at the lowest drain in the house: the basement floor drain, a basement shower, or the lowest toilet. It can be a slow seep or several inches of water in minutes. Either way, the water carries bacteria and other contaminants, and anything porous it touched (carpet, pad, drywall, insulation) is usually removed rather than cleaned.</p>

          <h2>Common causes</h2>
          <ul>
            <li>Tree roots growing into an older clay or cast-iron sewer lateral</li>
            <li>Grease, wipes (even ones labeled “flushable”), and other debris clogging the line</li>
            <li>A sagging or broken section of the line between the house and the city main</li>
            <li>Heavy storm water getting into the sewer system and overloading it</li>
            <li>A failed sewage ejector pump in a basement bathroom</li>
          </ul>

          <h2>What to do right now</h2>
          <ol>
            <li>Stop running water: no flushing, laundry, dishwasher, or showers until the line is cleared.</li>
            <li>Keep children, pets, and anyone with health concerns away from the area.</li>
            <li>Do not touch the water without gloves and boots. Wash thoroughly if you do.</li>
            <li>Turn off power to the area if you can do it without stepping in water.</li>
            <li>Call a plumber or sewer service to clear the line, and call {CALL} for a referral to a cleanup provider.</li>
          </ol>

          <h2>What professional sewage cleanup involves</h2>
          <p>Providers typically wear protective gear, extract the contaminated water, remove affected porous materials, clean and disinfect hard surfaces, and then dry the area. Some also run air scrubbers to deal with odor. Because the water is contaminated, the industry generally treats it as the highest risk category, which changes what can be saved.</p>

          <h2>Whose line is it?</h2>
          <p>In general, the homeowner is responsible for the sewer lateral that runs from the house to the public main, and the local sanitation district handles the main itself. If you think the backup came from the main, call the sanitation or water district listed on your utility bill. A camera inspection by a plumber can show where the blockage is.</p>

          <h2>Prevent the next one</h2>
          <ul>
            <li>Ask a plumber about a backwater valve on the main line.</li>
            <li>Keep grease and wipes out of drains.</li>
            <li>Have older lines scoped if you have repeated slow drains or gurgling.</li>
            <li>Check your insurance for a sewer or drain backup endorsement; many basic policies exclude it.</li>
          </ul>
          <p>Related: <a href="flooded-basement-cleanup.html">flooded basement cleanup</a> and <a href="mold-remediation.html">mold remediation</a>.</p>
''',
    "faqs": [
        ("Can I clean up a small sewage backup myself?",
         "A very small amount on a hard, non-porous floor is sometimes handled by homeowners with gloves and disinfectant. Anything on carpet, drywall, or larger areas should be handled by a professional."),
        ("Will the smell go away on its own?",
         "Not usually, if contaminated materials are left in place. Removing affected materials and drying the area is what removes the source of the odor."),
    ],
})

site.service_page({
    "file": "mold-remediation.html",
    "title": "Mold Remediation Referral | Commerce City, CO",
    "meta": "Musty smell or visible mold after a leak in your Commerce City home? Call free to connect with independent mold remediation providers.",
    "crumb": "Mold Remediation",
    "h1": "Mold Remediation After Water Damage",
    "lead": "Colorado’s dry air doesn’t stop mold from growing behind a wall that stayed wet. If you have a musty smell, visible growth, or a leak that went unnoticed, we can connect you with an independent mold remediation provider.",
    "schema_name": "Mold Remediation Referral",
    "service_type": "Mold remediation",
    "schema_desc": "Free referral connecting callers with independent mold remediation providers in Commerce City, Colorado.",
    "body": '''          <p>Outdoor humidity in the Denver area is low much of the year, so people are often surprised to find mold. Indoors, though, mold needs only a steady moisture source: a slow drip under a sink, a basement that took on water, a bathroom without a working fan, or attic insulation that got wet during a hailstorm. Hidden spaces like wall cavities and under flooring are where it usually starts.</p>

          <h2>Signs worth checking</h2>
          <ul>
            <li>A musty, earthy odor in a basement, closet, or bathroom</li>
            <li>Spotting or discoloration on drywall, baseboards, or ceilings</li>
            <li>Peeling paint or warped trim near a past leak</li>
            <li>Growth on the back of carpet or pad after a basement flood</li>
            <li>Stains in the attic after a roof leak</li>
          </ul>

          <h2>What remediation generally involves</h2>
          <p>Independent providers usually start by finding and stopping the moisture source, because mold will return if the water does. Depending on the size of the area, they may set up containment to keep spores and dust from spreading, remove affected porous materials like drywall and insulation, clean framing and other surfaces, and dry everything before walls are closed up. Some homeowners also choose independent testing before or after the work.</p>

          <h2>Good questions to ask a provider</h2>
          <ul>
            <li>What caused the moisture, and has it been fixed?</li>
            <li>How will you contain the work area?</li>
            <li>What materials will be removed, and what will be cleaned?</li>
            <li>What training or certifications does your crew have (for example, IICRC)?</li>
            <li>How will you confirm the area is dry before rebuilding?</li>
          </ul>

          <h2>What we will not claim</h2>
          <p>We do not diagnose health conditions, promise a “mold-free” home, or interpret lab results. If you have health concerns, talk to a medical professional. Our role is to connect you with a provider who can assess the home itself.</p>

          <h2>Mold usually starts with water</h2>
          <p>Most mold calls trace back to something on this site: a <a href="burst-frozen-pipes.html">frozen pipe</a> that leaked inside a wall, a <a href="storm-roof-leak-damage.html">roof leak after hail</a>, or a <a href="flooded-basement-cleanup.html">basement that took on water</a>. If you still have active water, start there.</p>

          <h2>Request a referral</h2>
          <p>Call {CALL}. There is no fee to use this line. We will try to connect you with an independent mold remediation provider serving Commerce City and the north metro.</p>
''',
    "faqs": [
        ("Is bleach enough?",
         "On small areas of hard, non-porous surfaces it may help, but it does not fix the moisture problem and is not recommended for porous materials like drywall. Larger areas should be assessed by a professional."),
        ("How big an area needs a professional?",
         "Guidance from the U.S. EPA suggests that areas larger than about 10 square feet, or any mold tied to sewage or contaminated water, are good candidates for professional help."),
    ],
})

site.service_page({
    "file": "fire-smoke-damage.html",
    "title": "Fire & Smoke Damage Restoration Referral | Commerce City",
    "meta": "Kitchen fire, soot, smoke odor, or water damage from firefighting in Commerce City? Call free to connect with independent fire and smoke restoration providers.",
    "crumb": "Fire &amp; Smoke Damage",
    "h1": "Fire &amp; Smoke Damage Restoration",
    "lead": "After a fire, the smoke, soot, and water from putting it out often cause more damage than the flames. We connect Commerce City homeowners with independent providers who clean, deodorize, and dry fire-damaged homes.",
    "schema_name": "Fire and Smoke Damage Restoration Referral",
    "service_type": "Fire and smoke damage restoration",
    "schema_desc": "Free referral for fire, smoke, and soot damage restoration in Commerce City, Colorado.",
    "side_h": "Had a fire?",
    "side_p": "Make sure the fire department has cleared the home, then call.",
    "body": '''          <p><strong>If there is an active fire, call 911 first.</strong> This page is for what comes after: once the fire is out and the fire department says the home is safe to enter.</p>

          <p>Even a small kitchen or dryer fire can spread soot through the HVAC system and leave smoke odor in carpet, cabinets, and clothing. Larger fires add a second problem: water. Hoses and sprinklers can soak floors, walls, and the basement below, and that water needs the same fast drying as any other <a href="water-damage-restoration.html">water damage</a>.</p>

          <h2>What fire restoration usually covers</h2>
          <ul>
            <li>Boarding up broken windows or tarping a damaged roof</li>
            <li>Removing water left by firefighting and drying the structure</li>
            <li>Soot cleanup on walls, ceilings, cabinets, and contents</li>
            <li>Odor treatment, which may include air scrubbers or other deodorizing methods</li>
            <li>Cleaning or replacing HVAC filters and, when needed, duct cleaning</li>
            <li>Inventory and pack-out of belongings for cleaning</li>
          </ul>

          <h2>Wildfire smoke on the Front Range</h2>
          <p>Colorado has seen how quickly fire can reach suburbs. The Marshall Fire in Boulder County in December 2021 destroyed more than a thousand homes. Even homes that are not touched by flames can pick up smoke odor and fine ash during regional wildfires. If smoke got inside your home, a restoration provider can assess cleaning and odor treatment.</p>

          <h2>Do’s and don’ts after a fire</h2>
          <ul>
            <li><strong>Do</strong> wait for the fire department to say the home is safe.</li>
            <li><strong>Do</strong> photograph damage before cleaning anything.</li>
            <li><strong>Do</strong> contact your insurer early; fire losses usually involve an adjuster.</li>
            <li><strong>Don’t</strong> wipe soot off walls with a wet rag; it can smear and set the stain.</li>
            <li><strong>Don’t</strong> run the HVAC system until filters and ducts are checked.</li>
            <li><strong>Don’t</strong> eat food or use medicine that was exposed to heat, smoke, or soot.</li>
          </ul>

          <h2>Get a referral</h2>
          <p>Call {CALL}. Tell us what burned, how much of the home has smoke or soot, and whether water was used to put it out. We will try to connect you with an independent fire restoration provider. Lingering moisture after a fire can also lead to <a href="mold-remediation.html">mold</a>, so ask about drying too.</p>
''',
    "faqs": [
        ("Can smoke odor be removed?",
         "Often, yes, but it usually takes more than air fresheners. Providers clean soot from surfaces and use deodorizing equipment. Some heavily affected materials need to be replaced."),
        ("Why is there water damage after a fire?",
         "Firefighting water and sprinkler systems can soak a home. That water needs to be extracted and dried quickly like any other water loss."),
    ],
})

# ======================= SERVICE AREAS =======================
areas_inner = '''          <p>When you call, tell us your neighborhood, a cross street, or your ZIP code. We use that to try to connect you with an independent provider who works in your area.</p>

          <h2>Commerce City</h2>
          <p>Commerce City is our main focus. Most of the city is in ZIP codes <strong>80022</strong> and <strong>80640</strong>, with some northern neighborhoods in 80603 and 80601. You do not need to know the neighborhood name; a cross street works.</p>
          <ul class="area-list">
            <li>Reunion</li>
            <li>Turnberry</li>
            <li>Belle Creek</li>
            <li>Buffalo Run</li>
            <li>River Run</li>
            <li>Dunes Park</li>
            <li>Second Creek</li>
            <li>Eagle Creek</li>
            <li>Derby</li>
            <li>Rose Hill</li>
            <li>Irondale</li>
            <li>Fairfax Park</li>
          </ul>

          <h2>Nearby communities</h2>
          <ul class="area-list">
            <li>Brighton</li>
            <li>Thornton</li>
            <li>Henderson</li>
            <li>Northglenn</li>
            <li>Welby</li>
            <li>Northeast Denver</li>
            <li>Montbello</li>
            <li>Green Valley Ranch</li>
          </ul>

          <h2>Older south end, newer north side</h2>
          <p>The south end of the city around Derby, Rose Hill, and Adams City has many older homes, where aging supply lines, water heaters, and sewer laterals are common sources of trouble. The newer master-planned neighborhoods north of 96th Avenue, like Reunion, Turnberry, and Buffalo Run, have newer plumbing, but basements, sump pumps, sprinkler systems, and roofs still face the same storms and cold snaps. We take calls from both.</p>

          <h2>What “service area” means for a referral line</h2>
          <p>We are not a contractor with trucks. The independent provider you talk with sets their own travel area, schedule, and prices. If one provider cannot take your job, you can ask about other options when you call.</p>

          <h2>Outside these areas?</h2>
          <p>If you are elsewhere in the Denver metro, you are still welcome to call. We will tell you honestly if we cannot connect you with someone for your location.</p>

          <div class="notice">
            <strong>Note:</strong> Listing a neighborhood here does not guarantee a provider is available the moment you call. Availability depends on the independent companies participating at that time.
          </div>'''
site.simple_page("service-areas.html", "Service Areas | Commerce City Water Damage Referral",
                 "Free water damage referral for Commerce City (80022, 80640), Reunion, Turnberry, Belle Creek, Brighton, Thornton, Henderson, and northeast Denver.",
                 "Service Areas", "Service Areas",
                 "Our free referral line focuses on Commerce City and nearby Adams County and northeast Denver communities. Provider availability can vary by day and exact location.",
                 areas_inner, prio="0.7", freq="monthly", with_side=True,
                 side_h="Call for your area", side_p="Commerce City &amp; the north metro")

# ======================= ABOUT =======================
about_inner = '''        <h2>Who we are</h2>
        <p>Commerce City Water Damage is a <strong>free referral / connection service</strong>. We are not a restoration contractor, mold remediator, fire restoration company, plumber, roofer, or insurance agency. We do not send crews, file insurance claims for you, or perform cleanup work.</p>
        <p>When you call {CALL}, your call may be connected or forwarded to an independent, licensed service provider who works in or near your area. That provider is a separate business, and any agreement you make is between you and them.</p>

        <h2>Why a referral line?</h2>
        <p>When a pipe bursts at night or a hailstorm opens up your ceiling, searching online is the last thing you want to do. Results mix national call centers, ads, and local companies without saying who will actually show up. We wanted one plain number for Commerce City-area homeowners to call about water, sewage, mold, or fire damage, with honest information about how it works.</p>

        <h2>What we provide</h2>
        <ul>
          <li>Plain-language pages about common types of damage in north metro homes</li>
          <li>A phone number you can call for a referral connection</li>
          <li>Clear disclosure that we are not the contractor</li>
        </ul>

        <h2>What we do not provide</h2>
        <ul>
          <li>On-site restoration, construction, roofing, plumbing, or mold removal</li>
          <li>Guarantees about response time, pricing, or insurance coverage</li>
          <li>Medical advice about mold, sewage, or smoke exposure</li>
          <li>A walk-in office</li>
        </ul>

        <h2>Honesty matters</h2>
        <p>We do not invent reviews, licenses, certifications, or years in business for this site, and we do not use another company’s name or address. Ask any provider you speak with directly about their credentials, insurance, and experience.</p>

        <h2>Questions about the site?</h2>
        <p>For referral calls, use {CALL}. For website or privacy questions, see our <a href="contact.html">Contact</a>, <a href="privacy.html">Privacy Policy</a>, and <a href="terms.html">Terms of Use</a> pages.</p>'''
site.simple_page("about.html", "About This Referral Service | Commerce City Water Damage",
                 "How the free Commerce City water damage referral line works, and what it does and does not provide.",
                 "About", "About This Referral Service",
                 "This site exists to give Commerce City homeowners one clear next step after water, sewage, mold, or fire damage: a phone call with an independent local provider.",
                 about_inner, prio="0.5")

# ======================= CONTACT =======================
contact_inner = f'''        <div class="card" style="text-align:center;padding:2.5rem 1.5rem">
          <h2 class="mt-0">Free referral line</h2>
          <p>For water damage, burst or frozen pipes, storm and roof leaks, flooded basements, sewage backups, mold, or fire and smoke damage in the Commerce City area:</p>
          <p style="font-size:1.75rem;font-weight:800;margin:1rem 0">
            <a class="phone-link" href="tel:{PHONE_TEL}">{PHONE_DISP}</a>
          </p>
          <a class="btn btn-primary btn-lg" href="tel:{PHONE_TEL}">Call {PHONE_DISP}</a>
          <p class="muted" style="margin-top:1.5rem;margin-bottom:0">On a phone, tap the button to dial.</p>
        </div>
        <div class="notice" style="margin-top:1.5rem">
          <strong>Reminder:</strong> This is a referral connection service. Calls may be forwarded to an independent provider. There is no walk-in office.
        </div>
        <h2>Before you call, it helps to know</h2>
        <ul>
          <li>Your address or nearest cross street and ZIP code</li>
          <li>What caused the problem, if you know (pipe, roof, sump, drain, fire)</li>
          <li>Which rooms or floors are affected, and whether the basement is finished</li>
          <li>Whether water is still coming in, and whether it could be sewage</li>
        </ul>'''
site.simple_page("contact.html", "Contact | Commerce City Water Damage Referral",
                 "Call the free Commerce City water damage referral line. Phone only, no form to fill out.",
                 "Contact", "Contact",
                 "The fastest way to reach us is by phone. There is no contact form on this site.",
                 contact_inner, prio="0.6")

site.legal_pages("November 11, 2026")
site.write()
