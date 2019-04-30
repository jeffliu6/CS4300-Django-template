$(document).ready(function () {
    $.getJSON("/static/data/select-options.json", function (select_data) {
        console.log(select_data.aromas);
        // Autocomplete Options
        let medical_effects = select_data.medical_effects
        let desired_effects = select_data.desired_effects;
        let undesired_effects = select_data.undesired_effects;
        let flavors = select_data.flavors;
        let aromas = select_data.aromas;

        $.each(medical_effects, function (key, value) {
            $('#medical-effects')
                .append($("<option></option>")
                    .text(value));
        });

        $.each(desired_effects, function (key, value) {
            $('#desired-effects')
                .append($("<option></option>")
                    .text(value));
        });

        $.each(undesired_effects, function (key, value) {
            $('#undesired-effects')
                .append($("<option></option>")
                    .text(value));
        });

        $.each(flavors, function (key, value) {
            $('#flavors')
                .append($("<option></option>")
                    .text(value));
        });

        $.each(aromas, function (key, value) {
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
                } else if (aromas.indexOf(word) > -1) type = "aroma";
            }

            switch (type) {
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
        $('#key-words').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13' && $(this).val() != "") {
                event.preventDefault();
                addTag($(this).val(), "key-word");
                $(this).val("");
            }
            $(".remove-btn").click(function () {
                $(this).parent().remove();
            });
        });
        $("#key-words-btn").click(function () {
            if ($("#key-words").val() != "") {
                addTag($("#key-words").val(), "key-word");
                $("#key-words").val("");
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            }
        });

        $('#medical-effects').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13' && $(this).val() != "") {
                event.preventDefault();
                addTag($(this).val(), "medical-effect");
                $(this).val("");
            }
            $(".remove-btn").click(function () {
                $(this).parent().remove();
            });
        }).autocomplete({
            source: function (request, response) {
                var results = $.ui.autocomplete.filter(medical_effects, request.term);

                response(results.slice(0, 5));
            }
        });
        $("#medical-effects-btn").click(function () {
            if ($("#medical-effects").val() != "") {
                addTag($("#medical-effects").val(), "medical-effect");
                $("#medical-effects").val("");
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            }
        });

        $('#desired-effects').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13' && $(this).val() != "") {
                event.preventDefault();
                addTag($(this).val(), "desired-effect");
                $(this).val("");
            }
            $(".remove-btn").click(function () {
                $(this).parent().remove();
            });
        }).autocomplete({
            source: desired_effects,
            max: 5
        });
        $("#desired-effects-btn").click(function () {
            if ($("#desired-effects").val() != "") {
                addTag($("#desired-effects").val(), "desired-effect");
                $("#desired-effects").val("");
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            }
        });

        $('#undesired-effects').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13' && $(this).val() != "") {
                event.preventDefault();
                addTag($(this).val(), "undesired-effect");
                $(this).val("");
            }
            $(".remove-btn").click(function () {
                $(this).parent().remove();
            });
        }).autocomplete({
            source: undesired_effects,
            max: 5
        });
        $("#undesired-effects-btn").click(function () {
            if ($("#undesired-effects").val() != "") {
                addTag($("#undesired-effects").val(), "undesired-effect");
                $("#undesired-effects").val("");
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            }
        });

        $('#flavors').keypress(function (event) {
            var keycode = (event.keyCode ? event.keyCode : event.which);
            if (keycode == '13' && $(this).val() != "") {
                event.preventDefault();
                addTag($(this).val(), "flavor");
                $(this).val("");
            }
            $(".remove-btn").click(function () {
                $(this).parent().remove();
            });
        }).autocomplete({
            source: flavors,
            max: 5
        });
        $("#flavors-btn").click(function () {
            if ($("#flavors").val() != "") {
                addTag($("#flavors").val(), "flavor");
                $("#flavors").val("");
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            }
        });

        $('#aromas').keypress(function (event) {
                let keycode = (event.keyCode ? event.keyCode : event.which);
                if (keycode == '13' && $(this).val() != "") {
                    event.preventDefault();
                    addTag($(this).val(), "aroma");
                    $(this).val("");
                }
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            })
            .autocomplete({
                source: aromas,
                max: 5
            });
        $("#aromas-btn").click(function () {
            if ($("#aromas").val() != "") {
                addTag($("#aromas").val(), "aroma");
                $("#aromas").val("");
                $(".remove-btn").click(function () {
                    $(this).parent().remove();
                });
            }
        });


        // Strength slider configuration
        $("#strengthRange").slider({
            value: 50,
            min: 0,
            max: 100,
            step: 1,
            slide: function (event, ui) {
                $("#strengthValue").html(ui.value);
                requestData.strength = ui.value;
            }
        });
        $("#strengthValue").html($('#strengthRange').slider('value'));

        let removeX = function (val) {
            return val.substring(0, val.length - 1)
        }
        let requestData = {};
        requestData.query = "custom";
        requestData.medicalEffects = [];
        requestData.desiredEffects = [];
        requestData.undesiredEffects = [];
        requestData.flavors = [];
        requestData.aromas = [];
        requestData.keywords = [];

        function get_popover(weights) {
            let popover = {};
            let str = "";

            if(weights.social) {
                let span = "<p class=\"feedback-weight\"><b class=\"mr-3\">Feedback</b> " + weights.social.toFixed(2) + "</p>";
                str = str.concat(span);
            }

            if (weights.rating != 0) {
                let span = "<p class=\"rating-weight\"><b class=\"mr-3\">Rating</b> " + weights.rating.toFixed(2) + "</p>";
                str = str.concat(span);
            }

            if (weights.keyword != 0) {
                let span = "<p class=\"keyword-weight\"><b class=\"mr-3\">Keywords</b> " + weights.keywords.toFixed(2) + "</p>";
                str = str.concat(span);
            }

            if (weights.medical) {
                popover.medical = [];
                let total = 0;
                Object.entries(weights.medical).forEach(function (entry) {
                    total += entry[1];
                    popover.medical.push(entry[0] + ": " + entry[1].toFixed(2));
                })
                let span = "<p class=\"medical-weights\"><b class=\"mr-3\">Medical Effects</b>" + total.toFixed(2) + "<br/><span class=\"text-muted\">" + popover.medical.join(', ') + "</span></p>";
                str = str.concat(span);
            }

            if (weights.positive) {
                popover.positive = [];
                let total = 0;
                Object.entries(weights.positive).forEach(function (entry) {
                    total += entry[1];
                    popover.positive.push(entry[0] + ": " + entry[1].toFixed(2));
                })
                let span = "<p class=\"positive-weights\"><b class=\"mr-3\">Desired Effects</b>" + total.toFixed(2) + "<br/><span class=\"text-muted\">" + popover.positive.join(', ') + "</span></p>";
                str = str.concat(span);
            }

            if (weights.negative) {
                popover.negative = [];
                let total = 0;
                Object.entries(weights.negative).forEach(function (entry) {
                    total += entry[1];
                    popover.negative.push(entry[0] + ": " + entry[1].toFixed(2));
                })
                let span = "<p class=\"negative-weights\"><b class=\"mr-3\">Undesired Effects</b>" + total.toFixed(2) + "<br/><span class=\"text-muted\">" + popover.negative.join(', ') + "</span></p>";
                str = str.concat(span);
            }

            if (weights.flavor) {
                popover.flavors = [];
                let total = 0;
                Object.entries(weights.flavor).forEach(function (entry) {
                    total += entry[1];
                    popover.flavors.push(entry[0] + ": " + entry[1].toFixed(2));
                })
                let span = "<p class=\"flavor-weights\"><b class=\"mr-3\">Flavors</b>" + total.toFixed(2) + "<br/><span class=\"text-muted\">" + popover.flavors.join(', ') + "</span></p>";
                str = str.concat(span);
            }

            if (weights.aroma) {
                popover.aromas = [];
                let total = 0;
                Object.entries(weights.aroma).forEach(function (entry) {
                    total += entry[1];
                    popover.aromas.push(entry[0] + ": " + entry[1].toFixed(2));
                })
                let span = "<p class=\"aroma-weights\"><b class=\"mr-3\">Aromas</b>" + total.toFixed(2) + "<br/><span class=\"text-muted\">" + popover.aromas.join(', ') + "</span></p>";
                str = str.concat(span);
            }

            if (weights.strength != 0) {
                let span = "<p class=\"strength-weight\"><b class=\"mr-3\">Strength</b><br/>" + weights.strength.toFixed(2) + "</p>";
                str = str.concat(span);
            }

            return str;
        }

        let like_status = {};

        if ($("#dislike-btn").attr("disliked")) {
            let disliked = $("#dislike-btn").attr("disliked");
            disliked = disliked.split(',');

            disliked.forEach(function (e) {
                like_status[e] = -1;
            });
        }

        if ($("#like-btn").attr("liked")) {
            let liked = $("#like-btn").attr("liked");
            liked = liked.split(',');

            liked.forEach(function (e) {
                like_status[e] = 1;
            });
        }

        function like_strain(name) {
            if (name in like_status && like_status[name] == 1) {
                like_status[name] = 0;
            } else {
                like_status[name] = 1;
            }
        }

        function dislike_strain(name) {
            if (name in like_status && like_status[name] == -1) {
                like_status[name] = 0;
            } else {
                like_status[name] = -1;
            }
        }

        function update_dislike_btn(strain) {
            if ($("#dislike-btn").attr("disliked")) {
                let strain_name = strain[1]["name"];
                if (strain_name in like_status) {
                    if (like_status[strain_name] == -1) {
                        $("#dislike-btn").attr("src", "/static/images/dislike-thumb-dark.png");
                        $("#like-btn").attr("src", "/static/images/thumbs-up-light.png");
                    } else {
                        $("#dislike-btn").attr("src", "/static/images/dislike-thumb-light.png");
                    }
                } else {
                    $("#dislike-btn").attr("src", "/static/images/dislike-thumb-light.png");
                }

            }
        }

        function update_like_btn(strain) {
            if ($("#like-btn").attr("liked")) {
                let strain_name = strain[1]["name"];
                if (strain_name in like_status) {
                    if (like_status[strain_name] == 1) {
                        $("#dislike-btn").attr("src", "/static/images/dislike-thumb-light.png");
                        $("#like-btn").attr("src", "/static/images/thumbs-up-dark.png");
                    } else {
                        $("#like-btn").attr("src", "/static/images/thumbs-up-light.png");
                    }
                } else {
                    $("#like-btn").attr("src", "/static/images/thumbs-up-light.png");
                }
            }
        }

        console.log(like_status);
        // Submit request logic
        $("#customSearch").submit(function (event) {
            event.preventDefault();
            console.log(like_status);
            requestData.medicalEffects = [];
            requestData.desiredEffects = [];
            requestData.undesiredEffects = [];
            requestData.flavors = [];
            requestData.aromas = [];
            requestData.keywords = [];

            $("#allEffects").children().each(function () {
                let tag = $(this).text();

                if ($(this).hasClass("medical-effect")) {
                    requestData.medicalEffects.push(removeX(tag));
                } else if ($(this).hasClass("desired-effect")) {
                    requestData.desiredEffects.push(removeX(tag));
                } else if ($(this).hasClass("undesired-effect")) {
                    requestData.undesiredEffects.push(removeX(tag));
                } else if ($(this).hasClass("flavor")) {
                    requestData.flavors.push(removeX(tag));
                } else if ($(this).hasClass("aroma")) {
                    requestData.aromas.push(removeX(tag));
                } else {
                    requestData.keywords.push(removeX(tag));
                }
            })

            console.log(requestData);
            $.post("results-custom", JSON.stringify(requestData))
                .always(function () {
                    $("#loadingDiv").fadeIn();
                })
                .done(function (data) {
                    console.log(data);
                    data = JSON.parse(data);

                    $('#results').empty();

                    let count = 0;

                    if (data.length == 0) {
                        $("#results").append("<h1>No Results Found</h1>");
                    }
                    data.forEach(function (strain) {
                        console.log(strain);
                        $("#results").append('<div id="strain_' + count + '" class="card bg-light strain-result ml-2 mr-2 mb-2 shadow">' +
                            '<div class="card-body">' +
                            '<div class="d-flex justify-content-between"><h5 class="card-title font-weight-bolder mb-1">' + strain[1]["name"] + '</h5><p class="text-muted text-small">' + strain[0].toFixed(2) + '</p></div>' +
                            '<p class="card-text mb-1 text-muted font-italic">Rating: ' + Number(strain[1]["rating"]).toFixed(2) + '/5.00</p>' +
                            '<p class="card-text">' + strain[1]["description"].substring(0, 90) + '...</p>' +
                            '<div class="d-flex justify-content-between"><p class="text-success modal-triggor" data-toggle="modal" data-target="#exampleModalLong">See More</p>' +
                            '<button type="button" class="btn" data-toggle="popover" data-triggor="focus" data-container="body" title="Score Breakdown"' +
                            '"><img class="question-icon float-right" src="/static/images/question-mark-light.png"/></button></div>' +
                            '</div>');

                        $("[data-toggle=popover]").popover({
                            trigger: 'focus',
                            html: true,
                            content: get_popover(strain[2])
                        });

                        $(".popover").addClass("shadow");
                        $("#strain_" + count).on("click", function () {

                            $("#modal-img").empty();
                            if (strain[1]["image"] != "https://www.cannabisreports.com/images/strains/no_image.png") {
                                $("#modal-img").append('<img style="max-height:300px" src="' + strain[1]["image"] + '" class="rounded mb-3 img-fluid" alt="...">');
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

                            update_like_btn(strain);
                            update_dislike_btn(strain);

                            $("#dislike-btn").unbind('click').on("click", function () {
                                let requestData = {};
                                requestData.user = $("#dislike-btn").attr("user");
                                requestData.strain = $(".modal-title").text();
                                dislike_strain(requestData.strain);
                                update_dislike_btn(strain);
                                requestData.input = like_status[requestData.strain];
                                console.log("Dislike button clicked");
                                $.post('provide-strain-feedback', JSON.stringify(requestData));
                                requestData = {}
                            });

                            $("#like-btn").unbind('click').on("click", function () {
                                let requestData = {};
                                requestData.user = $("#dislike-btn").attr("user");
                                requestData.strain = $(".modal-title").text();
                                like_strain(requestData.strain);
                                update_like_btn(strain);
                                requestData.input = like_status[requestData.strain];
                                console.log("Like button clicked");
                                $.post('provide-strain-feedback', JSON.stringify(requestData));
                                requestData = {}
                            });

                        });

                        count++;
                    });
                    $("#loadingDiv").fadeOut();


                    $(".question-icon").hover(function () {
                        $(this).attr("src", "/static/images/question-mark-dark.png");
                    }, function () {
                        $(this).attr("src", "/static/images/question-mark-light.png");
                    });

                    $("#customSearch").addClass("col-4", 500).removeClass("col-5", function () {
                        $("#results").addClass("d-flex").show(500);
                    });

                });
        });

    });
});