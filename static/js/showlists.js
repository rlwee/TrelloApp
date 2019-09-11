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
            //console.log(cardURL, 'url');
        });


        var $listContent = $('.list-content');

        $('.list-content').on('blur', function(){
            var url = $(this).data('update');
            var oldValue = $(this).data('title');
            var newTitle = $(this).text();
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
           
            if(newTitle.length == 0) {
                $(this).text(oldValue);
            } else {
                $.ajax({
                    url: url,
                    method: 'get',
                    data: {'title': newTitle}
                }).done(function(response){
                    console.log(response)
                });
            }
        });




    });

    function loadCards(url, element){
        $.ajax({
            url: url,
            method: 'GET',
        }).done(function(response){
            element.html(response);
            //var cardsElement = $('.card-section');

            editCard();
            addButton();
       
    })

}


    function editCard(){
        $('.card-content').on('blur', function(){
            var url =  $(this).data('update');
            var oldValue = $(this).data('title');
            var newTitle = $(this).text();

            $.ajax({
                url: url,
                method: 'get',
                data: {'title': newTitle}
            }).done(function(response){
                console.log(response)
            })

        });
    }


    function addButton(){
        $('#card-modal').on('shown.bs.modal',function(event){
            var remoteUrl = $(event.relatedTarget).data('remote');
            var modal = $(this);

            $.ajax({
                 'method': 'get',
                 'url': remoteUrl
            }).done(function(response){
                    modal.find('.modal-body').html(response);
                    //console.log(response, 'bla')
                    createCard();
                }); 

        });
    }

    function createCard(){
        $('.card-form').on('submit',function(event){
            event.preventDefault();
            var cardFormAction = $(this).attr('action');
            console.log(cardFormAction, 'action');
            var cardData = $(this).serialize();
        
            $.ajax({
                url: cardFormAction,
                data: cardData,
                method: 'POST',

                
                
            }).done(function(response){
                event.preventDefault();
                var listID = response.list_id;
                var cardContainer = $(`#list-${listID}`);
                var card_template = `<li class="card-content" data-title="" data-update="/board/${response.board_id}/list/${response.list_id}/card/${response.id}/update/" contenteditable="true">${response.title}</li>`;

                $(cardContainer).find('.list-view').append(card_template);
                $('#card-modal').modal('hide');

                console.log(response, 'done');
            })
        });


    }



});

