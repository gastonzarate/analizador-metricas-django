$(document).ready(function(){
    $ ('.open-popup-link').magnificPopup({ type : 'inline' , midClick : true});
    $ ('.open-popup-contacto').magnificPopup({ type : 'inline' , midClick : true});
    
    let estaMaximo = $(window).width() > 768;

    moverPrimeraVez(768);
    

    $(window).resize(function(){
		mover(768);
	});

	$('.collapse').on('show.bs.collapse hide.bs.collapse', function(e) {
        e.preventDefault();
    });
    $('[data-toggle="collapse"]').on('click', function(e) {
        e.preventDefault();
        $($(this).data('target')).toggleClass('in');
    });

	function mover(num){
		if ($(window).width() < num){
			if(estaMaximo===true){
				$("#mark").insertAfter("#mork");
				$("#mork").insertAfter("#panel-raro");
				estaMaximo = false;
			}
		}else{
			if(estaMaximo===false){
				$("#mork").insertAfter("#mark");
				$("#mark").insertBefore("#panel-raro");
				estaMaximo=true;
			}
		}
	};

	function moverPrimeraVez(num){
		if (estaMaximo!=true){
			$("#mark").insertAfter("#mork");
			$("#mork").insertAfter("#panel-raro");
		}
	};

});
