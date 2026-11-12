# PepCoupons website

A static website (plain HTML, CSS and JavaScript). No server needed. It works on GitHub Pages.

## Put it live on GitHub (about 10 minutes)
1. On github.com click **New repository**. Name it `pepcoupons`, set it to **Public**, and create it.
2. Click **uploading an existing file**. Drag in everything from inside this folder (all the files and folders, not the folder itself). Click **Commit changes**.
3. Open **Settings > Pages**. Under **Build and deployment**, choose **Deploy from a branch**, branch **main**, folder **/ (root)**, and Save.
4. After a minute or two GitHub shows your address, usually `https://YOUR-USERNAME.github.io/pepcoupons/`. The site works there as it is.
5. For your own domain: in **Settings > Pages > Custom domain** enter `pepcoupons.site` and Save. At your domain registrar add the DNS records GitHub shows you. Then tick **Enforce HTTPS**.
6. In Google Search Console add `pepcoupons.site` and submit `https://pepcoupons.site/sitemap.xml`.

## Change vendors
1. Edit `data/vendors.json` (name, slug, discount, code, ship, country, status, isNew, checked, url, logo, color, and optional exclusive, delivery, coa, min_order, payment, pros, cons).
2. Run `python3 build.py`. It rebuilds every page and the sitemap.
3. Upload the changed files to GitHub.

## Before real launch
- Replace the demo vendors and codes with real, checked ones, then set `DEMO = False` in `build.py`.
- Fill `checked` only for codes you have tested. Add `url` store links (they are marked sponsored and nofollow).
- Keep the About, How we pick and Disclaimer pages accurate.
- Optional: self-host the fonts for faster loading.

## Pages in this site
Home, Coupons, Compare, How we pick, FAQ, About, Contact, Affiliate disclosure, Privacy policy, Terms of use, Disclaimer, one page per vendor, and a 404 page. The sitemap lists all of them.

## Check these before you go public
- **Email:** the Contact, Privacy and Terms pages use `hello@pepcoupons.site`. Create that mailbox or change `EMAIL` at the top of `build.py`, then run `python3 build.py`.
- **Legal pages:** the Privacy policy, Terms and Affiliate disclosure are plain-language starting points, not legal advice. Have them reviewed for your country before you rely on them, and update the Privacy policy if you add analytics or ads.
