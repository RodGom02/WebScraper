import yfinance as yf
import time
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread


def get_stock_price(ticker):
    """
    Fetch the stock data for the given ticker through yfinance.
    """
    stock = yf.Ticker(ticker)
    price = stock.history(period="1d")["Close"].iloc[-1]
    return price


def track_stock_price(ticker, interval=5):
    """
    Track the stock price at regular intervals.
    """
    while True:
        try:
            price = get_stock_price(ticker)
            print(f"The current price of {ticker} is: ${price:.2f}")
        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(interval)


def plot_real_time_prices(ticker, duration=60, interval=5):
    """
    Plot real-time stock prices for a specified duration and update interval.
    """
    times = []
    prices = []

    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()

    start_time = time.time()
    while time.time() - start_time < duration:
        if not plt.fignum_exists(fig.number):
            print("Plot closed by user.")
            break

        try:
            price = get_stock_price(ticker)
            current_time = time.strftime("%H:%M:%S")

            # Update data
            times.append(current_time)
            prices.append(price)

            # Clear and replot
            ax.clear()
            ax.plot(times, prices, label=ticker, color="blue", marker="o")
            ax.set_title(f"Real-Time Stock Price of {ticker}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Price (USD)")
            ax.legend()

            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.pause(interval)
        except Exception as e:
            print(f"Error fetching data: {e}")
            break

    plt.ioff()
    plt.show()


def update_price_label(label, ticker):
    """
    Update the price label in the Tkinter GUI with live stock prices.
    """
    while True:
        try:
            price = get_stock_price(ticker)
            label.config(text=f"The current price of {ticker} is ${price:.2f}")
        except Exception as e:
            label.config(text=f"Error: {e}")
        time.sleep(5)


def start_tracker():
    """
    Start the real-time stock tracker from the Tkinter interface.
    """
    ticker = ticker_entry.get()
    if not ticker:
        error_label.config(text="Please enter a valid stock ticker!")
        return
    error_label.config(text="")  # Clear any previous error messages
    Thread(target=update_price_label, args=(price_label, ticker), daemon=True).start()


def plot_stock_prices():
    """
    Embed a live stock price plot into the Tkinter application.
    """
    ticker = ticker_entry.get()
    if not ticker:
        error_label.config(text="Please enter a valid stock ticker!")
        return
    error_label.config(text="")  # Clear any previous error messages
# Schedule the plotting function to run on the main thread
    root.after(0, lambda: plot_real_time_prices(ticker, duration=60, interval=5))

# Tkinter GUI Setup
root = tk.Tk()
root.title("Real-Time Stock Tracker")

# Input for stock ticker
tk.Label(root, text="Enter Stock Ticker:").pack()
ticker_entry = tk.Entry(root)
ticker_entry.pack()

# Error label for invalid input
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Buttons for tracking and plotting
tk.Button(root, text="Track Stock", command=start_tracker).pack()
tk.Button(root, text="Plot Prices", command=plot_stock_prices).pack()

# Label to display the current stock price
price_label = tk.Label(root, text="", font=("Arial", 16))
price_label.pack()

root.mainloop()