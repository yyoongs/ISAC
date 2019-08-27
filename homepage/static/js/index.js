$(document).ready(function () {
    $('#mainNav').css('background-image', 'none');
    $('#questionBtn').hover(function () {
        $('.probootstrap-image').css('background-image', 'url(/static/img/bg2.png)');
    }, function () {
        $('.probootstrap-image').css('background-image', 'url(/static/img/bg.jpeg)');
    });

    $('#SelectBigCate').change(function () {
        $.getJSON('/_update_midCate', {
            selected_big: $('#SelectBigCate').val()
        }).done(function (data) {
            // console.log(data);
            $('#SelectSmallCate').html('<option value="">전체</option>');
            $('#SelectMidCate').html(data.html_string_selected);
            console.log('중분류 떠라');
        })
    });

    $('#SelectMidCate').change(function () {
        $.getJSON('/_update_smallCate', {
            selected_big: $('#SelectBigCate').val(),
            selected_mid: $('#SelectMidCate').val(),
        }).done(function (data) {
            console.log(data);
            // console.log(data);
            $('#SelectSmallCate').html(data.html_string_selected);
        })
    });
});