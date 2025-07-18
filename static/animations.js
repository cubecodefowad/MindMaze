document.getElementById("riddle-form").addEventListener("submit", async function(e) {
  e.preventDefault();
  const answerInput = document.getElementById("answer-input");
  const answer = answerInput.value.trim();
  const form = e.target;
  const submitUrl = form.getAttribute("data-submit-url");
  const errorDiv = document.getElementById("answer-error");
  const livesBar = document.getElementById("lives-remaining");

  // Disable input and button to prevent double submission
  answerInput.disabled = true;
  form.querySelector("button[type='submit']").disabled = true;

  try {
    const response = await fetch(submitUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
      },
      body: new URLSearchParams({ answer })
    });

    if (response.redirected) {
      const url = new URL(response.url, window.location.origin);
      if (url.pathname.startsWith("/level") || url.pathname === "/victory") {
        // Correct answer: show green overlay, then redirect
        triggerSuccessEffect();
        setTimeout(() => {
          window.location.href = response.url;
        }, 1200);
      } else if (url.pathname === "/game-over") {
        // Game over: redirect immediately, no green overlay
        window.location.href = response.url;
      } else {
        // Fallback: just redirect
        window.location.href = response.url;
      }
      return;
    }

    // Handle AJAX JSON response for wrong answer
    const data = await response.json();
    if (typeof data.lives !== 'undefined' && livesBar) {
      livesBar.textContent = data.lives;
    }
    if (data.game_over) {
      triggerFailureEffect();
      setTimeout(() => {
        window.location.href = data.game_over_url;
      }, 1500);
      return;
    }
    // Wrong answer, not game over
    triggerFailureEffect();
    errorDiv.textContent = "Wrong answer! Try again.";
    errorDiv.style.display = "block";
    answerInput.value = "";
    answerInput.focus();
  } catch (err) {
    errorDiv.textContent = "An error occurred. Please try again.";
    errorDiv.style.display = "block";
  } finally {
    answerInput.disabled = false;
    form.querySelector("button[type='submit']").disabled = false;
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

function triggerSuccessEffect() {
  const overlay = document.createElement("div");
  overlay.className = "success-overlay";
  document.body.appendChild(overlay);
  setTimeout(() => {
    overlay.remove();
  }, 1200);
}
