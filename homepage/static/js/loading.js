function wrapWindowByMask() {
    //화면의 높이와 너비를 구한다.
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();

    //마스크의 높이와 너비를 화면 것으로 만들어 전체 화면을 채운다.
    $('#mask').css({'width': maskWidth, 'height': maskHeight});

    //애니메이션 효과 - 일단 1초동안 까맣게 됐다가 80% 불투명도로 간다.
    //$('#mask').fadeIn(1000);
    $('#mask').fadeTo("slow", 0.6);
}

$(function () {
    $('#counselForm').parsley().on('form:submit', function () {
        $.ajax({
            beforeSend: function () {
                var loading=$("<img alt='loading' id='loadingIMG' src='/static/img/spinner3.gif'>");

                $("#spinner").append($(loading));
                console.log('img 삽입 완료');

                console.log('준비');
                loading.show();
                $("#loadingImg").show();
                console.log("보여줌");
                wrapWindowByMask();
            },
            done: function (result) {
                console.log('끝');
                loading.hide();
                $('#mask').hide();
            },
            fail: function () {
                loading.hide();
                $('#mask').hide();
            }
        });
    });
});
$(window).resize(function () { //화면 크기가 바뀌면 발생하는 이벤트  반응형 웹을 만들때는 이부분을 수정해주면 될듯

    $('#mask').css({'width': $(window).width(), 'height': $(window).height()});
});
