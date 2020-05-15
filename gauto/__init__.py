# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making GAutomator available.
Copyright (C) 2016 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

    GAutomator底层框架
"""

import logging

def init_logger():
    fmt = '%(asctime)s - %(levelname)s - %(filename)20s:%(lineno)-3s $$ %(message)s'
    formatter = logging.Formatter(fmt)      # 实例化formatter
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)         # 为handler添加formatter
    logger = logging.getLogger("wetest")    # 获取名为wetest的logger
    logger.addHandler(handler)              # 为logger添加handler
    logger.setLevel(logging.DEBUG)

init_logger()
