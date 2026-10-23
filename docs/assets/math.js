/* 公式渲染配置：沿用 KaTeX，与洛谷端的写法保持一致。 */
window.FFFFYC_MATH = {
  delimiters: [
    { left: "$$", right: "$$", display: true },
    { left: "$", right: "$", display: false },
  ],
  macros: {
    "\\bm": "\\boldsymbol{#1}",
    "\\sube": "\\subseteq",
    "\\supe": "\\supseteq",
    "\\R": "\\mathbb{R}",
    "\\N": "\\mathbb{N}",
    "\\Z": "\\mathbb{Z}",
    "\\Q": "\\mathbb{Q}",
    "\\C": "\\mathbb{C}",
    "\\eps": "\\varepsilon",
    "\\argmax": "\\operatorname*{arg\\,max}",
  },
  throwOnError: false,
  ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
};

window.ffffycTypeset = function (el) {
  var target = el || document.body;
  if (window.renderMathInElement) {
    window.renderMathInElement(target, window.FFFFYC_MATH);
  } else {
    window.addEventListener("load", function () {
      if (window.renderMathInElement) {
        window.renderMathInElement(target, window.FFFFYC_MATH);
      }
    });
  }
};

document.addEventListener("DOMContentLoaded", function () {
  window.ffffycTypeset();
});
