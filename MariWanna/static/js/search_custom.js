$(document).ready(function(){ $.getJSON( "/static/data/select-options.json" , function( select_data ){
    console.log(select_data.aromas);
    // Autocomplete Options
    let medical_effects = select_data.medical_effects
    let desired_effects = select_data.desired_effects;
    let undesired_effects = select_data.undesired_effects;
    let flavors = select_data.flavors;
    let aromas = select_data.aromas;

    $.each(medical_effects, function(key, value){
        $('#medical-effects')
        .append($("<option></option>")
                   .text(value));     
    });

    $.each(desired_effects, function(key, value){
        $('#desired-effects')
        .append($("<option></option>")
                   .text(value));     
    });

    $.each(undesired_effects, function(key, value){
        $('#undesired-effects')
        .append($("<option></option>")
                   .text(value));     
    });

    $.each(flavors, function(key, value){
        $('#flavors')
        .append($("<option></option>")
                   .text(value));     
    });

    $.each(aromas, function(key, value){
        $('#aromas')
        .append($("<option></option>")
                   .text(value));     
    });
   
    $("#customSearch").fadeIn(500);

    function addTag(word, type) {
        let color_class = "";

        if (type == "key-word") {
            if (medical_effects.indexOf(word) > -1) type = "medical-effect";
            else if (desired_effects.indexOf(word) > -1) type = "desired-effect";
            else if (undesired_effects.indexOf(word) > -1) type = "undesired-effect";
            else if (flavors.indexOf(word) > -1) {
                type = "flavor";
                if (aromas.indexOf(word) > -1) addTag(word, "aroma");
            }
            else if (aromas.indexOf(word) > -1) type = "aroma";
        }
        
        switch(type) {
            case "medical-effect":
                color_class = "bg-primary";
                break;
            case "desired-effect":
                color_class = "bg-success";
                break;
            case "undesired-effect":
                color_class = "bg-danger";
                break;
            case "flavor":
                color_class = "bg-info";
                break;
            case "aroma":
                color_class = "bg-aroma";
                break;
            default:
                color_class = "bg-secondary";
        }

        $('#allEffects').append("<p class=\"tag " + type + 
            " d-inline-flex justify-content-center align-items-center shadow-sm " + 
            "border m-1 pl-2 pr-2 text-small text-light " + color_class + 
            " rounded\">" + word.toLowerCase() + "<span class=\"remove-btn\">x</span></p>");
    }

    // Effects entry set up
    $('#key-words').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            addTag($(this).val(), "key-word");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    });
    $("#key-words-btn").click(function(){
        if ($("#key-words").val() != "") {
            addTag($("#key-words").val(), "key-word");
            $("#key-words").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#medical-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            addTag($(this).val(), "medical-effect");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(medical_effects, request.term);
    
            response(results.slice(0, 5));
        }
    });
    $("#medical-effects-btn").click(function(){
        if ($("#medical-effects").val() != "") {
            addTag($("#medical-effects").val(), "medical-effect");
            $("#medical-effects").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#desired-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            addTag($(this).val(), "desired-effect");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: desired_effects,
        max: 5
    });
    $("#desired-effects-btn").click(function(){
        if ($("#desired-effects").val() != "") {
            addTag($("#desired-effects").val(), "desired-effect");
            $("#desired-effects").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#undesired-effects').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            addTag($(this).val(), "undesired-effect");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: undesired_effects,
        max: 5
    });
    $("#undesired-effects-btn").click(function(){
        if ($("#undesired-effects").val() != "") {
            addTag($("#undesired-effects").val(), "undesired-effect");
            $("#undesired-effects").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#flavors').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            addTag($(this).val(), "flavor");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    }).autocomplete({
        source: flavors,
        max: 5
    });
    $("#flavors-btn").click(function(){
        if ($("#flavors").val() != "") {
            addTag($("#flavors").val(), "flavor");
            $("#flavors").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });

    $('#aromas').keypress(function(event) {
        let keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13' && $(this).val()!=""){
            event.preventDefault();
            addTag($(this).val(), "aroma");
            $(this).val("");
        }
        $(".remove-btn").click(function() {
            $(this).parent().remove();
        });
    })
    .autocomplete({
        source: aromas,
        max: 5
    });
    $("#aromas-btn").click(function(){
        if ($("#aromas").val() != "") {
            addTag($("#aromas").val(), "aroma");
            $("#aromas").val("");
            $(".remove-btn").click(function() {
                $(this).parent().remove();
            });
        }
    });
    

    // Strength slider configuration
    $("#strengthRange").slider({
        value:50,
        min: 0,
        max: 100,
        step: 1,
        slide: function( event, ui ) {
            $( "#strengthValue" ).html( ui.value );
            requestData.strength = ui.value;
        }
    });
    $( "#strengthValue" ).html(  $('#strengthRange').slider('value') );

    let removeX = function(val) {
        return val.substring(0, val.length - 1)
    }
    let requestData = {};
    requestData.query = "custom";
    requestData.medicalEffects = [];
    requestData.desiredEffects = [];
    requestData.undesiredEffects = [];
    requestData.flavors = [];
    requestData.aromas = [];
    
    // Submit request logic
    $( "#customSearch" ).submit(function( event ) {
        event.preventDefault();
        requestData.medicalEffects = [];
        requestData.desiredEffects = [];
        requestData.undesiredEffects = [];
        requestData.flavors = [];
        requestData.aromas = [];
        $("#allEffects").children().each(function(){
            let tag = $(this).text();
            
            if ($(this).hasClass("medical-effect")) {
                requestData.medicalEffects.push(removeX(tag));
            } else if ($(this).hasClass("desired-effect")) {
                requestData.desiredEffects.push(removeX(tag));
            } else if ($(this).hasClass("undesired-effect")) {
                requestData.undesiredEffects.push(removeX(tag));
            } else if ($(this).hasClass("flavor")) {
                requestData.flavors.push(removeX(tag));
            } else {
                requestData.aromas.push(removeX(tag));
            }
        })

        console.log(requestData);
        $.post( "results-custom", JSON.stringify(requestData))
        .always(function() {
            $("#loadingDiv").fadeIn();
        })
        .done(function( data ) {
            console.log(data);
            data = JSON.parse(data);
            
            $('#results').empty();
            
            let count = 0;

            if (data.length == 0) {
                $("#results").append("<h1>No Results Found</h1>");
            }
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

            $("#customSearch").addClass("col-4", 500).removeClass("col-5", function(){
                $("#results").addClass("d-flex").show(500);
            });

        });
    });

});
});