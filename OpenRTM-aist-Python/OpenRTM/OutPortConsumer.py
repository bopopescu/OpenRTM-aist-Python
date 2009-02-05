#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  OutPortConsumer.py
# @brief OutPortConsumer class
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


##
# @if jp
#
# @class OutPortConsumer
#
# @brief OutPortConsumer ���饹
#
# ���ϥݡ��ȥ��󥷥塼�ޤΤ���Υ��饹
# �ƶ�ݥ��饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# - pull(): �ǡ�������
# - subscribeInterface(): �ǡ����������Τؤ���Ͽ
# - unsubscribeInterface(): �ǡ����������Τ���Ͽ���
#
# @since 0.4.0
#
# @else
# @class OutPortConsumer
# @brief OutPortConsumer class
# @endif
class OutPortConsumer:
  """
  """



  ##
  # @if jp
  #
  # @brief �ǡ������������(���֥��饹������)
  #
  # �ǡ���������¹Ԥ��뤿��δؿ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  #
  # @else
  #
  # @endif
  def pull(self):
    pass


  ##
  # @if jp
  #
  # @brief �ǡ����������Τؤ���Ͽ(���֥��饹������)
  #
  # ���ꤵ�줿�ץ�ѥƥ�����˴�Ť��ơ��ǡ����������Τ���Ͽ����ؿ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param properties ��Ͽ�ѥץ�ѥƥ�
  #
  # @return ��Ͽ�������(��Ͽ����:true����Ͽ����:false)
  #
  # @else
  #
  # @endif
  def subscribeInterface(self, properties):
    pass


  ##
  # @if jp
  #
  # @brief �ǡ����������Τ������Ͽ���(���֥��饹������)
  #
  # �ǡ����������Τ������Ͽ�������뤿��δؿ���<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  # @param properties ��Ͽ����ѥץ�ѥƥ�
  #
  # @return ��Ͽ����������(��Ͽ�������:true����Ͽ�������:false)
  #
  # @else
  #
  # @endif
  def unsubscribeInterface(self, properties):
    pass
