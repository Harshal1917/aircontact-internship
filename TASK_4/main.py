from order import Position,Order

def main():
    # Create a Position instance
    position = Position(trade_id=111)

    # Create Order instances
    order1 = Order(trade_id=111, pending_qty=0, executed_qty=15, 
                   status='executed', order_type='entry', order_side='buy', symbol='TCS')
    order2 = Order(trade_id=111, pending_qty=0, executed_qty=5, 
                   status='executed', order_type='entry', order_side='buy', symbol='TCS')
    order3 = Order(trade_id=111, pending_qty=0, executed_qty=5, 
                   status='executed', order_type='exit', order_side='sell', symbol='TCS')
    # order4 = Order(trade_id=111, pending_qty=0, executed_qty=5, 
    #                status='executed', order_type='entry', order_side='buy', symbol='TCS')
    # order5 = Order(trade_id=111, pending_qty=0, executed_qty=5, 
    #                status='pending', order_type='entry', order_side='buy', symbol='TCS')
    # Print the initial state
    print(position)

    # Add the executed orders to the position
    position.add_order(order1)
    position.add_order(order3)  # This will check for countering first
    position.add_order(order2)
    # position.add_order(order4)  # This will also check for countering first
    # position.add_order(order5)

    # Print the updated position and order statuses
    print(position)
    print(order1)
    print(order2)
    print(order3)
    # print(order4)
    # print(order5)
    print("Settled Orders:", position.settled_orders)

if __name__ == "__main__":
    main()

