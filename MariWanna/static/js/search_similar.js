$(document).ready(function() {

    $("#similarSearch").fadeIn(500);
    let requestData = {};
    requestData.query = "similar";

    // Submit request logic
    $( "#similarSearch" ).submit(function( event ) {
        event.preventDefault();
        requestData.strain = $("#strain-input").val();
        $.post( "results-similar", JSON.stringify(requestData))
        .always(function() {
            $("#loadingDiv").fadeIn();
        })
        .done(function( data ) {
            data = JSON.parse(data);
            
            $('#results').empty();
            
            let count = 0;

            data.forEach(function(strain){

                console.log(strain);
                
                $("#results").append('<div id="strain_'+ count +'" class="card strain-result ml-2 mr-2 mb-2 shadow">' + 
                // '<img src="' + strain[1]["image"] +'" class="card-img-top" alt="...">' +
                '<div class="card-body">' +
                    '<div class="d-flex justify-content-between"><h5 class="card-title font-weight-bolder mb-1">' + strain[1]["name"] +'</h5><p class="text-muted text-small">' + strain[0].toFixed(2) + '</p></div>' +
                        '<p class="card-text mb-1 text-muted font-italic">Rating: '+ Number(strain[1]["rating"]).toFixed(2) +'/5.00</p>' +
                        '<p class="card-text">'+ strain[1]["description"].substring(0, 90) +'...</p>' +
                        '<p class="text-success modal-triggor" data-toggle="modal" data-target="#exampleModalLong">See More</p>' +
                    '</div>' +
                '</div>');
                
                $("#strain_" + count).on("click", function() {
                    $("#modal-name").text(strain[1]["name"]);
                    $("#modal-description").text(strain[1]["description"]);
                    $("#modal-medical").text(strain[1]["medical"]);
                    $("#modal-desired").text(strain[1]["positive"]);
                    $("#modal-undesired").text(strain[1]["negative"]);                    
                    $("#modal-flavors").text(strain[1]["flavors"]);
                    $("#modal-aromas").text(strain[1]["aromas"]);
                });

                count++;

            });

            $("#loadingDiv").fadeOut();
            $("#similarSearch").slideUp();
            console.log(requestData.strain);
            $("#results-header").text("Strains similar to " + requestData.strain + ":").show();
            $("#results").addClass("d-flex").show(500);


        });
    });
});