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

        // $($listContent).click(function(event){
        //     var listURL = $(this).data('url');
        //     var esc = event.which==27,
        //         enter = event.which==13,
        //         el = event.target,
        //         data = {};

        //     if(esc){
        //         document.execCommand('undo');
        //         el.blur();
        //     }else if (enter){
        //         var edit = $(this).text();
        //         var editID = $(this).data('id');
        //         editList(listURL, data, $(this));
        //     }
        // });


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

        $()
        



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
            //var cardsElement = $('.card-section');

            editCard();

        $('#exampleModalCenter').on('shown.bs.modal',function(e){
            var remoteUrl = $(e.relatedTarget).data('remote');
            var modal = $(this);

            $.ajax({
                 'method': 'get',
                 'url': remoteUrl
            }).done(function(response){
                    modal.find('.modal-body').html(response);  
                }); 
        })

        

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



});

