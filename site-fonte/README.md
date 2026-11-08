# Site institucional do Stig

- `site/` — o site pronto, publicado pela Vercel (Root Directory = `site`). Não edite à mão.
- `site-fonte/` — onde se edita: `src/` (páginas), `assets/` (estilo, script, imagens) e `build.py`.

Para atualizar: edite em `site-fonte/` e rode `python site-fonte/build.py`. Ele remonta `site/` com o mesmo topo, rodapé e regras da marca em todas as páginas.

Formulários gravam na tabela `site_leads` do Supabase do portal (central-stig) pela função `submit_site_lead`.
