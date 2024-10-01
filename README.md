# Scalable-Cloud-API-for-Trading-Analysis
Cloud-Native API for Scalable Trading Strategy Risk and Profitability Analysis: A Multi-Cloud Approach with GAE and AWS Integration.

## Project Overview
This project focuses on developing a cloud-native API that leverages multiple cloud services to assess the risk and profitability of various trading strategies. The API integrates trading signals and Monte Carlo methods to offer insights into risk assessments and profitability metrics.

## Objective
The primary goal is to demonstrate the ability to effectively design and explain a cloud-native API, utilizing services from multiple cloud providers with scalable architecture. This API enables the evaluation of trading strategies by analyzing financial time series data.

## Key Features
- **Warm-up and Scalability**: Setup and scale cloud services for parallelized analysis.
- **Risk Assessment**: Conduct risk assessments using Monte Carlo simulations based on trading signals.
- **Profit/Loss Calculation**: Compute profit or loss after a set period following the trading signal.
- **Auditing and Reporting**: Maintain audit logs of all analyses and provide URLs for risk visualization.

## API Endpoints

1. **/warmup**
   - **Description**: Initializes the system with the specified scale for analysis. The ‘/warmup’ endpoint calls the ‘MonteCarloSimulation1’ Lambda function via HTTPS, passing the ‘is_warmup’ payload to warm up the appropriate number of Lambda functions defined by the scale.
   - **Method**: POST
   - **Inputs**: `{ "s": "lambda", "r": 3 }`
   - **Outputs**: `{ "result": "ok" }`

2. **/scaled_ready**
   - **Description**: Verifies if the system is scaled and ready for analysis.
   - **Method**: GET
   - **Outputs**: `{ "warm": true }` or `{ "warm": false }`

3. **/get_warmup_cost**
   - **Description**: Returns the cost and time estimates for the warm-up process.
   - **Method**: GET
   - **Outputs**: `{ "billable_time": 120.05, "cost": 2.97 }`

4. **/get_endpoints**
   - **Description**: Fetches the unique API endpoint URLs made available after warm-up.
   - **Method**: GET
   - **Outputs**: `{ "endpoint": "http://..." }`

5. **/analyse**
   - **Description**: Executes the risk analysis.
   - **Method**: POST
   - **Inputs**: `{ "h": 101, "d": 10000, "t": "sell", "p": 7 }`
   - **Outputs**: `{ "result": "ok" }`

6. **/get_sig_vars9599**
   - **Description**: Retrieves 95% and 99% Value at Risk (VaR) for each trading signal.
   - **Method**: GET
   - **Outputs**: `{ "var95": [0.3545, ...], "var99": [0.3657, ...] }`

7. **/get_avg_vars9599**
   - **Description**: Fetches the average risk values for all signals at 95% and 99% VaR.
   - **Method**: GET
   - **Outputs**: `{ "var95": 0.3545, "var99": 0.3657 }`

8. **/get_sig_profit_loss**
   - **Description**: Retrieves profit or loss figures for each trading signal.
   - **Method**: GET
   - **Outputs**: `{ "profit_loss": [10.2, -8.1, 12.6, ...] }`

9. **/get_tot_profit_loss**
   - **Description**: Returns the overall profit or loss across all signals.
   - **Method**: GET
   - **Outputs**: `{ "profit_loss": 15.55 }`

10. **/get_chart_url**
    - **Description**: The ‘/get_chart_url’ retrieves the link for the risk value chart stored on a temporary file on GAE.
    - **Method**: GET
    - **Outputs**: `{ "url": "http://..." }`

![Risk Chart](https://github.com/user-attachments/assets/ee242b6c-86fc-4484-bd17-4e9743e92d2b)


11. **/get_time_cost**
    - **Description**: Provides the total billable time and cost for the analysis.
    - **Method**: GET
    - **Outputs**: `{ "time": 100.00, "cost": 8.20 }`
   

![billable_times](https://github.com/user-attachments/assets/d3bbe32b-939c-4435-ab41-181f3bd95012)

12. **/get_audit**
    - **Description**: Retrieves the audit log of all previous analysis runs.
    - **Method**: GET
    - **Outputs**: `{ "audit": [...] }`

13. **/reset**
    - **Description**: Resets the current analysis setup.
    - **Method**: GET
    - **Outputs**: `{ "result": "ok" }`

14. **/terminate**
    - **Description**: Terminates the cloud services and scales down to zero.
    - **Method**: GET
    - **Outputs**: `{ "result": "ok" }`

15. **/scaled_terminated**
    - **Description**: Confirms whether the services have been successfully terminated.
    - **Method**: GET
    - **Outputs**: `{ "terminated": true }` or `{ "terminated": false }`
