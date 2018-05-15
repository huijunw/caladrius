""" This is the rooting logic for the Apache Heron topology performance
modelling API """
import logging

from typing import List, Type, Dict, Any

from flask_restful import Resource, reqparse

from caladrius.metrics.heron.client import HeronMetricsClient
from caladrius.graph.gremlin.client import GremlinClient
from caladrius.graph.utils.heron import graph_check
from caladrius.model.topology.base import TopologyModel

LOG: logging.Logger = logging.getLogger(__name__)

class HeronCurrent(Resource):

    def __init__(self, model_classes: List[Type], model_config: Dict[str, Any],
                 metrics_client: HeronMetricsClient,
                 graph_client: GremlinClient, tracker_url: str) -> None:


        self.metrics_client: HeronMetricsClient = metrics_client
        self.graph_client: GremlinClient = graph_client

        self.tracker_url: str = tracker_url
        self.model_config: Dict[str, Any] = model_config

        self.models: Dict[str, TopologyModel] = {}
        for model_class in model_classes:
            model = model_class(model_config, metrics_client, graph_client)
            self.models[model.name] = model

        self.parser = reqparse.RequestParser()
        self.parser.add_argument("cluster", type=str, required=True,
                                 help="The name of the cluster the topology is"
                                      " running in")
        self.parser.add_argument("environ", type=str, required=True,
                                 help="The name of the environment the "
                                      "topology is running in")
        self.parser.add_argument("model", type=str, required=False,
                                 action='append',
                                 help="The model(s) to run")

        super().__init__()

    def get(self, topology_id: str) -> dict:
        args = self.parser.parse_args()

        topology_ref: str = graph_check(self.graph_client, self.model_config,
                                        self.tracker_url, args["cluster"],
                                        args["environ"], topology_id)

        if args["model"] == "all":
            models = self.models.keys()
        else:
            models = args["model"]

        for model_name in models:
            LOG.info("Running topology performance model %s", model_name)
            model = self.models["model_name"]
            # TODO: Sort out model running

        return {"topology_id" : topology_id,
                "topology_ref" : topology_ref}

class HeronProposed(Resource):

    def __init__(self) -> None:
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('model_id', type=int, required=True,
                                 help='Model ID must be supplied')
        super().__init__()

    def get(self, topology_id: str) -> str:
        args = self.parser.parse_args()
        msg: str = (f"Results requested for model: {args['model_id']} of "
                    f"topology: {topology_id}")
        return msg

    def post(self, topo_id: str):
        return 202
