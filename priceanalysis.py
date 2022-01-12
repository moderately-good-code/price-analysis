#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 20:55:18 2021

@author: moderately-good-code
"""

import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

def predict_tomorrow(prices, method="linear regression"):
    if method == "linear regression":
        return np.sum(linear_regression(prices))
    else:
        raise NotImplementedError

def linear_regression(prices):
    """
    prices: prices as 1d numpy array
    """
    A = np.vstack((np.arange(-prices.shape[0]+1, 1),
                   np.ones(prices.shape[0]))).T
#    print(A)
    return np.linalg.pinv(A.T@A)@A.T@prices

def visualize_price_regression(timepoints, prices, coeff):
    """
    timepoints: time vector
    prices: prices as 1d numpy array
    coeff: regression coefficients
    """
    plt.plot(timepoints, prices, label="prices")
    x = np.linspace(timepoints[0], timepoints[-1], endpoint=True)
    plt.plot(x, coeff[1]+x*coeff[0], label="regression")
    plt.legend()

def regression_error(timepoints, prices, coeff):
    return np.mean(np.square(prices - (coeff[1]+coeff[0]*timepoints)))

def get_unitless_timepoints(prices):
    return np.arange(-prices.shape[0]+1, 1, dtype=np.float64)

def get_best_regression(minspan, maxspan, stepsize, timepoints, prices,
                        visualization=False):
    """
    minspan: minimum number of timepoints used for regression
    maxspan: maximum number of timepoints used for regression
    stepsize: number of timepoints to add each iteration
    timepoints: unitless timepoints from -n to 0
    prices: list of prices at timepoints
    visualization: visualize each regression
    
    return best timespan, best error, best coefficients
    """
    best_span = -1
    best_err = np.Inf
    best_coeff = np.empty(2)
    for timespan in range(minspan, maxspan, stepsize):
        # calculate linear regression
        coeff = linear_regression(prices[-timespan:])
        
        # calculate mean squared error for current regression
        err = regression_error(timepoints[-timespan:], prices[-timespan:],
                               coeff)
        
        # compare to previous errors
        if err < best_err:
            best_span = timespan
            best_err = err
            best_coeff = coeff
        
        # visualize current regression
        if visualization:
            t = np.linspace(-timespan+1, 1)
            plt.plot(t, coeff[1]+coeff[0]*t)
#            visualize_price_regression(timepoints[-timespan:],
#                                       prices[-timespan:], coeff)
    
    if visualization:
        plt.plot(timepoints, prices)
    
    return best_span, best_err, best_coeff

def current_deviation_from_trend(mean_err, coeff, current_timepoints,
                                 current_prices):
    """
    mean_err: mean squared error of the given regression
    coeff: linear regression coefficients
    current_timepoints: timepoints to be compared with general regression
    current_prices: prices at current_timepoints
    
    return: number between -1 (currently much cheaper than trend) and 1
            (currently much higher than trend)
    """
    current_err = regression_error(current_timepoints, current_prices, coeff)
    predicted_current_mean_price = np.mean(coeff[1]
                                           + coeff[0]*current_timepoints)
    real_current_mean_price = np.mean(current_prices)
    return 2*sigmoid(current_err / mean_err
                     * np.sign(real_current_mean_price
                               - predicted_current_mean_price)
                     ) - 1
    

def sigmoid(x):
    return np.exp(x) / (1.0 + np.exp(x))

def current_percentile(prices, current_timespan):
    """
    prices: list of prices
    current_timespan: the timespan over which the average current price is
            calculated
            
    return: percentile of average current price in list of prices
    """
    current_avg_price = np.mean(prices[-current_timespan:])
    return stats.percentileofscore(prices, current_avg_price)
    

def summarize_price_statistics(timepoints, prices, interval="1h", minspan=96,
                               maxspan=336, stepsize=6, current_timespan=12):
    """
    timepoints: unitless timepoints from -n to 0
    prices: prices at timepoints
    interval: interval between timepoints
    """
    # TODO: assert that parameters are in sensible range
    
    if interval == "1h":
        pass
    else:
        raise NotImplementedError
    
    summary = {"current price": prices[-1],
               "current timespan": current_timespan}
    
    # calculate average price for the current time
    avg_price = np.mean(prices[-current_timespan:])
    summary["current average price"] = avg_price
    
    # calculate current change rate
    current_coeff = linear_regression(prices[-current_timespan:])
    summary["current change"] = current_coeff[0]/avg_price*current_timespan
    
    # calculate best linear regression to get trend
    best_span, best_err, best_coeff = get_best_regression(minspan, maxspan,
                                                          stepsize, timepoints,
                                                          prices,
                                                          visualization=False)
    summary["regression span"] = best_span
    summary["regression error"] = best_err
    summary["regression coefficients"] = best_coeff
    
    # calculate the current deviation from the regression trend
    deviation = current_deviation_from_trend(best_err, best_coeff,
                                             timepoints[-current_timespan:],
                                             prices[-current_timespan:])
    summary["current deviation"] = deviation
    summary["current month percentile"] = current_percentile(prices[-30*24:],
           current_timespan)
    
    return summary