var mySwiper = new Swiper('.mySwiper1', {
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
    lazy: {
        loadPrevNext: true,
    },
    // pagination: {
    //   el: ".swiper-pagination",
    //   clickable: true,
    // },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
});
mySwiper.update();

var swiper = new Swiper(".mySwiper2", {
    slidesPerView: 5,
    spaceBetween: 3,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    breakpoints: {
      // 320px ~
      320: {
        slidesPerView: 2,
        spaceBetween: 20
      },
      // 480px ~
      480: {
        slidesPerView: 3,
        spaceBetween: 20
      },
      // 640px ~
      640: {
        slidesPerView: 4,
        spaceBetween: 0
      }
    }
});
swiper.update();
    $(document).ready(function() {
        $('[data-toggle="tooltip"]').tooltip();
    })

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })