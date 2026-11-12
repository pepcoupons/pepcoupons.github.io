import json, os, html, datetime
BASE = "https://pepcoupons.site"
EMAIL = "hello@pepcoupons.site"   # change to your real email address
DEMO = True                      # set False once real, checked codes are in data/vendors.json
TODAY = datetime.date.today().isoformat()
H = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(H + "/data/vendors.json", encoding="utf-8"))
V.sort(key=lambda v: (v["status"] == "expired", -v["discount"]))
e = html.escape

import re
def rel(p, s):
    pre = "../" * p.count("/") if "/" in p else "./"
    return re.sub(r'(href|src)="/', lambda m: m.group(1) + '="' + pre, s)

def w(p, s, raw=False):
    if p.endswith(".html") and not raw: s = rel(p, s)
    f = H + "/" + p
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, "w", encoding="utf-8").write(s)

def ld(*items):
    s = json.dumps([dict({"@context": "https://schema.org"}, **i) for i in items], ensure_ascii=False)
    return '<script type="application/ld+json">' + s.replace("</", "<\\/") + "</script>"

LOGO = '<svg viewBox="0 0 100 100" aria-hidden="true"><rect class="lb" width="100" height="100" rx="22"/><g transform="translate(-1.910 0.452) scale(0.07742)"><path fill="#fff" d="M383,285L787,285C936.7,285 1058,398.7 1058,539C1058,679.3 936.7,793 787,793L560,793C591,703 693,630 783,630C837.7,630 882,585.7 882,531C882,476.3 837.7,432 783,432L620,432C520,432 440,480 383,582Z"/><path fill="#ffb627" d="M284,995C395,990 450,920 498,799C547,681 627,628 745,596C581,511 366,567 299,750C290,775 284,795 284,818L284,995Z"/></g></svg>'

def head(t, d, p, schema):
    u = BASE + p
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    f'<title>{e(t)}</title><meta name="description" content="{e(d)}"><link rel="canonical" href="{u}">'
    '<meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="website"><meta property="og:site_name" content="PepCoupons">'
    f'<meta property="og:title" content="{e(t)}"><meta property="og:description" content="{e(d)}"><meta property="og:url" content="{u}"><meta property="og:image" content="{BASE}/og-image.png"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/og-image.png">'
    '<meta name="theme-color" content="#0b4f4a"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap">'
    f'<link rel="stylesheet" href="/style.css">{schema}</head>')

def header():
    return ('<header><div class="w"><nav aria-label="Main"><a class="logo" href="/">' + LOGO + '<span>Pep<em>Coupons</em></span></a>'
            '<a href="/coupons/">Coupons</a><a href="/compare/">Compare</a><a href="/how-we-pick/">How we pick</a><a href="/faq/">FAQ</a><a href="/about/">About</a></nav></div></header>')

def footer():
    def col(t, links): return f'<nav aria-label="{t}"><b>{t}</b>' + "".join(f'<a href="{h}">{n}</a>' for h, n in links) + '</nav>'
    return ('<footer><div class="w"><div class="fg"><div class="fb"><a class="logo" href="/">' + LOGO + '<span>Pep<em>Coupons</em></span></a><p>Compare peptide vendor discount codes in one place.</p></div><div class="fcols">'
            + col("Explore", [("/", "Home"), ("/coupons/", "Coupons"), ("/compare/", "Compare vendors"), ("/how-we-pick/", "How we pick"), ("/faq/", "FAQ")])
            + col("Company", [("/about/", "About"), ("/contact/", "Contact"), ("/affiliate-disclosure/", "Affiliate disclosure")])
            + col("Legal", [("/privacy-policy/", "Privacy policy"), ("/terms/", "Terms of use"), ("/disclaimer/", "Disclaimer")])
            + '</div></div><p class="fn">Some store links may be affiliate links. If you buy through them, PepCoupons may earn a commission at no extra cost to you. PepCoupons does not sell products and gives no medical advice.</p>'
            '<p class="fn">&copy; 2026 PepCoupons</p></div></footer>')

