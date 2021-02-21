from bitcoinrpc.authproxy import AuthServiceProxy
from datetime import timedelta
import matplotlib.pyplot as graph
import datetime as dt
import bitcoin
import bitcoinrpc
import matplotlib.animation as animation
import time

def get_server():
    host="blockchain.oss.unist.hr"
    port="8332"
    user="student"
    password="2B4DB3SmsM2B4DB3SmsM89QjgYFp89QjgYFp"
    server = AuthServiceProxy("http://%s:%s@%s:%s"%(user,password,host,port))

    return server

def menu():
    print("\nBlock explorer options:\n"
          "[1] Get block by block hash\n"
          "[2] Get X blocks by block height\n"
          "[3] Height/size graph for last X blocks\n"
          "[4] Custom height/size graph for X blocks\n"
          "[5] Height/number of transactions for last X blocks\n"
          "[6] Custom height/number of transactions graph for X blocks\n"
          "[7] Height/difficulty graph for last X blocks\n"
          "[8] Custom height/difficulty graph for X blocks\n"
          "[9] Height/total fee graph for last X blocks\n"
          "[10] Custom height/total fee graph for X blocks\n"
          "[11] Height/total output graph for last X blocks\n"
          "[12] Custom height/total output graph for X blocks\n"
          "[13] Live current number of tx in mempool\n"
          "[14] Live current usage of mempool\n"
          "[15] Get info about connected node\n"
          "[0] EXIT\n")
    
    choice = int(input("To use desired option choose corresponding number: "))
    print("\n")
    return choice

def menu_choice(choice):
    if choice == 1:
        block_by_hash()
    elif choice == 2:
        block_by_height(True)
    elif choice == 3:
        height_size_graph(False)
    elif choice == 4:
        height_size_graph(True)
    elif choice == 5:
        height_nTx_graph(False)
    elif choice == 6:
        height_nTx_graph(True)
    elif choice == 7:
        height_difficulty_graph(False)
    elif choice == 8:
        height_difficulty_graph(True)
    elif choice == 9:
        height_totalfee_graph(False)
    elif choice == 10:
        height_totalfee_graph(True)
    elif choice == 11:
        height_totalout_graph(False)
    elif choice == 12:
        height_totalout_graph(True)
    elif choice == 13:
        live_node("size")
    elif choice == 14:
        live_node("usage")
    elif choice == 15:
        print_network_info()
    elif choice == 0:
        return False
        
def get_block_by_height(height):
    if height > server.getblockcount() or height < 0:
        print("Block height out of range")
        return
    
    block_hash = server.getblockhash(height)
    block = server.getblock(block_hash)
    return block

def print_block(block):
    for i in block:
        print(i, ":", block[i])

def block_by_hash():
    block_hash = input("Block hash: ")
    block = server.getblock(block_hash)
    print_block(block)

def block_by_height(print_checker):
    blocks = []
    block_count = int(input("How many last blocks: "))
    height = int(input("Please insert ending block height (insert -1 for max block height): "))
    
    if height == -1:
        height = server.getblockcount()
    
    if block_count < 0 or block_count > height:
        print("Invalid block count")
        return
        
    while block_count != 0:
        block = get_block_by_height(height)
        blocks.append(block)
        
        if print_checker == True:
            print_block(block)
        
        height -= 1
        block_count -= 1
    
    return blocks

def block_by_height_custom():
    blocks = []
    block_count = int(input("How many last blocks: "))
    height = int(input("Please insert ending block height (insert -1 for max block height): "))
    previous_height = server.getblockcount()
    
    if height == -1:
        height = server.getblockcount()
    
    if block_count < 0 or block_count > height:
        print("Invalid block count")
        return False
        
    while block_count != 0:
        block = get_block_by_height(height)
        blocks.append(block)
        
        height = int(input("Please insert height for next block: "))
        if height > previous_height:
            print("Invalid height")
            return False
        
        previous_height = height
        block_count -= 1
    
    return blocks

def block_stats_by_height(print_checker):
    blocks = []
    block_count = int(input("How many last blocks: "))
    height = int(input("Please insert ending block height (insert -1 for max block height): "))
    
    if height == -1:
        height = server.getblockcount()
    
    if block_count < 0 or block_count > height:
        print("Invalid block count")
        return
        
    while block_count != 0:
        block = server.getblockstats(height)
        blocks.append(block)
        
        if print_checker == True:
            print_block(block)
        
        height -= 1
        block_count -= 1
    
    return blocks

