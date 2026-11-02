// Alterna o tema claro/escuro (lembrado neste navegador) e copia o e-mail.
(function () {
  var raiz = document.documentElement;
  function temaAtual() {
    var t = raiz.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var botao = document.querySelector(".tema");
  if (botao) {
    var rotular = function () {
      var escuro = temaAtual() === "dark";
      botao.setAttribute("aria-label", escuro ? "Usar tema claro" : "Usar tema escuro");
      botao.setAttribute("aria-pressed", String(escuro));
    };
    rotular();
    botao.addEventListener("click", function () {
      var novo = temaAtual() === "dark" ? "light" : "dark";
      raiz.setAttribute("data-theme", novo);
      try { localStorage.setItem("tema", novo); } catch (e) {}
      rotular();
    });
  }

  var copiar = document.querySelector(".copiar");
  if (copiar) {
    copiar.addEventListener("click", function () {
      var texto = copiar.getAttribute("data-copiar");
      var ok = function () { copiar.textContent = "Copiado"; setTimeout(function () { copiar.textContent = "Copiar e-mail"; }, 2000); };
      var manual = function () {
        var alvo = document.querySelector(".email");
        var r = document.createRange(); r.selectNodeContents(alvo);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        copiar.textContent = "Selecionado: use Ctrl+C";
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(texto).then(ok, manual);
      else manual();
    });
  }
})();
