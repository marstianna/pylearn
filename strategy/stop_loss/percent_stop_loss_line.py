
# action == 1 means buy else means sell
def percent_stop_loss_line_strategy(buy_price ,stop_loss_percent, action):
    k = 1 + stop_loss_percent if action == 1 else 1 - stop_loss_percent
    return buy_price * k
