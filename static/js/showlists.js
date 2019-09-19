$(document).ready(function(){
    boardButton();
    createBoard();
    listCreate();
    
    
    
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
            console.log(csrf, 'test')
            
           
            if(newTitle.length == 0) {
                $(this).text(oldValue);
            } else {
                $.ajax({
                    
                    url: url,
                    method: 'POST',
                    data: {'title': newTitle, 'csrfmiddlewaretoken':csrf}
                }).done(function(response){
                    console.log(response)
                    
                });
            }
        });




    }).fail(function(response){
        var errorMessage = '<p>This field is required!</p>';
        $('.error-list-create').html(errorMessage);
    });
    
    function loadCards(url, element){
        $.ajax({
            url: url,
            method: 'GET',
        }).done(function(response){
            element.html(response);
            //var cardsElement = $('.card-section');
            
            dragCard();
            editCard();
            addButton();
            
        
    })

}


    function editCard(){
        $('.card-content').on('blur', function(){
            var url =  $(this).data('update');
            var oldValue = $(this).data('title');
            var newTitle = $(this).text();
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();

            if (newTitle.length == 0){
                $(this).text(oldValue);
            } else {
                $.ajax({
                url: url,
                method: 'POST',
                data: {'title': newTitle, 'csrfmiddlewaretoken':csrf}
            }).done(function(response){
                console.log(response)
                
            })
            }
            
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
            }).fail(function(response){
                //alert('invalid input');
                var errorMessage = '<p>This field is required</p>';

                $('.error-card').html(errorMessage);


            });
        });
    }



    function boardButton(){
        $('#board-modal').on('shown.bs.modal',function(event){
            var remoteUrl = $(event.relatedTarget).data('remote');
            var modal = $(this);

            $.ajax({
                'method':'get',
                'url': remoteUrl
            }).done(function(response){
                modal.find('.modal-body').html(response);
                editBoard();
            })
            
        });
    }

    function editBoard(){
        $(document).on('submit', '.board-form', function(event){
            event.preventDefault();
            var boardFormAction = $(this).attr('action');
            var boardData = $(this).serialize();
            $.ajax({
                url:boardFormAction,
                data: boardData,
                method: 'POST'
            }).done(function(response){
                event.preventDefault();
                $('#boardbutton').text(`${response.title}`);
                $('.close').trigger('click');
            }).fail(function(response){
                var errorMessage = '<p>Board title is required</p>';
                $('.error').html(errorMessage);
            });

        });
    }

    function createBoard(){
        $('#board-modal').on('shown.bs.modal',function(event){
            var remoteUrl = $(event.relatedTarget).data('remote');
            var modal = $(this);
            $.ajax({
                method: 'get',
                url: remoteUrl
            }).done(function(response){
                modal.find('.modal-body').html(response);

                boardSubmit();
            });
        });
    }

    function boardSubmit(){
        $('#board-form').on('submit',function(event){
            event.preventDefault();
            var boardFormAction = $(this).attr('action');
            var boardData = $(this).serialize();
            
            $.ajax({
                method:'POST',
                url:boardFormAction,
                data:boardData
            }).done(function(response){
                event.preventDefault();
                window.location.href = "/board/detail/" + response.board_id
                console.log(response, 'test')
                $('.close').trigger('click');
            }).fail(function(response){
                //alert('invalid input');
                var errorMessage = '<p>This field is required</p>';

                $('.error-board-create').html(errorMessage);


            });
        })
    }



    function listCreate(){
        $(document).on('submit','#list-form',function(event){
            event.preventDefault();

            var listFormAction = $(this).attr('action');
            var listdata = $(this).serialize();

            $.ajax({
                method:'POST',
                url:listFormAction,
                data:listdata
            }).done(function(response){
                

            }).fail(function(response){
                var errorMessage = '<p>This field is required!</p>';
                $('.error-list-create').html(errorMessage);
            });
        })
    }

    function dragCard(){
        $('.draggable').draggable();
        
        var csrf = $('input[name="csrfmiddlewaretoken"]').val();
        //console.log(cardUrl, 'test URL');

        $('.list-section').droppable({
            drop:function(event, ui){
               var sectionID = $(this).data('id');
               console.log(sectionID, 'test section');
               console.log(event, 'test event');

               var cardID = $(event.toElement).data('id') ;
               var cardUrl = $(event.toElement).data('url');
               console.log(cardID,cardUrl, 'test ID,url');
                $.ajax({
                    method:'POST',
                    url:cardUrl,
                    data:{'card_id':cardID,'list_id':sectionID,'csrfmiddlewaretoken':csrf}
                }).done(function(response){
                    var cardcontainer = response.list_id;
                    var cardget = $(`#list-${cardcontainer}`);

                    var cardid = response.card_id;
                    var card = $(`#cardl-${cardid}`)

                    $(this).find(cardget).html(card);
                    console.log(response, 'response test');
                });
            }
        });
    }


    $(document).on('shown.bs.modal','#card-view-modal',function(event){
        event.preventDefault();
        var remoteUrl = $(event.relatedTarget).data('remote');
        var modal = $(this);
        $.ajax({
            
            url:remoteUrl,
            method:'GET'
            
        }).done(function(response){
            event.preventDefault();
            modal.find('.modal-body').html(response);
            
        });


    });


        
        $(document).on('blur','.card-detail-title', function(){
            var url = $(this).data('update');
            var oldValue = $(this).data('title');
            var newTitle = $(this).text();
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();
            
           
            if(newTitle.length == 0) {
                $(this).text(oldValue);
            } else {
                $.ajax({
                    url: url,
                    method: 'POST',
                    data: {'title': newTitle, 'csrfmiddlewaretoken':csrf}
                }).done(function(response){
                    //edit card title in background
                    var cardID = response.card_id
                    var card = $(`#carddetail-${cardID}`)
                    console.log(response.title, 'respondcard')
                    $(card).html(`${response.title}`);

                });
            }
        });




    
        $(document).on('blur','.card-detail-label', function(){
            var url = $(this).data('update');
            var oldValue = $(this).data('label');
            var newLabel = $(this).text();
            var csrf = $('input[name="csrfmiddlewaretoken"]').val();

            if(newLabel.length == 0){
                $(this).text(oldValue);
            } else {
                $.ajax({
                    url:url,
                    method:'POST',
                    data: {'labels': newLabel, 'csrfmiddlewaretoken':csrf}
                }).done(function(response){
                    
                    
                });
            }

        });

    
        

        
    
        

});
