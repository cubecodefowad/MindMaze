document.getElementById("riddle-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const answer = document.getElementById("answer").value.toLowerCase().trim();

  if (answer === "piano") {
    window.location.href = "/victory";
  } else {
    triggerFailureEffect();
  }
});

function triggerFailureEffect() {
  const overlay = document.createElement("div");
  overlay.className = "fail-overlay";
  document.body.appendChild(overlay);

  setTimeout(() => {
    overlay.remove();
  }, 1500);
}
