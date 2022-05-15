function prevPosts(secondPostIndex, PostCount, maxPerPage) {
	// get previous posts - when previous button is clicked
    var search_string = document.getElementById("tag-search").value;
    var temp = (secondPostIndex - (maxPerPage)) - ((secondPostIndex - (maxPerPage)) % maxPerPage);
	var firstPostIndex = 0;
	// if the posts do not meet the max allowed on each page
	if ((secondPostIndex == PostCount) && (temp < (secondPostIndex - maxPerPage))) {
        firstPostIndex = temp;
        secondPostIndex = temp + maxPerPage;
    } 
	else if ((secondPostIndex - maxPerPage) <= 0) {
        firstPostIndex = 0;
    }
	else {
		firstPostIndex = secondPostIndex - (2 * maxPerPage);
		secondPostIndex = secondPostIndex - maxPerPage;
	}

	// go to previous posts by using indexes as arguments
	window.location.href = '/search/' + search_string + '/' + 
    firstPostIndex + '/' + secondPostIndex + '/';
}

function nextPosts(secondPostIndex, PostCount, maxPerPage) {
    var search_string = document.getElementById("tag-search").value; 
    var lastPostIndex = secondPostIndex + maxPerPage;
	// if the next would exceed the post count, then make the last index the post count
    if (secondPostIndex - 1 + maxPerPage >= PostCount) {
        lastPostIndex = PostCount
    }
	
	// go to next posts by using indexes as arguments
	window.location.href = '/search/' + search_string + '/' + 
    secondPostIndex + '/' + lastPostIndex + '/';
}


function search_click(maxPerPage) {
    var search_string = document.getElementById("tag-search").value; 
	// when a link is clicked, go from 0 to 10
    window.location.href = '/search/' + search_string +'/0/'+maxPerPage+'/';
}
