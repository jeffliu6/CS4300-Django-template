$(document).ready(function(){

    $(window).resize( function() {
        $("#mainContent").css("min-height", $(window).height() - nav_height);
    });
})