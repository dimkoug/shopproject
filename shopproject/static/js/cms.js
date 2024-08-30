'use strict';
(function(w,d,$){
  $(d).ready(function(){

    $(".spinner-border").hide();

    function create_sortable($el){
      $el.sortable({
        /*placeholder : "ui-state-highlight",*/
        update  : function(event, ui)
        {
         var page_id_array = new Array();
         var model_name = '';
         $('.item').each(function(){
          page_id_array.push({"pk":$(this).data("pk")});
          model_name = $(this).data("model");
         });
         $.ajax({
          url:"/shop/cms/model/order/",
          method:"POST",
          data:{"page_id_array":JSON.stringify(page_id_array),model_name:model_name},
          success:function(data)
          {
           console.info(data);
          }
         });
        }
       });
    }
    create_sortable($('.order'))

    $("[id$='_date']").datepicker();
    //$("select").select2();

    $('.delete-tr').on('click', function(e){
      e.preventDefault();
      var that = $(this);
      var url = $(this).attr('href');
      var c = confirm("Delete the object");
      if (c == true) {
        $.post(url, function( data ) {
          $(that).parent().parent().fadeOut();
        });
      }
      return false;
  })
  $('.delete').on('click', function(e){
    e.preventDefault();
    var that = $(this);
    var url = $(this).attr('href');
    var c = confirm("Delete the object");
    if (c == true) {
      $.post(url, function( data ) {
        $(that).parent().fadeOut();
      });
    }
    return false;
})

$("body").on("click", '.page-link', function(e){
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
         $(".res").html(resp);
         $(".spinner-border").hide();
         create_sortable($('.order'))
         $(".order").sortable('refresh');
       })

  return false;
})


$("#search-form").submit(function(e){
  e.preventDefault();
  let form =$(this);
  let action = form.attr("action");
  let method = form.attr("method");
  let data = form.serializeArray();
  console.info(action,method,data)
  $.when($.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
           beforeSend: function(){
             $(".spinner-border").show();
           },
           complete: function(){
             $(".spinner-border").hide();
             
           }
       })).then(function( resp, textStatus, jqXHR ) {
         $(".res").html(resp);
         $(".spinner-border").hide();
         create_sortable($('.order'))
         $(".order").sortable('refresh');
       })

  return false;
})



let form = $("#search-form");
let action = form.attr("action");
let method = form.attr("method");
form.trigger("reset");
$.when($.ajax({
        url: form.attr("action"),
        data: {q: ""},
        type: form.attr("method"),
        dataType: 'json',
         beforeSend: function(){
           $(".spinner-border").show();
         },
         complete: function(){
           $(".spinner-border").hide();
           
         }
     })).then(function( resp, textStatus, jqXHR ) {
       $(".res").html(resp);
       $(".spinner-border").hide();
       create_sortable($('.order'))
       $(".order").sortable('refresh');
     })


  $('#search-form select').each(function(){
      let app = $(this).data("app");
      let model = $(this).data("model");
      $(this).select2({
        ajax: {
          url: '/sb_data/',
          data: function (params) {
            var query = {
              search: params.term,
              app:app,
              model: model,
              type: 'public'
            }
            // Query parameters will be ?search=[term]&type=public
            return query;
          }
        }
      });
  });



$("body").on("click", '.s-back', function(e){
  e.preventDefault();
  let form = $("#search-form");
  form.trigger("reset");
  $.when($.ajax({
          url: form.attr("action"),
          data: {q: ""},
          type: form.attr("method"),
          dataType: 'json',
           beforeSend: function(){
             $(".spinner-border").show();
           },
           complete: function(){
             $(".spinner-border").hide();
             
           }
       })).then(function( resp, textStatus, jqXHR ) {
         $(".res").html(resp);
         $(".spinner-border").hide();
         create_sortable($('.order'))
         $(".order").sortable('refresh');
       })

  return false;
})



$("body").on('click', '.js-load-form',function(e){
  e.preventDefault();
  $.when($.ajax({
    url: $(this).attr("href"),
    method: 'GET',
    beforeSend: function () {
        //$(".spinner-border").show();
        $('#modal').modal('hide');
        $('body').removeClass('modal-open');
        $('.modal-backdrop').remove();
    },
    complete: function (data) {
      $("#modal").html(data.html);
      $("#modal").show();
      $(".spinner-border").hide();
    }
})).then(function (resp, textStatus, jqXHR) {
  console.info(resp);  
  $("#modal").html(resp.html);
  $('#modal').modal('show');
  
  //$(".products").html(resp.html);
    //setFilterHeight()
    $(".spinner-border").hide();
})
  
  
  return false;



})






  })/*document ready */

})(window,document,jQuery)
