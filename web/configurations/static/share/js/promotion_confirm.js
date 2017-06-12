$(document).ready(function(){
        $(".eliminar").click(function(){

             let confirma = confirm("¿Estás seguro que deseas eliminar tu promoción? Esto eliminara los clientes de la misma.");
             if(!confirma){
                return false;
            };
        });
    });