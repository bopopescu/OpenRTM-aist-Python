#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherFlush.py
# @brief PublisherFlush class
# @date  $Date: 2007/09/06$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM_aist


##
# @if jp
# @class PublisherFlush
# @brief PublisherFlush ���饹
#
# Flush �� Publisher ���饹
# �Хåե���˳�Ǽ����Ƥ���̤�����ǡ������������롣
# �ǡ������Ф��Ԥĥ��󥷥塼�ޤ����Ф���¦��Ʊ������åɤ�ư����롣
#
# @else
# @class PublisherFlush
# @brief PublisherFlush class
# @endif
class PublisherFlush(OpenRTM_aist.PublisherBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  #
  # @param self
  # @param consumer �ǡ������Ф��Ԥĥ��󥷥塼��
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, consumer, property):
    self._consumer = consumer


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  # ����Publisher���˴�����ݤˡ�PublisherFactory�ˤ��ƤӽФ���롣
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    del self._consumer


  ##
  # @if jp
  # @brief Observer�ؿ�
  #
  # ���Х����ߥ󥰻��˸ƤӽФ���
  # ¨�¤�Ʊ�쥹��åɤˤƥ��󥷥塼�ޤ����н������ƤӽФ���롣
  #
  # @param self
  #
  # @else
  # @brief Observer function
  # @endif
  def update(self):
    self._consumer.push()
    return
  
