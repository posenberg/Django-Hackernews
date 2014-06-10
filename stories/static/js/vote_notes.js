
//make sure all dom elements are loaded

$(document).ready(function(){

function vote(storyID){
	$.ajax({ //pass in object 
		type: "POST", //that contains a type:"POST"
		url: "/vote/",
		data: {"story": storyID}, // has data that has an object containing a storyID
		success: function(){ // if this ajax request is sucessful
			// Note**  these are the ids that we will use index.html //

			//call the dollar sign function pass in the id for vote anchor tag and concatenate the story ID and hide it with the hide function.
			$("#story-vote-" + storyID).hide();
			//call the dollar sign function pass in ID for title anchor tag, and concatenate with Story id.Then call css function pass in the css
			
			$("#story-title-" + storyID).css({"margin-left":"15px"})
		}
	})
	//returns false to make sure that when the user clicks the link, that it doesn't go to the next page 
	return false;
}
//assume there is a class attached to all those anchor tags called vote or .vote.

// call the dollar sign function, pass the string a.vote to get all the anchor tags with the vote class
// then call the click function and then pass in our own function
$("a.vote").click(function(){
	//that will  get the  story id from the id of the current anchor tag
	// inside of this function that "this" function points to the anchor tag.
	// split the id on the dash "-" symbol, give us an array with 3 [2] symbols in it. First two are story and the vote,
	// and the last one has the storyid.
	var storyID = parseInt(this.id.split("-")[2]) //this.id.split returns a string so we need to use parseInt
	return vote(storyID);  //call the vote function and pass in storyId
	// should take care of adding the vote functionality to the arrow.gif anchor tags on our page. 
})

});

//now to add vote class to each of the anchor tags in index.html