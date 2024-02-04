'use strict';
(function(w,d,$){
 $(d).ready(function(){
   $("div[class*='mega-menu-container-']").hide();
   $(".spinner-border").hide();
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
              $(".spinner-border").show();
              $(".basket_res").html('');
            },
            complete: function(){
              $(".spinner-border").hide();
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
                $(".spinner-border").show();
              },
              complete: function(){
                $(".spinner-border").hide();
                
              }
          })).then(function( resp, textStatus, jqXHR ) {
            $(".products").html(resp.html);
            setFilterHeight()
            $(".spinner-border").hide();
          })

     return false;
 })

 $("body").on("submit", '#filters-form', function(e){
     e.preventDefault();
     $(".spinner-border").show();
     var data = $(this).serialize();
     $.when($.ajax({
              url: $(this).attr("action"),
              method: 'GET',
              data: data,
              datatype: 'json',
              beforeSend: function(){
                $(".spinner-border").show();
                $('#modal').modal('hide');
                $('body').removeClass('modal-open');
                $('.modal-backdrop').remove();
              },
              complete: function(){
                $(".spinner-border").hide();
              }
          })).then(function( resp, textStatus, jqXHR ) {
            $(".products").html(resp.html);
            setFilterHeight()
            $(".spinner-border").hide();
          })

     return false;
 })

 function setFilterHeight(){
  $('.scrollable-row').css('max-height', $(".results").height() + 'px');
 }

 setFilterHeight()


 $("body").on('click', '#reset-filters', function(e){
  e.preventDefault();
  w.location.reload()
  setFilterHeight()
 })

 $('[id^="third"]').hide();


$("body").on("click", "[id^='category']",function(e){
  e.preventDefault();
  let id = $(this).attr("id").split('-')[1];
  $('[id^="third"]').slideUp();
  $("#third-" + id).slideToggle()


})



$('body').on("click","[id*='caret_']", function(e){
  e.preventDefault();
  $(this).toggleClass('bi-caret-down-fill bi-caret-up-fill');
  let id = $(this).attr('id').split('_')[1];
  console.info(id);
  $(this).parents().find("#items_"+id).toggleClass('active-feature hide-feature');
  //$("[id*='items_']").removeClass();
  //$("[id*='items_']").removeClass('hide-feature');
  //$('.deactivate-'+pk).toggle()
  //$("#items_"+id).toggle();
  /*if ( $i.hasClass( 'active-feature' ) ) {
    alert('active')
    $i.removeClass( 'active-feature' ).addClass( 'hide-feature' );
  } else {
      alert('inactive')
      $i.removeClass( 'hide-feature' ).addClass( 'active-feature' );
  }*/



  //console.info($i.attr('class'))
  
  return false;
})


 }) /* document ready */


})(window,document,jQuery)
