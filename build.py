"""Gera o site a partir dos arquivos em conteudo/.

Uso:  python build.py
Edite conteudo/perfil.json e conteudo/cases/*.json; depois rode este script.
Gera index.html, cases/<slug>.html, sitemap.xml e robots.txt. Só usa a biblioteca padrão.
"""
import hashlib
import json
from datetime import date
from html import escape
from pathlib import Path

RAIZ = Path(__file__).parent
CONTEUDO = RAIZ / "conteudo"


def versao(arquivo):
    """Hash curto do arquivo, para o navegador não usar uma cópia antiga do CSS ou do JS."""
    return hashlib.sha1((RAIZ / "assets" / arquivo).read_bytes()).hexdigest()[:8]

FONTES = ("https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400..900;1,100,400"
          "&family=JetBrains+Mono:wght@400;500&display=swap")

ICONE_TEMA = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18z" fill="currentColor"/></svg>'
ICONE_BAIXAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11"/><path d="m7 10 5 5 5-5"/><path d="M5 20h14"/></svg>'
ICONE_DIAG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>'


def e(texto):
    return escape(str(texto), quote=True)


def carregar():
    perfil = json.loads((CONTEUDO / "perfil.json").read_text(encoding="utf-8"))
    cases = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((CONTEUDO / "cases").glob("*.json"))]
    return perfil, cases


