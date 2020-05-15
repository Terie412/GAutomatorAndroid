# -*- coding: UTF-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

"""
import six
import json, socket, struct, time
import threading
import logging
from gauto.common.wetest_exceptions import *

logger = logging.getLogger("gauto")

ResponseStatus = {
    0 : ["SUCCESS", "成功"],
    1 : ["NO_SUCH_CMD","没有这个命令"],
    2 : ["UNPACK_ERROR","解析信息错误"],
    3 : ["UN_KNOW_ERROR","未知错误"],
    4 : ["GAMEOBJ_NOT_EXIST","GameObject 不存在"],
    5 : ["COMPONENT_NOT_EXIST","Component 不存在"],
    6 : ["NO_SUCH_HANDLER","没有这个接口"],
    7 : ["REFLECTION_ERROR","反射错误"],
    8 : ["NO_SUCH_RESOURCE","没有这个资源"]
}

class SocketClient(object):
    def __init__(self, _host='localhost', _port=27018):
        self.host = _host
        self.port = _port
        self.connect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.socket.connect((self.host, self.port))

    def _send_data(self, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise WeTestInvaildArg('You can only send JSON-serializable data')
        length = len(serialized)
        buff = struct.pack("i", length)
        self.socket.send(buff)
        if six.PY3:
            self.socket.sendall(bytes(serialized, encoding='utf-8'))
        else:
            self.socket.sendall(serialized)

    def close(self):
        try:
            self.socket.close()
        except Exception as e:
            logger.exception(e)

    def recv_package(self):
        length_buffer = self.socket.recv(4)
        if length_buffer:
            total = struct.unpack_from("i", length_buffer)[0]
        else:
            raise WeTestSDKError('recv length is None?')
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = self.socket.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        try:
            if six.PY3:
                deserialized = json.loads(str(view.tobytes(), encoding='utf-8'))
            else:
                deserialized = json.loads(view.tobytes())
            return deserialized
        except (TypeError, ValueError) as e:
            raise WeTestInvaildArg('Data received was not in JSON format')

    def _recv_data(self):
        deserialized = self.recv_package()
        status = deserialized['status']
        if status != 0:
            logger.error(f"Error code = {status}, {ResponseStatus[status]}")
        return deserialized.get("data", None)

    def send_package(self, cmd, params=None):
        if not params:
            params = ""
        command = {}
        command["cmd"] = cmd
        command["value"] = params
        for retry in range(0, 2):
            try:
                self._send_data(command)
                return
            except WeTestRuntimeError as e:
                raise e
            except socket.timeout:
                self.socket.close()
                self.connect()
                raise WeTestSDKError("Recv Data From SDK timeout")
            except socket.error as e:
                time.sleep(1)
                print("Retry...{0}".format(e.errno))
                self.socket.close()
                self.connect()
                continue
        raise Exception('Socket Error')

    def send_command(self, cmd, params=None, timeout=20):
        if not params:
            params = ""
        command = {}
        command["cmd"] = cmd
        command["value"] = params
        for retry in range(0, 2):
            try:
                self.socket.settimeout(timeout)
                self._send_data(command)
                ret = self._recv_data()
                return ret
            except WeTestRuntimeError as e:
                raise e
            except socket.timeout:
                self.socket.close()
                self.connect()
                raise WeTestSDKError("Recv Data From SDK timeout")
            except socket.error as e:
                time.sleep(1)
                print("Retry...{0}".format(e.errno))
                self.socket.close()
                self.connect()
                continue
        raise Exception('Socket Error')
