import pandas as pd;
import numpy as np;
import pickle


matches_data  = pd.read_csv('./data/matches_cleaned.csv')
randomForestModel = pickle.load(open('./model/RandomForestModel.pkl','rb'))
logisticRegressionModel= pickle.load(open('./model/logModel.pkl','rb'))
naiveModel= pickle.load(open('./model/NaiveModel.pkl','rb'))
svmModel = pickle.load(open('./model/SVMModel.pkl','rb'))
modelEval = pickle.load(open('./model/eval_metric.pkl','rb'))

def predict_result(city,team_batting_first,team_batting_second,toss_winner,toss_decision):
    # Label encoding the received input to match our machine learning model
    venue = get_label_encoded_venue(city)
    team1 = get_label_encoded_team(team_batting_first)
    team2 = get_label_encoded_team(team_batting_second)
    toss_winner = get_label_encoded_toss_winner(team_batting_first,team_batting_second,toss_winner)
    toss_decision = get_label_encoded_toss_decision(toss_decision)

    # Getting the average strike rate of team batting first against team batting second
    average_SR_team1 = get_average_SR_team1(team_batting_first,team_batting_second)
    # average_SR_team1 = get_average_SR_team1(team_batting_first,team_batting_second,city)
    # Getting the average strike rate of team batting second against team batting first
    average_SR_team2 = get_average_SR_team2(team_batting_first,team_batting_second)
    # Getting the average runs scored in the powerplay by team batting first against the team batting second
    team1_powerplay = get_average_PP_team1(team_batting_first,team_batting_second)
    # Getting the average runs scored in the powerplay by team batting second against the team battting first
    team2_powerplay = get_average_PP_team2(team_batting_first,team_batting_second)
    # Getting the average extras bowled by the team bowling second against team batting second
    team1_extras = get_average_extras_team1(team_batting_first,team_batting_second)
    # Getting the average extras bowled by the team bowling first against team batting first
    team2_extras = get_average_extras_team2(team_batting_first,team_batting_second)
    # Fetching the average run rate score by team batting first
    average_RR_team1 = get_average_RR_team1(team_batting_first,team_batting_second)
    # Fetching the average run rate score by team batting first
    average_RR_team2 = get_average_RR_team2(team_batting_first,team_batting_second)

    # dict = {'city':venue,'team1':team1,'team2':team2,'toss_winner':toss_winner,'toss_decision':toss_decision,
    #         'average_SR_team1':average_SR_team1,'average_SR_team2':average_SR_team2,'team1_powerplay':team1_powerplay,
    #         'team2_powerplay':team2_powerplay,'team2_extras':team2_extras,'team1_extras':team1_extras}
    dict = {'city':venue,'team1':team1,'team2':team2,'toss_winner':toss_winner,'toss_decision':toss_decision,
            'team1_powerplay':team1_powerplay,'team2_powerplay':team2_powerplay,'average_SR_team1':average_SR_team1,
            'average_SR_team2':average_SR_team2,'average_RR_team1':average_RR_team1,'average_RR_team2':average_RR_team2,
            'team2_extras':team2_extras,'team1_extras':team1_extras}

    predict_features = pd.DataFrame(dict,index=[0])
    random_forest_predicted_value = randomForestModel.predict(predict_features)
    logistic_regression_predicted_value = logisticRegressionModel.predict(predict_features)
    naive_bayes_predicted_value = naiveModel.predict(predict_features)
    svm_predicted_value = svmModel.predict(predict_features)

    random_forest_winner = get_match_winner(team_batting_first,team_batting_second,random_forest_predicted_value)
    log_regression_winner = get_match_winner(team_batting_first,team_batting_second,logistic_regression_predicted_value)
    naive_bayes_winner = get_match_winner(team_batting_first,team_batting_second,naive_bayes_predicted_value)
    svm_winner = get_match_winner(team_batting_first,team_batting_second,svm_predicted_value)

    match_winner = {'rfc':random_forest_winner,'lrc':log_regression_winner,'nbc':naive_bayes_winner,'svc':svm_winner}
    print(venue,team1,team2,toss_winner,toss_decision,average_SR_team1,average_SR_team2,average_RR_team1,average_RR_team2,team1_powerplay,team2_powerplay,team2_extras,team1_extras)
    print(random_forest_winner)
    print(log_regression_winner)
    print(naive_bayes_winner)
    print(svm_winner)
    return match_winner

# Function to fetch the team batting first and team batting second
def get_team1_team2(home_team,away_team,toss_winner,toss_decision):
    team_batting_first =""
    team_batting_second = ""
    if home_team == toss_winner:
        if toss_decision == "Field":
            team_batting_second = home_team
            team_batting_first = away_team
        else:
            team_batting_second = away_team
            team_batting_first = home_team
    else:
        if toss_decision == "Field":
            team_batting_second = away_team
            team_batting_first = home_team
        else:
            team_batting_second = home_team
            team_batting_first = away_team
    return team_batting_first,team_batting_second

def get_match_winner(team_batting_first,team_batting_second,predicted_value):
    if  predicted_value[0]==0:
        return team_batting_first
    else:
        return team_batting_second
