'use strict';
(function(w,d,$){
  $(d).ready(function(){

    $(".spinner-border").hide();


    function create_sortable($els) {
      // Iterate over each element with the class 'order'
      $els.each(function() {
          var $el = $(this); // Get the current element
  
          // Make the current element sortable using jQuery UI
          $el.sortable({
              update: function(event, ui) {
                  // Array to store the sorted items' primary keys
                  var page_id_array = [];
                  var model_name = '';
                  var app_name = '';
                  
                  // Iterate through each item in the current sortable list
                  $el.find('.item').each(function() {
                      page_id_array.push({ "pk": $(this).data("pk") });
                      model_name = $(this).data("model");
                      app_name = $(this).data("app");
                  });
  
                  // Send the sorted data to the server via AJAX
                  $.ajax({
                      url: "/cms/model/order/",
                      method: "POST",
                      data: {
                          "page_id_array": JSON.stringify(page_id_array),
                          model_name: model_name,
                          app_name: app_name
                      },
                      success: function(data) {
                          console.info(data); // Log the server's response
                      }
                  });
              }
          });
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

$("body").on("submit",'#modal-delete',function(e){
    e.preventDefault();
    let url = $(this).attr('action');
    let method = "post";
    $.when($.ajax({
      url: url,
      method: method,
      //data: $(this).serialize(),
      dataType: 'json',
      headers: {'X-CSRFToken': $("input[name='csrfmiddlewaretoken']").val()},
      beforeSend: function () {
          //$(".spinner-border").show();
          $('#modal').modal('hide');
          $('body').removeClass('modal-open');
          $('.modal-backdrop').remove();
      },
      complete: function (data) {
        console.info(data)
        $("#item_"+ data["item"]).fadeOut();
        
        //$('#modal').modal('hide');
        //$('body').removeClass('modal-open');
        //$('.modal-backdrop').remove();
        //$(".spinner-border").hide();
      }
  })).then(function (resp, textStatus, jqXHR) {
    $("#item_"+ resp["item"]).fadeOut();
    console.info(resp);  
  })

return false;


})




  })/*document ready */

})(window,document,jQuery)
