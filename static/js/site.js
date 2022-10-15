'use strict';
(function(w,d,$){
 $(d).ready(function(){
   $("div[class*='mega-menu-container-']").hide();
   $(".loading").hide();
   $("div[class*='basket-container']").hide();
   $("body").on("click", "[id^='mega-menu-']", function(e){
        var id = $(this).attr('id').split("-")[2];
        console.info(id);
        $("div[class*='basket-container']").hide();
        console.info("class:not(mega-menu-container-"+id+")");
        $("div[class*='mega-menu-container-']").not(".mega-menu-container-"+id+"").hide();
        $(".mega-menu-container-"+id+"").fadeToggle("slow");
        return false;
   })
   $('body').on('click', '.form-check-input', function(e){
     $(this).parent().parent().toggleClass('checked');
   })

 $('body').on("click","[class*='ajax_']", function(e){
   e.preventDefault();
   $("div[class*='mega-menu-container-']").hide();
   $.when($.ajax({
            url: $(this).attr("href"),
            method: 'GET',
            datatype: 'json',
            beforeSend: function(){
              $(".loading").show();
              $(".basket_res").html('');
            },
            complete: function(){
              $(".loading").hide();
            }
        })).then(function( resp, textStatus, jqXHR ) {
          $(".basket_res").html(resp.html);
          $("div[class*='basket-container']").show();
        })
   return false;
 })
 $('body').on("click",'.close', function(e){
    $("div[class*='basket-container']").hide();
 })


 var swiper = new Swiper(".mySwiper", {
   navigation: {
     nextEl: ".swiper-button-next",
     prevEl: ".swiper-button-prev",
   },
 });


 $("body").on("click", '.tag-link, .remove-filter-link, .page-link', function(e){
     e.preventDefault();
     $.when($.ajax({
              url: $(this).attr("href"),
              method: 'GET',
              datatype: 'json',
              beforeSend: function(){
                $(".loading").show();
              },
              complete: function(){
                $(".loading").hide();
                
              }
          })).then(function( resp, textStatus, jqXHR ) {
            $(".products").html(resp.html);
            $('#filter-container').hide();
            $(".loading").hide();
          })

     return false;
 })

 $("body").on("submit", '#filters-form', function(e){
     e.preventDefault();
     var data = $(this).serialize();
     $.when($.ajax({
              url: $(this).attr("href"),
              method: 'GET',
              data: data,
              datatype: 'json',
              beforeSend: function(){
                $(".loading").show();
              },
              complete: function(){
                $(".loading").hide();
              }
          })).then(function( resp, textStatus, jqXHR ) {
            $(".products").html(resp.html);
            $(".loading").hide();
          })

     return false;
 })

 $('#filter-container').hide();

 $('body').on('click', '.filters', function(e){
    e.preventDefault();
    $('#filter-container').fadeToggle();


    return false;


 })

 $('body').on('click', '#reset-filters', function(e){
  e.preventDefault();
  w.location.reload();
  return false;
})



 }) /* document ready */


})(window,document,jQuery)
