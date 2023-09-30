# Crawl NSE Website
## Stock Data Analysis with Skip List and Visualization
This project retrieves historical stock data from the National Stock Exchange (NSE) website using Selenium and BeautifulSoup, stores the data in a Skip List data structure, and visualizes the stock prices using Matplotlib. The Skip List allows for efficient data retrieval and intersection of two stocks.

## Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.x installed
Required Python packages installed (Selenium, BeautifulSoup, pandas, numpy, matplotlib)
## Usage
1. Clone this repository to your local machine.

2. Install the required Python packages using pip:

```bash
pip install selenium beautifulsoup4 pandas numpy matplotlib
```
Download the [Chrome WebDriver](https://chromedriver.chromium.org/) and place it in the project directory or update the path to the WebDriver in the code.

Run the Python script by executing the following command:

```bash
python stock_data_analysis.py
```
Enter the stock symbols when prompted (e.g., "TATAPOWER" for Tata Power).

The script will fetch historical stock data from the NSE website, store it in Skip Lists, and display the data.

## Skip List Data Structure
The Skip List is a data structure that efficiently stores and retrieves data in sorted order.
It is implemented using Python classes and methods within the script.
The Skip List is used to store historical stock prices for efficient data intersection.
## Visualization
The script uses Matplotlib to visualize the historical closing prices of the two stocks.
It displays the closing prices over time in two separate graphs.
## Data Intersection
The Skip List allows for efficient intersection of the historical data of two stocks.
The script finds and displays the common dates where both stocks have historical data.
## Contributing
Contributions are welcome! If you have any improvements or suggestions, feel free to open an issue or create a pull request.
