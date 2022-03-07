let provider, accounts, signer;
let accountAddress = "";

$( "#metamask_login" ).on( "click", function() {
        $.get("/")
    });

$( "#mintNew" ).on( "click", function() {
        mintExample();
        //Fix delay so that the nft is displayed after reload (maybe asynchronous with the get query, wait for response)
        setTimeout(location.reload(), 3000);
    });

function mintExample() {
    $.get("/mint")
}

$(function() {
  $(".selectable").selectable({
    selected: function() {
      var selectedItemList = $("#selected-item-list").empty();
      $(".selectable img").each(function(index) {
        if ($(this).hasClass("ui-selected")) {
          selectedItemList.append((index + 1) + ", ");
          if($(this).hasClass("nft")) {
            $(".nftInput").val($(this).attr('id'))
          }else{
            $(".nodeInput").val($(this).attr('id'))
          }
        }
      });
    }
  });
});