/* ═══════════════════════════════════════════════════════════
   CRM Hub – App JavaScript (jQuery)
   Chatbot widget, toasts, sidebar toggle
   ═══════════════════════════════════════════════════════════ */

//  Toast Utility ─
function showToast(message, type = "info") {
  const icons = {
    success: "bi-check-circle-fill",
    danger: "bi-x-circle-fill",
    warning: "bi-exclamation-triangle-fill",
    info: "bi-info-circle-fill",
  };
  const id = "toast-" + Date.now();
  const html = `
        <div id="${id}" class="toast align-items-center text-bg-${type} border-0" role="alert" data-bs-autohide="true" data-bs-delay="4000">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${icons[type] || icons.info} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>`;
  $("#toastContainer").append(html);
  const toastEl = document.getElementById(id);
  const toast = new bootstrap.Toast(toastEl);
  toast.show();
  toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
}

//  Sidebar Toggle (Mobile) ─
$(document).ready(function () {
  $("#sidebarToggle").click(function () {
    $("#sidebar").toggleClass("open");
  });

  // Close sidebar when clicking outside on mobile
  $(document).click(function (e) {
    if ($(window).width() <= 768) {
      if (!$(e.target).closest("#sidebar, #sidebarToggle").length) {
        $("#sidebar").removeClass("open");
      }
    }
  });
});

//  Chatbot Widget 
$(document).ready(function () {
  const $fab = $("#chatbotFab");
  const $popup = $("#chatbotPopup");
  const $close = $("#chatbotClose");
  const $input = $("#chatInput");
  const $send = $("#chatSend");
  const $messages = $("#chatbotMessages");

  // Toggle popup
  $fab.click(function () {
    $popup.toggleClass("open");
    if ($popup.hasClass("open")) {
      $input.focus();
      $fab.css("animation", "none");
    } else {
      $fab.css("animation", "float 3s ease-in-out infinite");
    }
  });

  $close.click(function () {
    $popup.removeClass("open");
    $fab.css("animation", "float 3s ease-in-out infinite");
  });

  // Send message
  function sendMessage() {
    const msg = $input.val().trim();
    if (!msg) return;

    // Add user message
    appendMessage("user", msg);
    $input.val("").focus();

    // Show typing indicator
    const typingId = "typing-" + Date.now();
    $messages.append(`
            <div class="chat-message bot" id="${typingId}">
                <div class="message-avatar"><i class="bi bi-robot"></i></div>
                <div class="message-content">
                    <div class="typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            </div>
        `);
    scrollToBottom();

    // Call API
    $.ajax({
      url: "/api/chat",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ message: msg }),
      success: function (data) {
        $(`#${typingId}`).remove();
        appendMessage("bot", data.reply);
      },
      error: function (xhr) {
        $(`#${typingId}`).remove();
        const errMsg =
          xhr.responseJSON?.detail || "Something went wrong. Please try again.";
        appendMessage("bot", "⚠️ " + errMsg);
      },
    });
  }

  $send.click(sendMessage);
  $input.keypress(function (e) {
    if (e.which === 13) {
      e.preventDefault();
      sendMessage();
    }
  });

  function appendMessage(role, text) {
    // Convert markdown-style formatting
    let formatted = escapeHtml(text)
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");

    const avatarContent =
      role === "bot"
        ? '<i class="bi bi-robot"></i>'
        : '<i class="bi bi-person-fill"></i>';

    $messages.append(`
            <div class="chat-message ${role}">
                <div class="message-avatar">${avatarContent}</div>
                <div class="message-content"><p>${formatted}</p></div>
            </div>
        `);
    scrollToBottom();
  }

  function scrollToBottom() {
    $messages.scrollTop($messages[0].scrollHeight);
  }

  function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
});
