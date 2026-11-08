/* Stig — site institucional: menu, calculadoras e envio de cadastros ao Supabase */
(function () {
  "use strict";

  // Chave pública (publishable): só consegue chamar a função submit_site_lead.
  // A tabela não pode ser lida nem gravada diretamente por visitantes (RLS).
  var SUPABASE_URL = "https://mdxrleoonlnjcnsacdhu.supabase.co";
  var SUPABASE_KEY = "sb_publishable_H8uJKgiQUHSqNjiPkuapRw_c8C7xmd9";

  var brl = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", maximumFractionDigits: 0 });
  var brl2 = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL", minimumFractionDigits: 2 });
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // ---------- menu do celular ----------
  var mb = $(".menu-btn"), nav = $(".nav");
  if (mb && nav) {
    mb.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      mb.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // ---------- calculadora do restaurante ----------
  var rc = $("#calc-rest");
  if (rc) {
    var IFOOD_MENSAL = 150; // Plano Entrega, vendas acima de R$ 1.800/mês
    var upd = function () {
      var ped = +$("#c-ped").value, tk = +$("#c-tk").value, com = +$("#c-com").value / 10;
      var plano = $("input[name=c-plano]:checked").value;
      var stig = plano === "pro" ? 400 : 200;
      $("#o-ped").textContent = ped;
      $("#o-tk").textContent = brl.format(tk);
      $("#o-com").textContent = com.toLocaleString("pt-BR", { maximumFractionDigits: 1 }) + "%";
      var fat = ped * 30 * tk;
      var hoje = fat * com / 100 + (fat > 1800 ? IFOOD_MENSAL : 0);
      var eco = hoje - stig;
      $("#r-fat").textContent = brl.format(fat);
      $("#r-hoje").textContent = brl.format(hoje);
      $("#r-stig").textContent = brl.format(stig);
      $("#r-eco").textContent = eco > 0 ? brl.format(eco) : "—";
      $("#r-ano").textContent = eco > 0 ? brl.format(eco * 12) : "—";
    };
    $$("input", rc).forEach(function (i) { i.addEventListener("input", upd); });
    upd();
  }

  // ---------- calculadora do entregador ----------
  var cc = $("#calc-courier");
  if (cc) {
    var updc = function () {
      var c = +$("#e-cor").value, km = +$("#e-km").value / 2, d = +$("#e-dias").value;
      var frete = 5 + 1.5 * km;
      $("#oe-cor").textContent = c;
      $("#oe-km").textContent = km.toLocaleString("pt-BR", { maximumFractionDigits: 1 }) + " km";
      $("#oe-dias").textContent = d;
      $("#re-frete").textContent = brl2.format(frete);
      $("#re-dia").textContent = brl2.format(frete * c);
      $("#re-mes").textContent = brl.format(frete * c * d);
    };
    $$("input", cc).forEach(function (i) { i.addEventListener("input", updc); });
    updc();
  }

  // ---------- formulários ----------
  var onlyDigits = function (v) { return (v || "").replace(/\D/g, ""); };
  $$("input[type=tel]").forEach(function (i) {
    i.addEventListener("input", function () {
      var d = onlyDigits(i.value).slice(0, 11);
      if (d.length > 6) i.value = "(" + d.slice(0, 2) + ") " + d.slice(2, d.length - 4) + "-" + d.slice(-4);
      else if (d.length > 2) i.value = "(" + d.slice(0, 2) + ") " + d.slice(2);
      else i.value = d;
    });
  });

  $$("form[data-segment]").forEach(function (form) {
    var box = form.closest(".form"), msg = $(".msg", form), btn = $("button[type=submit]", form);

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      msg.className = "msg"; msg.textContent = "";
      $$("[aria-invalid]", form).forEach(function (el) { el.removeAttribute("aria-invalid"); });

      // validação simples, com mensagens claras
      var bad = [];
      $$("[required]", form).forEach(function (el) {
        var ok = el.type === "checkbox" ? el.checked : el.value.trim() !== "";
        if (ok && el.type === "tel") ok = onlyDigits(el.value).length >= 10;
        if (ok && el.type === "email" && el.value) ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value);
        if (!ok) { el.setAttribute("aria-invalid", "true"); bad.push(el); }
      });
      var em = $("input[type=email]", form);
      if (em && em.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value)) { em.setAttribute("aria-invalid", "true"); bad.push(em); }
      if (bad.length) {
        msg.className = "msg err";
        msg.textContent = "Confira os campos destacados" + (bad.some(function (b) { return b.type === "checkbox"; }) ? " e o aceite da Política de Privacidade." : ".");
        bad[0].focus();
        return;
      }

      // monta o pacote: campos fixos + "details" com o resto
      var fd = new FormData(form), details = {};
      var fixed = ["name", "phone", "email", "city", "how_found", "consent_privacy", "consent_marketing", "website"];
      fd.forEach(function (v, k) {
        if (fixed.indexOf(k) > -1) return;
        if (details[k] !== undefined) details[k] = [].concat(details[k], v);
        else details[k] = v;
      });
      var multi = $$("input[type=checkbox][data-multi]", form).map(function (c) { return c.name; });
      multi.forEach(function (n) { if (details[n] !== undefined) details[n] = [].concat(details[n]); });
      details.pagina = location.pathname;
      var q = new URLSearchParams(location.search);
      ["utm_source", "utm_medium", "utm_campaign"].forEach(function (k) { if (q.get(k)) details[k] = q.get(k); });

      var payload = {
        segment: form.dataset.segment,
        name: fd.get("name"),
        phone: onlyDigits(fd.get("phone")) || null,
        email: fd.get("email") || null,
        city: fd.get("city") || null,
        how_found: fd.get("how_found") || null,
        consent_privacy: fd.get("consent_privacy") === "on",
        consent_marketing: fd.get("consent_marketing") === "on",
        website: fd.get("website") || "",
        details: details
      };

      btn.disabled = true; var label = btn.textContent; btn.textContent = "Enviando…";
      fetch(SUPABASE_URL + "/rest/v1/rpc/submit_site_lead", {
        method: "POST",
        headers: { "Content-Type": "application/json", apikey: SUPABASE_KEY },
        body: JSON.stringify({ payload: payload })
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        box.classList.add("sent");
        var d = $(".done", box); if (d) { d.setAttribute("tabindex", "-1"); d.focus(); }
        if (window.va) window.va("event", { name: "cadastro_" + form.dataset.segment });
      }).catch(function () {
        msg.className = "msg err";
        msg.textContent = "Não conseguimos enviar agora. Verifique sua conexão e tente de novo em instantes.";
      }).finally(function () { btn.disabled = false; btn.textContent = label; });
    });

    var again = $(".again", box);
    if (again) again.addEventListener("click", function () { form.reset(); box.classList.remove("sent"); $("input", form).focus(); });
  });

  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
})();
