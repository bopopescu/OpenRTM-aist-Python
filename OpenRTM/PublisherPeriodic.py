#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherPeriodic.py
# @brief PublisherPeriodic class
# @date  $Date: 2007/09/28 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
from omniORB import any

import OpenRTM


##
# @if jp
# @class PublisherPeriodic
# @brief PublisherPeriodic ���饹
#
# ��������ǥ��󥷥塼�ޤ����н�����ƤӽФ� Publisher
# ���Ū�˥ǡ���������¹Ԥ�����˻��Ѥ��롣
#
# @else
# @class PublisherPeriodic
# @brief PublisherPeriodic class
# @endif
class PublisherPeriodic(OpenRTM.PublisherBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # ���н����θƤӽФ��ֳ֤�Property���֥������Ȥ�dataport.push_rate����
  # �����ꤷ�Ƥ���ɬ�פ����롣���дֳ֤ϡ�Hzñ�̤���ư����ʸ����ǻ��ꡣ
  # ���Ȥ��С�1000.0Hz�ξ��ϡ���1000.0�פ����ꡣ
  # �嵭�ץ�ѥƥ���̤����ξ��ϡ���1000Hz�פ����ꡣ
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
    self._running = True
    rate = property.getProperty("dataport.push_rate")

    if type(rate) == str or type(rate) == float or type(rate) == long :
      rate = float(rate)
    else:
      rate = float(any.from_any(rate,keep_structs=True))

    if rate:
      hz = rate
      if (hz == 0):
        hz = 1000.0
    else:
      hz = 1000.0

    self._usec = int(1000000.0/hz)

    self._running = True
    self._thread = threading.Thread(target=self.run)
    self._thread.start()


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    self._running = False
    del self._consumer


  ##
  # @if jp
  # @brief Observer�ؿ�(̤����)
  #
  # �� Publisher �Ǥϲ���¹Ԥ��ʤ���
  #
  # @param self
  #
  # @else
  # @brief Observer function
  # @endif
  def update(self):
    pass


  ##
  # @if jp
  # @brief ���������ϴؿ�
  #
  # ��Publisher��ư�����ѥ���åɤμ¹Ԥ򳫻Ϥ��롣
  #
  # @param self
  #
  # @else
  # @brief Thread execution function
  # @endif
  def run(self):
    import time
    while self._running:
      self._consumer.push()
      time.sleep(self._usec/1000000.0)

    return 0


  ##
  # @if jp
  # @brief ��������λ�ؿ�
  #
  # ACE_Task::release() �Υ����С��饤��
  # ��ư�ե饰��false�����ꤷ���� Publisher �ζ�ư����ߤ��롣
  # �����������磱�󥳥󥷥塼�ޤ����н������ƤӽФ�����礬���롣
  #
  # @param self
  #
  # @else
  # @brief Task terminate function
  #
  # ACE_Task::release() override function
  #
  # @endif
  def release(self):
    self._running = False
