#!/usr/bin/env python3
from flask_restx import fields, Resource
from flask import request
from Api.api import api
from joker import Utils

utils = Utils()

# The overall API namespace
kv_ns = api.namespace(
    name="joker",
    description="Generate or Retrieve Jokes")
kv_model = api.model(
    "Joker", {
        "topic": fields.String(
            required=False, pattern="[a-zA-Z0-9 ]+", min_length=1,
            description="Topics to generate for (animals, objects, etc.)"),
        "epoch": fields.Integer(
            required=False, description="Checkpoint epoch to generate the joke from."),
        "joke": fields.String(
            required=False, description="Generated Joke using GPT-2."),
        "explaination": fields.String(
            required=False, description="Explaination for the retrieved pun."),
    })

# Joke Generator Arguments
gen_parser = api.parser()
gen_parser.add_argument(
    "topic", type=str, required=False, location="form",
    help="Topics to generate for (animals, objects, etc.)")
gen_parser.add_argument(
    "epoch", type=int, required=False, location="form",
    help="Checkpoint epoch (0-4) to generate the joke from.")

# Pun finder arguments
find_parser = api.parser()
find_parser.add_argument(
    "topic", type=str, required=False, location="form",
    help="Topics to generate a pun for (animals, objects, etc.)")


@kv_ns.route("/generator/")
@api.doc(
    responses={
        401: "Unauthorized",
        404: "Path not found"},
    params={
        "topic": "Topics to generate for (animals, objects, etc.)",
        "epoch": "Checkpoint epoch (0-4) to generate the joke from.",
    })
class Joker(Resource):
    """Joke generator using GPT-2"""

    @api.doc(
        description="Joke generator using GPT-2",
        parser=gen_parser)
    @api.marshal_with(kv_model)
    def post(self, topic="", epoch=3):
        """Generate a joke"""
        args = gen_parser.parse_args()
        message = dict()
        topic = args.get('topic', "")
        epoch = args.get('epoch', 3)
        # Get the joke over here
        message["topic"] = None if (topic == "") else topic
        message["epoch"] = None if (epoch is None) else epoch
        message["joke"] = utils.say_joke(topic)
        code = 200
        return message  # , code


@kv_ns.route("/finder/")
@api.doc(
    responses={
        401: "Unauthorized",
        404: "Path not found"},
    params={
        "topic": "Topics to generate for (animals, objects, etc.)",
    })
class Finder(Resource):
    """Find and explain a pun"""

    @api.doc(
        description="Pun retriever and explaination",
        parser=find_parser)
    @api.marshal_with(kv_model)
    def post(self):
        """Find and explain a pun"""
        args = find_parser.parse_args()
        topic = args.get('topic', None)
        if topic is None:
            return "No topic given", 404

        message = dict()
        # Increase index for another joke
        idx = args.get('index', 0)
        # Get the joke over here
        message["topic"] = topic
        message["joke"] = "You're the joke"
        message["explaination"] = f"You and Joke have a similarity score of { 1.00 }"
        code = 200
        return message  # , code