def block_stats_by_height_custom():
    blocks = []
    block_count = int(input("How many last blocks: "))
    height = int(input("Please insert ending block height (insert -1 for max block height): "))
    previous_height = server.getblockcount()
    
    if height == -1:
        height = server.getblockcount()
    
    if block_count < 0 or block_count > height:
        print("Invalid block count")
        return False
        
    while block_count != 0:
        block = server.getblockstats(height)
        blocks.append(block)
        
        height = int(input("Please insert height for next block: "))
        if height > previous_height:
            print("Invalid height")
            return False
        
        previous_height = height
        block_count -= 1
    
    return blocks

def height_size_graph(custom_graph):
    if custom_graph == True:
        blocks = block_by_height_custom()
    else:
        blocks = block_by_height(False)
    heights = []
    sizes = []
    
    for one_block in blocks:
        for key in one_block:
            if key == "height":
                heights.append(one_block[key])
            elif key == "size":
                sizes.append(one_block[key])

    graph.plot(heights,sizes, 'c',heights,sizes,'gs')
    graph.xlabel("Block height")
    graph.ylabel("Block size")
    graph.title("Block size/height ratio")
    graph.grid(True)
    graph.show()
    
def height_nTx_graph(custom_graph):
    if custom_graph == True:
        blocks = block_by_height_custom()
    else:
        blocks = block_by_height(False)
    heights = []
    num_transactions = []
    
    for one_block in blocks:
        for key in one_block:
            if key == "height":
                heights.append(one_block[key])
            elif key == "nTx":
                num_transactions.append(one_block[key])

    graph.plot(heights,num_transactions, 'r',heights,num_transactions,'ms')
    graph.xlabel("Block height")
    graph.ylabel("Number of transactions")
    graph.title("Block height/number of transactions ratio")
    graph.grid(True)
    graph.show()
    
def height_difficulty_graph(custom_graph):
    if custom_graph == True:
        blocks = block_by_height_custom()
    else:
        blocks = block_by_height(False)
    heights = []
    diffs = []
    
    for one_block in blocks:
        for key in one_block:
            if key == "height":
                heights.append(one_block[key])
            elif key == "difficulty":
                diffs.append(one_block[key])

    graph.plot(heights,diffs, 'y',heights,diffs,'gs')
    graph.xlabel("Block height")
    graph.ylabel("Difficulty")
    graph.title("Block height/difficulty ratio")
    graph.grid(True)
    graph.show()
    
def height_totalfee_graph(custom_graph):
    if custom_graph == True:
        blocks = block_stats_by_height_custom()
    else:
        blocks = block_stats_by_height(False)
    heights = []
    totalfees = []
    
    for one_block in blocks:
        for key in one_block:
            if key == "height":
                heights.append(one_block[key])
            elif key == "totalfee":
                totalfees.append(one_block[key])

    graph.plot(heights,totalfees, 'b',heights,totalfees,'cs')
    graph.xlabel("Block height")
    graph.ylabel("Total fee")
    graph.title("Block height/total fee ratio")
    graph.grid(True)
    graph.show()
    
def height_totalout_graph(custom_graph):
    if custom_graph == True:
        blocks = block_stats_by_height_custom()
    else:
        blocks = block_stats_by_height(False)
    heights = []
    totalfees = []
    
    for one_block in blocks:
        for key in one_block:
            if key == "height":
                heights.append(one_block[key])
            elif key == "total_out":
                totalfees.append(one_block[key])

    graph.plot(heights,totalfees, 'y',heights,totalfees,'cs')
    graph.xlabel("Block height")
    graph.ylabel("Total amount in all outputs")
    graph.title("Block height/total output ratio")
    graph.grid(True)
    graph.show()

def animate(i, xs, ys):
    mempoolinfo = server.getmempoolinfo()
    for i in mempoolinfo:
        if i == chosen_parameter:    
            temp_c = mempoolinfo[i]

    xs.append(dt.datetime.now().strftime('%H:%M:%S'))
    ys.append(temp_c)

    xs = xs[-15:]
    ys = ys[-15:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format graph
    graph.xticks(rotation=45, ha='right')
    graph.subplots_adjust(bottom=0.30)
    
    if chosen_parameter == "size":
        graph.title('Current tx count over time')
        graph.ylabel('Tx count')
    else:
        graph.title('Total memory usage for the mempool over time')
        graph.ylabel('Memory usage')

def print_network_info():
    networkinfo = server.getnetworkinfo()
    for key in networkinfo:
        print(key, ":", networkinfo[key])

def live_node(choice):
    global chosen_parameter
    chosen_parameter = choice
    global fig
    fig= graph.figure()
    global ax
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []
    tmp = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
    graph.show()

if __name__ == '__main__':
    print("\n**** Welcome to Python block explorer ****\n\n")
    server = get_server()

    tmp = True
    while tmp == True:
        tmp = menu_choice(menu())