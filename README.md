# Portfólio de Cézar Santos Gonçalves

Site estático em HTML, CSS e um pouco de JavaScript. O conteúdo fica em arquivos JSON, separado do layout, e um script em Python monta as páginas.

## Estrutura

```
site/
├── conteudo/
│   ├── perfil.json          ← nome, métricas, sobre, experiências, habilidades, formação, contato
│   └── cases/
│       ├── 1-midia-paga.json
│       ├── 2-escuta-comentarios.json
│       ├── 3-decupagem.json
│       ├── 4-operacao-digital.json
│       └── 5-inspecao-5s.json
├── assets/                  ← estilo, script, foto (WebP + JPG), imagem de compartilhamento, currículo em PDF
├── build.py                 ← gera as páginas a partir de conteudo/
├── index.html               ← gerado
├── cases/*.html             ← gerados
├── sitemap.xml, robots.txt  ← gerados
```

Não edite `index.html` nem `cases/*.html` à mão: eles são recriados a cada build.

## Ver o site no computador

Abra `index.html` com dois cliques. Funciona direto no navegador, sem servidor.

## Editar o conteúdo

1. Abra o arquivo em `conteudo/` no Bloco de Notas ou no VS Code e altere o texto entre aspas.
2. No terminal, dentro da pasta `site`, rode:
   ```
   python build.py
   ```
3. Abra `index.html` de novo para conferir.

**Adicionar um case:** copie um arquivo de `conteudo/cases/`, mude o nome (o número na frente define a ordem) e troque o `slug` (vira o endereço da página, sem espaços nem acentos). O primeiro case aparece em destaque, ocupando a largura toda.

**Cuidados com o JSON:** todo texto vai entre aspas duplas, e os itens de uma lista são separados por vírgula, sem vírgula depois do último. Se o `build.py` der erro, a mensagem indica a linha do problema.

**Trocar o currículo:** salve o novo PDF em `assets/` com o nome `curriculo-cezar-santos-goncalves.pdf`, por cima do antigo.

## Publicar no GitHub Pages

O endereço final será `https://cezarep.github.io/`.

1. Entre em [github.com](https://github.com) com o usuário **CezarEP**.
2. Clique em **+** → **New repository**.
   - Nome do repositório, exatamente assim: `CezarEP.github.io`
   - Visibilidade: **Public**
   - Clique em **Create repository**.
3. Na página do repositório, clique em **uploading an existing file**.
4. Arraste **todo o conteúdo da pasta `site`**: `index.html`, `sitemap.xml`, `robots.txt` e as pastas `assets`, `cases` e `conteudo`. Pode deixar o `build.py` e este `README.md` também. Clique em **Commit changes**.
5. Vá em **Settings** → **Pages**. Em **Source**, escolha **Deploy from a branch**, depois **main** e **/ (root)**, e clique em **Save**.
6. Em 1 ou 2 minutos, o site estará em `https://cezarep.github.io/`.

**Para atualizar depois:** rode `python build.py` e envie de novo os arquivos que mudaram (normalmente `index.html`, a pasta `cases` e o JSON editado) pelo mesmo botão **Add file → Upload files**.

**Se usar outro endereço** (outro nome de repositório ou domínio próprio), troque `url_site` em `conteudo/perfil.json` e rode o build. É ele que vai para o mapa do site e para a imagem de compartilhamento.

## Depois de publicar

- Cole o endereço no LinkedIn (seção Contato e em "Em destaque") e no campo Website do perfil do GitHub.
- Para testar a imagem que aparece ao compartilhar o link, use o [Post Inspector do LinkedIn](https://www.linkedin.com/post-inspector/).
- Para aparecer no Google mais rápido, cadastre o site no [Google Search Console](https://search.google.com/search-console) e envie o `sitemap.xml`.
