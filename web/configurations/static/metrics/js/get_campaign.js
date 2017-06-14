$(document).ready(function(){
        $("#id_user").on("change",get_campaigns);
        get_campaigns();

        function get_campaigns(){
            let user_id = $("#id_user").val();
            if(user_id){
                $("#id_campaign").html("");
                let request = $.ajax({
                    type: "GET",
                    url: "/metrics/get_campaign/",
                    data: {
                        "user_id":user_id,
                    },
                });
                request.done(function(response){
                    $("#id_campaign").html(response.campaign);
                    $("#id_campaign").trigger("change");
                });
            }else{
                $("#id_campaign").html("<option value='' selected='selected'>-----</option>");
                $("#id_campaign").trigger("change");
            }
        }
    });