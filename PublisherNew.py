#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file  PublisherNew.py
# @brief PublisherNew class
# @date  $Date: 2007/09/27 $
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

import OpenRTM


##
# @if jp
# @class PublisherNew
# @brief PublisherNew ���饹
#
# �Хåե���˿����ǡ�������Ǽ���줿�����ߥ󥰤ǡ����ο����ǡ������������롣
# �ǡ������Х����ߥ󥰤��Ԥĥ��󥷥塼�ޤ����Ф���¦�Ȥϰۤʤ륹��åɤ�
# ư�������˻��ѡ�
# Publisher�ζ�ư�ϡ��ǡ������ФΥ����ߥ󥰤ˤʤ�ޤǥ֥�å����졢
# ���Х����ߥ󥰤����Τ������ȡ�¨�¤˥��󥷥塼�ޤ����н�����ƤӽФ���
#
# @else
# @class PublisherNew
# @brief PublisherNew class
# @endif
class PublisherNew(OpenRTM.PublisherBase):
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # �� Publisher �ѿ�������åɤ��������롣
  #
  # @param self
  # @param consumer �ǡ������Ф��Ԥĥ��󥷥塼��
  # @param property ��Publisher�ζ�ư�����������ꤷ��Property���֥�������
  #                 (��Publisher�Ǥ�̤����)
  # @else
  # @brief Constructor
  # @endif
  def __init__(self, consumer, property):
    self._data = self.NewData()
    self._consumer = consumer
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
  #
  # @endif
  def __del__(self):
    del self._consumer


  ##
  # @if jp
  # @brief Observer�ؿ�
  #
  # ���Х����ߥ󥰻��˸ƤӽФ���
  # �֥�å����Ƥ�������Publisher�ζ�ư�����Ϥ��졢���󥷥塼�ޤؤ����н�����
  # �Ԥ��롣
  #
  # @param self
  #
  # @else
  # @brief Observer function
  # @endif
  def update(self):
    if not self._data._cond.acquire(0):
      return

    self._data._updated = True
    self._data._cond.notify()
    self._data._cond.release()
    return


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
    while self._running:
      self._data._cond.acquire()
      # Waiting for new data updated
      while not self._data._updated and self._running:
        self._data._cond.wait()

      if self._data._updated:
        self._consumer.push()
        self._data._updated = False

      self._data._cond.release()


  ##
  # @if jp
  # @brief ��������λ�ؿ�
  #
  # ACE_Task::release() �Υ����С��饤��
  # ��ư�ե饰��false�����ꤷ���� Publisher �ζ�ư����ߤ��롣
  # ����������ư����åɤ��֥�å�����Ƥ�����ˤϡ�
  # ���磱�󥳥󥷥塼�ޤ����н������ƤӽФ�����礬���롣
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
    if not self._data._cond.acquire(0):
      return

    self._running = False
    self._data._cond.notify()
    self._data._cond.release()
    #self.wait()


  # NewData condition struct
  ##
  # @if jp
  # @class NewData
  # @brief �ǡ������ִ������������饹
  # @else
  # @endif
  class NewData:
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._updated = False
