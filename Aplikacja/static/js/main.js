
/* show bootstrap tab on on click */
function activateTab(tab){
	$('.nav-tabs a[href="#' + tab + '"]').tab('show');
}


$(".dropdown-menu li a").click(function(){
  var selText = $(this).text();
  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});





/* Languages */
var lang = new Lang('en');
lang.init({
	defaultLang: 'en',
	currentLang: 'en',
	cookie: {
			name: 'langCookie',
			expiry: 365,
			path: '/'
	},
	allowCookieOverride: true
});


$('.lang').click(function() {
	window.lang.change(  $(this).attr('data-lang')  );
	$(this).parent().click();
	$('.currentLangName').text(Cookies.get('langCookie').toUpperCase());
	$('html').attr("lang", Cookies.get('langCookie')).attr("class", "lang-" + Cookies.get('langCookie'));
	return false;
});





/* Form validation */
$(function() {
	
	if ( $("form[name='mc-embedded-subscribe-form']").length ) {
	
		$.validator.addMethod("checkboxes", function(value, element) {
				return $('input[type=checkbox]:checked').length > 0;
		});
	
		$("form[name='mc-embedded-subscribe-form']").validate({
			rules: {
				'email': { required: true, email: true },
				'gdpr[18417]' : { checkboxes: true }
			},
			messages: {
				'email': "Please enter a valid email address.",
				'gdpr[18417]': "Please select at least one checkbox."
			},
			submitHandler: function(form) { form.submit(); }
		});
		
	}
	
});



/* Newsletter */
$(document).ready( function () {
    var $form = $('form');
    $( "#successSubscribe" ).hide();
    $( "#errorSubscribe" ).hide();

    if ( $form.length > 0 ) {
        $('#btnSubmit').bind('click', function ( event ) {
            if ( event ) event.preventDefault();
            $( "#successSubscribe" ).hide();
            $( "#errorSubscribe" ).hide();

            register($form);
            //if ( validate_input($form) ) { register($form); }
        });
    }
});

function register($form) {
    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize(),
        cache       : false,
        dataType    : 'json',
        contentType: "application/json; charset=utf-8",
        error       : function(err) { 
            console.log("Could not connect to the registration server. Please try again later.");
            console.log(err);
         },
        success     : function(data) {
            console.log(data.msg);
            if (data.result != "success") {
                $( "#errorSubscribe" ).html(data.msg);
                $( "#errorSubscribe" ).slideDown( data.msg ); 
               
            } else {
                $( "#successSubscribe" ).html(data.msg);
                $( "#successSubscribe" ).slideDown( data.msg );
            }
        }
    });
}







/* DOC READY */

$(document).ready(function(){


	/* Set current language name */
	if ( Cookies.get('langCookie') ) {
		$('.currentLangName').text(Cookies.get('langCookie').toUpperCase());
		$('html').attr("lang", Cookies.get('langCookie')).attr("class", "lang-" + Cookies.get('langCookie'));
	}


	// Page scrolling to element
	$('a.page-scroll').click(function(event) {
		var $anchor = $(this);
		var offset = $(this).attr('scroll-offset');
		if (typeof offset == 'undefined') offset = 0;
		console.log(offset);

		$('html, body').clearQueue().animate({
				scrollTop: ($($anchor.attr('href')).offset().top + parseInt(offset))
		}, 1250, 'easeInOutExpo');

		event.preventDefault();
	});




	/* Quotes red block navigation */
	$(".qBlock .nav").click(function() {
		$(this).parent().siblings('.row:hidden').stop().clearQueue().fadeIn().siblings('.row').stop().hide();		
	});



	// Subnavigation - pin to the side
	if ( $( "#main-submenu" ).length && $( "#submenu-trigger" ).length ) {
		
		$('#main-submenu').affix({
				offset: {
						top: jQuery('#submenu-trigger').offset().top - 10
				}
		});
	}


	// Email address - antispam
	$('.email').each(function() {
		var $email = $(this);
		var address = $email.text()
			.replace(/\s*\[at\]\s*/, '@')
			.replace(/\s*\[dot\]\s*/g, '.');
		$email.html('<a href="mailto:' + address + '">' + address +'</a>');
	});




	// Roadmap interaction
	$('.milestone').click(function(event) {
		event.stopPropagation();			
		if ( $(this).hasClass("active") ) {}
		else {
			$(".roadmap .details").hide();
			$(".roadmap .milestone").removeClass('active');
			$(this).addClass('active');
			$(this).children(".details").slideDown();	
		}
	});
	


	// Roadmap interaction
	$('.section-problems .box3d').click(function() {
		$(this).toggleClass('active');
		$(this).parent().siblings().children().removeClass('active');
		$(this).siblings().removeClass('active');
	});




	// Team - show more persons
	$(".person-more").click(function() {
		$(this).parent().hide();		
		$(".person-hidden").fadeIn("slow");		
	});





	// Owl carousel
	$(".owl-carousel.owl01").owlCarousel({
		loop: false,
		nav: false,
		dots: true,
		autoplay: true,			
		responsive:{
				0:{
						items:1
				},
				500:{
						items:2
				},
				1000:{
						items:3
				}
		}
	});

	$(".owl-carousel.owl02").owlCarousel({
		loop: true,
		nav: false,
		dots: true,
		autoplay: true,			
		responsive:{
				0:{
						items:1
				}
		}
	});




	/* Open/hide mobile menu */
	$(".navbar-toggle").click(function() {
		$(".navbar-collapse.collapse").toggle();
	});



	/* Disable scrolling in the background when mobile menu is open */
	if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
		$('.navbar-collapse').on('shown.bs.collapse', function() { 
			 $('body').css('position', 'fixed').css('width','100%');
		});
		$('.navbar-collapse').on('hidden.bs.collapse', function() {
			 $('body').css('position', 'static').css('width','auto');
		});
	}



		/* Modal triggers */
	  $(".trigger-videModal").click(function(){
		$("#videoModal").modal("show");
	  });
	  $("#videoModal").on('hidden.bs.modal', function(){
			jQuery('.youtube-video')[0].contentWindow.postMessage('{"event":"command","func":"' + 'pauseVideo' + '","args":""}', '*');
	  });

	  $(".trigger-soonModal").click(function(){
		$("#soonModal").modal("show");
	  });

	  $(".bio-trigger").click(function(){
		$(this).parents().next(".modal-bio").modal("show");
	  });

	  $(".trigger-subscribe").click(function(){
		$("#subscribeModal").modal("show");
	  });




	

});
/* end of DOC READY */





