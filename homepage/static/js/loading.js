function wrapWindowByMask() {
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();

    $('#mask').css({'width': maskWidth, 'height': maskHeight});

    $('#mask').fadeTo("slow", 0.8);
}

$(function () {
    $('#counselForm').parsley().on('form:submit', function () {
        $.ajax({
            beforeSend: function () {
                var loading = "<div class=\"container2\">" +
                                "<div class=\"coast\">" +
                                    "<div class=\"wave-rel-wrap\">" +
                                        "<div class=\"wave\"></div>" +
                                    "</div>" +
                                "</div>" +
                                "<div class=\"coast delay\">" +
                                    "<div class=\"wave-rel-wrap\">" +
                                        "<div class=\"wave delay\"></div>" +
                                    "</div>" +
                                "</div>" +
                                "<div class=\"text text-w\">I</div>" +
                                "<div class=\"text text-a\">S</div>" +
                                "<div class=\"text text-v\">A</div>" +
                                "<div class=\"text text-e\">C</div>" +
                            "</div>";

                $("#spinner").html(loading);
                wrapWindowByMask();
            },
            done: function (result) {
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
$(window).resize(function () {
    $('#mask').css({'width': $(window).width(), 'height': $(window).height()});
});