def page(t, d, p, schema, body, extra=""):
    return head(t, d, p, schema) + '<body>' + header() + '<main id="main">' + body + '</main>' + footer() + extra + '<script src="/script.js" defer></script></body></html>'

def logo(v):
    if v["logo"]:
        return f'<img class="sm" src="{e(v["logo"])}" alt="{e(v["name"])} logo" width="46" height="46" loading="lazy">'
    return f'<span class="sm" style="background:{v["color"]}" aria-hidden="true">{e(v["name"].split()[-1][0])}</span>'

def tag(v):
    if v["status"] == "expired": return '<span class="tg x">Expired</span>'
    if v.get("exclusive"): return '<span class="tg e">Exclusive</span>'
    return '<span class="tg n">New</span>' if v["isNew"] else ""

def card(v):
    ex = v["status"] == "expired"
    return (f'<li class="cd{" ex" if ex else ""}"><div class="tt"><div class="ch">{logo(v)}<div><h3 class="vn"><a href="/{v["slug"]}/">{e(v["name"])}</a></h3>'
            f'<p class="ep">Ships from {e(v["ship"])}</p>{tag(v)}</div></div><p class="dn">{v["discount"]}<small>%</small></p></div><div class="perf"></div>'
            f'<div class="tb"><button class="cbtn" type="button" data-code="{e(v["code"])}"{" disabled" if ex else ""}><code>{e(v["code"])}</code><span>{"Expired" if ex else "Tap to copy"}</span></button>'
            f'<a class="gl" href="/{v["slug"]}/">{e(v["name"])} details</a></div></li>')

def checked(v):
    return f'<time datetime="{v["checked"]}">{v["checked"]}</time>' if v["checked"] else "Not checked yet (demo)"

def faq(items):
    h = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items)
    s = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return h, s

STEPS = ('<ol class="steps"><li><b>Pick a vendor</b><span>Compare discounts and shipping origin.</span></li>'
         '<li><b>Copy the code</b><span>One tap puts it on your clipboard.</span></li>'
         '<li><b>Paste at checkout</b><span>Check that the discount line appears before you pay.</span></li></ol>')

POP = '<p class="pop">Popular: ' + "".join(f'<a href="/{v["slug"]}/">{e(v["name"])}</a>' for v in V[:4]) + '</p>'
WHY = ('<section class="w why"><ul>'
 '<li><b>5 to 10 vendors only</b><span>A short list we can keep up to date.</span></li>'
 '<li><b>Exclusive discounts</b><span>Codes tagged Exclusive are arranged for PepCoupons readers.</span></li>'
 '<li><b>Dates you can see</b><span>Every code shows when it was last checked.</span></li></ul>'
 '<p><a href="/how-we-pick/">How we pick vendors</a></p></section>')
# ---------- home ----------
active = [v for v in V if v["status"] != "expired"]
top = max(v["discount"] for v in active)
HF = [("How do I use a peptide vendor coupon code?", "Copy the code, open the vendor's store, add products to your cart and paste the code into the discount field at checkout. Check that a discount line appears before you pay."),
      ("Why did a coupon code not work?", "Codes can expire, apply only to some products or need a minimum order. Check the terms on the vendor's site, and use the last-checked date on each listing to see how recent the code is."),
      ("Are the codes on PepCoupons verified?", "Each listing shows the date it was last checked. Listings marked as demo are placeholders and are not active offers."),
      ("Does PepCoupons sell peptides or give medical advice?", "No. PepCoupons only lists discount codes from vendors. It does not sell products and nothing on the site is medical advice.")]
fh, fs = faq(HF)
rows = "".join(f'<tr data-n="{e((v["name"] + " " + v["code"]).lower())}" data-d="{v["discount"]}" data-c="{v["country"]}"><th scope="row"><a href="/{v["slug"]}/">{e(v["name"])}</a>{tag(v)}</th>'
               f'<td class="dp">{v["discount"]}%</td><td><code>{e(v["code"])}</code></td><td>{e(v["ship"])}</td><td>{checked(v)}</td>'
               f'<td><button class="cp" type="button" data-code="{e(v["code"])}"{" disabled" if v["status"] == "expired" else ""}>{"Expired" if v["status"] == "expired" else "Copy"}</button></td></tr>' for v in V)
