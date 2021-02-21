$(function() {
    var vid = document.getElementById("vid");
});

$('#getTime').on('click', function() {
    var currentTime = vid.currentTime;
    $('#currentTime').html(currentTime);
});
