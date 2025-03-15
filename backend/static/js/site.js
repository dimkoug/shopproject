$(document).ready(function(){
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


// var swiper = new Swiper(".mySwiper", {
//   navigation: {
//     nextEl: ".swiper-button-next",
//     prevEl: ".swiper-button-prev",
//   },
// });


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
           $(".res").html(resp);
           $(".spinner-border").hide();
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
               $(".spinner-border").show();
                 $('#exampleModal').modal('hide');
             },
             complete: function(){
               $(".spinner-border").hide();
             }
         })).then(function( resp, textStatus, jqXHR ) {
          $('#exampleModal').modal('hide');
           $(".products").html(resp.html);
           $(".spinner-border").hide();
         })

    return false;
})

})


    $(document).ready(function () {
        let formsetContainer = document.querySelectorAll('.formset-container'),
            form = document.querySelector('#form'),
            addFormsetButton = document.querySelector('#add-formset'),
            totalForms = document.querySelector('#id_form-TOTAL_FORMS'),
            maxForms = parseInt(addFormsetButton.getAttribute('data-max-forms'), 10); // Dynamically fetch maxForms

        let formsetNum = formsetContainer.length - 1;

        addFormsetButton.addEventListener('click', $addFormset);

        function $addFormset(e) {
            e.preventDefault();

            // Check if max_forms is reached
            if (formsetNum + 1 >= maxForms) {
                return; // Prevent adding more forms
            }

            let newForm = formsetContainer[0].cloneNode(true),
                formRegex = RegExp(`form-(\\d){1}-`, 'g');
            formsetNum++;
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formsetNum}-`);
            form.insertBefore(newForm, addFormsetButton);
            totalForms.setAttribute('value', `${formsetNum + 1}`);

            // Disable button if max_forms is reached
            checkAddButton();
        }

        document.addEventListener('click', function (e) {
            if (e.target && e.target.classList.contains('remove-form')) {
                e.preventDefault();

                // Find the form to remove by traversing the DOM from the clicked button
                let formToRemove = e.target.closest('.formset-container');
                formToRemove.remove();

                // Update the TOTAL_FORMS count
                formsetNum--;
                totalForms.setAttribute('value', formsetNum);

                // Re-index the remaining forms to keep their field names and IDs consistent
                reIndexForms();

                // Re-enable button if max_forms is no longer reached
                checkAddButton();
            }
        });

        function reIndexForms() {
            // Reindex the forms after a removal to keep consistent form field names
            document.querySelectorAll('.formset-container').forEach((form, index) => {
                form.querySelectorAll('input, textarea, select, button').forEach(input => {
                    const name = input.getAttribute('name');
                    if (name) {
                        input.setAttribute('name', name.replace(/form-(\d+)-/, `form-${index}-`));
                    }
                    const id = input.getAttribute('id');
                    if (id) {
                        input.setAttribute('id', id.replace(/form-(\d+)-/, `form-${index}-`));
                    }
                });
            });
        }

        function checkAddButton() {
            // Enable or disable the "Add" button based on max_forms
            if (formsetNum + 1 >= maxForms) {
                addFormsetButton.setAttribute('disabled', true);
            } else {
                addFormsetButton.removeAttribute('disabled');
            }
        }

        // Initial check on page load
        checkAddButton();
    });
