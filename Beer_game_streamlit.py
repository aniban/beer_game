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

import streamlit as st
# if streamlit is not found in path, run in cmd window as -
# python -m streamlit run Beer_game_streamlit.py

st.title('Supply Chain Simulation')
st.write('To study the impact of a sudden market disruption on supply chain with information lags.')
st.write('Effect of variable Ordering strategies and Inventory norms across the 4 levels:')
st.text('Factory > Distributor > Stockist > Retailer > (customer)')

st.sidebar.title('Demand variables:')
d_value = st.sidebar.slider("Demand spike level (normal demand = 4)", min_value=4, max_value=12,value=8, step=2)
d_weeks = st.sidebar.slider("Duration of disruption (in weeks)", min_value=0, max_value=8,value=3)

st.sidebar.title('Operations variables:')
ops = st.sidebar.selectbox("Ordering strategy",['new order received this week',
                                                'new order received + backlog',
                                                'new order + backlog + inv. adjust',
                                                'new order + inventory adjustment'], index=1)
t_inv_wks = st.sidebar.slider("Target inventory norm in weeks", min_value=1, max_value=8,value=3)

st.sidebar.title('Network variables:')
O_DEL = st.sidebar.radio("Order lead time (in weeks)", [0,1,2,3,4], index=2, horizontal=True)
S_DEL = st.sidebar.radio("Delivery lead time (in weeks)", [0,1,2,3,4], index=2, horizontal=True)
M_DEL = st.sidebar.radio("Manufacturing lead time (in weeks)", [0,1,2,3,4], index=2, horizontal=True)

def update_inventory(lvl):
    inventory[lvl].append(inventory[lvl][-1] - despatch[lvl][-1] + supply[lvl][-1])
    return

def receive_n_generate_orders(lvl):
    if lvl == 3:
        order_received = mkt_demand[-1]   #recent market demand(n)
    else:
        order_received = order[lvl+1][-1-O_DEL] #delayed downstream order(n-2)
    
    if ops == 'new order received this week':
        order[lvl].append(order_received)
    elif ops == 'new order received + backlog':
        order[lvl].append(order_received+backlog[lvl][-1]) # downstream order received + last backlog(n-1)
    elif ops == 'new order + inventory adjustment':
        order[lvl].append(max(order_received-inventory[lvl][-1]+inv_norm,0)) # with inventory correction
    else:
        order[lvl].append(max(order_received+backlog[lvl][-1]-inventory[lvl][-1]+inv_norm,0)) 
    return

def calculate_backlog_n_despatch(lvl):
    if lvl == 3:
        demand = mkt_demand[-1]+backlog[lvl][-1]
    else:
        demand = order[lvl+1][-1-O_DEL]+backlog[lvl][-1]

    if inventory[lvl][-1]< demand:
        backlog[lvl].append(demand-inventory[lvl][-1])
        despatch[lvl].append(inventory[lvl][-1])
    else:
        backlog[lvl].append(0)
        despatch[lvl].append(demand)
    return

def receive_supply(lvl):
    if lvl == 0: # factory
        supply[0].append(order[0][-1-M_DEL])              # Mfg. lead time, order assumed fully fulfilled to despatch
    else:
        supply[lvl].append(despatch[lvl-1][-1-S_DEL])     # Despatch/transport delay
    return

# First 4 weeks of data:
mkt_demand = [4,4,4,4]
order = [[4,4,4,4],[4,4,4,4],[4,4,4,4],[4,4,4,4]]
despatch = [[4,4,4,4],[4,4,4,4],[4,4,4,4],[4,4,4,4]]
backlog = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
supply = [[4,4,4,4],[4,4,4,4],[4,4,4,4],[4,4,4,4]]
inv_norm = 4*t_inv_wks
inventory = [[inv_norm,inv_norm,inv_norm,inv_norm],[inv_norm,inv_norm,inv_norm,inv_norm],
             [inv_norm,inv_norm,inv_norm,inv_norm],[inv_norm,inv_norm,inv_norm,inv_norm]]

# Weekly simulation starting week 5
weekly_demand = [d_value]*d_weeks + [4]*(46-d_weeks)      # weekly market demand from week 5 to 50

for new_demand in weekly_demand:
    mkt_demand.append(new_demand)
    for lvl in range(3,-1,-1):
        update_inventory(lvl)
        receive_n_generate_orders(lvl)
    for lvl in range(3,-1,-1):
        calculate_backlog_n_despatch(lvl)
        receive_supply(lvl)


import matplotlib.pyplot as plt

# Define the list of weeks and axes
weeks = list(range(len(mkt_demand)))
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

for lvl in range(4):
    lvl_name = ('Factory', 'Distributor', 'Stockist', 'Retailer')[lvl]
    # Plot each list as a line graph
    axs[1-lvl//2, 1-lvl%2].plot(weeks, order[lvl], label='Order')
    axs[1-lvl//2, 1-lvl%2].plot(weeks, supply[lvl], label='Supply')
    axs[1-lvl//2, 1-lvl%2].plot(weeks, inventory[lvl], label='Inventory')
    axs[1-lvl//2, 1-lvl%2].plot(weeks, backlog[lvl], label='Backlog')
    axs[1-lvl//2, 1-lvl%2].set_title('Results for '+lvl_name)

# Add labels and legend
fig.suptitle('Operational variables across levels')
for ax in axs.flat:
    ax.set(xlabel='Week' , ylabel = 'Quantity')
    ax.legend()

fig2, ax2 = plt.subplots(1,1,figsize=(10,3))
total_inventory = []
for lvl in range(4):
    total_inventory.append(sum(inventory[lvl]))
    lvl_name = ('Factory', 'Distributor', 'Stockist', 'Retailer')[lvl]
    ax2.plot(weeks, [x/4 for x in inventory[lvl]], label=lvl_name)
ax2.set(xlabel='Week' , ylabel = 'Inventory (in weeks)')
ax2.legend()

st.subheader('Inventory levels maintained (in weeks of demand)')
st.pyplot(fig2)

st.write('Average weekly inventory level maintained across network is', str(int(sum(total_inventory)/50)),'units.')
inv_str = ''
for lvl in range(4):
    lvl_name = ('Factory', 'Distributor', 'Stockist', 'Retailer')[lvl]
    inv_str = inv_str +'<'+ lvl_name+' : '+ str(total_inventory[lvl]/50)+'units.>'
st.write(inv_str)
st.divider()
st.pyplot(fig)