countries = "".join(f'<option value="{c}">{c}</option>' for c in sorted({v["country"] for v in V}))
pc = json.dumps([{k: v[k] for k in ("name", "slug", "discount", "code", "ship", "type", "color", "logo")} for v in active]).replace("</", "<\\/")
pill = "Demo listings with placeholder codes" if DEMO else f"Updated {TODAY}"
home = (f'<section class="hero"><div class="w hg"><div><p class="pill">{pill}</p><h1>Peptide Coupon <em>&amp; Discount Codes</em></h1>'
        f'<p class="lead">Compare {len(active)} peptide vendor discount codes, up to {top}% off. Copy a code, open the store and paste it at checkout.</p>'
        '<div class="sb"><input id="q" type="search" placeholder="Search a vendor, e.g. Vendor Alpha" aria-label="Search a vendor or code"><button class="btn" id="go" type="button">Find code</button></div>' + POP + '</div>'
        '<div id="hc"><div class="stack"><div class="fc" id="fcard" aria-live="off"></div></div><div class="dots" id="dots"></div></div></div></section>'
        + WHY + '<section class="dk" id="deals"><div class="w"><p class="kick">TOP DEALS</p><h2>Best peptide discount codes right now</h2>'
        '<p class="sbt">The highest-value codes on the site. Copy the code, then visit the store and paste it at checkout.</p>'
        f'<ul class="grid">{"".join(card(v) for v in V[:4])}</ul><p class="more"><a class="btn y" href="#all">View all codes</a></p></div></section>'
        '<section class="w sec" id="all"><h2>All peptide vendor codes</h2><div class="flt"><label>Country<select id="fcty"><option value="">All</option>' + countries + '</select></label>'
        '<label>Discount<select id="fmin"><option value="0">Any</option><option value="15">15% and up</option><option value="25">25% and up</option></select></label></div>'
        '<div class="tw"><table><thead><tr><th scope="col">Vendor</th><th scope="col">Discount</th><th scope="col">Code</th><th scope="col">Ships from</th><th scope="col">Last checked</th><th scope="col"><span class="sr">Copy</span></th></tr></thead>'
        f'<tbody id="tb">{rows}</tbody></table></div><p class="none" id="none" hidden>No vendors match. Try another name or clear the filters.</p>'
        + ('<p class="note">Vendors and codes shown are placeholders, not active offers.</p>' if DEMO else '') + '</section>'
        '<section class="w sec"><h2>How to use a peptide coupon code</h2>' + STEPS + '</section>'
        f'<section class="w sec" id="faq"><h2>Frequently asked questions</h2><div class="fq">{fh}</div></section>')
items = [{"@type": "ListItem", "position": i + 1, "name": v["name"] + " discount code", "url": f'{BASE}/{v["slug"]}/'} for i, v in enumerate(V)]
schema = ld({"@type": "WebSite", "name": "PepCoupons", "url": BASE + "/"}, {"@type": "Organization", "name": "PepCoupons", "url": BASE + "/"},
            {"@type": "ItemList", "name": "Peptide vendor discount codes", "itemListElement": items}, fs)
w("index.html", page("Peptide Coupon & Discount Codes – Compare Vendor Promo Codes | PepCoupons",
    f"Compare {len(active)} peptide vendor discount codes, up to {top}% off. Copy a code, see where each vendor ships from and check when it was last checked.", "/", schema, home,
    f'<script>window.PC={pc}</script>'))

