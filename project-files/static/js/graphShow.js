$("#graphtype").change(function () {
    if ($(this).val() == "Verde") {
        console.log('test');
        $('#rect').css(
            'background-color', '#333333'
        );

    }
    if ($(this).val() == "Rosso") {
        console.log('test ma in rosso');
        $('#rect').css(
            'background-color', '#aaaaaa'
        );
    } 
});

$("#graphtype").trigger("change");
