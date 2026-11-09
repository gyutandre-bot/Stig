"""Monta o site estático: injeta <head>, topo e rodapé comuns em cada página de src/ e grava em dist/."""
import json, pathlib, shutil

ROOT = pathlib.Path(__file__).parent
SRC, DIST = ROOT / "src", ROOT.parent / "site"
SITE = "https://stig-site-two.vercel.app"  # trocar por https://stig.com.br quando o domínio for ligado

PAGES = {
    "index.html":        ("Stig — Delivery justo: zero comissão, 100% do frete ao entregador",
                          "Stig é o delivery de São José dos Campos sem comissão por pedido: restaurante paga mensalidade fixa, entregador fica com 100% do frete e você paga preço de balcão.", "stig"),
    "restaurantes.html": ("Stig para restaurantes — Delivery sem comissão, a partir de R$ 200/mês",
                          "Venda por delivery sem comissão por pedido. Mensalidade fixa a partir de R$ 200, preço de balcão e 30 dias grátis. Lançamento em São José dos Campos.", "rest"),
    "entregadores.html": ("Stig para entregadores — 100% do frete é seu",
                          "No Stig o entregador fica com 100% do frete, sem taxa por corrida, com saque via Pix. Cadastre-se para o lançamento em São José dos Campos.", "ent"),
    "privacidade.html":  ("Política de Privacidade — Stig",
                          "Como o Stig trata os dados pessoais enviados pelo site, conforme a LGPD.", ""),
    "termos.html":       ("Termos do pré-cadastro — Stig",
                          "Condições do pré-cadastro e da oferta de lançamento do Stig.", ""),
}

LOGO = ('<svg viewBox="0 0 92 36" role="img" aria-label="Stig"><text x="0" y="28" '
        'font-family="Playfair Display, Georgia, serif" font-size="34" font-weight="500" fill="#F5F0E8">st'
        '<tspan font-style="italic" fill="#FF6A3D">i</tspan>g</text></svg>')

def head(title, desc, path):
    url = SITE + "/" + ("" if path == "index.html" else path.replace(".html", ""))
    org = {
        "@context": "https://schema.org", "@type": "Organization", "name": "Stig",
        "legalName": "Stig", "taxID": "68.075.074/0001-20", "url": SITE,
        "logo": SITE + "/assets/og.png",
        "address": {"@type": "PostalAddress", "addressLocality": "São José dos Campos", "addressRegion": "SP", "addressCountry": "BR"},
    }
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Stig">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#161412">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{json.dumps(org, ensure_ascii=False)}</script>
<script defer src="/_vercel/insights/script.js" data-optional></script>
</head>
<body>"""

def top(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    cta = {"rest": ("#cadastro", "Quero ser parceiro"), "ent": ("#cadastro", "Quero entregar")}.get(active, ("#cadastro", "Avise-me no lançamento"))
    if not active:
        cta = ("/#cadastro", "Avise-me no lançamento")
    return f"""<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="top"><div class="wrap">
<a class="brand" href="/" aria-label="Stig — página inicial">{LOGO}</a>
<button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
<nav class="nav" id="nav" aria-label="Principal">{a("/", "O Stig", "stig")}{a("/restaurantes", "Para restaurantes", "rest")}{a("/entregadores", "Para entregadores", "ent")}</nav>
<a class="btn sm" href="{cta[0]}">{cta[1]}</a>
</div></header>
<main id="conteudo">"""

FOOT = f"""</main>
<footer><div class="wrap">
<div class="foot">
<div><a class="brand" href="/" aria-label="Stig">{LOGO}</a>
<p style="margin-top:14px;max-width:300px">Delivery sem comissão por pedido. Restaurante paga mensalidade fixa, entregador fica com 100% do frete.</p></div>
<div><h4>Stig</h4><ul><li><a href="/#como-funciona">Como funciona</a></li><li><a href="/#planos-usuario">Planos para quem pede</a></li><li><a href="/#faq">Perguntas frequentes</a></li></ul></div>
<div><h4>Parceiros</h4><ul><li><a href="/restaurantes">Para restaurantes</a></li><li><a href="/entregadores">Para entregadores</a></li></ul></div>
<div><h4>Legal</h4><ul><li><a href="/privacidade">Política de Privacidade</a></li><li><a href="/termos">Termos do pré-cadastro</a></li><li><a href="/#cadastro">Fale com a gente</a></li></ul></div>
</div>
<div class="legal">
<span>Stig · CNPJ <span class="num">68.075.074/0001-20</span> · São José dos Campos – SP</span>
<span>© <span id="year" class="num">2026</span> Stig. Pré-lançamento.</span>
</div>
</div></footer>
<script src="assets/app.js" defer></script>
</body>
</html>
"""

import re
HEAD_RE = re.compile(r"(<h[1-3][^>]*>)(.*?)(</h[1-3]>)", re.S)
NUM_RE = re.compile(r"(R\$\s?)?\d[\d.,]*%?")

def nums_in_headings(html):
    """Regra da marca: números e dinheiro nunca em Playfair. Envolve-os em <span class="num"> (DM Sans)."""
    def fix(m):
        parts = re.split(r"(<[^>]+>)", m.group(2))
        out = [p if p.startswith("<") else NUM_RE.sub(lambda n: f'<span class="num">{n.group(0)}</span>', p) for p in parts]
        return m.group(1) + "".join(out) + m.group(3)
    return HEAD_RE.sub(fix, html)

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for name, (title, desc, key) in PAGES.items():
        body = nums_in_headings((SRC / name).read_text(encoding="utf-8"))
        (DIST / name).write_text(relativize(head(title, desc, name) + top(key) + body + FOOT), encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    urls = "".join(f"<url><loc>{SITE}/{'' if n == 'index.html' else n[:-5]}</loc></url>" for n in PAGES)
    (DIST / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
    (DIST / "vercel.json").write_text(json.dumps({
        "cleanUrls": True, "trailingSlash": False,
        "headers": [{"source": "/(.*)", "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "X-Frame-Options", "value": "DENY"},
            {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"}]}],
    }, indent=2), encoding="utf-8")
    print("ok:", sorted(p.name for p in DIST.iterdir()))

def relativize(html):
    """Links internos relativos: funcionam na Vercel (cleanUrls) e em qualquer prévia."""
    html = re.sub(r'href="/(#[^"]*)?"', lambda m: f'href="index.html{m.group(1) or ""}"', html)
    html = re.sub(r'href="/(restaurantes|entregadores|privacidade|termos)(#[^"]*)?"', lambda m: f'href="{m.group(1)}.html{m.group(2) or ""}"', html)
    return html

if __name__ == "__main__":
    build()
