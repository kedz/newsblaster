
/**
  * Tap Mobile Device
  * Animation
  * Go Top Button
  * Lastest Tweets
  * Tabs
  * Toggles
  * Galleries
  * Dropdown List
  * Simple Slider
  * Slider
  * Handle Search Form
  * Handle Panel Toggle
  * Mega Menu
  * Detect Viewport
  * Hide Navigation
  * Scroll Bar
  * Login Popup
  * Google Map
  * Ajax Contact Form
  * Responsive Menu
  * Mailchimp Subscribe
*/

;(function($) {

   'use strict'

    var tapMobile = function() {
        $('.mainnav li:has(ul)').doubleTapToGo();
    };

    var gnAnimation = function() {
        $('.gn-animation').each( function() {
            var gnElement = $(this),
            gnAnimationClass = gnElement.data('animation'),
            gnAnimationDelay = gnElement.data('animation-delay'),
            gnAnimationOffset = gnElement.data('animation-offset');

            gnElement.css({
                '-webkit-animation-delay':  gnAnimationDelay,
                '-moz-animation-delay':     gnAnimationDelay,
                'animation-delay':          gnAnimationDelay
            });

            gnElement.waypoint(function() {
                gnElement.addClass('animated').addClass(gnAnimationClass);
            },{ triggerOnce: true, offset: gnAnimationOffset });
        });
    };

    var goTop = function() {
        $(window).scroll(function() {
            if ( $(this).scrollTop() > 800 ) {
                $('.go-top').addClass('show');
            } else {
                $('.go-top').removeClass('show');
            }
        }); 

        $('.go-top').on('click', function() {
            $("html, body").animate({ scrollTop: 0 }, 1000 , 'easeInOutExpo');
            return false;
        });
    };

    var lastestTweets = function() {
        if ( $().tweet ) {
            $('.latest-tweets').each(function() {
                var $this = $(this);

                $this.tweet({
                    username: $this.data('username'),
                    join_text: "auto",
                    avatar_size: null,
                    count: $this.data('number'),
                    template: "{text}{time}",
                    loading_text: "loading tweets...",
                    modpath: $this.data('modpath')      
                }); // tweet
            }); // lastest-tweets each
        }
    };

    var tabs = function() {
        $('.tabs').each(function() {
            $(this).children('.content-tab').children().hide();
            $(this).children('.content-tab').children().first().show();
            $(this).find('.menu-tab').children('li').on('click', function(e) {  
                var liActive = $(this).index(),
                	contentActive = $(this).siblings().removeClass('active').parents('.tabs').children('.content-tab').children().eq(liActive);

                contentActive.addClass('active').fadeIn('slow');
                contentActive.siblings().removeClass('active');
                $(this).addClass('active').parents('.tabs').children('.content-tab').children().eq(liActive).siblings().hide();
                e.preventDefault();
            });
        });
    };

    var toggles = function() {
        var args = {duration: 400};

        $('.toggle .toggle-title.active').siblings('.toggle-content').show();
        $('.toggle.toggle-enable .toggle-title').on('click', function() {
            $(this).closest('.toggle').find('.toggle-content').slideToggle(args);
            $(this).toggleClass('active');
        }); // toggle 

        $('.accordion .toggle-title').on('click', function () {
            if( !$(this).is('.active') ) {
                $(this).closest('.accordion').find('.toggle-title.active').toggleClass('active').next().slideToggle(args);
                $(this).toggleClass('active');
                $(this).next().slideToggle(args);
            } else {
                $(this).toggleClass('active');
                $(this).next().slideToggle(args);
            }     
        }); // accordion
    };

    var gnGallery = function() {
        $('.gn-gallery').each(function(){
            $(this).children('#gn-carousel').flexslider({
                animation: "slide",
                controlNav: false,
                animationLoop: false,
                slideshow: false,
                itemWidth: 92,
                itemMargin: 5,
                asNavFor: $(this).children('#gn-slider'),
                prevText: '<i class="fa fa-caret-left"></i>',
                nextText: '<i class="fa fa-caret-right"></i>'
            });
            $(this).children('#gn-slider').flexslider({
                animation: "slide",
                controlNav: false,
                animationLoop: false,
                slideshow: false,
                sync: $(this).children('#gn-carousel'),
                prevText: '<i class="fa fa-angle-left"></i>',
                nextText: '<i class="fa fa-angle-right"></i>'
            });
        });
    };

    var dropList = function() {
        $('.drop-list').each(function() {
            var menuDrop = $(this).children('.nav-dropdown'),
                activeDrop = $(this).find('.drop-wrap');

            menuDrop.on('click', function () {
                var drop = $(this).children('.dropdown');

                if ( drop.is(".show") ) {
                    drop.removeClass('show');
                    activeDrop.removeClass('active');
                } else {
                    drop.addClass('show');
                    activeDrop.addClass('active');
                }
                return false;
            });

            $(document).on('click', function() {
                menuDrop.children('.dropdown').removeClass('show');
                activeDrop.removeClass('active');
            });
        });
    };

   var gnSimpleSlider = function() {
      if ( $().flexslider ) {
         $('.simple-slider').each(function() {
            var $this = $(this);
            var easing = ( $this.data('effect') == 'fade' ) ? 'linear' : 'easeInOutExpo';
            $this.find('.flexslider').flexslider({
               animation      :  $this.data('effect'),
               direction      :  $this.data('direction'), // vertical
               pauseOnHover   :  true,
               useCSS         :  false,
               easing         :  easing,
               animationSpeed :  500,
               slideshowSpeed :  5000,
               controlNav     :  true,
               directionNav   :  false,
               smoothHeight   :  true,
               slideshow      :  $this.data('auto'),
               prevText    :  '<i class="fa fa-angle-left"></i>',
               nextText    :  '<i class="fa fa-angle-right"></i>'
            }); // flexslider
         }); // or-slider each
      }
   };

    var gnSlider = function() {
        $('.gnSlider .flexslider').flexslider({
            animation: 'fade',
            animationLoop: true,
            slideshow: true,
            slideshowSpeed: 4000,
            animationSpeed: 800,
            pauseOnHover: true, 
            pauseOnAction:true,
            controlNav: true,
            directionNav: true,
            prevText: '<i class="fa fa-angle-left"></i>',
            nextText: '<i class="fa fa-angle-right"></i>',
            controlsContainer: '.flex-container',
            start: function(slider) {
                var bottomtext = $('.gnSlider .flex-active-slide .item').data('bottomtext');

                $('.gnSlider .flex-active-slide').find('.item').css({ bottom: bottomtext });
                $('.gnSlider .flex-active-slide').find('.item').transition({ left: '0', opacity: '1'}, 1000);
                // remove class loading after start
                slider.removeClass('loading');
            },
            before: function(slider) {
                $('.gnSlider .flex-active-slide').find('.item').transition({ left: '-100%', opacity: '0'}, 1000);
            },
            after: function(slider) {
                var bottomtext = $('.gnSlider .flex-active-slide .item').data('bottomtext');

                $('.gnSlider .flex-active-slide').find('.item').css({ bottom: bottomtext});
                $('.gnSlider .flex-active-slide').find('.item').transition({ left: '0', opacity: '1'}, 1000);
            }
        });
    };

    var searchHandle = function() {
        $('.hide-navigation .search-icon').on('click', function() {
            var searchForm = $(this).parent().find('.search-form'),
                searchField = $(this).parent().find('.search-field');

            searchForm.stop(true, true).fadeToggle(function () {
                searchField.focus();
            });

            $('.search-field').on('click', function(e) {
                e.stopPropagation();
            })
        });

        $('.search-wrap .search-icon').on('click', function() {
            var searchForm = $(this).parent().find('.search-form'),
                searchField = $(this).parent().find('.search-field');

            searchForm.fadeIn(function () {
                searchForm.find('.search-field').focus();
            });
        });

        $('.search-wrap .search-close').on('click', function() {
            $(this).parent().fadeOut();
        });

        $(window).resize(function() {
            if ( $('.search-wrap .search-form').is(':hidden') ) {
                $('.search-wrap .search-form').removeAttr('style');
            }
        });

        $(document).on('click', function(e) {
            var clickID = e.target.id;

            if ( clickID != 'search-text-menu' ) {
                $(".search-text-menu").animate({
                    width:'1px',
                    },200,function(){
                        $(this).css( 'paddingLeft','41px');
                    });
            } else {
				$(".search-text-menu").animate({
	                width:'282px',
	                },200,function(){
	                    $(this).css( 'paddingLeft','55px');
	                });
            }
        });
    };

    var changePanel = function() {
        (function() {
            function handlePanel() {
                var typePanel = "normal";

                if ( matchMedia('only screen and (max-width: 991px)').matches ) {
                    typePanel = "float";
                }
                if ( $('body').hasClass('change-panel') ) {
                    
                    if ( typePanel === "float" ) {
                        var $mobilePanel = $('#sidebar2').hide();

                        $('body').addClass('floatPanel').append($mobilePanel);
                        $('#sidebar2, .toggle-panel').removeAttr('style');
                        $('.toggle-panel').css({
                            'top': $(window).height() / 2,
                            'marginTop' : '-46px'
                        });
                    } else {
                        var $normalPanel = $('#sidebar2');

                        $('.article-endless').find('.col-md-4').append($normalPanel);
                        $('body').removeClass('floatPanel');
                        $('.toggle-panel').hide();
                    }
                }
            }
            $(window).on("resize", handlePanel);
            $(document).on("ready", handlePanel);
        })();
        (function(){
            $('.toggle-panel').on('click', function(e) {
                if ( $("#sidebar2").css("left") === "-300px" ) {
                    $("#sidebar2").animate({ left: "0" }, 300, 'easeInOutExpo')
                } else {
                    $("#sidebar2").animate({ left: "-300px" }, 300, 'easeInOutExpo')
                }
                e.preventDefault();
            });
        })();
    };

    var megaMenu = function(winWidth) {
        if ( $('.gn-mega-menu').size() != 0 ) {
            var item = $('.gn-mega-menu'),
                megaMenuLeft = item.offset().left;

            item.children('.sub-menu').css({
                'width' : $(window).width(),
                'margin-left' : - megaMenuLeft
            });
        }
    };

    var detectViewport = function() {
        $('[data-waypoint-active="yes"]').waypoint(function() {
            $(this).trigger('on-appear');
        }, { offset: '90%' });

        $(window).on('load', function() {
            setTimeout(function() {
                $.waypoints('refresh');
            }, 100);
        });
    };

    var hideMenu = function() {
        $('#hide-menu').on('click', function(e) {
            if ( $("#navigation-panel").css("left") === "-215px" ) {
                $("#navigation-panel").animate({ left: "0" }, 300, 'easeInOutExpo')
            } else {
                $("#navigation-panel").animate({ left: "-215px" }, 300, 'easeInOutExpo')
            }
            e.preventDefault();
        });

        $('.close-nav').on('click', function() {
            $("#navigation-panel").animate({ left: "-215px" }, 200, 'easeInOutExpo');
        });
    };

    var scrollBar = function() {
        if ( $().mCustomScrollbar ) {
           $(".tabs.style2 .content-tab.scroll .content").mCustomScrollbar();
        }
    };

    var popupForm = function() {
        if ( $().leanModal ) {
            $('.login-popup > a, .signup-popup > a').leanModal({
                top: 110,
                overlay: 0.5,
                closeButton: ".close-modal"
            });
            $('#login-modal').submit(function(e) {
                return false;
            });
        }
    };

    var googleMap = function() {
        if ( $().gmap3 ) {
            $("#map").gmap3({
                map:{
                    options:{
                        zoom: 17,
                        mapTypeId: 'goodnews_style',
                        mapTypeControlOptions: {
                            mapTypeIds: ['goodnews_style', google.maps.MapTypeId.SATELLITE, google.maps.MapTypeId.HYBRID]
                        },
                        scrollwheel: false
                    }
                },
                getlatlng:{
                    address:  "3 London Rd London SE1 6JZ United Kingdom",
                    callback: function(results) {
                        if ( !results ) return;
                        $(this).gmap3('get').setCenter(new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng()));
                        $(this).gmap3({
                            marker:{
                                latLng:results[0].geometry.location
                            }
                        });
                    }
                },
                styledmaptype:{
                    id: "goodnews_style",
                    options:{
                        name: "Good News Map"
                    },
                },
            });
        }
    };

    var ajaxContactForm = function() {
        $('.contact-form').each(function() {
            var $this = $(this);

            $this.submit(function() {
                var str = $this.serialize();
                $.ajax({
                    type: "POST",
                    url:  $this.attr('action'),
                    data: str,
                    success: function(msg) {
                        var result;

                        if ( msg == 'OK' ) {
                            result = '<div class="alert alert-success">Thank you! Your message has been successfully sent.</div>';
                        } else {
                            result = msg;
                        }
                        result = '<div class="result">' + result + '</div>';
                        $this.find('.note').hide().html(result).fadeIn('slow');
                    }
                });
                return false;
            });
        });
    };

    var responsiveMenu = {

        menuType: 'desktop',

        initial: function(winWidth) {
            responsiveMenu.menuWidthDetect(winWidth);
            responsiveMenu.menuBtnClick();
            responsiveMenu.parentMenuClick();
        },

        menuWidthDetect: function(winWidth) {
            var currMenuType = 'desktop';

            if ( matchMedia('only screen and (max-width: 767px)').matches ) {
                currMenuType = 'mobile';
            } // change menu type

            if ( currMenuType !== responsiveMenu.menuType ) {
                responsiveMenu.menuType = currMenuType;

                if ( currMenuType === 'mobile' ) {
                    var $mobileMenu = $('#mainnav').attr('id', 'mainnav-mobi').hide();
                    var hasChildMenu = $('#mainnav-mobi').find('li.has-children'),
                        hasChildMenuMega = $('#mainnav-mobi').find('li.gn-mega-menu');

                    $('#header').find('.header-wrap').after($mobileMenu);
                    $('.header-wrap').hide();
                    hasChildMenu.children('ul').hide();
                    hasChildMenuMega.children('.sub-menu').hide();
                    hasChildMenu.children('a').after('<span class="btn-submenu"></span>');
                    hasChildMenuMega.children('a').after('<span class="btn-submenu"></span>');
                    $('#mainnav-mobi').children('.menu').prepend('<li class="added menu-addon"><span class="signup-link"><a href="login.html">Become a member</a></span><span class="login-link"><a href="login.html">Login</a></span></li>');
                    $('#mainnav-mobi').children('.menu').append('<li class="added"><div id="search-form-menu"><form action="#" method="get"><input type="text" class="search-text-menu" id="search-text-menu"></form></div><div class="social-mobi"><a href="#"><i class="fa fa-facebook"></i></a><a href="#"><i class="fa fa-twitter"></i></a><a href="#"><i class="fa fa-google-plus"></i></a><a href="#"><i class="fa fa-linkedin"></i></a></div></li>');
                    $('.btn-menu').removeClass('active');
                 } else {
                    var $desktopMenu = $('#mainnav-mobi').attr('id', 'mainnav').removeAttr('style');

                    $desktopMenu.find('.sub-menu').removeAttr('style');
                    $('.header-wrap').removeAttr('style');
                    $('#header').find('.col-md-9').append($desktopMenu);
                    $('.btn-submenu').remove()
                    $('.added').remove();
                }
            } // clone and insert menu
        },

        menuBtnClick: function() {
            $('.btn-menu').on('click', function() {
                $('#mainnav-mobi').slideToggle(300);
                $(this).toggleClass('active');
            });
        }, // click on moblie button

        parentMenuClick: function() {
            $(document).on('click', '#mainnav-mobi li .btn-submenu', function(e) {
                if ( $(this).has('.sub-menu') ) {
                    e.stopImmediatePropagation()
                    $(this).next('.sub-menu').slideToggle(300);
                    $(this).toggleClass('active');
                    $(this).parent('.has-children, .gn-mega-menu').toggleClass('active');
                }
            });
        } // click on sub-menu button
    };

    var ajaxSubscribe = {
        obj: {
            subscribeEmail    : $('#subscribe-email'),
            subscribeButton   : $('#subscribe-button'),
            subscribeMsg      : $('#subscribe-msg'),
            subscribeContent  : $("#subscribe-content"),
            dataMailchimp     : $('#subscribe-form').attr('data-mailchimp'),
            success_message   : '<div class="notification_ok">Thank you for joining our mailing list! Please check your email for a confirmation link.</div>',
            failure_message   : '<div class="notification_error">Error! <strong>There was a problem processing your submission.</strong></div>',
            noticeError       : '<div class="notification_error">{msg}</div>',
            noticeInfo        : '<div class="notification_error">{msg}</div>',
            basicAction       : 'mail/subscribe.php',
            mailChimpAction   : 'mail/subscribe-mailchimp.php'
        },

        eventLoad: function() {
            var objUse = ajaxSubscribe.obj;

            $(objUse.subscribeButton).on('click', function() {
                if ( window.ajaxCalling ) return;
                var isMailchimp = objUse.dataMailchimp === 'true';

                if ( isMailchimp ) {
                    ajaxSubscribe.ajaxCall(objUse.mailChimpAction);
                } else {
                    ajaxSubscribe.ajaxCall(objUse.basicAction);
                }
            });
        },

        ajaxCall: function (action) {
            window.ajaxCalling = true;
            var objUse = ajaxSubscribe.obj;
            var messageDiv = objUse.subscribeMsg.html('').hide();
            $.ajax({
                url: action,
                type: 'POST',
                dataType: 'json',
                data: {
                   subscribeEmail: objUse.subscribeEmail.val()
                },
                success: function (responseData, textStatus, jqXHR) {
                    if ( responseData.status ) {
                        objUse.subscribeContent.fadeOut(500, function () {
                            messageDiv.html(objUse.success_message).fadeIn(500);
                        });
                    } else {
                        switch (responseData.msg) {
                            case "email-required":
                                messageDiv.html(objUse.noticeError.replace('{msg}','Error! <strong>Email is required.</strong>'));
                                break;
                            case "email-err":
                                messageDiv.html(objUse.noticeError.replace('{msg}','Error! <strong>Email invalid.</strong>'));
                                break;
                            case "duplicate":
                                messageDiv.html(objUse.noticeError.replace('{msg}','Error! <strong>Email is duplicate.</strong>'));
                                break;
                            case "filewrite":
                                messageDiv.html(objUse.noticeInfo.replace('{msg}','Error! <strong>Mail list file is open.</strong>'));
                                break;
                            case "undefined":
                                messageDiv.html(objUse.noticeInfo.replace('{msg}','Error! <strong>undefined error.</strong>'));
                                break;
                            case "api-error":
                                objUse.subscribeContent.fadeOut(500, function () {
                                    messageDiv.html(objUse.failure_message);
                                });
                        }
                        messageDiv.fadeIn(500);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    alert('Connection error');
                },
                complete: function (data) {
                    window.ajaxCalling = false;
                }
            });
        }
    };

    // Dom Ready
    $(function() {
        tapMobile();
        detectViewport();
        gnSimpleSlider();
        gnSlider();
        gnGallery();
        hideMenu();
        scrollBar();
        dropList();
        tabs();
        changePanel();
        toggles();
        searchHandle();
        popupForm();
        gnAnimation();
        goTop()
        googleMap();
        ajaxContactForm();
        ajaxSubscribe.eventLoad();
        // Initialize responsive and mega menu
        responsiveMenu.initial($(window).width());
        megaMenu($(window).width());
        $(window).resize(function() {
            responsiveMenu.menuWidthDetect($(this).width());
            megaMenu($(window).width());
        });
        lastestTweets();
   });

})(jQuery);