import json
import unittest

from jsonrpc.exceptions import JSONRPCInvalidRequestException, JSONRPCParseException, JSONRPCMultipleRequestException
from jsonrpc.request import JSONRPCSingleRequest, JSONRPCBatchRequest
from jsonrpc.response import JSONRPCSingleResponse, JSONRPCBatchResponse


class TestJSONRPCSingleRequest(unittest.TestCase):
    """ Test JSONRPCSingleRequest functionality."""

    def setUp(self):
        self.request_params = {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [1, 2],
            "id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCSingleRequest(self.request_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(TypeError):
            JSONRPCSingleRequest()

    def test_method_validation_str(self):
        self.request_params.update({"method": "add"})
        JSONRPCSingleRequest(self.request_params)

    def test_method_validation_not_str(self):
        self.request_params.update({"method": []})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"method": {}})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

    def test_method_validation_str_rpc_prefix(self):
        """ Test method SHOULD NOT starts with rpc. """
        self.request_params.update({"method": "rpc."})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"method": "rpc.test"})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"method": "rpccorrect"})
        JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"method": "rpc"})
        JSONRPCSingleRequest(self.request_params)

    def test_params_validation_list(self):
        self.request_params.update({"params": []})
        JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"params": [0]})
        JSONRPCSingleRequest(self.request_params)

    def test_params_validation_tuple(self):
        self.request_params.update({"params": ()})
        JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"params": tuple([0])})
        JSONRPCSingleRequest(self.request_params)

    def test_params_validation_dict(self):
        self.request_params.update({"params": {}})
        JSONRPCSingleRequest(self.request_params)

        self.request_params.update({"params": {"a": 0}})
        JSONRPCSingleRequest(self.request_params)

    def test_params_validation_none(self):
        self.request_params.update({"params": None})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

    def test_params_validation_incorrect(self):
        self.request_params.update({"params": "str"})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

    def test_request_args(self):
        req_data = {"jsonrpc": "2.0", "method": "add", "id": 1}
        self.assertEqual(JSONRPCSingleRequest(req_data).args, ())
        self.assertEqual(JSONRPCSingleRequest(dict(req_data, params=[])).args, ())
        self.assertEqual(JSONRPCSingleRequest(dict(req_data, params={"a": 1})).args, ())
        self.assertEqual(JSONRPCSingleRequest(dict(req_data, params=[1, 2])).args, (1, 2))

    def test_request_kwargs(self):
        req_data = {"jsonrpc": "2.0", "method": "add", "id": 1}
        self.assertEqual(JSONRPCSingleRequest(req_data).kwargs, {})
        self.assertEqual(JSONRPCSingleRequest(dict(req_data, params=[1, 2])).kwargs, {})
        self.assertEqual(JSONRPCSingleRequest(dict(req_data, params={})).kwargs, {})
        self.assertEqual(JSONRPCSingleRequest(dict(req_data, params={"a": 1})).kwargs, {"a": 1})

    def test_id_validation_string(self):
        self.request_params.update({"id": "id"})
        JSONRPCSingleRequest(self.request_params)

    def test_id_validation_int(self):
        self.request_params.update({"id": 0})
        JSONRPCSingleRequest(self.request_params)

    def test_id_validation_null(self):
        self.request_params.update({"id": "null"})
        JSONRPCSingleRequest(self.request_params)

    def test_id_validation_none(self):
        self.request_params.update({"id": None})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

    def test_id_validation_float(self):
        self.request_params.update({"id": 0.1})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

    def test_id_validation_incorrect(self):
        self.request_params.update({"id": []})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)
            
        self.request_params.update({"id": ()})
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(self.request_params)

    def test_data_method_1(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add"})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_data_method_2(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": 1,
        })

    def test_data_params_1(self):
        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": None, "id": 1})

    def test_data_params_2(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": [], "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": [],
            "id": 1,
        })

    def test_data_params_3(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": (), "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": (),
            "id": 1,
        })

    def test_data_params_4(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": {}, "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": {},
            "id": 1,
        })

    def test_data_params_5(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": (1, 2), "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": (1, 2),
            "id": 1,
        })

    def test_data_params_6(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": {"a": 0}, "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "params": {"a": 0},
            "id": 1,
        })

    def test_data_id_1(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": "null"})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "null",
        })

    def test_data_id_1_notification(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add"})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
        })

    def test_data_id_2(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 1})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": 1,
        })

    def test_data_id_3(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": "id"})
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "method": "add",
            "id": "id",
        })


    def test_is_notification(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add"})
        self.assertTrue(r.is_notification)

        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 1})
        self.assertFalse(r.is_notification)

        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 'null'})
        self.assertFalse(r.is_notification)

        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 0})
        self.assertFalse(r.is_notification)

        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 1})
        r.is_notification = True
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 0})
        r.is_notification = True
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

    def test_set_unset_notification_keep_id(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 0})
        r.is_notification = True
        self.assertTrue(r.is_notification)
        self.assertNotIn("id", r.data)

        r.is_notification = False
        self.assertFalse(r.is_notification)
        self.assertTrue("id" in r.data)
        self.assertEqual(r.data["id"], 0)

    def test_serialize_method_1(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add"})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
            }, json.loads(r.json))

    def test_serialize_method_2(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 1})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": 1,
            },
            json.loads(r.json)
        )

    def test_serialize_params_1(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": [], "id": 1})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": [],
                "id": 1,
            },
            json.loads(r.json)
        )

    def test_serialize_params_3(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": (), "id": 1})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": [],
                "id": 1,
            },
            json.loads(r.json)
        )

    def test_serialize_params_4(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": [1, 2],
                "id": 1,
            },
            json.loads(r.json)
        )

    def test_serialize_params_5(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "params": {"a": 0}, "id": 1})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "params": {"a": 0},
                "id": 1,
            },
            json.loads(r.json)
        )

    def test_serialize_id_1(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": "null"})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": "null",
            },
            json.loads(r.json)
        )

    def test_serialize_id_3(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": "id"})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": "id",
            },
            json.loads(r.json)
        )

    def test_serialize_id_4(self):
        r = JSONRPCSingleRequest({"jsonrpc": "2.0", "method": "add", "id": 0})
        self.assertEqual(
            {
                "jsonrpc": "2.0",
                "method": "add",
                "id": 0,
            },
            json.loads(r.json)
        )

    def test_from_json_request_no_id(self):
        str_json = json.dumps({
            "method": "add",
            "params": [1, 2],
            "jsonrpc": "2.0",
        })

        request = JSONRPCSingleRequest(str_json)
        self.assertIsInstance(request, JSONRPCSingleRequest)
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [1, 2])
        self.assertEqual(request.id, None)
        self.assertTrue(request.is_notification)

    def test_from_json_request_no_params(self):
        str_json = json.dumps({
            "method": "add",
            "jsonrpc": "2.0",
        })

        request = JSONRPCSingleRequest(str_json)
        self.assertIsInstance(request, JSONRPCSingleRequest)
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, None)
        self.assertEqual(request.id, None)
        self.assertTrue(request.is_notification)


    def test_from_json_request(self):
        str_json = json.dumps({
            "method": "add",
            "params": [0, 1],
            "jsonrpc": "2.0",
            "id": "id",
        })

        request = JSONRPCSingleRequest(str_json)
        self.assertIsInstance(request, JSONRPCSingleRequest)
        self.assertEqual(request.method, "add")
        self.assertEqual(request.params, [0, 1])
        self.assertEqual(request.id, "id")
        self.assertFalse(request.is_notification)

    def test_from_json_invalid_request_jsonrpc(self):
        str_json = json.dumps({
            "method": "add",
        })

        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(str_json)

    def test_from_json_invalid_request_method(self):
        str_json = json.dumps({
            "jsonrpc": "2.0",
        })

        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(str_json)

    def test_from_json_invalid_request_extra_data(self):
        str_json = json.dumps({
            "jsonrpc": "2.0",
            "method": "add",
            "is_notification": True,
        })

        with self.assertRaises(JSONRPCInvalidRequestException):
            JSONRPCSingleRequest(str_json)

    def test_data_setter(self):
        request = JSONRPCSingleRequest(self.request_params)
        with self.assertRaises(JSONRPCMultipleRequestException):
            request.data = []

        with self.assertRaises(JSONRPCParseException):
            request.data = ""

        with self.assertRaises(JSONRPCInvalidRequestException):
            request.data = None