def glance(v):
    rows = [("Exclusive discount", f'{v["discount"]}% off with code {v["code"]}' if v.get("exclusive") else ""), ("Ships from", v["ship"]),
            ("Delivery time", v.get("delivery", "")), ("Lab reports (COA)", v.get("coa", "")), ("Minimum order", v.get("min_order", "")), ("Payment methods", v.get("payment", ""))]
    rows = [(a, b) for a, b in rows if b]
    h = f'<section class="sec"><h2>{e(v["name"])} at a glance</h2><div class="tw"><table class="gt"><tbody>' + "".join(f'<tr><th scope="row">{a}</th><td>{e(b)}</td></tr>' for a, b in rows) + '</tbody></table></div>'
    pr, co = v.get("pros", []), v.get("cons", [])
    if pr or co:
        h += '<div class="pcon">' + (('<div><h3>Pros</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in pr) + '</ul></div>') if pr else '') + (('<div><h3>Cons</h3><ul>' + "".join(f"<li>{e(x)}</li>" for x in co) + '</ul></div>') if co else '') + '</div>'
    return h + '</section>'

# ---------- vendor pages ----------
for v in V:
    n, d, c = v["name"], v["discount"], v["code"]
    ex = v["status"] == "expired"
    VF = [(f"What is the {n} discount code?", f"The {n} code is {c}, worth {d}% off. It is listed as {v['type'].lower()} and the vendor ships from {v['ship']}."),
          (f"How do I use the {n} code?", f"Copy {c}, open the {n} store, add products to your cart and paste the code at checkout. Check that the discount line appears before you pay."),
          (f"Does the {n} code work on every product?", f"It is listed as {v['type'].lower()}, but vendors can change terms without notice. Check the discount line in your cart before paying.")]
    fh2, fs2 = faq(VF)
    others = "".join(f'<li><a href="/{o["slug"]}/">{e(o["name"])}<span>{o["discount"]}%</span></a></li>' for o in V if o is not v)
    buy = f'<a class="btn" href="{e(v["url"])}" rel="sponsored nofollow noopener" target="_blank">Visit {e(n)}</a>' if v["url"] else ""
    body = (f'<div class="w"><nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/#all">Coupons</a> › <span aria-current="page">{e(n)}</span></nav>'
            f'<article class="tk"><div class="tl"><small>Discount</small><b>{d}<i>%</i></b><span>{e(n)}</span></div><div class="tr">'
            f'<h1>{e(n)} Discount Code: {d}% Off</h1>'
            f'<p class="ans">{e(n)} has a {e(v["type"].lower())} discount code worth {d}% off: <strong>{e(c)}</strong>. The vendor ships from {e(v["ship"])}.'
            + (' This code is listed as expired.' if ex else '') + '</p>'
            f'<button class="cbtn" type="button" data-code="{e(c)}"{" disabled" if ex else ""}><code>{e(c)}</code><span>{"Expired" if ex else "Tap to copy"}</span></button>'
            f'<dl class="facts"><div><dt>Ships from</dt><dd>{e(v["ship"])}</dd></div><div><dt>Applies to</dt><dd>{e(v["type"])}</dd></div>'
            f'<div><dt>Status</dt><dd>{"Expired" if ex else "Active"}{" (demo)" if DEMO else ""}</dd></div><div><dt>Last checked</dt><dd>{checked(v)}</dd></div></dl>{buy}</div></article>' + glance(v) +
            f'<section class="sec"><h2>How to use the {e(n)} code</h2>{STEPS}</section>'
            f'<section class="sec"><h2>{e(n)} coupon questions</h2><div class="fq">{fh2}</div></section>'
            f'<section class="sec"><h2>Other vendor codes</h2><ul class="ol">{others}</ul></section></div>')
    bar = f'<div class="sbar"><code>{e(c)}</code><button class="cp" type="button" data-code="{e(c)}"{" disabled" if ex else ""}>{"Expired" if ex else "Copy code"}</button></div>'
    crumbs = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
              {"@type": "ListItem", "position": 2, "name": "Coupons", "item": BASE + "/#all"}, {"@type": "ListItem", "position": 3, "name": n}]}
    desc = f"{n} discount code: {c} for {d}% off {v['type'].lower()}. Ships from {v['ship']}. Copy the code, apply it in the cart and check the total before you pay."
    w(f'{v["slug"]}/index.html', page(f"{n} Discount Code: {d}% Off ({c}) | PepCoupons", desc, f'/{v["slug"]}/',
      ld({"@type": "WebPage", "name": f"{n} Discount Code", "url": f'{BASE}/{v["slug"]}/', "description": desc}, crumbs, fs2), body, bar))

