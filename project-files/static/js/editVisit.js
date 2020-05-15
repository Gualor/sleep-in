$("#psg-radio0").change(function () {
    if (document.getElementById('psg-radio0').checked) {
        psg = "0";
    } else if (document.getElementById('psg-radio1').checked) {
        psg = "1";
    }
    console.log(psg);
    if (psg == "1") {
        $('#psg-div').show();
        $('#psg-div1').show();
        $('#file2').attr('required', '');
        $('#file2').attr('data-error', 'This field is required.');
    } else {
        $('#psg-div').hide();
        $('#psg-div1').hide();
        $('#file2').removeAttr('required');
        $('#file2').removeAttr('data-error');
    }
});

$("#psg-radio1").change(function () {
    if (document.getElementById('psg-radio0').checked) {
        psg = "0";
    } else if (document.getElementById('psg-radio1').checked) {
        psg = "1";
    }
    console.log(psg);
    if (psg == "1") {
        $('#psg-div').show();
        $('#psg-div1').show();
        $('#file2').attr('required', '');
        $('#file2').attr('data-error', 'This field is required.');
    } else {
        $('#psg-div').hide();
        $('#psg-div1').hide();
        $('#file2').removeAttr('required');
        $('#file2').removeAttr('data-error');
    }
});

$('#completed').hide();

if (comp == "0") {
    $('#comp-radio0').attr('checked', '');
    $('#vis-notcomp').show();
    $('#vis-comp').hide();
    if (psg == "0") {
        $('#psg-radio0').attr('checked', '');
    } else {
        $('#psg-radio1').attr('checked', '');
    }
} else {
    $('#comp-radio1').attr('checked', '');
    $('#vis-notcomp').hide();
    $('#vis-comp').show();
}

$("#psg-radio0").trigger("change");
$("#psg-radio1").trigger("change");
