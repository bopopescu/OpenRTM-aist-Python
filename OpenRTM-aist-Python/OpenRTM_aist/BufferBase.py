#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file BufferBase.py
# @brief Buffer abstract class
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



##
# @if jp
# @class BufferBase
# @brief BufferBase ��ݥ��饹
# 
# ��ΥХåե��Τ������ݥ��󥿡��ե��������饹��
# ��ݥХåե����饹�ϡ��ʲ��δؿ��μ������󶡤��ʤ���Фʤ�ʤ���
# 
# public���󥿡��ե������Ȥ��ưʲ��Τ�Τ��󶡤��롣
#  - write(): �Хåե��˽񤭹���
#  - read(): �Хåե������ɤ߽Ф�
#  - length(): �Хåե�Ĺ���֤�
#  - isFull(): �Хåե������դǤ���
#  - isEmpty(): �Хåե������Ǥ���
# 
# protected���󥿡��ե������Ȥ��ưʲ��Τ�Τ��󶡤��롣
#  - put(): �Хåե��˥ǡ�����񤭹���
#  - get(): �Хåե�����ǡ������ɤ߽Ф�
# 
# @since 0.4.0
# 
# @else
# 
# @class BufferBase
# @brief BufferBase abstract class
# 
# This is the abstract interface class for various Buffer.
# 
# @since 0.4.0
# 
# @endif
class BufferBase:
  """
  """


  ##
  # @if jp
  # 
  # @brief �Хåե���Ĺ�����������(���֥��饹������)
  # 
  # �Хåե�Ĺ���������<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # 
  # @return �Хåե�Ĺ
  # 
  # @else
  # 
  # @brief Get the buffer length
  # 
  # @return buffer length
  # 
  # @endif
  def length(self):
    pass


  ##
  # @if jp
  # 
  # @brief �Хåե��˥ǡ�����񤭹���(���֥��饹������)
  # 
  # �Хåե��˥ǡ�����񤭹���<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # @param value �񤭹����оݥǡ���
  # 
  # @return �ǡ����񤭹��߷��(true:�񤭹���������false:�񤭹��߼���)
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def write(self, value):
    pass


  ##
  # @if jp
  # 
  # @brief �Хåե�����ǡ������ɤ߽Ф�(���֥��饹������)
  # 
  # �Хåե�����ǡ������ɤ߽Ф�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # @param value �ɤ߽Ф��ǡ���
  # 
  # @return �ǡ����ɤ߽Ф����(true:�ɤ߽Ф�������false:�ɤ߽Ф�����)
  # 
  # @else
  # 
  # @brief Read data from the buffer
  # 
  # @endif
  def read(self, value):
    pass


  ##
  # @if jp
  # 
  # @brief �Хåե�full�����å�(���֥��饹������)
  # 
  # �Хåե�full�����å��Ѵؿ�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # 
  # @return full�����å����(true:�Хåե�full��false:�Хåե���������)
  # 
  # @else
  # 
  # @brief True if the buffer is full, else false.
  # 
  # @endif
  def isFull(self):
    pass


  ##
  # @if jp
  # 
  # @brief �Хåե�empty�����å�(���֥��饹������)
  # 
  # �Хåե�empty�����å��Ѵؿ�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # 
  # @return empty�����å����(true:�Хåե�empty��false:�Хåե��ǡ�������)
  # 
  # @else
  # 
  # @brief True if the buffer is empty, else false.
  # 
  # @endif
  def isEmpty(self):
    pass


  ##
  # @if jp
  # 
  # @brief �Хåե��˥ǡ������Ǽ����(���֥��饹������)
  # 
  # �Хåե��ؤΥǡ�����Ǽ�Ѵؿ�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # @param data �оݥǡ���
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def put(self, data):
    pass


  ##
  # @if jp
  # 
  # @brief �Хåե�����ǡ������������(���֥��饹������)
  # 
  # �Хåե��˳�Ǽ���줿�ǡ��������Ѵؿ�<BR>
  # �����֥��饹�Ǥμ���������
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
    pass


  ##
  # @if jp
  # 
  # @brief ���˽񤭹���Хåե��ؤλ��Ȥ��������(���֥��饹������)
  # 
  # �񤭹��ߥХåե��ؤλ��ȼ����Ѵؿ�<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self 
  # 
  # @return ���ν񤭹����оݥХåե��ؤλ���
  # 
  # @else
  # 
  # @brief Get the buffer's reference to be written the next
  # 
  # @endif
  def getRef(self):
    pass


