# -*- coding: utf-8 -*-

MIN_BET = 1

def kelly_div_10(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    
    if probability_1 and odd_1 - 1/probability_1 > 0:
        result_1 = all_money * min(0.1, ((probability_1 * odd_1) / (odd_1 - 1))/10)
        
        if result_1 < MIN_BET:
            result_1 = 0
    else:
        result_1 = 0
        
    if probability_X and odd_X - 1/probability_X > 0:
        result_X = all_money * min(0.1, ((probability_X * odd_X) / (odd_X - 1))/10)
        
        if result_X < MIN_BET:
            result_X = 0
    else:
        result_X = 0

    if probability_2 and odd_2 - 1/probability_2 > 0:
        result_2 = all_money * min(0.1, ((probability_2 * odd_2) / (odd_2 - 1))/10)
        
        if result_2 < MIN_BET:
            result_2 = 0
    else:
        result_2 = 0

    return result_1, result_X, result_2


def always_bet_highest_odd_with_div_100(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    if odd_1 > odd_X and odd_1 > odd_2:
        return all_money*0.01, 0, 0
    elif odd_2 > odd_X and odd_2 > odd_1:
        return 0, 0, all_money*0.01
    elif odd_X > odd_1 and odd_X > odd_2:
        return 0, all_money*0.01, 0
    else:
        return 0,0,0
    

def always_bet_lowest_odd_with_div_100(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    if odd_1 < odd_X and odd_1 < odd_2:
        return all_money*0.01, 0, 0
    elif odd_2 < odd_X and odd_2 < odd_1:
        return 0, 0, all_money*0.01
    elif odd_X < odd_1 and odd_X < odd_2:
        return 0, all_money*0.01, 0
    else:
        return 0,0,0


def bet_randomly(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    import random
    result = [0,0,0]
    result[random.randint(0,3)] = all_money*0.01    
    return result
    

def div_10(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    result = div_100(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2)

    return result[0]*10, result[1]*10, result[2]*10

def div_100(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    if probability_1 and odd_1 - 1/probability_1 > 0:
        result_1 = 0.01 * all_money
        
        if result_1 < MIN_BET:
            result_1 = MIN_BET
    else:
        result_1 = 0
        
    if probability_X and odd_X - 1/probability_X > 0:
        result_X = 0.01 * all_money
        
        if result_X < MIN_BET:
            result_X = MIN_BET
    else:
        result_X = 0
        
    if probability_2 and odd_2 - 1/probability_2 > 0:
        result_2 = 0.01 * all_money
        
        if result_2 < MIN_BET:
            result_2 = MIN_BET
    else:
        result_2 = 0
        
    return result_1, result_X, result_2
    
    
def bet_2(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    return bet_X(2, all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2)
    
def bet_10(all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    return bet_X(10, all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2)
    
def bet_X(x, all_money, probability_1, odd_1, probability_X, odd_X, probability_2, odd_2):
    if probability_1 and odd_1 - 1/probability_1 > 0:
        result_1 = x
        
        if result_1 < MIN_BET:
            result_1 = MIN_BET
    else:
        result_1 = 0
        
    if probability_X and odd_X - 1/probability_X > 0:
        result_X = x
        
        if result_X < MIN_BET:
            result_X = MIN_BET
    else:
        result_X = 0
        
    if probability_2 and odd_2 - 1/probability_2 > 0:
        result_2 = x
        
        if result_2 < MIN_BET:
            result_2 = MIN_BET
    else:
        result_2 = 0
        
    return result_1, result_X, result_2
