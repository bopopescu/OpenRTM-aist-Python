#!/usr/bin/env python
# -#- coding: euc-jp -#-


##
# @file TimeValue.py
# @brief TimeValue class
# @date $Date: 2007/08/23$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.


import OpenRTM_aist

TIMEVALUE_ONE_SECOND_IN_USECS = 1000000.0 # 1 [sec] = 1000000 [usec]

##
# @if jp
# @class TimeValue
# @brief ���ַ׻��ѥ��饹
# 
# ���ꤷ�������ͤ��ݻ����뤿��Υ��饹��
# �����ͤ��Ф���Ƽ�׻��ѥ��ڥ졼�������󶡤��롣
#
# @since 0.4.0
#
# @else
#
# @endif
class TimeValue:
  """
  """



  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # ���ꤵ�줿�á��ޥ������äǽ�������롣
  #
  # @param self
  # @param sec ��(�ǥե������:None)
  # @param usec �ޥ�������(�ǥե������:None)
  # 
  # @else
  #
  # @endif
  def __init__(self, sec=None, usec=None):
    if sec is None:
      self.tv_sec = 0
    else:
      self.tv_sec = float(sec)

    if usec is None:
      self.tv_usec = 0
    else:
      self.tv_usec = float(usec)
    self.normalize()


  ##
  # @if jp
  #
  # @brief ���ָ���
  # 
  # ���ꤵ�줿���֤��������Ϳ����줿���֤򸺻����롣
  #
  # @param self
  # @param tm ��������
  # 
  # @return �������
  # 
  # @else
  #
  # @endif
  def __sub__(self, tm):
    global TIMEVALUE_ONE_SECOND_IN_USECS
    try:
      res = TimeValue()
    except:
      res = OpenRTM_aist.TimeValue()
    
    if self.tv_sec >= tm.tv_sec:
      if self.tv_usec >= tm.tv_usec:
        res.tv_sec  = self.tv_sec  - tm.tv_sec
        res.tv_usec = self.tv_usec - tm.tv_usec
      else:
        res.tv_sec  = self.tv_sec  - tm.tv_sec - 1
        res.tv_usec = (self.tv_usec + TIMEVALUE_ONE_SECOND_IN_USECS) - tm.tv_usec
    else:
      if tm.tv_usec >= self.tv_usec:
        res.tv_sec  = -(tm.tv_sec  - self.tv_sec)
        res.tv_usec = -(tm.tv_usec - self.tv_usec)
      else:
        res.tv_sec  = -(tm.tv_sec - self.tv_sec - 1)
        res.tv_usec = -(tm.tv_usec + TIMEVALUE_ONE_SECOND_IN_USECS) + self.tv_usec

    self.normalize()
    return res


  ##
  # @if jp
  #
  # @brief ���ֲû�
  # 
  # ���ꤵ�줿���֤˰�����Ϳ����줿���֤�û����롣
  #
  # @param self
  # @param tm �û�����
  # 
  # @return �û����
  # 
  # @else
  #
  # @endif
  def __add__(self, tm):
    res = TimeValue()
    res.tv_sec  = self.tv_sec  + tm.tv_sec
    res.tv_usec = self.tv_usec + tm.tv_usec
    if res.tv_usec > TIMEVALUE_ONE_SECOND_IN_USECS:
      res.tv_sec += 1
      res.tv_usec -= TIMEVALUE_ONE_SECOND_IN_USECS

    self.normalize()
    return res


  def sec(self):
    return self.tv_sec


  def usec(self):
    return self.tv_usec


  ##
  # @if jp
  #
  # @brief double�������ַ��Ѵ�
  # 
  # ������Ϳ����줿double������ַ����Ѵ����롣
  #
  # @param self
  # @param time �Ѵ�����
  # 
  # @return �Ѵ����
  # 
  # @else
  #
  # @endif
  def set_time(self, time):
    global TIMEVALUE_ONE_SECOND_IN_USECS

    self.tv_sec  = long(time)
    self.tv_usec = long((time - float(self.tv_sec))*TIMEVALUE_ONE_SECOND_IN_USECS)
    return self

  ##
  # @if jp
  #
  # @brief ���ַ���double���Ѵ�
  # 
  # �ݻ����Ƥ������Ƥ�double�����Ѵ����롣
  #
  # @param self
  # @return double���Ѵ����
  # 
  # @else
  #
  # @endif
  def toDouble(self):
    global TIMEVALUE_ONE_SECOND_IN_USECS
    return float(self.tv_sec) + float(self.tv_usec/TIMEVALUE_ONE_SECOND_IN_USECS)


  ##
  # @if jp
  # @brief ������֤���Ϥ���
  #
  # ������֤�ʸ������Ϥ��롣<br>
  #
  # @param self
  #
  # @return �������ʸ����ɽ��
  #
  # @else
  #
  # @endif
  def __str__(self):
    global TIMEVALUE_ONE_SECOND_IN_USECS
    return str(self.tv_sec + self.tv_usec/TIMEVALUE_ONE_SECOND_IN_USECS)

  ##
  # @if jp
  # @brief ���Ƚ��
  #
  # �ݻ����Ƥ������Ƥ�����Ƚ�ꤹ�롣<br>
  #
  # @param self
  #
  # @return ���ʤ��1����ʤ��-1��0�ʤ��0
  #
  # @else
  #
  # @endif
  def sign(self):
    if self.tv_sec > 0:
      return 1
    if self.tv_sec < 0:
      return -1
    if self.tv_usec > 0:
      return 1
    if self.tv_usec < 0:
      return -1
    return 0

  
  ##
  # @if jp
  # @brief ������
  # @else
  # @brief Normalize
  # @endif
  #
  def normalize(self):
    global TIMEVALUE_ONE_SECOND_IN_USECS
    if self.tv_usec >= TIMEVALUE_ONE_SECOND_IN_USECS:
      self.tv_sec += 1
      self.tv_usec -= TIMEVALUE_ONE_SECOND_IN_USECS

      while self.tv_usec >= TIMEVALUE_ONE_SECOND_IN_USECS:
        self.tv_sec += 1
        self.tv_usec -= TIMEVALUE_ONE_SECOND_IN_USECS
        
    elif self.tv_usec <= -TIMEVALUE_ONE_SECOND_IN_USECS:
      self.tv_sec -= 1
      self.tv_usec += TIMEVALUE_ONE_SECOND_IN_USECS

      while self.tv_usec <= -TIMEVALUE_ONE_SECOND_IN_USECS:
        self.tv_sec -= 1
        self.tv_usec += TIMEVALUE_ONE_SECOND_IN_USECS
        
    
    if self.tv_sec >= 1 and self.tv_usec < 0:
      self.tv_sec -= 1
      self.tv_usec += TIMEVALUE_ONE_SECOND_IN_USECS

    elif self.tv_sec < 0 and self.tv_usec > 0:
      self.tv_sec += 1
      self.tv_usec -= TIMEVALUE_ONE_SECOND_IN_USECS
