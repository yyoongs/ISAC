$(document).ready(function () {
    $('#Upjong').change(function () {

        $.getJSON('/_update_gijun', {
            selected_class: $('#Upjong').val()

        }).success(function (data) {
            $('#Trouble1').html(data.html_string_selected);
        })
    });
});