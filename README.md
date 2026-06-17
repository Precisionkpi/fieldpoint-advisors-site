# FieldPoint Advisors — Marketing Site

Static HTML/CSS/JS marketing site for FieldPoint Advisors. Built for landscape
contractors who use Aspire Software.

## Local preview

```bash
python -m http.server 5173
# then open http://localhost:5173
```

## Deploy

Auto-deploys to Netlify on every push to `main`.
Custom domain: **fieldpointadvisor.com**

## Files

- `index.html` — single-page site
- `styles.css` — all styling
- `script.js` — interactivity (mobile nav, scroll reveal, sticky header)
- `assets/brand/` — logo (`logo.png` light-on-light, `logo-light.png` for dark backgrounds)
- `assets/team/` — founder headshots
- `make_light_logo.py` — helper that regenerates `logo-light.png` from `logo.png`
- `netlify.toml` — Netlify config (cache headers)
