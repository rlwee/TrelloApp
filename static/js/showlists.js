$(document).ready(function(){
    const $listContainer = $('.list-container');
    const url = $listContainer.data('url');

    $.ajax({
        url: url,
        method: 'GET'
    }).done(function(response){
        $listContainer.html(response);
        var listsElement = $('.list-section');


        var $cardContainer = $('.card-container');

        $($cardContainer).each(function(index){
            var cardURL = $(this).data('url');
            loadCards(cardURL, $(this));
            console.log(cardURL, 'url');
        });

        var $listContent = $('.list-content');

        $($listContent).click(function(){
        editList($(this));
        })


    });
    // var $cardContainer = $('.card-container');

    // $($cardContainer).each(function(index){
    //     var cardID = $(this).data('id');
    //     var cardURL = $(this).data('url');
    //     loadCards(cardID, $(this));
    //     console.log(cardURL, 'url');
    // });

    function loadCards(url, element){
        $.ajax({
            url: url,
            method: 'GET',
        }).done(function(response){
            element.html(response);
            var cardsElement = $('.card-section');
        })

    }

    function editList(element){
        element.slideUp();
    }


});

