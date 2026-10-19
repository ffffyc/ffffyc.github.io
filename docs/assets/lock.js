/* 隐藏内容解锁：口令只在本地参与派生，浏览器记住派生结果，不保存口令本身。 */
(function () {
  const KEY_STORE = "ffffyc.key";
  const box = document.getElementById("lock-data");
  if (!box) return;

  const payload = JSON.parse(box.textContent);
  const form = document.getElementById("lock-form");
  const input = document.getElementById("lock-pass");
  const hint = document.getElementById("lock-hint");
  const article = document.getElementById("secret");
  const list = document.getElementById("secret-list");
  const titleEl = document.getElementById("secret-title");
  const tocEl = document.getElementById("secret-toc");
  const pdfSlot = document.getElementById("pdf-slot");

  const b64 = (buf) => btoa(String.fromCharCode.apply(null, new Uint8Array(buf)));
  const raw = (s) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));

  async function derive(pass, salt, iterations) {
    const base = await crypto.subtle.importKey(
      "raw",
      new TextEncoder().encode(pass),
      "PBKDF2",
      false,
      ["deriveKey"]
    );
    return crypto.subtle.deriveKey(
      { name: "PBKDF2", salt: raw(salt), iterations: iterations, hash: "SHA-256" },
      base,
      { name: "AES-GCM", length: 256 },
      true,
      ["decrypt"]
    );
  }

  function setTitle(title) {
    if (!title) return;
    if (titleEl) titleEl.textContent = title;
    const suffix = window.FFFFYC_SUFFIX || "";
    document.title = suffix ? title + " — " + suffix : title;
  }

  function buildToc(items) {
    if (!tocEl || !items || !items.length) return;
    tocEl.innerHTML = "";
    const label = document.createElement("p");
    label.className = "toc-title";
    label.textContent = "目录";
    tocEl.appendChild(label);
    items.forEach(function (t) {
      const a = document.createElement("a");
      a.href = "#" + t.id;
      a.className = "lv" + t.level;
      a.textContent = t.text;
      tocEl.appendChild(a);
    });
    if (window.ffffycTypeset) window.ffffycTypeset(tocEl);
  }

  async function showFile(url, key) {
    if (!pdfSlot) return;
    pdfSlot.textContent = "正在解密…";
    try {
      const resp = await fetch(url);
      const text = (await resp.text()).trim();
      const [nonce, cipher] = text.split("\n");
      const plain = await crypto.subtle.decrypt(
        { name: "AES-GCM", iv: raw(nonce) },
        key,
        raw(cipher)
      );
      const blob = new Blob([plain], { type: "application/pdf" });
      const blobUrl = URL.createObjectURL(blob);
      pdfSlot.innerHTML =
        '<iframe class="pdf-frame" title="作业解答" src="' + blobUrl + '"></iframe>' +
        '<p class="post-back"><a href="' + blobUrl + '" download="解答.pdf">下载 PDF</a></p>';
    } catch (err) {
      pdfSlot.textContent = "解密失败，请刷新后重试。";
    }
  }

  async function render(data, key) {
    setTitle(data.title);
    if (form) form.parentElement.hidden = true;

    if (data.file && key) {
      await showFile(data.file, key);
      return;
    }

    if (data.html && article) {
      article.innerHTML = data.html;
      buildToc(data.toc);
      if (window.ffffycTypeset) window.ffffycTypeset(article);
    }

    if (data.items && list) {
      const ul = document.createElement("ul");
      ul.className = "postlist";
      data.items.forEach(function (it) {
        const li = document.createElement("li");
        li.innerHTML =
          '<a class="pl-title" href="' + it.u + '">' + it.t + "</a>" +
          '<span class="pl-date">' + it.d + "</span>";
        ul.appendChild(li);
      });
      list.appendChild(ul);
      list.hidden = false;
    }
  }

  async function decryptJson(key) {
    const plain = await crypto.subtle.decrypt(
      { name: "AES-GCM", iv: raw(payload.n) },
      key,
      raw(payload.c)
    );
    return JSON.parse(new TextDecoder().decode(plain));
  }

  async function tryStored() {
    const saved = localStorage.getItem(KEY_STORE);
    if (!saved) return false;
    try {
      const key = await crypto.subtle.importKey("raw", raw(saved), "AES-GCM", false, ["decrypt"]);
      await render(await decryptJson(key), key);
      return true;
    } catch (err) {
      localStorage.removeItem(KEY_STORE);
      return false;
    }
  }

  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      hint.textContent = "正在验证…";
      try {
        const key = await derive(input.value, payload.s, payload.i);
        const data = await decryptJson(key);
        localStorage.setItem(KEY_STORE, b64(await crypto.subtle.exportKey("raw", key)));
        hint.textContent = "";
        await render(data, key);
      } catch (err) {
        hint.textContent = "口令不正确。";
      }
    });
  }

  tryStored().then(function (ok) {
    if (ok) return;
    if (form) {
      form.parentElement.hidden = false;
      input.focus();
    }
  });
})();
