function create_message(message){
    $(document).ready(() => {
        $("#lnkLegal").click(() => {
            $("#message").text(message);
            $("#modal_info").modal("show");
        });
    })
}

