#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file RingBuffer.py
# @brief Defautl Buffer class
# @date $Date: 2007/09/12 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import RTC
import OpenRTM_aist

##
# @if jp
# @class RingBuffer
# @brief ��󥰥Хåե��������饹
# 
# ���ꤷ��Ĺ���Υ�󥰾��Хåե�����ĥХåե��������饹��
# �Хåե����Τ˥ǡ�������Ǽ���줿��硢�ʹߤΥǡ����ϸŤ��ǡ�������
# �缡��񤭤���롣
# ���äơ��Хåե���ˤ�ľ��ΥХåե�Ĺʬ�Υǡ����Τ��ݻ�����롣
#
# ��)���ߤμ����Ǥϡ����ֺǸ�˳�Ǽ�����ǡ����ΤߥХåե������ɤ߽Ф���ǽ
#
# @param DataType �Хåե��˳�Ǽ����ǡ�����
#
# @since 0.4.0
#
# @else
#
# @endif
class RingBuffer(OpenRTM_aist.BufferBase):
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # ���ꤵ�줿�Хåե�Ĺ�ǥХåե����������롣
  # �����������ꤵ�줿Ĺ������̤���ξ�硢Ĺ�����ǥХåե����������롣
  #
  # @param self
  # @param length �Хåե�Ĺ
  # 
  # @else
  #
  # @endif
  def __init__(self, length):
    self._oldPtr = 0
    if length < 2:
      self._length = 2
      self._newPtr = 1
    else:
      self._length = length
      self._newPtr = length - 1

    self._inited = False
    self._buffer = [self.Data() for i in range(self._length)]


  ##
  # @if jp
  #
  # @brief �����
  # 
  # �Хåե��ν������¹Ԥ��롣
  # ���ꤵ�줿�ͤ�Хåե����Τ˳�Ǽ���롣
  #
  # @param self
  # @param data ������ѥǡ���
  # 
  # @else
  #
  # @endif
  def init(self, data):
    for i in range(self._length):
      self.put(data)


  ##
  # @if jp
  #
  # @brief ���ꥢ
  # 
  # �Хåե��˳�Ǽ���줿����򥯥ꥢ���롣
  #
  # @param self
  # 
  # @else
  #
  # @endif
  def clear(self):
    self._inited = False


  ##
  # @if jp
  #
  # @brief �Хåե�Ĺ���������
  # 
  # �Хåե�Ĺ��������롣
  #
  # @param self
  # 
  # @return �Хåե�Ĺ
  # 
  # @else
  #
  # @brief Get the buffer length
  #
  # @endif
  def length(self):
    return self._length


  ##
  # @if jp
  #
  # @brief �Хåե��˽񤭹���
  # 
  # ������Ϳ����줿�ǡ�����Хåե��˽񤭹��ࡣ
  # 
  # @param self
  # @param value �񤭹����оݥǡ���
  #
  # @return �ǡ����񤭹��߷��(���true:�񤭹����������֤�)
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # @endif
  def write(self, value):
    self.put(value)
    return True


  ##
  # @if jp
  #
  # @brief �Хåե������ɤ߽Ф�
  # 
  # �Хåե��˳�Ǽ���줿�ǡ������ɤ߽Ф���
  # 
  # @param self
  # @param value �ɤ߽Ф����ǡ���
  #
  # @return �ǡ����ɤ߽Ф����
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # @endif
  def read(self, value):
    if not self._inited:
      return False
    value[0] = self.get()
    return True


  ##
  # @if jp
  #
  # @brief �Хåե������դǤ��뤫��ǧ����
  # 
  # �Хåե����դ��ǧ���롣(���false���֤���)
  # 
  # @param self
  #
  # @return ���ճ�ǧ���(���false)
  # 
  # @else
  #
  # @brief True if the buffer is full, else false.
  #
  # @endif
  def isFull(self):
    return False


  ##
  # @if jp
  #
  # @brief �Хåե������Ǥ��뤫��ǧ����
  # 
  # �Хåե������ǧ���롣
  # 
  # ��)���ߤμ����Ǥϡ����ߤΥХåե����֤˳�Ǽ���줿�ǡ������ɤ߽Ф��줿��
  # �ɤ������֤���( true:�ǡ����ɤ߽Ф��ѡ�false:�ǡ���̤�ɤ߽Ф�)
  # 
  # @param self
  #
  # @return ����ǧ���
  # 
  # @else
  #
  # @brief True if the buffer is empty, else false.
  #
  # @endif
  def isEmpty(self):
    return not self._inited


  ##
  # @if jp
  #
  # @brief �ǿ��ǡ�������ǧ����
  # 
  # ���ߤΥХåե����֤˳�Ǽ����Ƥ���ǡ������ǿ��ǡ�������ǧ���롣
  # 
  # @param self
  #
  # @return �ǿ��ǡ�����ǧ���
  #           ( true:�ǿ��ǡ������ǡ����Ϥޤ��ɤ߽Ф���Ƥ��ʤ�
  #            false:���Υǡ������ǡ����ϴ����ɤ߽Ф���Ƥ���)
  # 
  # @else
  #
  # @endif
  def isNew(self):
    return self._buffer[self._newPtr].isNew()


  ##
  # @if jp
  #
  # @brief �Хåե��˥ǡ������Ǽ����
  # 
  # ������Ϳ����줿�ǡ�����Хåե��˳�Ǽ���롣
  # 
  # ��)���ߤμ����Ǥϥǡ������Ǽ�����Ʊ���ˡ��ǡ������ɤ߽Ф����֤�
  # ��Ǽ�����ǡ������֤����ꤷ�Ƥ��롣���Τ��ᡢ���ľ��˳�Ǽ�����ǡ�����
  # ����������ȤʤäƤ��롣
  # 
  # @param self
  # @param data ��Ǽ�оݥǡ���
  # 
  # @else
  #
  # @brief Write data into the buffer
  #
  # @endif
  def put(self, data):
    self._buffer[self._oldPtr].write(data)
    self._newPtr = self._oldPtr
    ptr = self._oldPtr + 1
    self._oldPtr = ptr % self._length
    self._inited = True


  ##
  # @if jp
  #
  # @brief �Хåե�����ǡ������������
  # 
  # �Хåե��˳�Ǽ���줿�ǡ�����������롣
  # 
  # @param self
  #
  # @return �����ǡ���
  # 
  # @else
  #
  # @brief Get data from the buffer
  #
  # @endif
  def get(self):
    return self._buffer[self._newPtr].read()


  ##
  # @if jp
  #
  # @brief ���˽񤭹���Хåե��ؤλ��Ȥ��������
  # 
  # �񤭹��ߥХåե��ؤλ��Ȥ�������롣
  # 
  # @return ���ν񤭹����оݥХåե��ؤλ���
  # 
  # @param self
  #
  # @else
  #
  # @brief Get the buffer's reference to be written the next
  #
  # @endif
  def getRef(self):
    return self._buffer[self._newPtr].data


  ##
  # @if jp
  # @class Data
  # @brief �Хåե��ǡ������饹
  # 
  # �Хåե��ǡ�����Ǽ�����󥯥饹��
  #
  # @since 0.4.0
  #
  # @else
  # @brief Buffer sequence
  # @endif
  class Data:
    def __init__(self):
      self.data = None
      self.is_new = False


    def write(self, other):
      self.is_new = True
      self.data = other


    def read(self):
      self.is_new = False
      return self.data


    def isNew(self):
      return self.is_new
