document.addEventListener("DOMContentLoaded", () => {
  // 1. ЛОГИКА ЛАЙКОВ И ДИЗЛАЙКОВ
  const voteGroups = document.querySelectorAll(".vote-group");
  voteGroups.forEach((group) => {
    const btnLike = group.querySelector(".btn-like");
    const btnDislike = group.querySelector(".btn-dislike");
    const countDisplay = group.querySelector(".vote-count");

    if (btnLike && btnDislike && countDisplay) {
      btnLike.addEventListener("click", () => {
        let currentScore = parseInt(countDisplay.textContent) || 0;
        if (btnLike.classList.contains("active")) {
          btnLike.classList.remove("active");
          countDisplay.textContent = currentScore - 1;
        } else {
          btnLike.classList.add("active");
          if (btnDislike.classList.contains("active")) {
            btnDislike.classList.remove("active");
            countDisplay.textContent = currentScore + 2;
          } else {
            countDisplay.textContent = currentScore + 1;
          }
        }
      });

      btnDislike.addEventListener("click", () => {
        let currentScore = parseInt(countDisplay.textContent) || 0;
        if (btnDislike.classList.contains("active")) {
          btnDislike.classList.remove("active");
          countDisplay.textContent = currentScore + 1;
        } else {
          btnDislike.classList.add("active");
          if (btnLike.classList.contains("active")) {
            btnLike.classList.remove("active");
            countDisplay.textContent = currentScore - 2;
          } else {
            countDisplay.textContent = currentScore - 1;
          }
        }
      });
    }
  });

  // 2. ЛОГИКА ВАЛИДАЦИИ ФОРМ
  const forms = document.querySelectorAll(".needs-validation");
  Array.from(forms).forEach((form) => {
    form.addEventListener("submit", (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add("was-validated");
    }, false);
  });

  // 3. ПОПОСВЕТЫ ДЛЯ ОТКЛЮЧЕННЫХ ЭЛЕМЕНТОВ (кроме чекбоксов)
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