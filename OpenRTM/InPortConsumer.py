#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file  InPortConsumer.py
# @brief InPortConsumer class
# @date  $Date: 2007/09/04$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM

##
# @if jp
#
# @class InPortConsumer
#
# @brief InPortConsumer ���쥯�饹
#
# ���ϥݡ��ȥ��󥷥塼�ޤΤ������ݥ��󥿡��ե��������饹
# �ƶ�ݥ��饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# - push(): �ǡ�������
# - clone(): �ݡ��ȤΥ��ԡ�
# - subscribeInterface(): �ǡ����������Τؤ���Ͽ
# - unsubscribeInterface(): �ǡ����������Τ���Ͽ���
#
# @since 0.4.0
#
# @else
# @class InPortConsumer
# @brief InPortConsumer class
# @endif
class InPortConsumer:
  """
  """



  ##
  # @if jp
  # @brief ��³��ؤΥǡ�������(���֥��饹������)
  #
  # ��³��Υݡ��Ȥإǡ������������뤿��δؿ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  #
  # @else
  #
  # @endif
  def push(self):
    pass

  ##
  # @if jp
  # @brief �����ݡ��ȤΥ��ԡ�(���֥��饹������)
  #
  # �����ݡ��ȤΥ��ԡ����������뤿��δؿ���
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  #
  # @return ʣ�����줿 InPortConsumer ���֥�������
  #
  # @else
  #
  # @endif
  def clone(self):
    pass


  ##
  # @if jp
  # @brief �ǡ����������μ������ؤ���Ͽ(���֥��饹������)
  #
  # ���ꤵ�줿�ץ�ѥƥ������Ƥ˴�Ť��ơ��ǡ����������Τμ���������Ͽ����
  # ����δؿ���
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param properties ��Ͽ���˻��Ȥ���ץ�ѥƥ�
  #
  # @return ��Ͽ�������
  #
  # @else
  #
  # @endif
  def subscribeInterface(self, properties):
    pass


  ##
  # @if jp
  # @brief �ǡ����������μ�����꤫�����Ͽ���(���֥��饹������)
  #
  # �ǡ����������Τμ�����꤫����Ͽ������뤿��δؿ���
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param properties ��Ͽ������˻��Ȥ���ץ�ѥƥ�
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    pass
