# UV FoodBot

## Objective 
To build a chatbot for a online food ordering platform which helps users to :
1) Place Order
2) Track Order

## Archetecture

<img width="1394" alt="image" src="https://github.com/user-attachments/assets/ff21453c-a310-4a8d-b1ef-89401e5c4d1a">

## Building ChatBot

### Setting Intents
The intent is the mapping between what user say and what action is taken by the chatbot.

**Intents Used in the ChatBot :**
- Default Welcome Intent
- Default Fallback Intent
- New Order Intent
- Add Item Intent
- Remove Item Intent
- Complete/Confirm Order Intent
- Track Order Intent

We train the intents by giving some **training Phrases** that a user would use to trigger that pirticular intent. And when similar phrase is used, the intent is triggered.

<div style="display: flex;">
  <img src="https://github.com/user-attachments/assets/0e5cc309-65d1-404b-90fc-574c5d3888e9" alt="Intent track order" style="width: 50%;">
  <img src="https://github.com/user-attachments/assets/f22e2cf7-0a58-47af-8bdd-009eb9f23cb4" alt="Intent add order" style="width: 50%;">
</div>

<img width="1055" alt="Screenshot 2024-08-29 at 2 23 40 PM" src="https://github.com/user-attachments/assets/9ef7f8bf-a6ce-4282-aada-e3ef21a637b2">

### Setting Entities
- food entity : for food Item
- number entity : for quantity of food item

### Setting Context
To correctly interpret the followup messages that the user give we need to define the the context for the flow of messages that each intent belongs to.

#### Contexts in the Bot:
**Ongoing Order :** Starts from "New Order" intent and end after "Order Complete" intent.

**Ongoing Tracking :** Starts from "track Order" intent and end after "track.order.id" intent.

## ChaBot Workflow:

![Screenshot 2024-08-29 at 10 06 23 PM](https://github.com/user-attachments/assets/1ad74b2d-035d-49e4-8d86-2058147cfc96)

## Demo:
https://github.com/user-attachments/assets/3da73325-7900-4172-a249-7d8fcdb0ed86