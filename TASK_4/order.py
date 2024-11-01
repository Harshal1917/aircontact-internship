class Position:
    def __init__(self, trade_id, poston_qty=0, symbol=None):
        self.trade_id = trade_id  # Unique identifier for the trade
        self.poston_qty = poston_qty  # Current quantity in the position
        self.symbol = symbol  # Symbol for the position
        self.orders = {'entry': [], 'exit': []}  # Dictionary to track added orders: {'entry': entry queue, 'exit': exit queue}
        self.settled_orders = {'entry': [], 'exit': []}  # Dictionary to track settled orders: {'entry': entry queue, 'exit': exit queue}

    def add_order(self, order):
        """Add an order to this position if the trade_id matches."""
        if self.can_add_order(order):
            print(f"Order can be added to the position: {order}")
            
            # Check for countering before adding the order
            self.counter_position(order)
            
            # If the order is not settled, update the position
            if order.status != 'settled':
                self.update_position(order.executed_qty)
            
            # Track the added order in the appropriate queue
            if order.order_type == 'entry':
                self.orders['entry'].append(order)
            elif order.order_type == 'exit':
                self.orders['exit'].append(order)
            
            # Set the symbol if it's not already set
            if self.symbol is None:
                self.symbol = order.symbol
        else:
            print(f"Order cannot be added to the position: {order}")

    def can_add_order(self, order):
        """Check if the order can be added to this position based on trade_id and symbol."""
        return self.trade_id == order.trade_id and (self.symbol == order.symbol or self.symbol is None)

    def update_position(self, executed_qty):
        """Update the position quantity based on the executed order quantity."""
        self.poston_qty += executed_qty

    def counter_position(self, new_order):
        """Counter the position quantity based on the new order quantity."""
        if new_order.order_type == 'entry' and new_order.order_side == 'buy':
            queue = self.orders['exit']
            settled_queue = self.settled_orders['exit']
        elif new_order.order_type == 'exit' and new_order.order_side == 'sell':
            queue = self.orders['entry']
            settled_queue = self.settled_orders['entry']
        else:
            print("Invalid order type or side.")
            return

        for existing_order in queue:
            if existing_order.status == 'executed':
                # Counter the order regardless of executed quantity
                counter_qty = min(existing_order.executed_qty, new_order.executed_qty)
                self.poston_qty -= counter_qty
                existing_order.settled_qty += counter_qty
                new_order.settled_qty += counter_qty
                existing_order.executed_qty -= counter_qty
                new_order.executed_qty -= counter_qty

                if existing_order.executed_qty == 0:
                    existing_order.status = 'settled'  # Mark the existing order as settled
                    settled_queue.append(existing_order.__dict__)  # Move to settled orders
                if new_order.executed_qty == 0:
                    new_order.status = 'settled'  # Mark the new order as settled
                    settled_queue.append(new_order.__dict__)  # Move to settled orders

                print(f"Countered order: {existing_order} with new order: {new_order}")
                if new_order.status == 'settled':
                    return  # Exit after countering

        # If no matching order is found
        print("No matching order found to counter.")

    def __str__(self):
        return (f"Position - Trade ID: {self.trade_id}, "
                f"Poston Qty: {self.poston_qty}, "
                f"Symbol: {self.symbol}, "
                f"Orders: {len(self.orders['entry']) + len(self.orders['exit'])}, "
                f"Settled Orders: {len(self.settled_orders['entry']) + len(self.settled_orders['exit'])}")


class Order:
    def __init__(self, trade_id, pending_qty, executed_qty, status, order_type, order_side, symbol):
        self.trade_id = trade_id  # Unique identifier for the trade
        self.pending_qty = pending_qty  # Quantity still pending
        self.executed_qty = executed_qty  # Quantity that has been executed
        self.status = status  # Status of the order (e.g., executed, pending, settled, failed)
        self.order_type = order_type  # Type of order (e.g., entry, exit)
        self.order_side = order_side  # Side of the order (e.g., buy, sell)
        self.symbol = symbol  # Symbol for the order
        self.settled_qty = 0  # Quantity that has been settled

    def __str__(self):
        return (f"Order - Trade ID: {self.trade_id}, "
                f"Pending Qty: {self.pending_qty}, "
                f"Executed Qty: {self.executed_qty}, "
                f"Settled Qty: {self.settled_qty}, "
                f"Status: {self.status}, "
                f"Type: {self.order_type}, "
                f"Order Side: {self.order_side}, "
                f"Symbol: {self.symbol}")


# Example Usage

# Create a Position instance
position = Position(trade_id=111)

# Create Order instances
order1 = Order(trade_id=111, pending_qty=0, executed_qty=15, 
               status='executed', order_type='entry', order_side='buy', symbol='TCS')
order3 = Order(trade_id=111, pending_qty=0, executed_qty=5, 
               status='executed', order_type='exit', order_side='sell', symbol='TCS')
order4 = Order(trade_id=111, pending_qty=0, executed_qty=85, 
               status='executed', order_type='exit', order_side='sell', symbol='TCS')
order2 = Order(trade_id=111, pending_qty=0, executed_qty=25, 
               status='executed', order_type='entry', order_side='buy', symbol='TCS')
order5 = Order(trade_id=111, pending_qty=0, executed_qty=5, 
               status='executed', order_type='entry', order_side='buy', symbol='TCS')

# Print the initial state
print(position)

# Add the executed orders to the position
position.add_order(order1)
position.add_order(order3)  # This will check for countering first
position.add_order(order4)  # This will also check for countering first
position.add_order(order2)
position.add_order(order5)  # This will also check for countering first
# Print the updated position and order statuses
print(position)
print(order1)
print(order3)
print(order4)
print(order2)
print(order5)
print("Settled Orders:", position.settled_orders)
