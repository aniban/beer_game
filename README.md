# beer_game
Supply chain simulation for disruptions
This is based on Jay Forrester's classic simulation exercise at MIT that continues to be the classic demonstration of the "Bullwhip Effect" of disruptions on a supply chain with information delays.
The simulation is built on python3 with streamlit as interface. 


#To find the optimal ordering strategy for supply chain of 4 levels : Factory > Distributor > Stockist > Retailer >
#When unable to despatch orders received - backlog/stock-out. Maintain optimal inventory, and Order stock to avoid backlog
#Week by week simulation of planning / ordering - Order and Supply has travel delays of 2 weeks between levels both ways*
#Retailer receives market order/despatches immediate. Factory orders take 2 weeks to manufacture (receive supply)

#Start of week (n) - Inventory(n) is calculated = Inventory(n-1) - Despatch(n-1) + Supply(n-1)
#Start of week (n) - Order(n) is placed to upstream element, with 2 week delay - VARIABLE STRATEGIES
#By end of week (n) - Despatch(n) quantity is sent out = min(Downstream_Order(n-2)+Backlog(n-1), Inventory(n))
#By end of week (n) - Backlog(n) created if Despatch shipment(n) < order just received + last week's backlog
#By end of week (n) - Supply(n) is received = Upstream_Despatch(n-2) <in case of factory, = Factory_Order(n-2)>

# Variables in use : inventory, order (placed), despatch, backlog, supply (received) 
# across as matrix of [lvl][n] where n is current week and lvl is supply chain level
