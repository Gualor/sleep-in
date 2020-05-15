$("#usertype").change(function() {
  if ($(this).val() == "M") {
    $('#spec-div').show();
    $('#specialization').attr('required', '');
    $('#specialization').attr('data-error', 'This field is required.');
    $('#unit-div').show();
    $('#unit').attr('required', '');
    $('#unit').attr('data-error', 'This field is required.');
  } else {
    $('#spec-div').hide();
    $('#specialization').removeAttr('required');
    $('#specialization').removeAttr('data-error');
    $('#unit-div').hide();
    $('#unit').removeAttr('required');
    $('#unit').removeAttr('data-error');
  }
});

$("#usertype").trigger("change");