##
# @if jp
# @class NullBuffer
# @brief ���ߡ��Хåե��������饹
# 
# �Хåե�Ĺ��������Υ��ߡ��Хåե��������饹��
# 
# @param DataType �Хåե��˳�Ǽ����ǡ�����
# 
# @since 0.4.0
# 
# @else
# 
# @endif
class NullBuffer(BufferBase):
  """
  """



  ##
  # @if jp
  # 
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # �Хåե�Ĺ��(����)�ǽ�������롣
  # 
  # @param self 
  # @param size �Хåե�Ĺ(�ǥե������:None��������̵��)
  # 
  # @else
  # 
  # @endif
  def __init__(self, size=None):
    if size is None:
      size=1
    self._length = 1
    self._data = None
    self._is_new = False
    self._inited = False


  ##
  # @if jp
  # 
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  # 
  # @param self 
  # @param data ��Ǽ�ǡ���
  # 
  # @else
  # 
  # @endif
  def init(self, data):
    self.put(data)


  ##
  # @if jp
  # 
  # @brief �Хåե��ν����
  # 
  # �Хåե��ν������¹Ԥ��롣
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
  # @brief �Хåե�Ĺ(������)���������
  # 
  # �Хåե�Ĺ��������롣(��ˣ����֤���)
  # 
  # @param self 
  # 
  # @return �Хåե�Ĺ(������)
  # 
  # @else
  # 
  # @brief Get the buffer length
  # 
  # @return buffer length(always 1)
  # 
  # @endif
  def length(self):
    return 1


  ##
  # @if jp
  # 
  # @brief �Хåե��˥ǡ�����񤭹���
  # 
  # ������Ϳ����줿�ǡ�����Хåե��˽񤭹��ࡣ
  # 
  # @param self 
  # @param value �񤭹����оݥǡ���
  # 
  # @return �ǡ����񤭹��߷��(true:�񤭹���������false:�񤭹��߼���)
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
  # @brief �Хåե�����ǡ������ɤ߽Ф�
  # 
  # �Хåե��˳�Ǽ���줿�ǡ������ɤ߽Ф���
  # 
  # @param self 
  # @param value �ɤ߽Ф����ǡ���
  # 
  # @return �ǡ����ɤ߽Ф����(true:�ɤ߽Ф�������false:�ɤ߽Ф�����)
  # 
  # @else
  # 
  # @brief Read data from the buffer
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
  # @brief �Хåե�full�����å�
  # 
  # �Хåե�full������å����롣(���false���֤���)
  # 
  # @param self 
  # 
  # @return full�����å����(���false)
  # 
  # @else
  # 
  # @brief Always false.
  # 
  # @endif
  def isFull(self):
    return False


  ##
  # @if jp
  # 
  # @brief �Хåե�empty�����å�
  # 
  # �Хåե�empty������å����롣(���false���֤���)
  # ���׳�ǧ
  # 
  # @param self 
  # 
  # @return empty�����å����(���false)
  # 
  # @else
  # 
  # @brief Always false.
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
  #            ( true:�ǿ��ǡ������ǡ����Ϥޤ��ɤ߽Ф���Ƥ��ʤ�
  #             false:���Υǡ������ǡ����ϴ����ɤ߽Ф���Ƥ���)
  # 
  # @else
  # 
  # @endif
  def isNew(self):
    return self._is_new


  ##
  # @if jp
  # 
  # @brief �Хåե��˥ǡ������Ǽ
  # 
  # ������Ϳ����줿�ǡ�����Хåե��˳�Ǽ���롣
  # 
  # @param self 
  # @param data �оݥǡ���
  # 
  # @else
  # 
  # @brief Write data into the buffer
  # 
  # @endif
  def put(self, data):
    self._data = data
    self._is_new = True
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
    self._is_new = False
    return self._data


  ##
  # @if jp
  # 
  # @brief ���˽񤭹���Хåե��ؤλ��Ȥ��������
  # 
  # �񤭹��ߥХåե��ؤλ��Ȥ�������롣
  # �ܥХåե������ǤϥХåե�Ĺ�ϸ���ǣ��Ǥ��뤿�ᡤ
  # ���Ʊ�����֤ؤλ��Ȥ��֤���
  # 
  # @param self 
  # 
  # @return ���ν񤭹����оݥХåե��ؤλ���(����)
  # 
  # @else
  # 
  # @brief Get the buffer's reference to be written the next
  # 
  # @endif
  def getRef(self):
    return self._data
