import yfinance as yf

def handler(event, context):
    ticker = event.get("ticker")
    statement_type = event.get("statement")
    
    if not ticker:
        return {"message": "No ticket provided"}
    
    stock = yf.Ticker(ticker)
    
    def stringify_keys(d):
        return {str(k): v for k, v in d.items()}
    
    if statement_type == "balance_sheet":
        last_quarter_date, last_quarter_data = next(iter(stock.get_balance_sheet(as_dict=True, pretty=True, freq="quarterly").items()), (None, None))
        balance_sheet_data = stock.get_balance_sheet(as_dict=True, pretty=True)

        return {
            "data": stringify_keys(balance_sheet_data),
            "lastQuarter": {"date": str(last_quarter_date), "data": last_quarter_data}
        }
    elif statement_type == "cash_flow":
        last_quarter_date, last_quarter_data = next(iter(stock.get_cash_flow(as_dict=True, pretty=True, freq="quarterly").items()), (None, None))
        cash_flow_statement_data = stock.get_cash_flow(as_dict=True, pretty=True)
        
        return {
            "data": stringify_keys(cash_flow_statement_data),
            "lastQuarter": {"date": str(last_quarter_date), "data": last_quarter_data}
        }
    elif statement_type == "income_statement":
        last_quarter_date, last_quarter_data = next(iter(stock.get_income_stmt(as_dict=True, freq="quarterly", pretty=True).items(), (None, None)))
        income_statement_data = stock.get_income_stmt(as_dict=True, pretty=True)

        return {
            "data": stringify_keys(income_statement_data),
            "lastQuarter": {"date": str(last_quarter_date), "data": last_quarter_data}
        }
    
    return {
        "message": "Incorrect statement type was passed."
    }
