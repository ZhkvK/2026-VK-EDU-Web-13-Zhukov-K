document.addEventListener('DOMContentLoaded', () => {

  // 1. ЛОГИКА ЛАЙКОВ И ДИЗЛАЙКОВ
  
  const voteGroups = document.querySelectorAll('.vote-group');

  voteGroups.forEach(group => {
    const btnLike = group.querySelector('.btn-like');
    const btnDislike = group.querySelector('.btn-dislike');
    const countLike = btnLike.querySelector('.vote-count');
    const countDislike = btnDislike.querySelector('.vote-count');

    // Логика нажатия на Лайк
    if (btnLike && btnDislike) { // Проверка, что кнопки существуют (защита от ошибок)
      btnLike.addEventListener('click', () => {
        if (btnLike.classList.contains('active')) {
          btnLike.classList.remove('active');
          countLike.textContent = parseInt(countLike.textContent) - 1;
        } else {
          btnLike.classList.add('active');
          countLike.textContent = parseInt(countLike.textContent) + 1;

          if (btnDislike.classList.contains('active')) {
            btnDislike.classList.remove('active');
            countDislike.textContent = parseInt(countDislike.textContent) - 1;
          }
        }
      });

      // Логика нажатия на Дизлайк
      btnDislike.addEventListener('click', () => {
        if (btnDislike.classList.contains('active')) {
          btnDislike.classList.remove('active');
          countDislike.textContent = parseInt(countDislike.textContent) - 1;
        } else {
          btnDislike.classList.add('active');
          countDislike.textContent = parseInt(countDislike.textContent) + 1;

          if (btnLike.classList.contains('active')) {
            btnLike.classList.remove('active');
            countLike.textContent = parseInt(countLike.textContent) - 1;
          }
        }
      });
    }
  });

  // 2. ЛОГИКА ВАЛИДАЦИИ ФОРМ
  
  // Находим все формы на странице с классом needs-validation
  const forms = document.querySelectorAll('.needs-validation');

  // Перебираем их и вешаем слушатель на событие отправки (submit)
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      // Если форма не прошла внутреннюю проверку HTML5 (required, minlength и т.д.)
      if (!form.checkValidity()) {
        event.preventDefault(); // Останавливаем отправку формы
        event.stopPropagation(); // Останавливаем всплытие события
      }

      // Добавляем класс was-validated, чтобы Bootstrap показал красные/зеленые рамки
      form.classList.add('was-validated');
    }, false);
  });

});