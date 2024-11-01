class Position:
    def __init__(self, trade_id, poston_qty=0, symbol=None):
        self.trade_id = trade_id  # Unique identifier for the trade
        self.poston_qty = poston_qty  # Current quantity in the position
        self.symbol = symbol  # Symbol for the position
        self.orders = []  # List to track added orders
        self.settled_orders = []  # List to track settled orders

    def add_order(self, order):
        """Add an order to this position if the trade_id matches and the order status is 'executed'."""
        if self.can_add_order(order) and order.status == 'executed':
            print(f"Order can be added to the position: {order}")
            
            # Check for countering before adding the order
            self.counter_position(order)
            
            # If the order is not settled, update the position
            if order.status != 'settled':
                self.update_position(order.executed_qty)
            
            self.orders.append(order)  # Track the added order
            
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
        # First, try to find an order with the same quantity to counter
        for existing_order in self.orders:
            if (existing_order.order_type == 'entry' and existing_order.order_side == 'buy' and 
                existing_order.status == 'executed' and 
                existing_order.executed_qty == new_order.executed_qty and
                new_order.order_type == 'exit' and new_order.order_side == 'sell'):
                
                # Fully counter the entry order
                self.poston_qty -= existing_order.executed_qty
                existing_order.status = 'settled'  # Mark the entry order as settled
                self.settled_orders.append(existing_order.__dict__)  # Move to settled orders
                new_order.status = 'settled'  # Mark the new order as settled
                self.settled_orders.append(new_order.__dict__)  # Move to settled orders
                print(f"Countered entry order: {existing_order} with new order: {new_order}")
                return  # Exit after countering

            elif (existing_order.order_type == 'exit' and existing_order.order_side == 'sell' and 
                  existing_order.status == 'executed' and 
                  existing_order.executed_qty == new_order.executed_qty and
                  new_order.order_type == 'entry' and new_order.order_side == 'buy'):
                
                # Fully counter the exit order
                self.poston_qty -= existing_order.executed_qty
                existing_order.status = 'settled'  # Mark the exit order as settled
                self.settled_orders.append(existing_order.__dict__)  # Move to settled orders
                new_order.status = 'settled'  # Mark the new order as settled
                self.settled_orders.append(new_order.__dict__)  # Move to settled orders
                print(f"Countered exit order: {existing_order} with new order: {new_order}")
                return  # Exit after countering

        # If no matching order is found, counter with the first available order
        for existing_order in self.orders:
            if (existing_order.order_type == 'entry' and existing_order.order_side == 'buy' and 
                existing_order.status == 'executed' and
                new_order.order_type == 'exit' and new_order.order_side == 'sell'):
                
                # Partially counter the entry order
                if existing_order.executed_qty >= new_order.executed_qty:
                    self.poston_qty -= new_order.executed_qty
                    existing_order.executed_qty -= new_order.executed_qty
                    new_order.status = 'settled'  # Mark the new order as settled
                    self.settled_orders.append(new_order.__dict__)  # Move to settled orders
                    if existing_order.executed_qty == 0:
                        existing_order.status = 'settled'  # Mark the entry order as settled
                        self.settled_orders.append(existing_order.__dict__)  # Move to settled orders
                    print(f"Partially countered entry order: {existing_order} with new order: {new_order}")
                    return  # Exit after countering

            elif (existing_order.order_type == 'exit' and existing_order.order_side == 'sell' and 
                  existing_order.status == 'executed' and
                  new_order.order_type == 'entry' and new_order.order_side == 'buy'):
                
                # Partially counter the exit order
                if existing_order.executed_qty >= new_order.executed_qty:
                    self.poston_qty -= new_order.executed_qty
                    existing_order.executed_qty -= new_order.executed_qty
                    new_order.status = 'settled'  # Mark the new order as settled
                    self.settled_orders.append(new_order.__dict__)  # Move to settled orders
                    if existing_order.executed_qty == 0:
                        existing_order.status = 'settled'  # Mark the exit order as settled
                        self.settled_orders.append(existing_order.__dict__)  # Move to settled orders
                    print(f"Partially countered exit order: {existing_order} with new order: {new_order}")
                    return  # Exit after countering

        # If no matching order is found
        print("No matching order found to counter.")

    def __str__(self):
        return (f"Position - Trade ID: {self.trade_id}, "
                f"Poston Qty: {self.poston_qty}, "
                f"Symbol: {self.symbol}, "
                f"Orders: {len(self.orders)}, "
                f"Settled Orders: {len(self.settled_orders)}")


class Order:
    def __init__(self, trade_id, pending_qty, executed_qty, status, order_type, order_side, symbol):
        self.trade_id = trade_id  # Unique identifier for the trade
        self.pending_qty = pending_qty  # Quantity still pending
        self.executed_qty = executed_qty  # Quantity that has been executed
        self.status = status  # Status of the order (e.g., executed, pending, settled, failed)
        self.order_type = order_type  # Type of order (e.g., entry, exit)
        self.order_side = order_side  # Side of the order (e.g., buy, sell)
        self.symbol = symbol  # Symbol for the order

    def __str__(self):
        return (f"Order - Trade ID: {self.trade_id}, "
                f"Pending Qty: {self.pending_qty}, "
                f"Executed Qty: {self.executed_qty}, "
                f"Status: {self.status}, "
                f"Type: {self.order_type}, "
                f"Order Side: {self.order_side}, "
                f"Symbol: {self.symbol}")
