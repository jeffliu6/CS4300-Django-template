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
        let popover = {};
        let str = "";
        
        if(weights.rating != 0) {
            let span = "<p class=\"rating-weight\"><b class=\"mr-3\">Rating</b> " + weights.rating.toFixed(2) + "</p>";
            str = str.concat(span);
        }

        if(weights.strength != 0) {
            let span = "<p class=\"keyword-weight\"><b class=\"mr-3\">Keywords</b> " + weights.keywords.toFixed(2) + "</p>";
            str = str.concat(span);
        }

        if(weights.medical) {
            popover.medical = [];
            let total = 0;
            Object.entries(weights.medical).forEach(function(entry){
                total += entry[1];
                popover.medical.push(entry[0]);
            })
            let span = "<p class=\"medical-weights\"><b class=\"mr-3\">Medical Effects</b>" + total.toFixed(2) +"<br/><span class=\"text-muted\">" +popover.medical.join(', ') + "</span></p>";
            str = str.concat(span);
        }

        if(weights.positive) {
            popover.positive = [];
            let total = 0;
            Object.entries(weights.positive).forEach(function(entry){
                total += entry[1];
                popover.positive.push(entry[0]);
            })
            let span = "<p class=\"positive-weights\"><b class=\"mr-3\">Desired Effects</b>" + total.toFixed(2) +"<br/><span class=\"text-muted\">" +popover.positive.join(', ') + "</span></p>";
            str = str.concat(span);
        }

        if(weights.negative) {
            popover.negative = [];
            let total = 0;
            Object.entries(weights.negative).forEach(function(entry){
                total += entry[1];
                popover.negative.push(entry[0]);
            })
            let span = "<p class=\"negative-weights\"><b class=\"mr-3\">Undesired Effects</b>" + total.toFixed(2) +"<br/><span class=\"text-muted\">" + popover.negative.join(', ') + "</span></p>";
            str = str.concat(span);
        }

        if(weights.flavor) {
            popover.flavors = [];
            let total = 0;
            Object.entries(weights.flavor).forEach(function(entry){
                total += entry[1];
                popover.flavors.push(entry[0]);
            })
            let span = "<p class=\"flavor-weights\"><b class=\"mr-3\">Flavors</b>" + total.toFixed(2) +"<br/><span class=\"text-muted\">" +popover.flavors.join(', ') + "</span></p>";
            str = str.concat(span);
        }
        
        if(weights.aroma) {
            popover.aromas = [];
            let total = 0;
            Object.entries(weights.aroma).forEach(function(entry){
                total += entry[1];
                popover.aromas.push(entry[0]);
            })
            let span = "<p class=\"aroma-weights\"><b class=\"mr-3\">Aromas</b>" + total.toFixed(2) +"<br/><span class=\"text-muted\">" +popover.aromas.join(', ') + "</span></p>";
            str = str.concat(span);
        }

        if(weights.strength != 0) {
            let span = "<p class=\"strength-weight\"><b class=\"mr-3\">Strength</b><br/>" + weights.strength.toFixed(2) + "</p>";
            str = str.concat(span);
        }

        return str;
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
                $("#similar-results").append('<div id="strain_'+ count +'" class="card bg-light strain-result ml-2 mr-2 mb-2 shadow">' + 
                // '<img src="' + strain[1]["image"] +'" class="card-img-top" alt="...">' +
                '<div class="card-body">' +
                    '<div class="d-flex justify-content-between"><h5 class="card-title font-weight-bolder mb-1">' + strain[1]["name"] +'</h5><p class="text-muted text-small">' + strain[0].toFixed(2) + '</p></div>' +
                        '<p class="card-text mb-1 text-muted font-italic">Rating: '+ Number(strain[1]["rating"]).toFixed(2) +'/5.00</p>' +
                        '<p class="card-text">'+ strain[1]["description"].substring(0, 90) +'...</p>' +
                        '<div class="d-flex justify-content-between"><p class="text-success modal-triggor" data-toggle="modal" data-target="#exampleModalLong">See More</p>' +
                        '<button type="button" class="btn" data-toggle="popover" data-triggor="focus" data-container="body" title="Shared Trait Weightings" ' + 
                        '"><img class="question-icon float-right" src="/static/images/question-mark-light.png"/></button></div>' +
                        '</div>' +
                '</div>');
                
                $("[data-toggle=popover]").popover({
                    trigger: 'focus',
                    html: true,
                    content: get_popover(strain[2])
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