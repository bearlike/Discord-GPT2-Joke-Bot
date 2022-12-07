#!/usr/bin/env python3
from flask_restx import fields, Resource
from flask import request
from Api.api import api
from joker import Utils

utils = Utils()

# KV Namespace
kv_ns = api.namespace(
    name="generate/joke",
    description="Generate Jokes")
kv_model = api.model(
    "Joke Generator", {
        "topic": fields.String(
            required=False, pattern="[a-zA-Z0-9 ]+", min_length=1,
            description="Topics to generate for (animals, objects, etc.)"),
        "epoch": fields.Integer(
            required=False, description="Checkpoint epoch to generate the joke from."),
        "message": fields.String(
            required=False, description="Generated Joke"),
    })

# KV Arguments
kv_parser = api.parser()
kv_parser.add_argument(
    "topic", type=str, required=False, location="form",
    help="Topics to generate for (animals, objects, etc.)")
kv_parser.add_argument(
    "epoch", type=int, required=False, location="form",
    help="Checkpoint epoch (0-4) to generate the joke from.")


@kv_ns.route("/")
@api.doc(
    responses={
        401: "Unauthorized",
        404: "Path not found"},
    params={
        "topic": "Topics to generate for (animals, objects, etc.)",
        "epoch": "Checkpoint epoch (0-4) to generate the joke from.",
    })
class Engine_KV(Resource):
    """Key-Value API operations"""

    @api.doc(
        description="Joke generator using GPT-2",
        parser=kv_parser)
    @api.marshal_with(kv_model)
    def post(self, topic="", epoch=3):
        """Generate a joke"""
        args = kv_parser.parse_args()
        message = dict()
        topic = args.get('topic', "")
        epoch = args.get('epoch', 3)
        # Get the joke over here
        message["topic"] = None if (topic == "") else topic
        message["epoch"] = None if (epoch is None) else epoch
        message["message"] = utils.say_joke(topic)
        code = 200 
        return message # , code
