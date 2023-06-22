App = function () {
  function configurarPasswordEye(selector) {
    var eyeButton = document.querySelector(selector);
    var icon = eyeButton.firstElementChild.firstElementChild;

    eyeButton.addEventListener('click', function () {
      var input = eyeButton.parentElement.parentElement.firstElementChild.firstElementChild;

      if (input.getAttribute('type') === 'text') {
        eyeButton.setAttribute('title', 'Clique para visualizar a senha');
        input.setAttribute('type', 'password');
        icon.setAttribute('class', 'fa-solid fa-eye');
      } else {
        eyeButton.setAttribute('title', 'Clique para esconder a senha');
        input.setAttribute('type', 'text');
        icon.setAttribute('class', 'fa-solid fa-eye-slash');
      }
    });
  }

  function configurarTabs() {
    var tabs = document.querySelectorAll('.tabs li');
    var tabContents = document.querySelectorAll('#tab-content > div');

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (item) {
          item.classList.remove('is-active');
        });
        tab.classList.add('is-active');

        var target = tab.dataset.target;
        tabContents.forEach(function (div) {
          if (div.getAttribute('id') === target) {
            div.classList.remove('is-hidden');
          } else {
            div.classList.add('is-hidden');
          }
        });
      });
    });
  }

  return {
    configurarPasswordEye: configurarPasswordEye,
    configurarTabs: configurarTabs
  };
}();
