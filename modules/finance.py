__author__ = 'Djidiouf'

# Python built-in modules
##

# Third-party modules
import googlefinance.client

# Project modules
import modules.connection


def convert_to_notation(i_number):
    result = i_number

    if i_number <= 1:
        result = "1D"
    elif i_number <= 31:
        result = "1M"
    elif i_number > 31:
        nb_month_per_year = 30.41666667
        nb_month = i_number / nb_month_per_year
        result = str(int(nb_month) + 1) + "M"

    return result


def main(i_string, i_medium, i_alias=None):

    # !finance NASDAQ:TSLA
    # !finance NASDAQ:TSLA 1Y

    tuple_string = i_string.partition(' ')
    exchange_stock = tuple_string[0].upper()
    period = tuple_string[2] # 1D, xM, xY, 365, 3, 65

    if period == "":
        period = "1D"

    try:
        period = convert_to_notation(int(period))
    except ValueError:
        period = period.upper()

    tuple_string = exchange_stock.partition(':')
    exchange = tuple_string[0]  # "NASDAQ"
    stock = tuple_string[2]  # "TSLA"

    param = {
        'q': stock, # Stock symbol (ex: "AAPL")
        'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
        'x': exchange, # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': period # Period (Ex: "1Y" = 1 year)
    }

    # get price data (return pandas dataframe)
    df = googlefinance.client.get_price_data(param)

    #print(df.tail(3).to_string(header=False)) # Display dataframe without header

    if period == "1D":
        df_express = df  # or df.head(1)
    else:
        df_express = df.iloc[[0, -1]]  #retrieve first and last line only

    displayed_df_express = str(df_express).splitlines()  # Set the dataframe as a string and split into lines when /n or /r is seen

    # Display rates
    for line in displayed_df_express:
        if line == "Empty DataFrame":
            modules.connection.send_message("ERROR: This code is not recognised.", i_medium, i_alias)
            return
        elif line.startswith(" "):
            line = line.replace("  ", "   ")  # try to make it prettier
        modules.connection.send_message(line, i_medium, i_alias)

    # Display difference
    if period != "1D":
        # Get close values of the extreme points
        value_first_close = df_express.iloc[0, 3]  # [line, column)
        value_last_close = df_express.iloc[1, 3]  # [line, column)

        diff_value = value_last_close - value_first_close
        diff_percent = (diff_value / value_first_close) * 100

        sign = ""
        if diff_value >= 0:
            sign = "+"
        modules.connection.send_message("Difference on close rates: %s%.2f (%s%.2f%%)" % (sign, diff_value, sign, diff_percent), i_medium, i_alias)