class TestJSONRPCBatchRequest(unittest.TestCase):
    """ Test JSONRPCBatchRequest functionality."""

    def test_batch_request(self):
        request = JSONRPCBatchRequest([
            JSONRPCSingleRequest({"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1, "jsonrpc": "2.0"}),
            JSONRPCSingleRequest({"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2, "jsonrpc": "2.0"}),
        ])
        self.assertEqual(json.loads(request.json), [
            {"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1, "jsonrpc": "2.0"},
            {"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2, "jsonrpc": "2.0"},
        ])
        self.assertTrue(request)

    def test_batch_request_from_list_dicts(self):
        request = JSONRPCBatchRequest([
            {"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1, "jsonrpc": "2.0"},
            {"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2, "jsonrpc": "2.0"},
        ])
        self.assertEqual(json.loads(request.json), [
            {"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1, "jsonrpc": "2.0"},
            {"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2, "jsonrpc": "2.0"},
        ])
        self.assertTrue(request)

    def test_from_json_batch(self):
        str_json = json.dumps([
            {"method": "add", "params": [1, 2], "jsonrpc": "2.0"},
            {"method": "mul", "params": [1, 2], "jsonrpc": "2.0"},
        ])

        requests = JSONRPCBatchRequest(str_json)
        self.assertIsInstance(requests, JSONRPCBatchRequest)
        for r in requests:
            self.assertIsInstance(r, JSONRPCSingleRequest)
            self.assertTrue(r.method in ["add", "mul"])
            self.assertEqual(r.params, [1, 2])
            self.assertEqual(r.id, None)
            self.assertTrue(r.is_notification)

    def test_from_json_batch_one(self):
        req_data = {"method": "add", "params": [1, 2], "jsonrpc": "2.0", "id": 1}

        request = JSONRPCSingleRequest(req_data)
        requests = JSONRPCBatchRequest(request)
        self.assertIsInstance(requests, JSONRPCBatchRequest)
        self.assertEqual(len(requests), 1)
        r = requests[0]
        self.assertIsInstance(r, JSONRPCSingleRequest)
        self.assertEqual(r.method, "add")
        self.assertEqual(r.params, [1, 2])
        self.assertEqual(r.id, 1)
        self.assertFalse(r.is_notification)

    def test_response_iterator(self):
        requests = [
            JSONRPCSingleRequest({"method": "devide", "params": {"num": 1, "denom": 2}, "id": 1, "jsonrpc": "2.0"}),
            JSONRPCSingleRequest({"method": "devide", "params": {"num": 3, "denom": 2}, "id": 2, "jsonrpc": "2.0"}),
        ]
        batch = JSONRPCBatchRequest(requests)
        for request in batch:
            self.assertIsInstance(request, JSONRPCSingleRequest)
            self.assertIsInstance(batch, JSONRPCBatchRequest)
            self.assertEqual(request.method, "devide")


class TestJSONRPCSingleResponse(unittest.TestCase):
    """ Test JSONRPCSingleResponse functionality."""

    def setUp(self):
        self.response_success_params = {
            "result": "",
            "id": 1,
        }
        self.response_error_params = {
            "error": {
                "code": 1,
                "message": "error",
            },
            "id": 1,
        }

    def test_correct_init(self):
        """ Test object is created."""
        JSONRPCSingleResponse(**self.response_success_params)

    def test_validation_incorrect_no_parameters(self):
        with self.assertRaises(ValueError):
            JSONRPCSingleResponse()

    def test_validation_incorrect_result_and_error(self):
        with self.assertRaises(ValueError):
            JSONRPCSingleResponse(result="", error={"code": 1, "message": ""})

        response = JSONRPCSingleResponse(error={"code": 1, "message": ""})
        with self.assertRaises(ValueError):
            response.result = ""

    def test_validation_error_correct(self):
        JSONRPCSingleResponse(**self.response_error_params)

    def test_validation_error_incorrect(self):
        self.response_error_params["error"].update({"code": "str"})
        with self.assertRaises(ValueError):
            JSONRPCSingleResponse(**self.response_error_params)

    def test_validation_error_incorrect_no_code(self):
        del self.response_error_params["error"]["code"]
        with self.assertRaises(ValueError):
            JSONRPCSingleResponse(**self.response_error_params)

    def test_validation_error_incorrect_no_message(self):
        del self.response_error_params["error"]["message"]
        with self.assertRaises(ValueError):
            JSONRPCSingleResponse(**self.response_error_params)

    def test_validation_error_incorrect_message_not_str(self):
        self.response_error_params["error"].update({"message": 0})
        with self.assertRaises(ValueError):
            JSONRPCSingleResponse(**self.response_error_params)

    def test_validation_id(self):
        response = JSONRPCSingleResponse(**self.response_success_params)
        self.assertEqual(response.id, self.response_success_params["id"])

    def test_validation_id_incorrect_type(self):
        response = JSONRPCSingleResponse(**self.response_success_params)

        with self.assertRaises(ValueError):
            response.id = []

        with self.assertRaises(ValueError):
            response.id = {}

        with self.assertRaises(ValueError):
            response.id = 0.1

    def test_data_result(self):
        r = JSONRPCSingleResponse(result="")
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "result": "",
            "id": None,
        })

    def test_data_result_id_none(self):
        r = JSONRPCSingleResponse(result="", id=None)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "result": "",
            "id": None,
        })

    def test_data_result_id(self):
        r = JSONRPCSingleResponse(result="", id=0)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "result": "",
            "id": 0,
        })

    def test_data_error(self):
        r = JSONRPCSingleResponse(error={"code": 0, "message": ""})
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "error": {
                "code": 0,
                "message": "",
            },
            "id": None,
        })

    def test_data_error_id_none(self):
        r = JSONRPCSingleResponse(error={"code": 0, "message": ""}, id=None)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "error": {
                "code": 0,
                "message": "",
            },
            "id": None,
        })

    def test_data_error_id(self):
        r = JSONRPCSingleResponse(error={"code": 0, "message": ""}, id=0)
        self.assertEqual(json.loads(r.json), r.data)
        self.assertEqual(r.data, {
            "jsonrpc": "2.0",
            "error": {
                "code": 0,
                "message": "",
            },
            "id": 0,
        })

    def test_data_setter(self):
        response = JSONRPCSingleResponse(**self.response_success_params)
        with self.assertRaises(ValueError):
            response.data = []

        with self.assertRaises(ValueError):
            response.data = ""

        with self.assertRaises(ValueError):
            response.data = None


