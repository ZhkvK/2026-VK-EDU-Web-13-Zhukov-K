document.addEventListener("DOMContentLoaded", () => {
  // 1. ЛОГИКА ЛАЙКОВ И ДИЗЛАЙКОВ

  const voteGroups = document.querySelectorAll(".vote-group");

  voteGroups.forEach((group) => {
    const btnLike = group.querySelector(".btn-like");
    const btnDislike = group.querySelector(".btn-dislike");
    const countDisplay = group.querySelector(".vote-count");

    if (btnLike && btnDislike && countDisplay) {
      // Логика нажатия на Лайк
      btnLike.addEventListener("click", () => {
        let currentScore = parseInt(countDisplay.textContent) || 0;

        if (btnLike.classList.contains("active")) {
          // Снимаем свой лайк (-1)
          btnLike.classList.remove("active");
          countDisplay.textContent = currentScore - 1;
        } else {
          // Ставим лайк
          btnLike.classList.add("active");

          if (btnDislike.classList.contains("active")) {
            // Если до этого стоял дизлайк, снимаем его и ставим лайк (+2)
            btnDislike.classList.remove("active");
            countDisplay.textContent = currentScore + 2;
          } else {
            // Если ничего не стояло (+1)
            countDisplay.textContent = currentScore + 1;
          }
        }
      });

      // Логика нажатия на Дизлайк
      btnDislike.addEventListener("click", () => {
        let currentScore = parseInt(countDisplay.textContent) || 0;

        if (btnDislike.classList.contains("active")) {
          // Снимаем свой дизлайк (+1 возвращаем обратно)
          btnDislike.classList.remove("active");
          countDisplay.textContent = currentScore + 1;
        } else {
          // Ставим дизлайк
          btnDislike.classList.add("active");

          if (btnLike.classList.contains("active")) {
            // Если до этого стоял лайк, снимаем его и ставим дизлайк (-2)
            btnLike.classList.remove("active");
            countDisplay.textContent = currentScore - 2;
          } else {
            // Если ничего не стояло (-1)
            countDisplay.textContent = currentScore - 1;
          }
        }
      });
    }
  });
  // 2. ЛОГИКА ВАЛИДАЦИИ ФОРМ

  // Находим все формы на странице с классом needs-validation
  const forms = document.querySelectorAll(".needs-validation");

  // Перебираем их и вешаем слушатель на событие отправки (submit)
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        // Если форма не прошла внутреннюю проверку HTML5 (required, minlength и т.д.)
        if (!form.checkValidity()) {
          event.preventDefault(); // Останавливаем отправку формы
          event.stopPropagation(); // Останавливаем всплытие события
        }

        // Добавляем класс was-validated, чтобы Bootstrap показал красные/зеленые рамки
        form.classList.add("was-validated");
      },
      false,
    );
  });
});