def cabecalho(perfil, titulo, descricao, url, prefixo):
    imagem = perfil["url_site"] + "assets/og.jpg"
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)}</title>
<meta name="description" content="{e(descricao)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descricao)}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{e(imagem)}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#E9E5DC">
<link rel="icon" href="{prefixo}assets/favicon.svg" type="image/svg+xml">
<script>try{{var t=localStorage.getItem("tema");if(t)document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTES}">
<link rel="stylesheet" href="{prefixo}assets/estilo.css?v={versao("estilo.css")}">
</head>
<body>
<a class="pular" href="#conteudo">Pular para o conteúdo</a>
"""


def nav(perfil, prefixo):
    nome = perfil["nome"].split()
    return f"""<div class="nav">
<a class="marca" href="{prefixo or './'}">{e(nome[0])} {e(nome[-1])}</a>
<nav class="menu" aria-label="Principal"><a href="{prefixo}#sobre">Sobre</a><a href="{prefixo}#cases">Cases</a><a href="{prefixo}#experiencia">Experiência</a></nav>
<div class="nav-acoes"><button class="tema" type="button" aria-label="Alternar tema">{ICONE_TEMA}</button><a class="pill" href="{prefixo}#contato">Fale comigo {ICONE_DIAG}</a></div>
</div>"""


def rodape(perfil, prefixo):
    return f"""<footer class="rodape"><div class="wrap">
<span>© {date.today().year} {e(perfil["nome"])}</span>
<span>{e(perfil["contato"]["cidade"])}</span>
</div></footer>
<script src="{prefixo}assets/site.js?v={versao("site.js")}" defer></script>
</body>
</html>
"""


def chips(itens):
    return '<ul class="chips">' + "".join(f"<li>{e(i)}</li>" for i in itens) + "</ul>"


def card(caso, principal):
    destaque = caso["destaque"]
    corpo = f"""<span class="rotulo">{e(caso["categoria"])}</span>
<h3><a href="cases/{e(caso["slug"])}.html">{e(caso["titulo"])}</a></h3>
<p class="contexto">{e(caso["contexto"])}</p>
<p class="resumo">{e(caso["resumo"])}</p>"""
    bloco_destaque = f"""<div class="destaque"><span class="valor">{e(destaque["valor"])}</span><span class="legenda">{e(destaque["legenda"])}</span></div>"""
    rodape_card = f"""{chips(caso["tecnologias"][:5])}<span class="ver" aria-hidden="true">Ver case {ICONE_DIAG}</span>"""
    if principal:
        return (f'<article class="card principal"><div class="corpo">{corpo}</div>{bloco_destaque}'
                f'<div class="fim">{rodape_card}</div></article>')
    return f"""<article class="card">{corpo}{bloco_destaque}{rodape_card}</article>"""


def pagina_inicial(perfil, cases):
    c = perfil["contato"]
    nome = perfil["nome"].split()
    metricas = ""
    for m in perfil["metricas"]:
        miolo = ((f'<span class="area">{e(m["area"])}</span>' if m.get("area") else "")
                 + f'<span class="valor">{e(m["valor"])}</span>'
                 + (f'<span class="titulo">{e(m["titulo"])}</span>' if m.get("titulo") else "")
                 + f'<span class="legenda">{e(m["legenda"])}</span>')
        if m.get("case"):
            # o destaque inteiro leva ao case que o comprova
            miolo = f'<a href="cases/{e(m["case"])}.html">{miolo}<span class="ir">Ver o case {ICONE_DIAG}</span></a>'
        metricas += f"<li>{miolo}</li>"
    sobre = "".join(f"<p>{e(p)}</p>" for p in perfil["sobre"])
    empresas = "".join(f'<span class="e">{e(x)}</span>' for x in perfil.get("empresas", []))
    cards = "".join(card(caso, i == 0) for i, caso in enumerate(cases))
    tempo = "".join(f"""<li><span class="periodo">{e(x["periodo"])}</span><div class="quem"><h3>{e(x["empresa"])}</h3>
<span class="cargo-x">{e(x["cargo"])}</span><span class="ctx">{e(x["contexto"])}</span></div><p>{e(x["resumo"])}</p></li>""" for x in perfil["experiencias"])
    grupos = "".join(f'<div class="grupo"><h3>{e(g["grupo"])}</h3>{chips(g["itens"])}</div>' for g in perfil["habilidades"])
    formacao = ""
    for f in perfil["formacao"]:
        inst = ", ".join(x for x in (f["instituicao"], f["ano"]) if x)
        formacao += (f'<li><h3>{e(f["titulo"])}</h3>' + (f'<span class="inst">{e(inst)}</span>' if inst else "")
                     + (f'<span class="det">{e(f["detalhe"])}</span>' if f["detalhe"] else "") + "</li>")
    pessoa = {
        "@context": "https://schema.org", "@type": "Person", "name": perfil["nome"], "jobTitle": perfil["titulo"],
        "url": perfil["url_site"], "email": "mailto:" + c["email"], "image": perfil["url_site"] + "assets/foto-440.jpg",
        "address": {"@type": "PostalAddress", "addressLocality": c["cidade"].split(",")[0], "addressRegion": "BA", "addressCountry": "BR"},
        "alumniOf": "Universidade Estadual de Santa Cruz", "sameAs": [c["linkedin"], c["github"]],
    }
    titulo = f'{perfil["nome"]} · {perfil["titulo"]}'
    return (cabecalho(perfil, titulo, perfil["descricao_seo"], perfil["url_site"], "") + f"""
<header class="topo"><div class="wrap"><div class="cartao">
{nav(perfil, "")}
<div class="hero-grid" id="conteudo">
<div class="hero-txt">
<span class="rotulo">Dados · automação · processos</span>
<h1 class="nome"><span>{e(nome[0])}<span class="brilho" aria-hidden="true">✦</span></span><span>{e(nome[-1])}</span></h1>
<p class="cargo">{e(perfil["titulo"])}</p>
<p class="complemento">{e(perfil["complemento"])}</p>
<p class="proposta">{e(perfil["proposta"])}</p>
<p class="local">{e(c["cidade"])} · {e(perfil["disponibilidade"])}</p>
<div class="acoes"><a class="pill" href="#cases">Ver projetos {ICONE_DIAG}</a><a class="pill vazada" href="{e(perfil["curriculo_pdf"])}" download>Baixar currículo</a><a class="pill vazada" href="#contato">Contato</a></div>
</div>
<figure class="hero-foto">
<picture>
<source type="image/webp" srcset="assets/foto-220.webp 220w, assets/foto-440.webp 440w" sizes="(max-width: 820px) 272px, 400px">
<img src="assets/foto-440.jpg" width="440" height="641" alt="Foto de {e(perfil["nome"])}, de camisa preta e braços cruzados, sorrindo" fetchpriority="high">
</picture>
</figure>
</div>
</div>
<div class="empresas"><span class="rotulo">Onde já atuei</span>{empresas}</div>
</div></header>

<main>
<section class="secao metricas" aria-label="Entregas em destaque"><div class="wrap">
<div class="cabeca"><div><span class="rotulo">Entregas em destaque</span><h2>O que já entreguei</h2></div></div>
<ul>{metricas}</ul>
</div></section>

<section class="secao" id="sobre"><div class="wrap">
<div class="cabeca"><div><span class="rotulo">Sobre</span></div></div>
<div class="sobre"><p class="frase">Dado para decidir, <em>processo</em> para repetir.</p><div class="sobre-texto">{sobre}</div></div>
</div></section>

<section class="secao" id="cases"><div class="wrap">
<div class="cabeca"><div><span class="rotulo">{len(cases)} cases</span><h2>Projetos</h2></div><p class="intro">Cada case mostra o problema, o que eu fiz, as ferramentas e o resultado. Documentos de clientes não são publicados.</p></div>
<div class="cases">{cards}</div>
</div></section>

<section class="secao" id="experiencia"><div class="wrap">
<div class="cabeca"><div><span class="rotulo">Trajetória</span><h2>Experiência</h2></div></div>
<ol class="tempo">{tempo}</ol>
</div></section>

<section class="secao" id="habilidades"><div class="wrap">
<div class="cabeca"><div><span class="rotulo">Ferramentas</span><h2>Habilidades</h2></div></div>
<div class="grupos">{grupos}</div>
</div></section>

<section class="secao" id="formacao"><div class="wrap">
<div class="cabeca"><div><span class="rotulo">Estudo</span><h2>Formação</h2></div></div>
<ul class="formacao">{formacao}</ul>
</div></section>

<section class="secao" id="contato"><div class="wrap"><div class="contato-bloco">
<span class="rotulo">Contato</span>
<h2>Vamos<br>conversar</h2>
<p class="intro">Aberto a oportunidades em análise de dados, automação, BI e inteligência para campanhas.</p>
<div class="email-linha"><a class="email" href="mailto:{e(c["email"])}">{e(c["email"])}</a><button class="copiar" type="button" data-copiar="{e(c["email"])}">Copiar e-mail</button></div>
<ul class="canais">
<li><span class="k">Telefone e WhatsApp</span><a href="https://wa.me/{e(c["whatsapp"])}" target="_blank" rel="noopener">{e(c["telefone"])}</a></li>
<li><span class="k">LinkedIn</span><a href="{e(c["linkedin"])}" target="_blank" rel="noopener">{e(c["linkedin"].split("linkedin.com/")[-1].strip("/"))}</a></li>
<li><span class="k">GitHub</span><a href="{e(c["github"])}" target="_blank" rel="noopener">{e(c["github"].split("github.com/")[-1])}</a></li>
<li><span class="k">Cidade</span><span class="v">{e(c["cidade"])}</span></li>
</ul>
<a class="pill" href="{e(perfil["curriculo_pdf"])}" download>{ICONE_BAIXAR} Baixar currículo (PDF)</a>
</div></div></section>
</main>
<script type="application/ld+json">{json.dumps(pessoa, ensure_ascii=False)}</script>
""" + rodape(perfil, ""))


def pagina_case(perfil, cases, i):
    caso = cases[i]
    url = f'{perfil["url_site"]}cases/{caso["slug"]}.html'
    titulo = f'{caso["titulo"]} · {perfil["nome"]}'
    ant = cases[i - 1] if i > 0 else None
    prox = cases[i + 1] if i + 1 < len(cases) else None
    navc = ""
    if ant:
        navc += f'<a href="{e(ant["slug"])}.html"><span class="k">← Case anterior</span><span class="t">{e(ant["titulo"])}</span></a>'
    if prox:
        navc += f'<a class="prox" href="{e(prox["slug"])}.html"><span class="k">Próximo case →</span><span class="t">{e(prox["titulo"])}</span></a>'
    lista = lambda itens, cls="": f'<ul class="lista {cls}">' + "".join(f"<li>{e(x)}</li>" for x in itens) + "</ul>"
    evid = '<div class="nota">' + "".join(f"<p>{e(x)}</p>" for x in caso["evidencias"]) + "</div>"
    d = caso["destaque"]
    bloco = lambda titulo, html: f'<div class="case-bloco"><h2>{titulo}</h2><div>{html}</div></div>'
    ficha = "".join(f'<div><dt>{rot}</dt><dd>{e(caso[k])}</dd></div>'
                    for k, rot in (("periodo", "Período"), ("papel", "Meu papel"), ("status", "Status")) if caso.get(k))
    ficha = f'<dl class="ficha">{ficha}</dl>' if ficha else ""
    como = ""
    if caso.get("fluxo"):
        como += '<ol class="fluxo">' + "".join(
            f'<li><span class="etapa">{e(f["etapa"])}</span><span class="det">{e(f["detalhe"])}</span></li>' for f in caso["fluxo"]) + "</ol>"
    if caso.get("como_funciona"):
        como += lista(caso["como_funciona"])
    resultado = lista(caso["resultados"], "resultados")
    if caso.get("tabela"):
        tb = caso["tabela"]
        cab = "".join(f'<th scope="col" class="{"n" if i else ""}">{e(c)}</th>' for i, c in enumerate(tb["colunas"]))
        corpo = "".join("<tr>" + "".join(
            (f'<th scope="row">{e(v)}</th>' if i == 0 else f'<td class="n">{e(v)}</td>') for i, v in enumerate(lin)) + "</tr>"
            for lin in tb["linhas"])
        resultado += (f'<div class="tabela"><table><caption>{e(tb["titulo"])}</caption><thead><tr>{cab}</tr></thead>'
                      f'<tbody>{corpo}</tbody></table></div>' + (f'<p class="medicao">{e(tb["nota"])}</p>' if tb.get("nota") else ""))
    if caso.get("medicao"):
        resultado += f'<p class="medicao"><strong>Como foi medido:</strong> {e(caso["medicao"])}</p>'
    tecnico = ""
    if caso.get("decisao"):
        tecnico += bloco("Decisão técnica", f'<h3 class="sub">{e(caso["decisao"]["titulo"])}</h3><p>{e(caso["decisao"]["texto"])}</p>')
    if caso.get("codigo"):
        cod = caso["codigo"]
        tecnico += bloco("Trecho do código", f'<figure class="codigo"><pre><code>{e(cod["trecho"])}</code></pre><figcaption>{e(cod["legenda"])}</figcaption></figure>')
    if caso.get("limitacoes"):
        tecnico += bloco("Limitações", lista(caso["limitacoes"]))
    imagens = ""
    if caso.get("imagens"):
        g = caso["imagens"]
        grupos = ""
        for grupo in g["grupos"]:
            # a imagem nunca passa do tamanho original (não fica borrada) e abre inteira numa nova aba
            figs = "".join(
                f'<figure class="fig{" larga" if im.get("larga") else ""}" style="--max:{int(im["largura"])}px">'
                f'<a href="../{e(im["arquivo"])}" target="_blank" rel="noopener" aria-label="Ampliar: {e(im["alt"])}">'
                f'<img src="../{e(im["arquivo"])}" alt="{e(im["alt"])}" width="{int(im["largura"])}" height="{int(im["altura"])}" loading="lazy"></a>'
                f'<figcaption><span class="fonte">{e(im["fonte"])}</span>{e(im["legenda"])}</figcaption></figure>'
                for im in grupo["itens"])
            grupos += (f'<div class="antes-depois-grupo"><div class="grupo-cab"><span class="etiqueta">{e(grupo["etiqueta"])}</span>'
                       f'<h3>{e(grupo["titulo"])}</h3><p>{e(grupo["texto"])}</p></div><div class="figs">{figs}</div></div>')
        imagens = (f'<div class="antes-depois"><div class="ad-cab"><h2>{e(g["titulo"])}</h2><p>{e(g["intro"])}</p></div>'
                   f'{grupos}<p class="credito">{e(g["credito"])} Toque numa imagem para ver em tamanho original.</p></div>')
    demo = ""
    # "demo" pode ser um objeto ou uma lista; endereço externo (http) abre em nova aba
    for dm in ([caso["demo"]] if isinstance(caso.get("demo"), dict) else caso.get("demo", [])):
        ext = dm["url"].startswith("http")
        href = e(dm["url"]) if ext else f'../{e(dm["url"])}'
        alvo = ' target="_blank" rel="noopener"' if ext else ""
        demo += (f'<div class="demo"><a class="pill" href="{href}"{alvo}>{e(dm["rotulo"])} {ICONE_DIAG}</a>'
                 f'<span>{e(dm["nota"])}</span></div>')
    return (cabecalho(perfil, titulo, caso["resumo"], url, "../") + f"""
<header class="topo"><div class="wrap"><div class="cartao">
{nav(perfil, "../")}
<div class="case-topo" id="conteudo">
<a class="voltar" href="../#cases">← Todos os cases</a>
<span class="rotulo">{e(caso["categoria"])}</span>
<h1>{e(caso["titulo"])}</h1>
<p class="contexto">{e(caso["contexto"])}</p>
<div class="case-destaque"><span class="valor">{e(d["valor"])}</span><span class="legenda">{e(d["legenda"])}</span></div>
{demo}
</div>
</div></div></header>
<main>
<section class="case-corpo secao"><div class="wrap">
{ficha}
<div class="case-bloco"><h2>Problema</h2><div><p>{e(caso["problema"])}</p></div></div>
<div class="case-bloco"><h2>O que eu fiz</h2><div>{lista(caso["solucao"])}</div></div>
{bloco("Como funciona", como) if como else ""}
{imagens}
<div class="case-bloco"><h2>Resultado</h2><div>{resultado}</div></div>
{tecnico}
<div class="case-bloco"><h2>Tecnologias</h2><div>{chips(caso["tecnologias"])}</div></div>
<div class="case-bloco"><h2>Evidências</h2><div>{evid}</div></div>
</div></section>
<div class="wrap"><nav class="navcases" aria-label="Outros cases">{navc}</nav></div>
</main>
""" + rodape(perfil, "../"))


def main():
    perfil, cases = carregar()
    (RAIZ / "index.html").write_text(pagina_inicial(perfil, cases), encoding="utf-8")
    (RAIZ / "cases").mkdir(exist_ok=True)
    for i, caso in enumerate(cases):
        (RAIZ / "cases" / f'{caso["slug"]}.html').write_text(pagina_case(perfil, cases, i), encoding="utf-8")
    hoje = date.today().isoformat()
    urls = [perfil["url_site"]] + [f'{perfil["url_site"]}cases/{c["slug"]}.html' for c in cases]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url><loc>{e(u)}</loc><lastmod>{hoje}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    (RAIZ / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f'User-agent: *\nAllow: /\nSitemap: {perfil["url_site"]}sitemap.xml\n', encoding="utf-8")
    print(f"Site gerado: index.html + {len(cases)} cases, sitemap.xml e robots.txt")


if __name__ == "__main__":
    main()
