document.addEventListener('DOMContentLoaded', function () {
  chrome.windows.getCurrent(function(w) { chrome.tabs.getSelected(w.id, function (response){
          $('#pagemoveiframe').attr('src','http://pagemove.se/saveUrl/?url=' + response.url);
        });
    });


    $.get('http://pagemove.se/validToken/', function(data) {
          if(data == 'false'){
            chrome.tabs.create({"url":"http://pagemove.se/login","selected":true},function(tab){
              $("#setUp").html("<b>Bringing you to Twitter for setup</b><br><br><img src='icon.png' height='80px'/>");
              var t=setTimeout("closeWindow()",2000);

            });
        }
    });
});
