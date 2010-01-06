#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ConnectorBase.py
# @brief Connector base class
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

import OpenRTM_aist


class ConnectorInfo:

    # ConnectorInfo(const char* name_, const char* id_,
    #               coil::vstring ports_, coil::Properties properties_)
    def __init__(self, name_, id_, ports_, properties_):
        self.name       = name_        # str
        self.id         = id_          # str
        self.ports      = ports_       # [str,...]
        self.properties = properties_  # OpenRTM_aist.Properties

#!
# @if jp
# @class ConnectorBase
# @brief Connector ���쥯�饹
#
# InPort/OutPort, Push/Pull �Ƽ� Connector �����������뤿���
# ���쥯�饹��
#
# @since 1.0.0
#
# @else
# @class ConnectorBase
# @brief Connector Base class
#
# The base class to derive subclasses for InPort/OutPort,
# Push/Pull Connectors
#
# @since 1.0.0
#
# @endif
class ConnectorBase(OpenRTM_aist.DataPortStatus):

    #!
    # @if jp
    # @class Profile
    # @brief Connector profile �����빽¤��
    #
    # ConnectorBase ����Ӥ����������饹�ǰ��� ConnectorProfile ��¤�Ρ�
    #
    # @since 1.0.0
    #
    # @else
    # @class Profile
    # @brief local representation of Connector profile
    #
    # ConnectorProfile struct for ConnectorBase and its subclasses.
    #
    # @since 1.0.0
    #
    # @endif

    #!
    # @if jp
    # @brief �ǥ��ȥ饯��
    # @else
    # @brief Destructor
    # @endif
    def __del__(self):
        pass

