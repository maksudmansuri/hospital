(function ($){ "use strict";


  $(window).on('load', function () {
    $('#preloader-active').delay(450).fadeOut('slow');
    $('body').delay(450).css({
      'overflow': 'visible'
    });
  });


/* 1. mainSlider-1 */
    // h1-hero-active
    // mainSlider
    function mainSlider() {
      var BasicSlider = $('.h1-hero-active');
      BasicSlider.on('init', function (e, slick) {
        var $firstAnimatingElements = $('.single-slider:first-child').find('[data-animation]');
        doAnimations($firstAnimatingElements);
      });
      BasicSlider.on('beforeChange', function (e, slick, currentSlide, nextSlide) {
        var $animatingElements = $('.single-slider[data-slick-index="' + nextSlide + '"]').find('[data-animation]');
        doAnimations($animatingElements);
      });
      BasicSlider.slick({
        autoplay: false,
        autoplaySpeed: 10000,
        dots: false,
        fade: true,
        arrows: true,
        prevArrow: '<button type="button" class="slick-prev"><img src="static/front/img/hero_thumb/arrow-left.png" alt=""><img class="secondary-img" src="static/front/img/hero_thumb/left-white.png" alt=""></button>',
        nextArrow: '<button type="button" class="slick-next"><img src="static/front/img/hero_thumb/arrow-right.png" alt=""><img class="secondary-img" src="static/front/img/hero_thumb/right-white.png" alt=""></button>',
        responsive: [{
            breakpoint: 1024,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
              infinite: true,
            }
          },
          {
            breakpoint: 991,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
              arrows: false
            }
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
              arrows: false
            }
          }
        ]
      });

      function doAnimations(elements) {
        var animationEndEvents = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        elements.each(function () {
          var $this = $(this);
          var $animationDelay = $this.data('delay');
          var $animationType = 'animated ' + $this.data('animation');
          $this.css({
            'animation-delay': $animationDelay,
            '-webkit-animation-delay': $animationDelay
          });
          $this.addClass($animationType).one(animationEndEvents, function () {
            $this.removeClass($animationType);
          });
        });
      }
    }
    mainSlider();


/* 2. owlCarousel */
    //HTM active: owl-carousel-active , owl-carousel
    $('.owl-carousel-active').owlCarousel({
      loop:true,
      margin:0,
    items:1,
    navText:['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>'],
      nav:true,
    dots:false,
      responsive:{
          0:{
              items:1
          },
          767:{
              items:3
          },
          992:{
              items:5
          }
      }
  });


/* 3. h2-testmonial-active*/
  $('.testmonial-active').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor:'.testmonial-nav'
  });
  $('.testmonial-nav').slick({
    slidesToShow: 3,
    slidesToScroll: 1,
    asNavFor: '.testmonial-active',
    dots: false,
    infinite: true,
    autoplay: true,
    autoplaySpeed: 3000,
    arrows: false,
    prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-chevron-left"></i></button>',
    nextArrow: '<button type="button" class="slick-next"><i class="fas fa-chevron-right"></i></button>',
    centerMode: true,
    focusOnSelect: true,
    centerPadding:0,
  });

/* 4. Brand-Active -slick */
    $('.brand-active').slick({
      dots: false,
      autoplay:true,
      infinite: true,
      speed: 2500,
      arrows: false,
      slidesToShow: 5,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: true,
            dots: false,
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 991,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });

// 5. h2-team-active
    $('.h2-team-active').slick({
      dots: true,
      infinite: true,
      speed: 300,
      arrows: false,
      slidesToShow: 3,
      slidesToScroll: 1,
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 3,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });


// 6. feeds-active
    $('.feeds-active').slick({
      dots: false,
      infinite: true,
      speed: 300,
      arrows: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      prevArrow: '<button type="button" class="slick-prev"><i class="fas fa-arrow-left"></i></button>',
      nextArrow: '<button type="button" class="slick-next"><i class="fas fa-arrow-right"></i></button>',
      responsive: [
        {
          breakpoint: 1024,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            infinite: true,
            dots: false
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });


/* 7. Nice Selectorp */
    $('select').niceSelect();


/* 9. Mobile  manu Active */
    // menu ke upore show korar jonno je header er modde ase take bole dete hobe width: 100%; position: fixed;  z-index: 9999;
    jQuery('#mobile-menu').meanmenu({
      meanMenuContainer: '.mobile-menu',
      meanScreenWidth: "991",
      onePage:false
    });


/* 10. magnificPopup img view */
    $('.popup-image').magnificPopup({
      type: 'image',
      gallery: {
        enabled: true
      }
    });


/* 11. magnificPopup video view */
    $('.popup-video').magnificPopup({
      type: 'iframe'
    });

/* 14. Custom Sticky Menu */
  $(window).on('scroll', function () {
    var scroll = $(window).scrollTop();
    if (scroll < 245) {
      $(".header-sticky").removeClass("sticky-bar");
    } else {
      $(".header-sticky").addClass("sticky-bar");
    }
  });

/* 15. one Page Nav */
    var top_offset = $('.header-area').height() - 10;
    $('.main-menu nav ul').onePageNav({
      currentClass: 'active',
      scrollOffset: top_offset,
    });

/* 18. sildeBar scroll */
    $.scrollUp({
      scrollName: 'scrollUp', // Element ID
      topDistance: '300', // Distance from top before showing element (px)
      topSpeed: 300, // Speed back to top (ms)
      animation: 'fade', // Fade, slide, none
      animationInSpeed: 200, // Animation in speed (ms)
      animationOutSpeed: 200, // Animation out speed (ms)
      scrollText: '<i class="fas fa-arrow-up"></i>', // Text for element
      activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
    });

/* 19. data-background */
    $("[data-background]").each(function () {
      $(this).css("background-image", "url(" + $(this).attr("data-background") + ")")
      });


/* 20. WOW active */
    new WOW().init();

    	// map
    	function basicmap() {
    	  // Basic options for a simple Google Map
    	  // For more options see: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    	  var mapOptions = {
    	    // How zoomed in you want the map to start at (always required)
    	    zoom: 11,
    	    scrollwheel: false,
    	    // The latitude and longitude to center the map (always required)
    	    center: new google.maps.LatLng(40.6700, -73.9400), // New York
    	    // This is where you would paste any style found on Snazzy Maps.
    	    styles: [{
    	      "stylers": [{
    	        "hue": "#dd0d0d"
    	      }]
    	    }, {
    	      "featureType": "road",
    	      "elementType": "labels",
    	      "stylers": [{
    	        "visibility": "off"
    	      }]
    	    }, {
    	      "featureType": "road",
    	      "elementType": "geometry",
    	      "stylers": [{
    	        "lightness": 100
    	      }, {
    	        "visibility": "simplified"
    	      }]
    	    }]
    	  };
    	  // Get the HTML DOM element that will contain your map
    	  // We are using a div with id="map" seen below in the <body>
    	  var mapElement = document.getElementById('contact-map');

    	  // Create the Google Map using our element and options defined above
    	  var map = new google.maps.Map(mapElement, mapOptions);

    	  // Let's also add a marker while we're at it
    	  var marker = new google.maps.Marker({
    	    position: new google.maps.LatLng(40.6700, -73.9400),
    	    map: map,
    	    title: 'Cryptox'
    	  });
    	}
    	if ($('#contact-map').length != 0) {
    	  google.maps.event.addDomListener(window, 'load', basicmap);
    	}



})(jQuery);