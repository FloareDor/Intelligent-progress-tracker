from flask import Flask, jsonify, request
from pymongo import MongoClient
import bson
from bson import json_util
from datetime import datetime
import logging
import sys
import uuid
import json
from flask_cors import CORS
import timedelta
import itertools
from datetime import datetime, timedelta
import openai
from flask_sslify import SSLify

openai.api_key = "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"

def generate_quote(event):
    
    if event["progress"] == 1: #doing
        prompt = f"Generate a creative motivational quote for completing the ongoing task '{event['title']}' with the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            )
        return response.choices[0].text.strip()
        
    if event["progress"] == 0: #done
        prompt = f"Generate a creative appreciation quote for finishing the task '{event['title']}' with the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            )

        return response.choices[0].text.strip()
        
    if event["progress"] == 2: #overdue
        prompt = f"Generate a creative motivating quote for the overdue task '{event['title']}' with the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            )
        quote = response.choices[0].text.strip()
        return quote
        
    if event["progress"] == 3: #upcoming
        prompt = f"Generate a creative motivating quote for the upcoming task with title as '{event['title']}' and the description '{event['description']}'"
        response = openai.Completion.create( 
            engine="text-davinci-003" ,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
            )
        quote = response.choices[0].text.strip()
        return quote

def printf(x):
    print(x, file=sys.stderr)
    #app.logger.info(x)
printf("Running!")
def parse_json(data):
    return json.loads(json_util.dumps(data))

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
sslify = SSLify(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# with collection.watch() as stream:
#     for change in stream:
#         printf(change)

collection.delete_many({})

unique_id = str(uuid.uuid4())
one = {
        "id": unique_id,
        'title' :  'Gym',
        'description' : 'Hit the Gym',
        'date' : "2023-04-01",
        'duration' : '2',
        'deadline' : "2023-04-01",
        'type' : 'Personal',
        "progress": 0,

}



unique_id = str(uuid.uuid4())
quote1 = generate_quote({'title' :  'Machine Learning Project',
        'description' : 'Implementing exchange rate prediction using different regression models and choosing the best from them',
        "progress": 1})
two = {
        "id": unique_id,
        'title' :  'Machine Learning Project',
        'description' : 'Implementing exchange rate prediction using different regression models and choosing the best from them',
        'date' : "2023-04-01",
        'duration' : '8',
        'deadline' : "2023-04-10",
        'type' : 'Personal',
        "progress": 1,
        "quote": quote1
}

quote2 = generate_quote({        'title' :  'Deep Learning',
        'description' : 'Implementing exchange rate prediction using different regression models and choosing the best from them',
        "progress": 2})
two = {
        "id": unique_id,
        'title' :  'Deep Learning',
        'description' : 'Implementing exchange rate prediction using different regression models and choosing the best from them',
        'date' : "2023-04-01",
        'duration' : '8',
        'deadline' : "2023-04-10",
        'type' : 'Personal',
        "progress": 2,
        "quote": quote2
}
collection.insert_one(one)
collection.insert_one(two)

printf(collection)

def fetch():
    data = []
    printf(collection.find())
    blocks = collection.find()

    data = []
    for block in blocks:
        data.append(block)
    printf(data)
    json_data = parse_json(data)

    # Print the JSON string
    print(json_data)
    return {"data":json_data}


@app.route("/")
def route():
    return "Hello World!"

@app.route("/api/create", methods=["POST", "GET"])
def create():
    data = request.json
    unique_id = str(uuid.uuid4())
    #deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
    try:
        my_data = {   
                        "id": unique_id,
                        "title": data.get('title'),
                        "description": data.get('description'),
                        "duration": data.get('duration'),
                        "date": str(datetime.today().replace(microsecond=0)),
                        "deadline": data.get('deadline'),
                        "type": data.get('type'),
                        "progress": 0
                    }
        quote = generate_quote(my_data)
        my_data = {   
                        "id": unique_id,
                        "title": data.get('title'),
                        "description": data.get('description'),
                        "duration": data.get('duration'),
                        "date": str(datetime.today().replace(microsecond=0)),
                        "deadline": data.get('deadline'),
                        "type": data.get('type'),
                        "progress": 0,
                        "quote": quote
                    }

        collection.insert_one(my_data)
        x = parse_json({"data": my_data})

        return x

    except Exception as e:
        printf(e)
        return ({"Exception": e})

    

@app.route("/api/read", methods=["POST", "GET"])
def read():
    data = []
    printf(collection.find())
    blocks = collection.find()

    data = []
    for block in blocks:
        data.append(block)
    printf(data)
    json_data = parse_json(data)

    # Print the JSON string
    print(json_data)
    return {"data":json_data}

@app.route("/api/update", methods=["POST", "GET"])
def update():
    data = request.json
    blocks = collection.find()

    old_data = []
    quote = ""
    for block in blocks:
        old_data.append(block)
    if old_data["progress"] != data["progress"]:
        quote = generate_quote(data)
    
    my_query = {
        "id": data["id"]}
    
    new_values = {"$set": {
        "title": data.get('title'),
        "description": data.get("description"),
        "duration": data.get("duration"),
        "date": data.get("date"),
        "deadline": data.get("deadline"),
        "type": data.get("type"),
        "progress": data.get("progress"),
        "quote": quote
    }}
    collection.update_one(my_query, new_values)
    return {"data": new_values}

@app.route("/api/delete", methods=["POST", "GET"])
def delete():
    data = request.json
    my_query = {"id": data["id"]}
    collection.delete_one(my_query)
    return "Data deleted successfully!"

@app.route("/api/optimize")
def optimize():
    d = fetch()
    data = fetch()["data"]
    #printf(type(data))
    events = [
        {"id": 1, "title": "Event A", "duration": 2, "deadline": "2023-04-10"},
        {"id": 2, "title": "Event B", "duration": 3, "deadline": "2023-04-05"},
        {"id": 3, "title": "Event C", "duration": 1, "deadline": "2023-04-07"},
        {"id": 4, "title": "Event D", "duration": 2, "deadline": "2023-04-12"},
        {"id": 5, "title": "Event E", "duration": 1, "deadline": "2023-04-09"}
    ]
    events = []

    for i in data:
        #printf(data)
        events.append(data)
    printf("FUCKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK\n")
    printf(events)
    # Step 1: Sort the events by deadline
    events_list = list(itertools.chain.from_iterable(events))
    printf(events_list)
    events = sorted(events_list, key=lambda x: x["deadline"])
    

    # Step 2: Assign priority scores to each event based on deadline
    for i, event in enumerate(events):
        event["priority"] = i

    # Step 3: Initialize the scheduling queue with all events
    scheduling_queue = events.copy()

    # Step 4: Schedule events based on priority score
    current_time = datetime.strptime("2023-04-01", "%Y-%m-%d")  # Set initial time as a datetime object
    while scheduling_queue:
        # Select the event with the highest priority score
        next_event = max(scheduling_queue, key=lambda x: x["priority"])
        # Convert the deadline string to a datetime object
        deadline = datetime.strptime(next_event["deadline"], "%Y-%m-%d")
        # Check if there is enough time to complete the event before the deadline
        if current_time + timedelta(days=int(next_event["duration"])) <= deadline:
            # Assign the event to the current time slot
            next_event["start_time"] = current_time
            current_time += timedelta(days=int(next_event["duration"]))
            # Remove the event from the scheduling queue
            scheduling_queue.remove(next_event)
        else:
            # Remove the event from the scheduling queue if there isn't enough time
            scheduling_queue.remove(next_event)

    # Print the scheduled events
    for event in events:
        print(event)
    return {"sorted data": events}
    return d

if __name__ == "__main__":
    app.run(host="64.227.168.53", port=5000, debug=True)
