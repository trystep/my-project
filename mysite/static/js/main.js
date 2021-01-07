$(document).ready(function () {
    $(function(){
        $nav = $('.fixed-div');
        $nav.css('width', $nav.outerWidth());
        $window = $(window);
        $h = $nav.offset().top;
        $window.scroll(function(){
            if ($window.scrollTop() > $h) {
                $nav.addClass('fixed');
            } else {
                $nav.removeClass('fixed');
            }
        });
    });
});
$(document).ready(function () {
    $(document).mouseup(function (e) {
        var container = $("#sidebar");
        if (container.has(e.target).length === 0){
            container.removeClass('sidebar-active');
        }
    });
    var menuBtn = $('#menu-icon');
  $('#menu-icon').on('click', function () {
;
    if ($(menuBtn).hasClass("btn-menu-active")) {
        $(menuBtn).removeClass('btn-menu-active');
      $('#sidebar').removeClass('sidebar-active'); 
    } 
    else{
        $(this).addClass('btn-menu-active');
        $('#sidebar').addClass('sidebar-active')
    }
  });
});
$(document).ready(function () {

    var searchBtn = $('.btn-search-toggle');
  $(searchBtn).on( 'click', function () {
    $('.search-modal').addClass('search-modal-active'); 
  });
  $(document).mouseup(function (e) {
    var container = $(".search-section-mobile");
    if (container.has(e.target).length === 0){
        $('.search-modal').removeClass('search-modal-active'); 
        console.log('+')
    }
}); 
});