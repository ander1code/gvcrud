$(function(){
    // CPF
    $('#id_cpf').mask('000.000.000-00', {placeholder: "___.___.___-__"});

    // income_range
    var $income = $('#id_income_range');

    $income.maskMoney({
        prefix: 'R$ ',
        allowNegative: false,
        thousands: '.',
        decimal: ',',
        affixesStay: true
    });

    if ($income.val()) {
        $income.maskMoney('mask');
    }

    birthday = $('#id_birthday').val();

    var $picker = $('#birthday_picker');          
    var $input = $('#id_birthday');              
    var maxDate = moment().subtract(18, 'years'); 

    $picker.datetimepicker({
        format: 'DD/MM/YYYY',
        locale: 'pt-br',
        maxDate: maxDate,
    });

    if(birthday){
        $('#id_birthday').val(moment(birthday, 'YYYY-MM-DD').format('DD/MM/YYYY'));
    }else{
        $('#id_birthday').val(moment().subtract(18, 'years').format('DD/MM/YYYY'));
    }

    $('#id_birthday').on('keydown paste', function(e) {
        e.preventDefault();
    });
});