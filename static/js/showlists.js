$(document).ready(function(){
    const $listContainer = $('.list-container');
    const url = $listContainer.data('url');

   // const $cardContainer = $('.card-container');
   // const urls = $cardContainer.data('urls');


    $.ajax({
        url: url,
        method: 'GET'
    }).done(function(response){
        $listContainer.html(response);
        var listsElement = $('.list-section');

        listsElement.forEach(function(element){
            var url = $(element).data('cards');
        });

    });





});

