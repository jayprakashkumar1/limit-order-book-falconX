from bisect import bisect_right

class KeyWrapper:
    def __init__(self, iterable, key):
        self.it = iterable
        self.key = key

    def __getitem__(self, i):
        return self.key(self.it[i])

    def __len__(self):
        return len(self.it)

# class Limit for limit order book
class Limit:
    # class constructor
    def __init__(self):
        self.order_id = 0
        # initially assigned some values
        self.asks = [('','',-1,-1)]
        self.asks.sort(key=lambda x: x[3])

        self.bids = [('','',-1,-1)]
        self.bids.sort(key=lambda x: x[3])
    # to add the order 
    def add_limit_order(self,side,user_id,quanity,price):
        self.order_id=self.order_id+1
        newCol = (self.order_id,user_id,quanity,price)
        if side=="ask":
            bslindex = bisect_right(KeyWrapper(self.asks, key=lambda c: c[3]), newCol[3])
            self.asks.insert(bslindex, newCol)     
        else:
            bslindex = bisect_right(KeyWrapper(self.bids, key=lambda c: c[3]), newCol[3])
            self.bids.insert(bslindex, newCol)
        return self.order_id   

    def show(self):
        print(self.asks[1:])
        print(self.bids[1:])

    def place_market_order(self,side, quantity):
        if quantity<=0:
            return
        totalQuantity = quantity
        totalAsk = 0
        totalPrice = 0.0

        if side=="ask" :
            length = len(self.asks)-1
            for item in range(length):
                if totalAsk==totalQuantity:
                    break

                if quantity>=self.asks[1][2]:
                    quantity=quantity-self.asks[1][2]

                    totalAsk=totalAsk+self.asks[1][2]
                    totalPrice=totalPrice+self.asks[1][2]*self.asks[1][3]

                    self.asks[1]=list(self.asks[1])  
                    del(self.asks[1])
                    
                else:
                    totalAsk=totalQuantity
                    totalPrice=totalPrice + quantity * self.asks[1][3]
                    self.asks[1]=list(self.asks[1])

                    self.asks[1][2] = self.asks[1][2]-quantity
                    self.asks[1]=tuple(self.asks[1])
                    break
        else:
            length = len(self.bids)-1
            for item in range(length):
                if totalAsk==totalQuantity:
                    break

                if quantity>=self.bids[-1][2]:
                    quantity=quantity-self.bids[-1][2]

                    totalAsk=totalAsk+self.bids[-1][2]
                    totalPrice=totalPrice+self.bids[-1][2]*self.bids[-1][3]

                    self.bids[-1]=list(self.bids[-1])  
                    del(self.bids[-1])    
                else:
                    totalAsk=totalQuantity
                    totalPrice=totalPrice + quantity * self.bids[-1][3]
                    self.bids[-1]=list(self.bids[-1])

                    self.bids[-1][2] = self.bids[-1][2]-quantity
                    self.bids[-1]=tuple(self.bids[-1])
                    break
        return [totalAsk,round(totalPrice/totalAsk,4)]

    def cancel_limit_order(self,order_id):
        # print("from cancel_order_limit")
        length = len(self.bids)
        i=0
        for item in self.bids: 
            if item[0]==order_id:
                self.bids[i]=list(self.bids[i])  
                del(self.bids[i])
            i+=1

    def bbo(self):
        bestAsk = self.asks[1][3]
        bestBid = self.bids[-1][3]
        print("[" + str(self.bids[-1][3]) + "," + str(self.asks[1][3]) + "]")
lob_example = Limit()
lob_example.add_limit_order("ask", "alice", 10,100)
lob_example.add_limit_order("ask",'bob',5,90)
lob_example.add_limit_order("bid","charles", 20, 85)
lob_example.add_limit_order("bid","dave", 10, 80)
lob_example.add_limit_order("ask", "eve", 10, 95) 
# for showing asks & bids 
lob_example.show()
# to print best bid offer
lob_example.bbo()
# returns filled qnty & avg price
x = lob_example.place_market_order("ask",19)

print(x)
lob_example.bbo()
# to cancel the order having this order_id
lob_example.cancel_limit_order(4)
lob_example.show()
