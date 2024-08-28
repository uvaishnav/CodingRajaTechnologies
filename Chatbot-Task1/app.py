from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_connector
import re

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "UV FoodBot"}

in_progress_order = {}

@app.post("/")
async def handle_requests(request: Request):
    # retrieve the request body
    payload = await request.json()

    # Getting intent
    intent = payload['queryResult']['intent']['displayName']
    print(intent)

    # Getting parameters
    parameters = payload['queryResult']['parameters']

    # Output Contexts
    output_contexts = payload['queryResult']['outputContexts']

    uuid_regex = r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
    match = re.search(uuid_regex, output_contexts[0]['name'])

    if match:
        session_id = match.group(0)
    else:
        session_id = None

    print(session_id)

    intent_hadler_dict = {
        'track.order.id': track_order,
        'order.add': add_order,
        'order.remove': remove_order,
        'order.complete': complete_order
    }

    # handling each intent

    return JSONResponse(content={"fulfillmentText": intent_hadler_dict[intent](parameters,session_id)})


def track_order(parameters: dict, session_id: str):
    try:
        order_id = parameters['number'][0]
        order_status = db_connector.get_order_status(order_id)
        if order_status is None:
            return f"Order with ID: {int(order_id)} not found"
        else:
            return f"Your Order with ID: {int(order_id)} is {order_status}"
    except KeyError:
        return "Invalid parameters. Please provide a valid order ID."
    except Exception as e:
        return f"An error occurred while tracking the order: {str(e)}"


def add_order(parameters: dict, session_id: str):
    try:
        food_items = parameters['food_item']
        quantities = parameters['number']

        if len(food_items) != len(quantities):
            return "Please provide the quantity for each food item"

        cur_order = {}

        for item, quantity in zip(food_items, quantities):
            cur_order[item] = quantity

        if session_id in in_progress_order:
            in_progress_order[session_id].update(cur_order)
        else:
            in_progress_order[session_id] = cur_order

        order_items = in_progress_order[session_id]
        order_description = ", ".join([f"{int(quantity)} {item}" for item, quantity in order_items.items()])
        return f"Your order now contains {order_description}\n\nWould you like to add more items?"
    except KeyError:
        return "Invalid parameters. Please provide valid food items and quantities."
    except Exception as e:
        return f"An error occurred while adding the order: {str(e)}"




def remove_order(parameters:dict,session_id:str):
    food_items = parameters['food_item']

    for item in food_items:
        if item in in_progress_order[session_id]:
            del in_progress_order[session_id][item]

    order_items = in_progress_order[session_id]
    order_description = ", ".join([f"{int(quantity)} {item}" for item, quantity in order_items.items()])
    return f"Removed {', '.join(food_items)} from your order\n\nYour order now contains {order_description}\n\nWould you like to add more items?"



def complete_order(parameters:dict,session_id:str):
    if session_id not in in_progress_order:
        return "Sorry I could not find any items in your order.\n Try ordering by typing \"New Order\". Sorry for the inconvenience."
    
    order_items = in_progress_order[session_id]
    order_details = db_connector.add_order_to_db(order_items)

    in_progress_order.pop(session_id)

    order_description = ", ".join([f"{int(quantity)} {item}" for item, quantity in order_items.items()])
    return f"Your order has been placed successfully.\nYour order ID is {order_details['order_id']}.\nYou have ordered {order_description}.\nYour total amount is {int(order_details['total_price'])}.\nYour order will be delivered in {order_details['delivery_time']} minutes."