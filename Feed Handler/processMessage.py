from dataclasses import dataclass
from enum import Enum, auto


type Quantity = int
type Price = float
type SeqNo = int


# DO NOT MODIFY
class Event(Enum):
    DISCONNECT = auto()
    ADD = auto()
    CHANGE = auto()
    DELETE = auto()


# DO NOT ADD OR DELETE ANY DATACLASS FIELDS
@dataclass
class DataBlock:
    event: Event
    price: Price | None
    quantity: Quantity | None
    seqNo: SeqNo
    isBuy: bool | None


@dataclass
class OrderBook:
    bids: dict[Price | None, Quantity | None]
    asks: dict[Price | None, Quantity | None]
    def add(self, data: DataBlock):
        if data.price is not None: 
            if data.isBuy:
                self.bids[data.price] = data.quantity
            else:
                self.asks[data.price] = data.quantity
        print(self)  
    def change(self, data: DataBlock):
        if data.isBuy:
            if data.quantity < 0: # type: ignore
                self.bids[data.price] = self.bids[data.price] + data.quantity # type: ignore
            elif data.quantity >= 0: # type: ignore
                self.bids[data.price] = data.quantity
        else:
            if data.quantity < 0: #type: ignore
                self.asks[data.price] = self.asks[data.price] + data.quantity # type: ignore
            elif data.quantity >= 0: # type: ignore
                self.bids[data.price] = data.quantity

    def delete(self, data: DataBlock):
        if data.isBuy:
            self.bids.pop(data.price)
        else:
            self.asks.pop(data.price)


@dataclass
class Snapshot:
    book: OrderBook
    asOfSeqNo: SeqNo


class EventStream:
    def __init__(self):
        self.orderBook: OrderBook = OrderBook({}, {})
        self.currentSeqNo: SeqNo = 1
        self.ss: Snapshot = Snapshot(self.orderBook, self.currentSeqNo)
        self.connected: bool = False
        self.cache: dict[SeqNo, DataBlock] = {}

    # Implement this
    def processMessage(self, msg: DataBlock | Snapshot) -> None:
        if self.connected is False:
            if isinstance(msg, Snapshot):
                self.processSnapShot(msg)
                for sequence in sorted(self.cache.keys()):
                    if sequence <= self.currentSeqNo: 
                        continue
                    if sequence > self.currentSeqNo:
                        self.msgEvent(self.cache[sequence])
                self.cache.clear()
                self.connected = True
            else:
                self.cache[msg.seqNo] = msg
        else:
            self.msgEvent(msg) # type: ignore

    def processSnapShot(self, msg: Snapshot):
        print(f"""Processing Snapshot - 
                {msg}""")
        self.currentSeqNo = msg.asOfSeqNo
        self.orderBook.bids = msg.book.bids
        self.orderBook.asks = msg.book.asks

    def msgEvent(self, dataBlock: DataBlock):
        print(f"""Processing Message Event({dataBlock.event}) -
                Price: {dataBlock.price}
                Quantity: {dataBlock.quantity}
                Sequence Number: {dataBlock.seqNo}
                isBuy: {dataBlock.isBuy}""")
        event: Event = dataBlock.event
        match event:
            case Event.DISCONNECT:
                self.ss.asOfSeqNo = self.currentSeqNo
                self.ss.book = self.orderBook
                self.orderBook.asks.clear()
                self.orderBook.bids.clear()
                self.connected = False
                

            case Event.ADD:
                self.orderBook.add(dataBlock)
            case Event.CHANGE:
                self.orderBook.change(dataBlock)
            case Event.DELETE:
                self.orderBook.delete(dataBlock)
            case _:
                pass
        self.currentSeqNo = self.currentSeqNo + 1

        #***self.data = {key: self.data[key] for key in sorted(self.data)}

## TEST 1 PASSED ***************************************************************************
#e = EventStream()
#snapShot_1 = Snapshot(OrderBook({1: 2}, {5: 3}), 1)
#dataBlock_1 = DataBlock(Event.ADD, 2, 5, 1, True)
#dataBlock_2 = DataBlock(Event.DELETE, 5, None, 2, False)
#
#e.processMessage(snapShot_1)  # As of SeqNo 1
#print(e.orderBook)
#e.processMessage(dataBlock_1)  # SeqNo 1
#print(e.orderBook)
#e.processMessage(dataBlock_2)  # SeqNo 2
#print(e.orderBook)
## Final OrderBook = Bids: {1:2, 2:5}, Asks: {}
## _____________________________________________________________
## TEST 2 PASSED ************************************************************************************
#e = EventStream()
#snapShot_1 = Snapshot(OrderBook({1: 2}, {5: 3}), 1)
#dataBlock_1 = DataBlock(Event.DISCONNECT, None, None, 1, None)
#dataBlock_2 = DataBlock(Event.CHANGE, 5, 5, 3, True)
#dataBlock_3 = DataBlock(Event.CHANGE, 7, -2, 2, False)
#snapShot_2 = Snapshot(OrderBook({5: 2}, {7: 3}), 2)
#
#e.processMessage(snapShot_1)  # As of SeqNo 1
#print(e.orderBook)
#e.processMessage(dataBlock_1)  # SeqNo 1
#print(e.orderBook)
#e.processMessage(dataBlock_2)  # SeqNo 3
#print(e.orderBook)
#e.processMessage(dataBlock_3)  # SeqNo 2
#print(e.orderBook)
#e.processMessage(snapShot_2)  # As of SeqNo 2
#print(e.orderBook)
## Final OrderBook = Bids: {5:5}, Asks: {7:3}

e = EventStream()
snapShot_1 = Snapshot(OrderBook({1:2}, {5:3}), 1) 
dataBlock_1 = DataBlock(Event.DISCONNECT, None, None, 1, None) 
dataBlock_2 = DataBlock(Event.CHANGE, 5, 5, 3, True)
dataBlock_3 = DataBlock(Event.CHANGE, 7, -2, 2, False)
snapShot_2 = Snapshot(OrderBook({5:2}, {7:3}), 2)

e.processMessage(snapShot_1) # As of SeqNo 1
e.processMessage(dataBlock_1) # SeqNo 1
e.processMessage(dataBlock_2) # SeqNo 3
e.processMessage(dataBlock_3) # SeqNo 2
e.processMessage(snapShot_2) # As of SeqNo 2
print(e.orderBook)
# Final OrderBook = Bids: {5:5}, Asks: {7:3}