//make sure all dom elements are loaded
$( document ).ready(function() {

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function vote (storyID) {
    $.ajax({
        type: "POST",
        url: "/vote/",
        data: {"story": storyID},
        success: function() {
            $("#story-vote-" + storyID).hide();
            $("#story-title-" + storyID).css({"margin-left": "15px"});
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    return false;
}
//assume there is a class attached to all those anchor tags called vote or .vote.

// call the dollar sign function, pass the string a.vote to get all the anchor tags with the vote class
// then call the click function and then pass in our own function
$("a.vote").click(function() {
	console.log("works");
    var storyID = parseInt(this.id.split("-")[2]);
    return vote(storyID);
});

});

//now to add vote class to each of the anchor tags in index.html