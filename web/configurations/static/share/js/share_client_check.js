$(document).ready(function() {
        $("#id_user_share").on("change", getOffers);
        getOffers();

    });

        function getOffers() {
            var offerId = $("#id_user_share").val();
            if (offerId) {
                // Eliminamos las opciones anteriores del select
                $("#id_offer").html("");
                var request = $.ajax({
                    type: "GET",
                    url: "{% url 'get_offers' %}",
                    data: {
                        "user_share_id": offerId,
                    },
                });
                request.done(function(response) {
                    // Agregamos los resultados al select
                    $("#id_offer").html(response.offers);
                    $("#id_offer").trigger("change");
                });
            } else {
                $("#id_offer").html("<option value='' selected='selected'>---------</option>");
                $("#id_offer").trigger("change");
            }
        }
