document.addEventListener("DOMContentLoaded", () => {
  // Функция для получения CSRF-токена из cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  // ==========================================
  // 1. ЛОГИКА ЛАЙКОВ И ДИЗЛАЙКОВ (AJAX)
  // ==========================================
  const voteGroups = document.querySelectorAll(".vote-group");

  voteGroups.forEach((group) => {
    const objectId = group.dataset.objectId;
    const objectType = group.dataset.objectType; // 'question' или 'answer'
    const countDisplay = group.querySelector(".vote-count");
    const buttons = group.querySelectorAll("button");

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const value = btn.dataset.value;
        const url = objectType === "question"
            ? `/question/${objectId}/vote`
            : `/answer/${objectId}/vote`;

        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            [objectType + "_id"]: objectId, // 'question_id' или 'answer_id'
            value: value,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "ok") {
              // Обновляем рейтинг
              countDisplay.textContent = data.updated_rating;

              // Логика подсветки кнопок
              const wasActive = btn.classList.contains("active");
              buttons.forEach((b) => b.classList.remove("active"));
              if (!wasActive) {
                btn.classList.add("active");
              }
            } else {
              alert("Ошибка: " + data.error);
            }
          })
          .catch((error) => console.error("Network error:", error));
      });
    });
  });

  // ==========================================
  // 2. ЛОГИКА ПРАВИЛЬНОГО ОТВЕТА (AJAX)
  // ==========================================
  const correctCheckboxes = document.querySelectorAll(".mark-correct-checkbox");
  
  correctCheckboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", (e) => {
      const answerId = e.target.closest(".form-check").dataset.objectId;

      fetch(`/answer/${answerId}/is_correct`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          answer_id: answerId,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "ok") {
            // Если ответ теперь правильный, снимаем галочки с остальных ответов на странице
            if (data.is_correct) {
              correctCheckboxes.forEach((cb) => {
                if (cb !== checkbox) cb.checked = false;
              });
            }
          } else {
            // Если сервер выдал ошибку, возвращаем галочку в исходное состояние
            checkbox.checked = !checkbox.checked;
            alert("Ошибка: " + data.error);
          }
        })
        .catch((error) => {
          checkbox.checked = !checkbox.checked;
          console.error("Network error:", error);
        });
    });
  });

  // ==========================================
  // 2. ЛОГИКА ПОДГРУЗКИ КОММЕНТОВ (AJAX)
  // ==========================================

  const loadMoreBtns = document.querySelectorAll(".load-more-comments");

  loadMoreBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      
      const answerId = btn.dataset.answerId;
      const offset = parseInt(btn.dataset.offset);
      const wrapper = document.getElementById(`load-more-wrapper-${answerId}`);
      
      // Защита от кучи запросов
      const originalText = btn.textContent;
      btn.textContent = "Загрузка...";
      btn.disabled = true;

      fetch(`/answer/${answerId}/comments/load`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          offset: offset,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          btn.textContent = originalText;
          btn.disabled = false;

          if (data.status === "ok") {
            wrapper.insertAdjacentHTML("beforebegin", data.html);
            btn.dataset.offset = offset + 3;

            if (!data.has_more) {
              wrapper.style.display = "none";
            }
          } else {
            alert("Ошибка при загрузке: " + data.error);
          }
        })
        .catch((error) => {
          btn.textContent = originalText;
          btn.disabled = false;
          console.error("Network error:", error);
        });
    });
  });

  // 3. ЛОГИКА ВАЛИДАЦИИ ФОРМ
  // const forms = document.querySelectorAll(".needs-validation");
  // Array.from(forms).forEach((form) => {
  //   form.addEventListener("submit", (event) => {
  //     if (!form.checkValidity()) {
  //       event.preventDefault();
  //       event.stopPropagation();
  //     }
  //     form.classList.add("was-validated");
  //   }, false);
  // });

  // 4. ПОПОВЕРЫ ДЛЯ ОТКЛЮЧЕННЫХ ЭЛЕМЕНТОВ (кроме чекбоксов)
  if (typeof bootstrap !== 'undefined') {
    document.querySelectorAll(':disabled').forEach(el => {
      // Пропускаем чекбоксы
      if (el.matches('input[type="checkbox"]')) return;
      
      // Защита от повторного оборачивания при динамической подгрузке
      if (el.parentElement?.classList.contains('disabled-tooltip-wrapper')) return;

      const wrapper = document.createElement('span');
      wrapper.className = 'disabled-tooltip-wrapper d-inline-block';
      wrapper.setAttribute('data-bs-toggle', 'popover');
      wrapper.setAttribute('data-bs-trigger', 'hover focus');
      wrapper.setAttribute('data-bs-content', 'Войдите в систему, чтобы выполнить действие');
      wrapper.setAttribute('data-bs-placement', 'top');
      wrapper.setAttribute('tabindex', '0');

      // Оборачиваем элемент (официальный workaround Bootstrap 5 для disabled)
      el.parentNode.insertBefore(wrapper, el);
      wrapper.appendChild(el);

      // Инициализируем поповер
      new bootstrap.Popover(wrapper);
    });
  }
});