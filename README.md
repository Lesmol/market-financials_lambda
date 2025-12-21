# 📈 Market Financials Lambda

This repository contains a containerized AWS Lambda function that retrieves financial data using the `yfinance` library. It is designed to be deployed to Amazon ECR and run as a Lambda function in the `af-south-1` region.

## ✨ Features

* 📊 **Comprehensive Financial Statements**: Fetches Balance Sheets, Cash Flow Statements, and Income Statements.
* 📅 **Historical & Recent Data**: Returns both full historical data and specific data for the most recent quarter.
* 🐍 **Modern Stack**: Built using Python 3.14.
* 🚀 **Automated Deployment**: Fully automated CI/CD pipeline via GitHub Actions.

## 🔌 API Specification

The function handles POST requests with a JSON body to retrieve specific financial data.

### 📥 Request Body

| Field | Type | Description |
| :--- | :--- | :--- |
| `ticker` | String | The stock symbol (e.g., "AAPL"). |
| `statement` | String | Type of statement: `balance_sheet`, `cash_flow`, or `income_statement`. |

#### Example Request
```json
{
    "ticker": "TSLA",
    "statement": "income_statement"
}
```

### 📤 Responses

* **200 OK ✅**: Returns a JSON object containing the requested financial data.
* **400 Bad Request ❌**: Returned if a ticker is missing, the statement type is missing, or an invalid statement type is provided.

## 🔄 CI/CD Workflow

The project uses GitHub Actions for deployment, triggered manually via `workflow_dispatch` on the `develop` branch:

1.  **🛠 Build**: Checks out the code, logs into Amazon ECR, builds the Docker image, and pushes it with both `:latest` and `:short-sha` tags.
2.  **☁️ Deploy**: Configures AWS credentials and updates the Lambda function code to use the newly pushed image URI.

## 💻 Local Development

To build the image locally for testing, run the following command:

```bash
docker build -t market-financials-lambda .
