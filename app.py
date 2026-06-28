from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]


def get_event_by_id(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask CRUD API!"})


@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])


@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    new_id = max((event.id for event in events), default=0) + 1
    event = Event(new_id, data["title"])
    events.append(event)

    return jsonify(event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = get_event_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)
    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict())


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = get_event_by_id(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return jsonify({}), 204


if __name__ == "__main__":
    app.run(debug=True)
