import pandas as pd

def bet(game, pred, expected_win):
    stake = (expected_win/game['B365'+pred])
    print(game['HomeTeam'], game['AwayTeam'], pred, game['B365'+pred], game['FTR'])
    return expected_win - stake if pred == game['FTR'] else -1 * stake, stake
    #return (10 * game['B365'+pred]) - 10 if pred == game['FTR'] else -10, 10

def simulate(ratio, expected_win, filename):
    total = 0
    df = pd.read_csv(filename)

    count = 0
    betted_money = 0

    for i, game in df.iterrows():
        #for x in ["H", "D", "A"]:
        #for x in ["H", "A"]:
        for x in ["D"]:
            #if (1+ratio)*game["B365"+x] < game[x+"_odds"] and game["B365"+x] < 2 and game[x+"_odds"] > 1:
            if (1+ratio)*game["B365"+x] < game[x+"_odds"]:
                count += 1
                res, bm = bet(game, x, expected_win)
                #print(res)
                total += res
                betted_money += bm
    print(total)
    print(count)
    print(total / count)
    print(betted_money)
    return total, count

files = ["all","E0","D1","I1","SP1","F1"]
results = {}
for file in files:
    total, count = simulate(0.25, 10.0, "Odds/last1-"+file+".csv")
    results[file] = {'total': total, 'count': count}
print(results)