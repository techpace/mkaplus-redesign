/* Static site forms: no server needed. On submit, open the visitor's email app
   with the form filled into a message to hello@mkaplus.com. To switch to a server
   endpoint later, set data-endpoint on the <form> (see website/README.md). */
(function () {
  var TO = "hello@mkaplus.com";
  document.querySelectorAll("form[data-subject]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var lines = [];
      var seen = {};
      form.querySelectorAll("[name]").forEach(function (el) {
        var name = el.name;
        if (seen[name]) return;
        seen[name] = true;
        var values = data.getAll(name).filter(function (v) { return String(v).trim() !== ""; });
        if (!values.length) return;
        var label = el.getAttribute("data-label") || name;
        lines.push(label + ": " + values.join(", "));
      });
      var result = form.querySelector(".form-result");
      var endpoint = form.getAttribute("data-endpoint");
      if (endpoint) {
        fetch(endpoint, { method: "POST", body: data })
          .then(function (r) {
            if (!r.ok) throw new Error(r.status);
            if (result) result.textContent = "Thanks. We received your message and will reply by email.";
            form.reset();
          })
          .catch(function () {
            if (result) result.textContent = "Sending failed. Please email us at " + TO + ".";
          });
        return;
      }
      var href = "mailto:" + TO +
        "?subject=" + encodeURIComponent(form.getAttribute("data-subject")) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      if (result) result.textContent = "Your email app should open with these details filled in. If it doesn't, email us at " + TO + ".";
    });
  });
})();
