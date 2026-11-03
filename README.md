# Spigelmeyer Productions website (spigiproducts.com)

Static site (plain HTML/CSS/JS, no framework), hosted on Cloudflare Pages.

| Folder | What it is |
|---|---|
| `pages-site/` | **The live website.** Cloudflare Pages publishes this folder as-is. |
| `pages-src/` | `build.py` generates every page in `pages-site/` from shared header, nav and footer templates, plus source images and nav assets. |
| `forms-worker/` | `sp-forms` Cloudflare Worker that emails Contact, Start a Project and subscribe submissions. Deployed separately with `npx wrangler deploy`. |

## Making changes
1. Edit `pages-src/build.py` (copy, pages, nav) or the assets it copies.
2. Run `python3 pages-src/build.py` to regenerate `pages-site/`.
3. Commit and push. Cloudflare Pages redeploys automatically.

Cloudflare Pages settings: build command **none**, output directory **`pages-site`**.

`PREVIEW=1 python3 pages-src/build.py` writes unreleased pages to `pages-site-preview/` (not committed).
