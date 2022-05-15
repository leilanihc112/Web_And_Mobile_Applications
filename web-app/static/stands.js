// A script file for dealing with logic related to stands

// Calculate and route the page to the previous stand page
// The calculations ensure that the stand indices are bound correctly
function prevStands(secondStandIndex, standCount, maxPerPage) {
	var temp = (secondStandIndex - (maxPerPage)) - ((secondStandIndex - (maxPerPage)) % maxPerPage);
	var firstStandIndex = 0;
	if ((secondStandIndex == standCount) && (temp < (secondStandIndex - maxPerPage))) {
        firstStandIndex = temp;
        secondStandIndex = temp + maxPerPage;
    }
	else if ((secondStandIndex - maxPerPage) <= 0) {
        firstStandIndex = 0;
    }
	else {
		firstStandIndex = secondStandIndex - (2 * maxPerPage);
		secondStandIndex = secondStandIndex - maxPerPage;
	}

	window.location.href = '/view_all_stands/' + firstStandIndex + '/' + secondStandIndex;
}

// Calculate and route the page to the next stand page
// The calculations ensure that the stand indices are bound correctly
function nextStands(secondStandIndex, standCount, maxPerPage) {
    var lastStandIndex = secondStandIndex + maxPerPage;
    if (secondStandIndex - 1 + maxPerPage >= standCount) {
        lastStandIndex = standCount;
    }
	window.location.href = '/view_all_stands/' + secondStandIndex + '/' + lastStandIndex;
}

// Route the user to be subscribed to a stand
function subscribe(stand_id, first_post_index, second_post_index) {
    window.location.href = '/view/stand/' + stand_id + '/subscribe/' + first_post_index + '/' + second_post_index;
}

// Route the user to be unsubscribed from a stand
function unsubscribe(stand_id, first_post_index, second_post_index) {
    window.location.href = '/view/stand/' + stand_id + '/unsubscribe/' + first_post_index + '/' + second_post_index;
}

// Calculate and route to the previous set of posts on a stand page
// The calculations ensure that the post indices are bound correctly
function prevPosts(standId, secondPostIndex, postCount, maxPerPage) {
	var temp = (secondPostIndex - (maxPerPage)) - ((secondPostIndex - (maxPerPage)) % maxPerPage);
	var firstPostIndex = 0;
	if ((secondPostIndex == postCount) && (temp < (secondPostIndex - maxPerPage))) {
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
	window.location.href = '/view/stand/' + standId + '/' + firstPostIndex + '/' + secondPostIndex;
}

// Calculate and route to the next set of posts on a stand page
// The calculations ensure that the post indices are bound correctly
function nextPosts(standId, secondPostIndex, postCount, maxPerPage) {
	var lastPostIndex = secondPostIndex + maxPerPage;
    if (secondPostIndex - 1 + maxPerPage >= postCount) {
        lastPostIndex = postCount;
    }
	window.location.href = '/view/stand/' + standId + '/' + secondPostIndex + '/' + lastPostIndex;
}