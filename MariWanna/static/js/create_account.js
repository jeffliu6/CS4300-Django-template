$(document).ready(function () {

    $("#create-account").fadeIn(500);
    let requestData = {};
    // Submit request logic
    $("#create-account").submit(function (event) {
        event.preventDefault();
        requestData.email = $("#email").val();
        requestData.password = $("#password").val();
        console.log(requestData)

        $.post("enter-user", JSON.stringify(requestData))
            .always(function () {
                $("#loadingDiv").fadeIn();
            })
            .done(function (data) {
                window.location.href = "login";
            });
    });
});