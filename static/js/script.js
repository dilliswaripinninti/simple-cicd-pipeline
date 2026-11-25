(function () {
  "use strict";

  var stateEl = document.getElementById("live-state");
  var textEl = document.getElementById("live-text");
  var uptimeEl = document.getElementById("uptime");
  var outputEl = document.getElementById("output");

  function formatUptime(seconds) {
    var h = Math.floor(seconds / 3600);
    var m = Math.floor((seconds % 3600) / 60);
    var s = seconds % 60;
    if (h > 0) { return h + "h " + m + "m"; }
    if (m > 0) { return m + "m " + s + "s"; }
    return s + "s";
  }

  function refreshStatus() {
    fetch("/api/status")
      .then(function (res) {
        if (!res.ok) { throw new Error("Bad response"); }
        return res.json();
      })
      .then(function (data) {
        stateEl.dataset.state = "ok";
        textEl.textContent = "Running on " + data.environment;
        uptimeEl.textContent = formatUptime(data.uptime_seconds);
      })
      .catch(function () {
        stateEl.dataset.state = "down";
        textEl.textContent = "The app did not respond";
        uptimeEl.textContent = "–";
      });
  }

  document.querySelectorAll("[data-endpoint]").forEach(function (button) {
    button.addEventListener("click", function () {
      var endpoint = button.dataset.endpoint;
      outputEl.textContent = "Requesting " + endpoint + "…";
      fetch(endpoint)
        .then(function (res) {
          return res.json().then(function (body) {
            outputEl.textContent = "HTTP " + res.status + "\n" + JSON.stringify(body, null, 2);
          });
        })
        .catch(function () {
          outputEl.textContent = "Request failed. Check that the app is running.";
        });
    });
  });

  refreshStatus();
  setInterval(refreshStatus, 15000);
})();
