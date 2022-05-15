// When button is clicked to view previous or next post or stands, update page
// without refreshing
$(document).ready(function() {

    $('#prev_post').click(function(e) {
      var lk = $(this).attr('href');
      searchResults(lk);
      e.preventDefault();
	});

	$('#next_post').click(function(e) {
      var lk = $(this).attr('href');
      searchResults(lk);
      e.preventDefault();
	});

	$('#prev_stand').click(function(e) {
      var lk = $(this).attr('href');
      searchResults(lk);
	  e.preventDefault();
	});

	$('#next_stand').click(function(e) {
      var lk = $(this).attr('href');
      searchResults(lk);
	  e.preventDefault();
	});

	$('body').css('background-color', '#252526');
});

// When button is clicked to view previous or next post or stands, get the information and
// then update
var searchResults = function(lk) {
  req = $.ajax({
	url: lk,
	type: "GET",
	datatype: "html",
	success: function(data) {
		$('body').html(data);
	}
  });
};

// unsubscribe from a stand by routing to the function that will remove it from the list for the 
// user in the database
function unsubscribeStand(standId, postIndex, firstStandIndex, lastStandIndex) {
	window.location.href = '/management/unsubscribe/' + standId + '/' + postIndex + '/' +
	firstStandIndex + '/' + lastStandIndex;
}