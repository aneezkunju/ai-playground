from mcp.server import MCPServer
from cafe_data import MENU, COUPONS
from pydantic import BaseModel

mcp = MCPServer(name="Cafe Bahar", instructions="Order food from Charminar Cafe in Hyderabad: read the menu, place orders, apply coupons, track delivery.")
ORDERS : dict[str,dict] = {}

@mcp.resource("cafe://menu")
def menu_card()->str :
    pass

# @mcp.resource("cafe://receipt")
@mcp.resource("cafe://order/{order_id}")
def order_receipt(order_id:str)->str :
    pass

def todays_special()->str:
    pass

def cafe_policies()->str:
    pass

class OrderLine(BaseModel):
    item:str
    quantity:int

class OrderConfirmation(BaseModel):
    order_id:str
    total_rupees:float|int
    eta:str
    message:str

class OrderStatus(BaseModel):
    order_id:str
    status:str
    minutes_left:int

@mcp.tool()
def place_order(table_no:str, order:list[OrderLine], customer:str) -> OrderConfirmation:
    pass
@mcp.tool()
def apply_coupon(order_id:str, code:str)->OrderConfirmation:
    pass
@mcp.tool()
def track_status(order_id:str)->OrderStatus:
    pass

if __name__ == "__main__":
    mcp.run("stdio")