$(document).ready(function () {
    $('#SelectBigCate').change(function () {
        $.getJSON('/_update_midCate', {
            selected_big: $('#SelectBigCate').val()
        }).done(function (data) {
            // console.log(data);
            $('#SelectSmallCate').html('<option value="">전체</option>');
            $('#SelectMidCate').html(data.html_string_selected);
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

    // 업종 별로 분쟁유형1 보여주기
    $('#Upjong').change(function () {
        $.getJSON('/_update_trouble', {
            selected_class: $('#Upjong').val()

        }).done(function (data) {
            $('#Trouble4').html('<option value="">전체</option>');
            $('#Trouble3').html('<option value="">전체</option>');
            $('#Trouble2').html('<option value="">전체</option>');
            $('#Trouble1').html(data.html_string_selected);
        })
    });

    // 분쟁유형1 별로 분쟁유형2 보여주기
    $('#Trouble1').change(function () {
        $.getJSON('/_update_trouble2', {
            selected_upjong: $('#Upjong').val(),
            selected_trouble1: $('#Trouble1').val()

        }).done(function (data) {
            $('#Trouble4').html('<option value="">전체</option>');
            $('#Trouble3').html('<option value="">전체</option>');
            console.log(data);
            if (!data) {
                console.log('분쟁유형2 없다');
                var searchBtn = $("<input type='button' class='btn btn-outline-dark' id='show_gijun_table' value='검색'></input>");
                $("#solutionBtn").append($(searchBtn));
            } else {
                console.log(data);
                var inputTrouble2 = $("<label for='Trouble2'></label><select class='form-control' id='Trouble2' name='Trouble2'><option selected>전체</option></select>");
                $("#InputTrouble2").append($(inputTrouble2));
                $('#Trouble2').html(data.html_string_selected);
                var inputTrouble3 = $("<label for='Trouble3'></label><select class='form-control' id='Trouble3' name='Trouble3'><option selected>전체</option></select>");
                $("#InputTrouble3").append($(inputTrouble3));
                console.log('숨기자');
                inputTrouble3.hide();
                console.log('숨겼다');
            }
        })
    });

    // 분쟁유형2 별로 분쟁유형3 보여주기
    $('#Trouble2').on('change', '#Trouble3', function (e) {
         e.preventDefault();
         console.log('ㅎㅇㅎㅇ2->3');
    // $('#Trouble2').change(function () {
        $.getJSON('/_update_trouble3', {
            selected_upjong: $('#Upjong').val(),
            selected_trouble1: $('#Trouble1').val(),
            selected_trouble2: $('#Trouble2').val()

        }).done(function (data) {
            inputTrouble3.show();
            $('#Trouble4').html('<option value="">전체</option>');
            console.log(data);
            if (!data) {
                console.log('분쟁유형3 없다');
                var searchBtn = $("<input type='button' class='btn btn-outline-dark' id='show_gijun_table' value='검색'></input>");
                $("#solutionBtn").append($(searchBtn));
            } else {
                console.log(data);
                // var inputTrouble3 = $("<label for='Trouble3'></label><select class='form-control' id='Trouble3' name='Trouble3'><option selected>전체</option></select>");
                // $("#InputTrouble3").append($(inputTrouble3));
                $('#Trouble3').html(data.html_string_selected);
            }
        })
    });

    // 분쟁유형3 별로 분쟁유형4 보여주기
    $('#Trouble3').on('change', '#Trouble4', function (e) {
         e.preventDefault();
    // $('#Trouble3').change(function () {
        $.getJSON('/_update_trouble4', {
            selected_upjong: $('#Upjong').val(),
            selected_trouble1: $('#Trouble1').val(),
            selected_trouble2: $('#Trouble2').val(),
            selected_trouble3: $('#Trouble3').val()

        }).done(function (data) {
            $('#Trouble4').html(data.html_string_selected);
            console.log(data);
            if (!data) {
                console.log('분쟁유형4 없다');
                var searchBtn = $("<input type='button' class='btn btn-outline-dark' id='show_gijun_table' value='검색'></input>");
                $("#solutionBtn").append($(searchBtn));
            } else {
                console.log(data);
                var inputTrouble4 = $("<label for='Trouble4'></label><select class='form-control' id='Trouble4' name='Trouble4'><option selected>전체</option></select>");
                $("#InputTrouble4").append($(inputTrouble4));
                $('#Trouble4').html(data.html_string_selected);
            }
        })
    });


    $('#solutionBtn').on('click', '#show_gijun_table', function (e) {
        e.preventDefault();
        $.getJSON('/_show_gijun_table', {
            upjong: $('#Upjong').val(),
            trouble1: $('#Trouble1').val(),
            // format:json,
        }).done(function (data) {

            console.log(data[0]['category_name']);
            // 테이블 부분 깨끗하게
            $('#show_gijuns').html("");

            var makeIntro = $("<div></div>");
            $("#show_gijuns").append("<div class=\"row\"><div class=\"col-sm-4\">업종 : " + data[0]['category_name'] + "</div><div class=\"col-sm-8\">분쟁유형1 : " + data[0]['type_1'] + "</div></div>");


            // 테이블 보여주기
            var makeTable = $("<table class='table' style='width:100% margin-top:10px;'><thead></thead><tbody></tbody>");
            $("#show_gijuns").append($(makeTable));

            $(makeTable).find("thead").append("<th>해결기준</th><th>비고</th>");

            $.each(data, function (key, val) {
                var str = '<tr>'
                str += '<td>' + val.standard + '</td><td>' + val.bigo + '</td>';
                str += '</tr>';
                $(makeTable).find('tbody').append(str);
            });
        }).fail(function (data) {
            console.log("에러 발생!");
            console.log(data);
        });
        return false;
    });
});