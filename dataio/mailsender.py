import smtplib, ssl
from email.mime.text import MIMEText
import numpy as np
import dataio.cryptoscraper as cs
import priceanalysis as pa
import yfinance as yf

def send_mail(sender_email, receiver_email, password, message):
    """
    TODO: documentation
    """
    
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # TODO: Send email here
        
        server.sendmail(sender_email, receiver_email, message)

def coin_percentile_message(timespans_h=[150,450,1500], thresh_low=25, thresh_high=90):
    """
    TODO: documentation
    """
    message_header = f"timespans (h): {timespans_h}\n"
    message_header += f"thresholds: {thresh_low} and {thresh_high}\n"
    message_low_perc = "Coins with low percentile:\n"
    message_high_perc = "Coins with high percentile:\n"
    
    # iterate over all coins on Kraken and Yahoo Finance
    for coin_name in cs.KRAKEN_COINS_YF:
        # get historical data
        data = yf.Ticker(coin_name + "-EUR")
        history = data.history(period="3mo", interval="1h")
        for timespan in timespans_h:
            prices = np.array(history["Close"][-timespan:], dtype=np.float64)
            if prices.shape[0] < timespan:
                # raise RuntimeError("Could not get historical data for "+coin_name)
                message_header += f"Could not get historical data for {coin_name}\n"
            
            perc = pa.current_percentile(prices, 1)
            if perc < thresh_low:
                message_low_perc += f"{coin_name}: {perc} ({timespan}h)\n"
            elif perc > thresh_high:
                message_high_perc += f"{coin_name}: {perc} ({timespan}h)\n"
    
    entire_message = message_header + "\n" + message_low_perc + "\n" \
                     + message_high_perc
    return entire_message
        

def coin_summary_message(period="3mo", interval="1h", minspan=96, maxspan=720,
                         stepsize=6, current_timespan=24):
    """
    TODO: documentation
    """
    
    # check argument values
    total_timespan = -1
    if period == "3mo":
        total_timespan = 3*30*24
    else:
        raise NotImplementedError("Period " + period)
    if interval != "1h":
        raise NotImplementedError("Interval " + interval)
    if minspan < 24:
        raise NotImplementedError("Minimum timespan " + minspan)
    if maxspan <= minspan:
        raise ValueError("maxspan <= minspan")
    if stepsize < 1:
        raise ValueError("stepsize < 1")
    if current_timespan < 12:
        raise NotImplementedError("current_timespan < 12")
        
    # creat message headings
    message_rising = "Coins with rising trend:"
    message_falling = "Coins with falling trend:"
    message_deviating_upwards = "Coins currently deviating upwards:"
    message_deviating_downwards = "Coins currently deviating downwards:"
    message_high_perc = "Coins in a high percentile for the current month:"
    message_low_perc = "Coins in a low percentile for the current month:"
    message_2_3_buying = "Coins with 2 out of 3 buying indicators:\n"
    message_2_3_selling = "Coins with 2 out of 3 selling indicators:\n"
    message_detailed = "Detailed info about coins:"
    coin_statistics = {}
    
    # iterate over all coins on Kraken and Yahoo Finance
    for coin_name in cs.KRAKEN_COINS_YF:
        # get historical data
        data = yf.Ticker(coin_name + "-EUR")
        history = data.history(period=period, interval=interval)
        prices = np.array(history["Close"][-total_timespan:], dtype=np.float64)
        if prices.shape[0] == 0:
            raise RuntimeError("Could not get historical data for "+coin_name)
        timepoints = pa.get_unitless_timepoints(prices)
    
        # calculate price statistics
        stats = pa.summarize_price_statistics(timepoints=timepoints, prices=prices,
                                              interval=interval, minspan=minspan,
                                              maxspan=maxspan, stepsize=stepsize,
                                              current_timespan=current_timespan)
        coin_statistics[coin_name] = stats
        
        # add coins to message that are currently rising
        if stats["current change"] > 0.12:
            message_rising += f"\n{coin_name}: {stats['current change']}"
        
        # add coins to message that are currently falling
        if stats["current change"] < -0.12:
            message_falling += f"\n{coin_name}: {stats['current change']}"
        
        # add coins to message that are deviating upwards
        if stats["current deviation"] > 0.4:
            message_deviating_upwards += f"\n{coin_name}: {stats['current deviation']}"
        
        # add coins to message that are deviating downwards
        if stats["current deviation"] < -0.4:
            message_deviating_downwards += f"\n{coin_name}: {stats['current deviation']}"
        
        # add coins to message that are currently in high percentile
        if stats["current month percentile"] > 95:
            message_high_perc += f"\n{coin_name}: {stats['current month percentile']}"
        
        # add coins to message that are currently in low percentile
        if stats["current month percentile"] < 35:
            message_low_perc += f"\n{coin_name}: {stats['current month percentile']}"
        
        # add coins that have at least 2 buying indicators:
        indicators = int(stats["current change"] > 0.09) \
                     + int(stats["current deviation"] < -0.3) \
                     + int(stats["current month percentile"] > 95)
        if indicators >= 2:
            message_2_3_buying += f"{coin_name}, "
        
        # add coins that have at least 2 selling indicators:
        indicators = int(stats["current change"] < -0.09) \
                     + int(stats["current deviation"] > 0.3) \
                     + int(stats["current month percentile"] < 40)
        if indicators >= 2:
            message_2_3_selling += f"{coin_name}, "
        
        # add coin statistics to message if trend or deviation from trend are strong
        if np.abs(stats["regression coefficients"][0]) > 1.2 \
                or np.abs(stats["current deviation"]) > 0.3:
            message_detailed += f"\n\n{coin_name}: {stats}"
            
            
    entire_message = message_2_3_buying + "\n\n" + message_2_3_selling
#                    message_rising + "\n\n" + message_falling + "\n\n" \
#                     + message_deviating_upwards + "\n\n" \
#                     + message_deviating_downwards + "\n\n" \
#                     + message_high_perc + "\n\n" + message_low_perc
##                     + "\n\n" + message_detailed
                     
    return entire_message
