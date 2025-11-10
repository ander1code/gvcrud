$("#frm_login").on("click", function(){
    $(this).find("input").prop("readonly", true);
    $(this).find("button").prop("input", null);
});