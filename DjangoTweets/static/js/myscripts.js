$(document).ready(function() {
   (function onload() {
   	$("#last_refresh_datetime")[0].value = ($.now())
   })();
  (function poll() {
    
    lastRefreshDT =$("#last_refresh_datetime")[0].value  
    url = "/CheckIfRefreshNecessary/"

    setTimeout(function(url) {
        $.ajax({
            url: "/CheckIfRefreshNecessary/" ,
            data: {
            	clientdt : lastRefreshDT
            },
            type: "POST",
            success: function(data) {
               if(data.message)
               {
               		//refresh page
               		$.ajax({
               			url: "/home/",
               			type: "GET",
               			success: function(data)
               			{
               				window.location.reload();
               			}
               		});
               }

            },
            dataType: "json",
            complete: poll,
            timeout: 5000
        })
    }, 5000);
  })();
});


function searchusers()
{
	searchquery =$("#searchquery")[0].value
	$.ajax({
        url: "/search/" ,
        data: {
        	searchquery  : searchquery
        },
        type: "POST",
        success: function(data) {
           if(data)
           {
        	   searchresultsdiv = $("#searchResults")
        	   
           	$("#searchResults")[0].innerHTML = data.user_choices_list
           	$("#myTab a[href='#results']").tab('show')
           }
        },
        dataType: "json"        
    })
}
function sendmessage()
{
	tweetmessage =$("#tweetmessage")[0].value
	
    $.ajax({
        url: "/PostTweet/" ,
        data: {
        	tweetmessage  : tweetmessage
        },
        type: "POST",
        success: function(data) {
           if(data.message=="Success")
           {
           	
           }
        },
        dataType: "json"        
    })
}