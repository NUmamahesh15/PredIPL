

var team_venue_mapping = {'Chennai':'Chennai Super Kings', 'Delhi':'Delhi Capitals','Chandigarh':'Kings XI Punjab',
                      'Kolkata':'Kolkata Knight Riders', 'Mumbai':'Mumbai Indians',
                      'Jaipur':'Rajasthan Royals', 'Bengaluru':'Royal Challengers Bangalore', 'Hyderabad':'Sunrisers Hyderabad'};
// Function to fetch the venue of the match based on the home team
function getVenue(city) {
// console.log(city)
document.getElementById("city").value =city;
}

// Function to check if the user entered the same team for both home team and away team
function checkTeam(type) {
var homeId=document.getElementById("homeId").value;
var awayId=document.getElementById("awayId").value;
// console.log(homeId)
// console.log(awayId)
if(homeId==awayId){
		window.alert("Please select two different teams for Prediction");
		document.getElementById("reset").click();
	}
}

// Function to populate the teams based on the home and away team
function teamWinningToss(type) {
var homeTeam=document.getElementById("homeId").value;
var awayTeam=document.getElementById("awayId").value;

for(i=document.getElementById("toss").length;i>0;i--)
{
document.getElementById("toss").remove(i);
}
var t1=homeTeam;
var t2=awayTeam;


if(t1!=""){
$(document.getElementById("toss")).append("<option  value="+t1+">" +team_venue_mapping[homeTeam]+ "</option>")

}
if(t2!=""){$(document.getElementById("toss")).append("<option  value="+t2+">" +team_venue_mapping[awayTeam]+ "</option>")
}

}

// Function to display other results and evaluation metric based on click event
$(document).ready(function(){
  $('#eval').on('click',function(){
    $('#evalMetric').toggle();
  });
  $('#oth-model').on('click',function(){
    $('#oth-table').toggle();
  });
});
