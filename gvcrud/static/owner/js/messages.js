$(document).ready(function(){
    setTimeout(function(){
        $(".alert-dismissible").addClass("fade-out");
        setTimeout(function(){
            $(".alert-dismissible").alert('close');
        }, 3000); 
    }, 5000);
});