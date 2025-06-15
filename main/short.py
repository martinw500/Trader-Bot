import numpy as np

class ShortSpikeReversalStrategy:
    def __init__(self, window=20, spike_threshold=2.5, trailing_stop=0.5):
        """
        window: lookback period for volatility calculation
        spike_threshold: how many std deviations above mean to trigger short
        trailing_stop: percent trailing stop-loss
        """
        self.window = window
        self.spike_threshold = spike_threshold
        self.trailing_stop = trailing_stop
        self.position = None
        self.entry_price = None
        self.highest_price = None

    def should_short(self, prices):
        if len(prices) < self.window + 1:
            return False
        recent = prices[-self.window-1:-1]
        mean = np.mean(recent)
        std = np.std(recent)
        last = prices[-1]
        # Short if price spikes above mean by threshold
        return last > mean + self.spike_threshold * std

    def update_trailing_stop(self, price):
        if self.highest_price is None or price > self.highest_price:
            self.highest_price = price
        stop_price = self.entry_price * (1 + self.trailing_stop / 100)
        # For shorts, stop-loss moves down as price falls
        trailing_stop_price = self.highest_price * (1 + self.trailing_stop / 100)
        return min(stop_price, trailing_stop_price)

    def on_new_price(self, prices):
        price = prices[-1]
        signal = None
        if self.position is None:
            if self.should_short(prices):
                self.position = 'short'
                self.entry_price = price
                self.highest_price = price
                signal = 'enter_short'
        else:
            stop = self.update_trailing_stop(price)
            if price >= stop:
                # Exit short position
                self.position = None
                self.entry_price = None
                self.highest_price = None
                signal = 'exit_short'
        return signal

# Example usage:
# prices = [...]  # list of historical prices
# strategy = ShortSpikeReversalStrategy()
# for i in range(len(prices)):
#     signal = strategy.on_new_price(prices[:i+1])
#     if signal == 'enter_short':
#         print(f"Short at {prices[i]}")
#     elif signal == 'exit_short':
#         print(f"Cover at {prices[i]}")
