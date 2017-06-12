$(document).ready(function(){
    $(".delete").click(function(){
         let confirma = confirm("¿Estás seguro que deseas eliminar tu comercio? Esto eliminara todas las promociones y clientes del mismo.");
         if(!confirma){
            return false;
        };
    });
});