class TestJSONRPCBatchResponse(unittest.TestCase):
    """ Test JSONRPCBatchResponse functionality."""

    def test_batch_response(self):
        response = JSONRPCBatchResponse([
            JSONRPCSingleResponse(result="result", id=1),
            JSONRPCSingleResponse(error={"code": 0, "message": ""}, id=2),
        ])
        self.assertEqual(json.loads(response.json), [
            {"result": "result", "id": 1, "jsonrpc": "2.0"},
            {"error": {"code": 0, "message": ""}, "id": 2, "jsonrpc": "2.0"},
        ])

    def test_response_iterator(self):
        responses = JSONRPCBatchResponse([
            JSONRPCSingleResponse(result="result", id=1),
            JSONRPCSingleResponse(result="result", id=2),
        ])
        for response in responses:
            self.assertIsInstance(response, JSONRPCSingleResponse)
            self.assertEqual(response.result, "result")

    def test_batch_response_data(self):
        response = JSONRPCBatchResponse([
            JSONRPCSingleResponse(result="result", id=1),
            JSONRPCSingleResponse(result="result", id=2),
            JSONRPCSingleResponse(result="result"),
        ])
        self.assertEqual(response.data, [
            {"id": 1, "jsonrpc": "2.0", "result": "result"},
            {"id": 2, "jsonrpc": "2.0", "result": "result"},
            {"id": None, "jsonrpc": "2.0", "result": "result"},
        ])
