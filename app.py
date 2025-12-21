import yfinance as yf
import json


def stringify_keys(d):
    return {str(k): v for k, v in d.items()}


def ok(response_data):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_data)
    }


def bad_request(response_data):
    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_data)
    }


def handler(event, context):
    print(f"Full event: {json.dumps(event)}")
    
    if "body" in event and event["body"]:
        body_data = json.loads(event["body"])

        statement_type = body_data.get("statement")
        ticker = body_data.get("ticker")

        print(f"Processing {statement_type} for {ticker}")

    if not ticker:
        return bad_request({"message": "No ticker provided"})
    elif not statement_type:
        return bad_request({"message": "No statement type provided"})

    stock = yf.Ticker(ticker)

    if statement_type == "balance_sheet":
        last_quarter_date, last_quarter_data = next(iter(stock.get_balance_sheet(
            as_dict=True, pretty=True, freq="quarterly").items()), (None, None))
        balance_sheet_data = stock.get_balance_sheet(as_dict=True, pretty=True)

        response = {
            "data": stringify_keys(balance_sheet_data),
            "lastQuarter": {"date": str(last_quarter_date), "data": last_quarter_data}
        }

        return ok(response)
    elif statement_type == "cash_flow":
        last_quarter_date, last_quarter_data = next(iter(stock.get_cash_flow(
            as_dict=True, pretty=True, freq="quarterly").items()), (None, None))
        cash_flow_statement_data = stock.get_cash_flow(
            as_dict=True, pretty=True)

        response = {
            "data": stringify_keys(cash_flow_statement_data),
            "lastQuarter": {"date": str(last_quarter_date), "data": last_quarter_data}
        }

        return ok(response)
    elif statement_type == "income_statement":
        last_quarter_date, last_quarter_data = next(iter(stock.get_income_stmt(
            as_dict=True, freq="quarterly", pretty=True).items()), (None, None))
        income_statement_data = stock.get_income_stmt(
            as_dict=True, pretty=True)

        response = {
            "data": stringify_keys(income_statement_data),
            "lastQuarter": {"date": str(last_quarter_date), "data": last_quarter_data}
        }

        return ok(response)

    return bad_request({"message": "Incorrect statement type was passed."})