# Function for label encoding city
def get_label_encoded_venue(city):
    city_label_encoding = {'Bengaluru': 2, 'Chandigarh': 6, 'Chennai': 7, 'Delhi': 9,
                        'Hyderabad': 14, 'Jaipur': 16, 'Kolkata': 21,'Mumbai': 23}
    return city_label_encoding[city]

# Function for label encoding team
def get_label_encoded_team(team):
    team_label_encoding = {'Chennai Super Kings': 0, 'Delhi Capitals': 1,'Kings XI Punjab': 3,'Kolkata Knight Riders': 5,
                    'Mumbai Indians': 6,'Rajasthan Royals': 8, 'Royal Challengers Bangalore': 9, 'Sunrisers Hyderabad': 10}
    return team_label_encoding[team]

# Function for label encoding toss decision
def get_label_encoded_toss_decision(toss_decision):
    if toss_decision == 'Bat':
        return 0
    else:
        return 1

# Function for label encoding toss winner
def get_label_encoded_toss_winner(team1,team2,toss_winner):
    if toss_winner == team1:
        return 0
    else:
        return 1

# Function to fetch the match data
def get_matches(team_batting_first,team_batting_second):
    matches = matches_data[(matches_data['team1']== team_batting_first)&(matches_data['team2']== team_batting_second)]\
    [['team1','team2','average_SR_inning1','average_SR_inning2','average_RR_inning1','average_RR_inning2',
    'team1_powerplay','team2_powerplay','team2_extras','team1_extras']]
    return matches

# Function to return the average strike rate of team batting first
def get_average_SR_team1(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team1_average_SR = matches_between_team1_team2[['team1','average_SR_inning1']].groupby('team1').mean().reset_index()
    return round(team1_average_SR.iloc[0][1],2)

# Function to return the average strike rate of team batting second
def get_average_SR_team2(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team2_average_SR = matches_between_team1_team2[['team2','average_SR_inning2']].groupby('team2').mean().reset_index()
    return round(team2_average_SR.iloc[0][1],2)

# Function to return the average run rate of team batting first against team batting second
def get_average_RR_team1(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team1_average_RR = matches_between_team1_team2[['team1','average_RR_inning1']].groupby('team1').mean().reset_index()
    return round(team1_average_RR.iloc[0][1],2)
# Function to return the average run rate of team batting second against team batting first
def get_average_RR_team2(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team2_average_RR = matches_between_team1_team2[['team2','average_RR_inning2']].groupby('team2').mean().reset_index()
    return round(team2_average_RR.iloc[0][1],2)

# Function to return the average runs scored in the powerplay of team batting first
def get_average_PP_team1(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team1_average_PP = matches_between_team1_team2[['team1','team1_powerplay']].groupby('team1').mean().reset_index()
    return round((team1_average_PP.iloc[0][1]/6),2)

# Function to return the average runs scored in the powerplay of team batting second
def get_average_PP_team2(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team2_average_PP = matches_between_team1_team2[['team2','team2_powerplay']].groupby('team2').mean().reset_index()
    return round((team2_average_PP.iloc[0][1]/6),2)

# Function to return the average extras given by team batting first
def get_average_extras_team1(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team1_average_extras = matches_between_team1_team2[['team1','team1_extras']].groupby('team1').mean().reset_index()
    return round((team1_average_extras.iloc[0][1]),2)

# Function to return the average extras given by team batting second
def get_average_extras_team2(team_batting_first,team_batting_second):
    matches_between_team1_team2 = get_matches(team_batting_first,team_batting_second)
    team2_average_extras = matches_between_team1_team2[['team2','team2_extras']].groupby('team2').mean().reset_index()
    return round((team2_average_extras.iloc[0][1]),2)

# Function to return the team name from the venue
def get_team(venue):
  team_venue_mapping=get_team_venue_mapping()
  return list(team_venue_mapping.keys())[list(team_venue_mapping.values()).index(venue)]

# Function to return the team_venue_mapping
def get_team_venue_mapping():
  team_venue_mapping = {'Chennai Super Kings': 'Chennai', 'Delhi Capitals': 'Delhi','Kings XI Punjab': 'Chandigarh',
                      'Kolkata Knight Riders': 'Kolkata', 'Mumbai Indians': 'Mumbai',
                      'Rajasthan Royals': 'Jaipur', 'Royal Challengers Bangalore': 'Bengaluru', 'Sunrisers Hyderabad': 'Hyderabad'}
  return team_venue_mapping

# Function to return the matches data
def get_matches_data():
  return matches_data

# Function to return team name and its abbreviation mapping
def get_team_abbreviation_mapping():
  team_abbreviation_mapping = {"Chennai Super Kings":"CSK", "Delhi Capitals":"DC","Gujarat Lions":"GL","Kings XI Punjab":"KXIIP",
                                "Kochi Tuskers Kerala":"KTK","Kolkata Knight Riders":"KKR","Mumbai Indians":"MI",
                                "Pune Warriors":"PW","Rajasthan Royals":"RR","Royal Challengers Bangalore":"RCB"
                                ,"Sunrisers Hyderabad":"SRH"}
  return team_abbreviation_mapping

def get_model_evaluation():
  return modelEval
