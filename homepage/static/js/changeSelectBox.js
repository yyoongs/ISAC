$(document).ready(function () {
     $('#SelectBigCate').change(function () {
        $.getJSON('/_update_midCate', {
            selected_class: $('#SelectBigCate').val()
        }).success(function (data) {
            // console.log(data);
            $('#SelectMidCate').html(data.html_string_selected);
        })
    });

    $('#Upjong').change(function () {
        $.getJSON('/_update_gijun', {
            selected_class: $('#Upjong').val()

        }).success(function (data) {
            $('#Trouble1').html(data.html_string_selected);
        })
    });

    $('#show_gijun_table').bind('click', function () {
        $.getJSON('/_show_gijun_table', {
            selected_class: $('#Upjong').val(),
            selected_entry: $('#Trouble1').val(),
            // format:json,
        }).success(function (data) {

            console.log(data[0]['category_name']);
            // 테이블 부분 깨끗하게
            $('#show_gijuns').html("");

            // 업종, 분쟁유형 보여주기
            // var intro = '<div class="row"><div class="col-sm-4">업종 : ';
            // intro += data[0]['category_name']+'</div><div class="col-sm-8">분쟁유형1 : ';
            // intro += data[0]['type_1'];
            // intro  += '</div></div>'
            // $("#show_gijuns").append(intro);
            var makeIntro = $("<div></div>");
            $("#show_gijuns").append("<div class=\"row\"><div class=\"col-sm-4\">업종 : +data[0]['category_name']+'</div><div class=\"col-sm-8\">분쟁유형1 : +data[0]['type_1']+</div></div>");


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
        });
        return false;
    });
});