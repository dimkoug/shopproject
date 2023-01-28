'use strict';
(function(w,d,$){
  $(d).ready(function(){
    $(".order").sortable({
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
             $(".loading").show();
           },
           complete: function(){
             $(".loading").hide();
             
           }
       })).then(function( resp, textStatus, jqXHR ) {
         $(".res").html(resp);
         $(".loading").hide();
       })

  return false;
})



  })/*document ready */

})(window,document,jQuery)
