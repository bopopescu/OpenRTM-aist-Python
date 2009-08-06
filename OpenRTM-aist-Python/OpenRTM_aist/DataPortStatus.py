#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PushConnector.py
# @brief Push type connector class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#


class DataPortStatus:
    def __init__(self):
        pass

    PORT_OK              = 0
    PORT_ERROR           = 1
    BUFFER_FULL          = 2
    BUFFER_EMPTY         = 3
    BUFFER_TIMEOUT       = 4
    SEND_FULL            = 5
    SEND_TIMEOUT         = 6
    RECV_EMPTY           = 7
    RECV_TIMEOUT         = 8
    INVALID_ARGS         = 9
    PRECONDITION_NOT_MET = 10
    CONNECTION_LOST      = 11    
    UNKNOWN_ERROR        = 12

    def toString(self, status):
        str = ["PORT_OK",
               "PORT_ERROR",
               "BUFFER_FULL",
               "BUFFER_EMPTY",
               "BUFFER_TIMEOUT",
               "SEND_FULL",
               "SEND_TIMEOUT",
               "RECV_EMPTY",
               "RECV_TIMEOUT",
               "INVALID_ARGS",
               "PRECONDITION_NOT_MET",
               "CONNECTION_LOST",
               "UNKNOWN_ERROR"]
        return str[status]
