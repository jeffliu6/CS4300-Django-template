$(document).ready(function () {

    $("#login").fadeIn(500);
    let requestData = {};
    // Submit request logic
    $("#login").submit(function (event) {
        event.preventDefault();
        requestData.email = $("#email").val();
        requestData.password = $("#password").val();

        $.post("perform-signin", JSON.stringify(requestData), Boolean)
            .always(function () {
                $("#loadingDiv").fadeIn();
            })
            .done(function (isUserExistent) {
                if (isUserExistent == "true") {
                    console.log("Killer Queen")
                } else {
                    console.log("Benny and the Jets")
                }
                //window.location.href = "search-similar";
            });
    });
});