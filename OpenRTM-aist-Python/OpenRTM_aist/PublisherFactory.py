#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFactory.py
# @brief PublisherFactory class
# @date  $Date: 2007/09/05$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

from omniORB import any

import OpenRTM_aist


##
# @if jp
# @class PublisherFactory
# @brief PublisherFactory ���饹
#
# �Ƽ�Publisher���֥������Ȥ��������˴����������ե����ȥꥯ�饹
# ���ƥ�ݥ��ʼ���
#   ����Ū�ˤ�Ǥ�դ�Publisher�������Ǥ���褦�ˤ��롣
#
# @else
# @class PublisherFactory
# @brief PublisherFactory class
# @endif
class PublisherFactory:
  """
  """


  ##
  # @if jp
  # @brief Publisher������
  #
  # Publisher���֥������Ȥ��������롣
  # ���ꤵ�줿�����˱�����Ŭ�ڤ�Publisher�����Υ��֥������Ȥ���������롣
  # ��������Publisher�μ��̤򡢻��ꤵ�줿Property���֥������Ȥ�
  # dataport.subscription_type���Ф����ꤷ�Ƥ���ɬ�פ����롣
  # �ޤ������̤ˤ�äƤϡ�Publisher�ζ�ư�����椹�����򤵤�����ꤹ��ɬ�פ�
  # ���롣
  # �����ζ���Ū�����Ƥϡ����줾���Publisher�����򻲾ȤΤ��ȡ�
  #
  # @param self
  # @param consumer Publisher�ˤ�äƥǡ������Ф��ư����륳�󥷥塼��
  # @param property �������٤�Publisher�����ꤹ�뤿��ξ���䡢Publisher��
  #                 ��ư�����椹�뤿��ξ������ꤵ��Ƥ���Property���֥���
  #                 ����
  #
  # @return ��������Publisher���֥������ȡ������˼��Ԥ�������Null���֤���
  #
  # @else
  # @brief Create Publisher
  # @endif
  def create(self, consumer, property):
    pub_type = property.getProperty("dataport.subscription_type", "New")

    if type(pub_type) != str :
      pub_type = str(any.from_any(pub_type,keep_structs=True))
    if pub_type == "New":
      return OpenRTM_aist.PublisherNew(consumer, property)
    elif pub_type == "Periodic":
      return OpenRTM_aist.PublisherPeriodic(consumer, property)
    elif pub_type == "Flush":
      return OpenRTM_aist.PublisherFlush(consumer, property)

    return None


  ##
  # @if jp
  # @brief Publisher���˴�
  #
  # ���ꤵ�줿Publisher���֥������Ȥ��˴����롣
  #
  # @param self
  # @param publisher �˴��о�Publisher���֥�������
  #
  # @else
  # @brief Destroy Publisher
  # @endif
  def destroy(self, publisher):
    if publisher:
      publisher.release()
    del publisher
