$(document).ready(function() {

    $("#similarSearch").fadeIn(500);
    let requestData = {};
    requestData.query = "similar";

    $.getJSON("/static/data/strain_names.json", function(names){
        let count = 0;
        names = names.map((name) => {return {"id":name, "text":name};});
        
        $("#strain-input").select2({
            data: names
        });
    });

    function get_popover(weights) {
        return Object.keys(weights).join(", ");
    }

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
            
            $('#similar-results').empty();
            
            let count = 0;

            data.forEach(function(strain){

                console.log(strain);
                $("#similar-results").append('<div id="strain_'+ count +'" class="card strain-result ml-2 mr-2 mb-2 shadow">' + 
                // '<img src="' + strain[1]["image"] +'" class="card-img-top" alt="...">' +
                '<div class="card-body">' +
                    '<div class="d-flex justify-content-between"><h5 class="card-title font-weight-bolder mb-1">' + strain[1]["name"] +'</h5><p class="text-muted text-small">' + strain[0].toFixed(2) + '</p></div>' +
                        '<p class="card-text mb-1 text-muted font-italic">Rating: '+ Number(strain[1]["rating"]).toFixed(2) +'/5.00</p>' +
                        '<p class="card-text">'+ strain[1]["description"].substring(0, 90) +'...</p>' +
                        '<div class="d-flex justify-content-between"><p class="text-success modal-triggor" data-toggle="modal" data-target="#exampleModalLong">See More</p>' +
                        '<button type="button" class="btn" data-toggle="popover" data-triggor="focus" data-container="body" title="Shared Traits" data-content=" ' + 
                        get_popover(strain[3]) + '"><img class="question-icon float-right" src="/static/images/question-mark-light.png"/></button></div>' +
                        '</div>' +
                '</div>');
                
                $("[data-toggle=popover]").popover({
                    trigger: 'focus'
                  });

                $("#strain_" + count).on("click", function() {

                    $("#modal-img").empty();
                    if (strain[1]["image"] != "https://www.cannabisreports.com/images/strains/no_image.png") {
                        $("#modal-img").append('<img style="max-height:300px" src="' + strain[1]["image"] +'" class="rounded mb-3 img-fluid" alt="...">');
                    }
                    $("#modal-name").text(strain[1]["name"]);
                    $("#modal-description").text(strain[1]["description"]);

                    if (strain[1]["medical"]) {
                        $("#modal-medical").text(strain[1]["medical"].join(", "));
                    } else {
                        $("#modal-medical-label").hide();
                    }
                    
                    if (strain[1]["positive"]) {
                        $("#modal-desired").text(strain[1]["positive"].join(", "));
                    } else {
                        $("#modal-desired-label").hide();
                    }

                    if (strain[1]["negative"]) {
                        console.log(strain[1]["negative"].length)
                        $("#modal-undesired").text(strain[1]["negative"].join(", "));   
                    } else {
                        $("#modal-undesired-label").hide();
                    }

                    if (strain[1]["flavor_descriptors"]) {
                        $("#modal-flavors").text(strain[1]["flavor_descriptors"].join(", "));
                    } else {
                        $("#modal-flavors-label").remove();
                    }      
                    
                    if (strain[1]["aroma"]) {
                        $("#modal-aromas").text(strain[1]["aroma"].join(", "));
                    } else {
                        $("#modal-aromas-label").remove();
                    }                

                    
                });

                count++;
            });
            $("#loadingDiv").fadeOut();

            $("#similarSearch").slideUp();
            $("#results-header").html("Strains similar to <b>" + requestData.strain + "</b>:").show();
            $("#similar-results").addClass("d-flex").show(500);


        });
    });
});