# ---------- about, disclaimer, 404 ----------
def simple(slug, title, desc, inner):
    body = f'<div class="w prose"><h1>{title}</h1>{inner}</div>'
    w(f"{slug}/index.html", page(f"{title} | PepCoupons", desc, f"/{slug}/", ld({"@type": "WebPage", "name": title, "url": f"{BASE}/{slug}/"}), body))
simple("about", "About PepCoupons", "PepCoupons lists peptide vendor discount codes so you can compare them quickly.",
       "<p>PepCoupons lists discount codes from peptide vendors so you can compare them in one place. We do not sell products.</p>"
       "<h2>How we list codes</h2><p>Each listing shows the vendor, the discount, where it ships from and the date a code was last checked. Codes can change or expire without notice, so always check the discount line in your cart before you pay.</p>"
       "<h2>Affiliate links</h2><p>Some store links may be affiliate links. If you buy through them, PepCoupons may earn a commission at no extra cost to you. This never decides which codes are listed.</p>")
simple("disclaimer", "Disclaimer", "PepCoupons gives no medical advice and does not sell products.",
       "<p>PepCoupons only lists discount codes. We do not sell, ship or recommend any product, and nothing on this site is medical advice.</p>"
       "<p>Vendors set their own terms, prices and product descriptions. Read each vendor's terms before you buy, and speak to a qualified professional about any health question.</p>")
simple("how-we-pick", "How We Pick Vendors", "How PepCoupons chooses which peptide vendors to list: lab reports, pricing, shipping and reader discounts.",
       "<p>We list only a small number of vendors, so each one can be checked and kept up to date.</p>"
       "<h2>What we look at</h2><ul><li><b>Lab reports (COA).</b> Whether the vendor publishes third-party lab reports for its products.</li>"
       "<li><b>Pricing.</b> Clear prices per product and per mg, with no hidden fees at checkout.</li>"
       "<li><b>Shipping and support.</b> Where it ships from, delivery estimates and how problems are handled.</li>"
       "<li><b>Reader value.</b> Whether the vendor offers a discount code for PepCoupons readers. These are tagged Exclusive.</li></ul>"
       "<h2>What changes a listing</h2><p>Codes expire and terms change. Each listing shows when it was last checked, and we remove vendors that stop meeting these points.</p>"
       "<h2>How we earn money</h2><p>Some store links may be affiliate links, and PepCoupons may earn a commission at no extra cost to you. A vendor cannot pay to be listed as better than it is.</p>")
def cc(x): return e(x) if x else "&mdash;"
cb = ('<div class="w prose wide"><h1>Peptide Vendors Compared</h1><p>A side-by-side look at every vendor we list: discount, shipping origin and what each vendor shares.</p><div class="tw"><table><thead><tr>'
      '<th scope="col">Vendor</th><th scope="col">Discount</th><th scope="col">Ships from</th><th scope="col">Delivery</th><th scope="col">Lab reports</th><th scope="col">Min. order</th></tr></thead><tbody>'
      + "".join(f'<tr><th scope="row"><a href="/{v["slug"]}/">{e(v["name"])}</a>{tag(v)}</th><td class="dp">{v["discount"]}%</td><td>{cc(v["ship"])}</td><td>{cc(v.get("delivery",""))}</td><td>{cc(v.get("coa",""))}</td><td>{cc(v.get("min_order",""))}</td></tr>' for v in V)
      + '</tbody></table></div>' + ('<p class="note">Demo data. Real details are added after each vendor is reviewed.</p>' if DEMO else '') + '</div>')
w("compare/index.html", page("Peptide Vendors Compared: Discounts, Shipping & Lab Reports | PepCoupons", "Compare peptide vendors side by side: discount code, shipping origin, delivery time, lab reports and minimum order.", "/compare/",
   ld({"@type": "WebPage", "name": "Peptide Vendors Compared", "url": BASE + "/compare/"}), cb))

# ---------- more pages ----------
def legal(slug, title, desc, inner):
    simple(slug, title, desc, f'<p class="note">Last updated {TODAY}</p>' + inner)
mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
legal("privacy-policy", "Privacy Policy", "How PepCoupons handles information when you visit the site.",
 '<p>PepCoupons lists peptide vendor discount codes. This page explains what information is involved when you use the site.</p>'
 '<h2>What we collect</h2><p>We do not ask you to create an account, and we do not collect your name, email or payment details on this site. If you email us, we receive your email address and message and use them only to reply.</p>'
 "<h2>Hosting and logs</h2><p>The site is hosted on GitHub Pages. Like most web hosts, GitHub may log technical data such as your IP address when you visit. See GitHub's own privacy statement for details.</p>"
 "<h2>Fonts</h2><p>Pages load fonts from Google Fonts, so your browser contacts Google's servers to download them.</p>"
 '<h2>Analytics and cookies</h2><p>We do not currently use analytics or advertising cookies. If we add them, we will update this page.</p>'
 '<h2>Store links</h2><p>When you click a link to a vendor, you leave PepCoupons. The vendor and any affiliate network may set cookies so a commission can be credited. We do not control them. Read the vendor\'s own privacy policy.</p>'
 f'<h2>Questions</h2><p>Email {mail} with any question about this policy. We may update it, and the date above shows the latest change.</p>')
legal("terms", "Terms of Use", "The terms for using the PepCoupons website.",
 '<p>By using PepCoupons you agree to these terms. If you do not agree, please do not use the site.</p>'
 '<h2>Information only</h2><p>PepCoupons lists discount codes and basic vendor details for information. It does not sell products, and nothing here is medical advice or a recommendation to buy or use any product.</p>'
 '<h2>Codes can change</h2><p>Vendors can change or end a code at any time. We try to show when each code was last checked, but we cannot promise that a code will work. Always check the discount in your cart before you pay.</p>'
 '<h2>Third-party sites</h2><p>Links lead to sites we do not run. Your purchase is a deal between you and the vendor, who sets its own prices, terms, shipping and returns.</p>'
 '<h2>No warranty</h2><p>The site is provided as is. To the extent the law allows, PepCoupons is not responsible for losses that come from using the site or from buying from a vendor we list.</p>'
 f'<h2>Changes and contact</h2><p>We may update these terms. The date above shows the latest change. Questions: {mail}.</p>')
legal("affiliate-disclosure", "Affiliate Disclosure", "How PepCoupons earns money and what that means for you.",
 '<p>Some links on PepCoupons are affiliate links. If you click one and buy something, PepCoupons may earn a commission from the vendor at no extra cost to you.</p>'
 '<h2>What this means</h2><ul><li>The price you pay is the same with or without our link.</li><li>Some discount codes, tagged Exclusive, are arranged with a vendor for our readers.</li><li>Commissions help pay for running the site.</li></ul>'
 '<h2>Our approach</h2><p>We list only a small number of vendors and show the details we have, such as shipping origin and when a code was last checked. See <a href="/how-we-pick/">how we pick vendors</a>. We follow advertising disclosure guidelines such as those from the US Federal Trade Commission.</p>'
 f'<h2>Questions</h2><p>Email {mail}.</p>')
simple("contact", "Contact PepCoupons", "Contact PepCoupons to report a broken code, ask a question or suggest a correction.",
 f'<p>The best way to reach us is by email: {mail}.</p><h2>What to write to us about</h2><ul><li><b>A code that did not work.</b> Tell us the vendor, the code and what you saw at checkout.</li><li><b>A correction.</b> If a detail on a page is wrong, tell us and we will fix it.</li><li><b>Vendor questions.</b> We list only a few vendors and cannot be paid to list one. You are welcome to introduce a vendor, but we make no promise to list it.</li></ul>')
