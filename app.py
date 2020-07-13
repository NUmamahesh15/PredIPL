from flask import Flask, render_template,request,jsonify,redirect,url_for
import json
from computation import predict_result,get_team1_team2,get_team,get_team_venue_mapping,get_matches_data,get_team_abbreviation_mapping,get_model_evaluation
import pandas as pd
import numpy as np

app = Flask(__name__)

matches_data = get_matches_data()
# team_venue_mapping = {'Chennai Super Kings': 'Chennai', 'Delhi Capitals': 'Delhi','Kings XI Punjab': 'Chandigarh',
#                       'Kolkata Knight Riders': 'Kolkata', 'Mumbai Indians': 'Mumbai',
#                       'Rajasthan Royals': 'Jaipur', 'Royal Challengers Bangalore': 'Bengaluru', 'Sunrisers Hyderabad': 'Hyderabad'}
# team_abbreviation_mapping = {"Chennai Super Kings":"CSK", "Delhi Capitals":"DC","Gujarat Lions":"GL","Kings XI Punjab":"KXIIP",
#                                 "Kochi Tuskers Kerala":"KTK","Kolkata Knight Riders":"KKR","Mumbai Indians":"MI",
#                                 "Pune Warriors":"PW","Rajasthan Royals":"RR","Royal Challengers Bangalore":"RCB"
#                                 ,"Sunrisers Hyderabad":"SRH"}


@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def get_match_details():
    return render_template('home.html')


@app.route('/predict',methods=['POST','GET'])
def get_prediction_page():
    team_venue_mapping = get_team_venue_mapping()
    return render_template('predict.html',team_venue_mapping=team_venue_mapping)

# @app.route('/gallery',methods=['POST','GET'])
# def get_gallery():
#     return render_template('gallery.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        # Getting home team from the web page and fetching its equivalent full team name
        home_team = get_team(request.form['homeTeam'])
        # Getting away team from the web page and fetching its equivalent full team name
        away_team = get_team(request.form['awayTeam'])
        # Fetching city from web page
        city = request.form['city']
        # Getting toss winner from the web page and fetching its equivalent full team name
        toss_winner = get_team(request.form['tossWinner'])
        # Fetching the decision taken by the team winning  the toss
        toss_decision = request.form['selector1']

        # Getting team batting first and team batting second using the input from the user
        team_batting_first,team_batting_second = get_team1_team2(home_team=home_team,away_team=away_team,toss_winner=toss_winner,toss_decision=toss_decision)

        winner = predict_result(city=city,team_batting_first=team_batting_first,team_batting_second=team_batting_second,toss_winner=toss_winner,toss_decision=toss_decision)
        
        # match_details = [home_team,away_team,city,toss_winner,toss_decision,team_batting_first,team_batting_second,winner]
        match_details = {'home_team':home_team,'away_team':away_team,'city':city,'toss_winner':toss_winner,'toss_decision':toss_decision,
                        'team_batting_first':team_batting_first,'team_batting_second':team_batting_second,'winner':winner}
        print(home_team, away_team, city, toss_winner, toss_decision,winner)
        eval_metrics = get_model_evaluation()
        eval_metrics = eval_metrics.to_dict()
        print(eval_metrics)
    return render_template('submit.html',match_details=match_details,eval_metrics=eval_metrics)

@app.route('/stats', methods=['GET'])
def get_display_stats():
    return render_template("statistics.html")

@app.route('/franchise', methods=['GET'])
def get_franchise():
    return render_template("franchises.html")

