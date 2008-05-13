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


import OpenRTM

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
    try:
      res = TimeValue()
    except:
      res = OpenRTM.TimeValue()
    
    if self.tv_sec >= tm.tv_sec:
      if self.tv_usec >= tm.tv_usec:
        res.tv_sec  = self.tv_sec  - tm.tv_sec
        res.tv_usec = self.tv_usec - tm.tv_usec
      else:
        res.tv_sec  = self.tv_sec  - tm.tv_sec - 1
        res.tv_usec = (self.tv_usec + 1000000) - tm.tv_usec
    else:
      if tm.tv_usec >= self.tv_usec:
        res.tv_sec  = -(tm.tv_sec  - self.tv_sec)
        res.tv_usec = -(tm.tv_usec - self.tv_usec)
      else:
        res.tv_sec  = -(tm.tv_sec - self.tv_sec - 1)
        res.tv_usec = -(tm.tv_usec + 1000000) + self.tv_usec
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
    if res.tv_usec > 1000000:
      res.tv_sec += 1
      res.tv_usec -= 1000000
    return res

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
    self.tv_sec  = long(time)
    self.tv_usec = long((time - float(self.tv_sec))*1000000)
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
    return float(self.tv_sec) + float(self.tv_usec/1000000.0)


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
    return str(self.tv_sec + self.tv_usec/1000000.0)

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