FA = [("How do I use a peptide vendor coupon code?", "Copy the code, open the vendor's store, add products to your cart and paste the code into the discount field at checkout. Check that a discount line appears before you pay."),
 ("Why did a coupon code not work?", "Codes can expire, apply only to some products, or need a minimum order. Check the vendor's terms, and look at the last-checked date on each listing."),
 ("What does Exclusive mean?", "An Exclusive tag means the code is arranged with the vendor for PepCoupons readers. A code without the tag is a general code the vendor offers."),
 ("Are the codes on PepCoupons verified?", "Each listing shows the date it was last checked. Listings marked as demo are placeholders and are not active offers."),
 ("Why do you list only a few vendors?", "A short list is easier to keep accurate and up to date. We would rather check a few vendors well than list many without care."),
 ("How does PepCoupons make money?", "Some store links may be affiliate links, so we may earn a commission if you buy, at no extra cost to you. See our affiliate disclosure for details."),
 ("Can I trust the vendor details on each page?", "We show what we know, such as shipping origin and delivery time, and leave fields out when we do not know them. Always read the vendor's own terms before you buy."),
 ("How do I report a code that does not work?", f"Email {EMAIL} with the vendor, the code and what happened at checkout. We will check it and update the listing."),
 ("Does PepCoupons sell peptides or give medical advice?", "No. PepCoupons only lists discount codes from vendors. It does not sell products, and nothing on the site is medical advice.")]
fh3, fs3 = faq(FA)
w("faq/index.html", page("Peptide Coupon FAQ: Using Codes, Vendors & Discounts | PepCoupons", "Answers to common questions about peptide vendor discount codes: how to use them, why one may fail, and how PepCoupons works.", "/faq/",
   ld({"@type": "WebPage", "name": "PepCoupons FAQ", "url": BASE + "/faq/"}, fs3), f'<div class="w prose"><h1>Frequently Asked Questions</h1><div class="fq">{fh3}</div></div>'))
cpb = ('<div class="w sec" style="padding-top:40px"><h1>Peptide Vendor Coupon Codes</h1>'
       f'<p class="lead">All {len(V)} vendors we list, with the code, the discount, where each ships from and when it was last checked.</p>'
       '<div class="sb" style="margin-bottom:18px"><input id="q" type="search" placeholder="Search a vendor or code" aria-label="Search a vendor or code"></div>'
       '<div class="flt"><label>Country<select id="fcty"><option value="">All</option>' + countries + '</select></label>'
       '<label>Discount<select id="fmin"><option value="0">Any</option><option value="15">15% and up</option><option value="25">25% and up</option></select></label></div>'
       '<div class="tw"><table><thead><tr><th scope="col">Vendor</th><th scope="col">Discount</th><th scope="col">Code</th><th scope="col">Ships from</th><th scope="col">Last checked</th><th scope="col"><span class="sr">Copy</span></th></tr></thead>'
       f'<tbody id="tb">{rows}</tbody></table></div><p class="none" id="none" hidden>No vendors match. Try another name or clear the filters.</p>'
       + ('<p class="note">Vendors and codes shown are placeholders, not active offers.</p>' if DEMO else '') + '</div>'
       '<section class="w sec"><h2>How to use a peptide coupon code</h2>' + STEPS + '</section>')
w("coupons/index.html", page("Peptide Vendor Coupon Codes: All Discounts in One Table | PepCoupons", f"All {len(V)} peptide vendor discount codes in one table, with discount size, shipping origin and last-checked date.", "/coupons/",
   ld({"@type": "WebPage", "name": "Peptide Vendor Coupon Codes", "url": BASE + "/coupons/"}, {"@type": "ItemList", "name": "Peptide vendor discount codes", "itemListElement": items}), cpb))
w("404.html", head("Page not found | PepCoupons", "This page could not be found.", "/404.html", "").replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
  + '<body>' + header() + '<main><div class="w prose"><h1>Page not found</h1><p><a href="/">Back to all peptide codes</a></p></div></main>' + footer() + '</body></html>', raw=True)

# ---------- static files ----------
urls = ["/"] + [f'/{v["slug"]}/' for v in V] + ["/coupons/", "/compare/", "/how-we-pick/", "/faq/", "/about/", "/contact/", "/affiliate-disclosure/", "/privacy-policy/", "/terms/", "/disclaimer/"]
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
w("CNAME", "pepcoupons.site\n")
w(".nojekyll", "")
print("built", len(urls), "pages")
