'use strict';
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
       page_id_array.push($(this).data("pk"));
       model_name = $(this).data("model");
      });
      $.ajax({
       url:"/shop/cms/model/order/",
       method:"POST",
       data:{page_id_array:page_id_array,model_name:model_name},
       success:function(data)
       {
        console.info(data);
       }
      });
     }
    });

    $("[id$='_date']").datepicker();
    $("select").select2();
  })/*document ready */

})(window,document,jQuery)
