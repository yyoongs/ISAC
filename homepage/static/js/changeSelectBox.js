$(document).ready(function () {
    var inputTrouble2 = $("<label for='Trouble2'></label><select class='form-control' id='Trouble2' name='Trouble2'><option selected>전체</option></select>");
    var inputTrouble3 = $("<label for='Trouble3'></label><select class='form-control' id='Trouble3' name='Trouble3'><option selected>전체</option></select>");
    var inputTrouble4 = $("<label for='Trouble4'></label><select class='form-control' id='Trouble4' name='Trouble4'><option selected>전체</option></select>");
    var searchBtn = $("<input type='button' class='btn btn-outline-dark' id='show_gijun_table' value='검색'></input>");


    // 업종 별로 분쟁유형1 보여주기
    $('#Upjong').on('change', function (e) {
        e.preventDefault();
        $.getJSON('/_update_trouble', {
            selected_class: $('#Upjong').val()

        }).done(function (data) {
            inputTrouble4.remove();
            inputTrouble3.remove();
            inputTrouble2.remove();
            searchBtn.remove();

            $('#Trouble1').html(data.html_string_selected);
        })
    });


    $('#Trouble1').on('change', function (e) {
        e.preventDefault();
        $.getJSON('/_update_trouble2', {
            selected_upjong: $('#Upjong').val(),
            selected_trouble1: $('#Trouble1').val()

        }).done(function (data) {
            if (!data) {
                inputTrouble4.remove();
                inputTrouble3.remove();
                inputTrouble3.remove();

                $("#solutionBtn1").append($(searchBtn)).show();
            } else {
                $('#InputTrouble2').html("");
                $("#InputTrouble2").append($(inputTrouble2));
                $('#Trouble2').html(data.html_string_selected);

                $("#InputTrouble3").append($(inputTrouble3));
                inputTrouble3.hide();

                searchBtn.remove();
            }
        })
    });

    // 분쟁유형2 별로 분쟁유형3 보여주기
    $('#InputTrouble2').on('change', '#Trouble2', function () {
        $.getJSON('/_update_trouble3', {
            selected_upjong: $('#Upjong').val(),
            selected_trouble1: $('#Trouble1').val(),
            selected_trouble2: $('#Trouble2').val(),
        }).done(function (data) {
            console.log(data);
            if (!data) {
                inputTrouble3.remove();
                inputTrouble4.remove();

                $("#solutionBtn2").append($(searchBtn)).show();
            } else {
                $('#InputTrouble3').html("");
                $('#InputTrouble3').append($(inputTrouble3));
                $('#Trouble3').html(data.html_string_selected);

                inputTrouble3.show();
                $("#InputTrouble4").append($(inputTrouble4));
                inputTrouble4.hide();

                searchBtn.remove();
            }
        })
    });

    // 분쟁유형3 별로 분쟁유형4 보여주기
    $('#InputTrouble3').on('change', '#Trouble3', function (e) {
        e.preventDefault();
        $.getJSON('/_update_trouble4', {
            selected_upjong: $('#Upjong').val(),
            selected_trouble1: $('#Trouble1').val(),
            selected_trouble2: $('#Trouble2').val(),
            selected_trouble3: $('#Trouble3').val()

        }).done(function (data) {
            if (!data) {
                inputTrouble4.remove();
                $("#solutionBtn3").append($(searchBtn)).show();
            } else {
                searchBtn.remove();
                $('#InputTrouble4').html("");
                $('#InputTrouble4').append($(inputTrouble4));
                $('#Trouble4').html(data.html_string_selected);
                inputTrouble4.show();
                $("#solutionBtn4").append($(searchBtn)).show();
            }

        })
    });

    $('.solutionBtn').on('click', '#show_gijun_table', function (e) {
        e.preventDefault();
        console.log('해결기준 테이블 보여주자');
        $.getJSON('/_show_gijun_table', {
            upjong: $('#Upjong').val(),
            trouble1: $('#Trouble1').val(),
            trouble2: $('#Trouble2').val(),
            trouble3: $('#Trouble3').val(),
            trouble4: $('#Trouble4').val(),
            // format:json,
        }).done(function (data) {

            console.log(data[0]['category_name']);
            // 테이블 부분 깨끗하게
            $('#show_gijuns').html("");

            var makeIntro = $("<div></div>");
            $("#show_gijuns").append("<div class=\"row\"><div class=\"col-sm-4\">업종 : " + data[0]['category_name'] + "</div><div class=\"col-sm-8\">분쟁유형1 : " + data[0]['type_1'] + "</div></div>");


            // 테이블 보여주기
            var makeTable = $("<table class='table table-bordered table-hover' style='width:100% margin-top:10px;'><thead></thead><tbody></tbody>");
            $("#show_gijuns").append($(makeTable));

            $(makeTable).find("thead").append("<th style='width: 45%' class='text-center'>해결기준</th><th style='width: 55%' class='text-center'>비고</th>");

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