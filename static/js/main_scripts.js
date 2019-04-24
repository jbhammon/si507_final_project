/*
This code inspired by this Stack Overflow post:
https://stackoverflow.com/questions/8814472/how-to-make-an-html-back-link

Lets the user navigate back to the party they came from after viewing
details about a Pokemon
*/
var backToTeam = document.getElementById('back-link');

backToTeam.setAttribute('href', document.referrer);

backToTeam.onclick = function() {
  history.back();
  return false;
}
