$(document).ready(function(){


    $("#connectds").on('click',function(){
      $('.home-welcome').css('display','none');
      $('.home-select').css('display','block');
    });

    $(".card-ds").on('click',function(){
        var datasourceSelected = $(this).attr('id');
        $('.home-select').css('display','none');
        $('.home-configure').css('display','block');
        $("#ds-id").val(datasourceSelected);

    });



  });