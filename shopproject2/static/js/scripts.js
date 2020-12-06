  $(document).ready(function(){
    $(".mega-menu-container").hide();
    $("body").on("click", "#mega-menu", function(e){
      $(".mega-menu-container").fadeIn();
      return false;
    })
    $("body").on("click", "#close-menu",function(e){
      $(".mega-menu-container").fadeOut();
    })
  })
