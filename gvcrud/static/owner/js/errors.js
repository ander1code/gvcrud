$(document).ready(function(){
    setTimeout(function(){
        $("#error-alert").addClass("fade-out");
        setTimeout(function(){
            $("#error-alert").alert('close');
        }, 3000); 
    }, 5000);
});