@app.route('/pie', methods=['POST', 'GET'])
def get_stats():
    number_matches =len(matches_data)
    args = request.args
    # Compute toss winner vs match winner - Number of matches won by the team also winning the toss
    if args['chart']=="tossWinnerMatchWinner":
        toss_win_match_win = matches_data[matches_data['toss_winner']==matches_data['winner']]
        number_matches_toss_win_match_win = len(toss_win_match_win)
        number_matches_toss_win_match_lost = number_matches - number_matches_toss_win_match_win

        dict_data = {"num_played":number_matches,"number_matches_toss_win_match_win": number_matches_toss_win_match_win
        , "number_matches_toss_win_match_lost":number_matches_toss_win_match_lost,'chart_type':'tossWinMatchWin' }
        data = json.dumps({"won": number_matches_toss_win_match_win, "lost":number_matches_toss_win_match_lost })
        return render_template("pieChart.html",data=data,dict_data=dict_data)
    # Computing the toss decision taken by the teams over the years
    elif args['chart']=="tossDecision":
        toss_decision_field = len(matches_data[matches_data['toss_decision']=="field"])
        toss_decision_bat = number_matches - toss_decision_field
        dict_data = {"num_played":number_matches,"field": toss_decision_field, "bat":toss_decision_bat, 'chart_type':'tossDecision' }
        data = json.dumps({"field": toss_decision_field, "bat":toss_decision_bat })
        return render_template("pieChart.html",data=data,dict_data=dict_data)

    # Computing toss decision field
    elif args['chart']=="tossDecisionField":
        toss_decision_field = matches_data[matches_data['toss_decision']=="field"]
        number_matches =len(toss_decision_field)
        matches_won = toss_decision_field[toss_decision_field['toss_winner']==toss_decision_field['winner']]
        number_matches_won = len(matches_won)
        number_matches_lost = number_matches - number_matches_won
        dict_data = {"num_played":number_matches,"won": number_matches_won, "lost":number_matches_lost, 'chart_type':'tossDecisionField' }
        data = json.dumps({"won": number_matches_won, "lost":number_matches_lost})
        return render_template("pieChart.html",data=data,dict_data=dict_data)
    # Computing toss decision bat
    elif args['chart']=="tossDecisionBat":
        toss_decision_bat = matches_data[matches_data['toss_decision']=="bat"]
        number_matches =len(toss_decision_bat)
        matches_won = toss_decision_bat[toss_decision_bat['toss_winner']==toss_decision_bat['winner']]
        number_matches_won = len(matches_won)
        number_matches_lost = number_matches - number_matches_won
        dict_data = {"num_played":number_matches,"won": number_matches_won, "lost":number_matches_lost, 'chart_type':'tossDecisionBat' }
        data = json.dumps({"won": number_matches_won, "lost":number_matches_lost})
        return render_template("pieChart.html",data=data,dict_data=dict_data)
    # Compute performance of the team on home ground
    elif args['chart']=="homeGround":
        if request.method=='POST':
            home_team = get_team(request.form['homeTeam'])
            city = request.form['city']
            home_ground_matches=matches_data[((matches_data['team1']==home_team)|(matches_data['team2']==home_team))&(matches_data['city']==city)]
            home_ground_win = home_ground_matches[home_ground_matches['winner']==home_team]
            home_ground_lost = len(home_ground_matches)-len(home_ground_win)
            dict_data = {"num_played":len(home_ground_matches),"won": len(home_ground_win), "lost":home_ground_lost,
                        'chart_type':'homeGround','team':home_team }
            data = json.dumps({"won": len(home_ground_win), "lost":home_ground_lost})
        return render_template("pieChart.html",data=data,dict_data=dict_data)


@app.route('/homeGround', methods=['GET'])
def get_homeGround():
    if request.method=='GET':
        team_venue_mapping = get_team_venue_mapping()
        return render_template("homeGround.html",teams=team_venue_mapping)

@app.route('/barTossDecision', methods=['GET'])
def get_bar_toss_decision():
    args = request.args
    if args['chart'] == "barTossDecision":

        season_group = pd.DataFrame(matches_data[['season','toss_decision','id']].groupby(['season','toss_decision']).count().unstack().reset_index())
        season_group.columns =['season','bat','field']
        season_field= season_group[['season','field']]
        season_field.columns=['season','value']
        season_bat= season_group[['season','bat']]
        season_bat.columns=['season','value']
        bat_chart_data = season_bat.to_dict(orient='records')
        field_chart_data = season_field.to_dict(orient='records')
        bat_chart_data = json.dumps(bat_chart_data)
        field_chart_data = json.dumps(field_chart_data)
        data = {'bat_chart_data': bat_chart_data,'field_chart_data':field_chart_data}
        return render_template("tossDecision.html",data=data,chart_type='barTossDecision')

    elif args['chart'] == "barMatchesPlayed":
        # Number of matches played batting first
        number_of_matches_played_team1 = matches_data[['team1','id']].groupby('team1').count()
        # Number of matches played batting second
        number_of_matches_played_team2 = matches_data[['team2','id']].groupby('team2').count()
        # Combining the number of matches to ge tthe total number of matches
        number_of_matches_played = number_of_matches_played_team1['id'] + number_of_matches_played_team2['id']
        number_of_matches_played = number_of_matches_played.to_frame().reset_index()
        number_of_matches_played.rename(columns= {"team1":"team","id":"count"},inplace=True)
        team_abbreviation_mapping = get_team_abbreviation_mapping()
        number_of_matches_played['team'] = number_of_matches_played['team'].map(team_abbreviation_mapping)
        chart_data = number_of_matches_played.to_dict(orient='records')
        chart_data = json.dumps(chart_data)
        data = {'chart_data': chart_data}
        return render_template("matches.html",data=data,chart_type='barMatchesPlayed')

    elif args['chart'] == "barMatchesWon":
        # Fetching the number of matches won by the teams participating in IPL
        matches_won=matches_data[['id','winner']].groupby('winner').count().reset_index()
        team_abbreviation_mapping = get_team_abbreviation_mapping()
        matches_won['winner'] = matches_won['winner'].map(team_abbreviation_mapping)
        matches_won.rename(columns= {"winner":"team","id":"count"},inplace=True)
        chart_data = matches_won.to_dict(orient='records')
        chart_data = json.dumps(chart_data)
        data = {'chart_data': chart_data}
        return render_template("matches.html",data=data,chart_type='barMatchesWon')

if __name__ == '__main__':
    app.run(debug=True)
