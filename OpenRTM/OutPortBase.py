#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file OutPortBase.py
# @brief OutPortBase base class
# @date $Date: 2007/09/19 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
# Copyright (C) 2003-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.



##
# @if jp
#
# @class OutPortBase
# @brief OutPort ���쥯�饹
# 
# OutPort �μ����Ǥ��� OutPort<T> �δ��쥯�饹��
#
# OutPortBase �� PublisherBase �ϰ��� Observer �ѥ������������Ƥ��롣
# OutPortBase �� attach(), detach(), notify() �����
# PublisherBase �� push() �� Observer �ѥ�����˴�Ϣ�����᥽�åɤǤ��롣
#
# @since 0.2.0
#
# @else
#
# @class OutPortBase
# @brief Output port base class.
#
# The base class of OutPort<T> s which are implementations of OutPort  
#
# @endif
class OutPortBase:
  """
  """



  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯����
  #
  # @param self
  # @param name �ݡ���̾
  #
  # @else
  #
  # @brief A constructor of OutPortBase class.
  #
  # Constructor of OutPortBase.
  #
  # @endif
  def __init__(self, name):
    self._name = name
    self._publishers = []


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯����
  # ��Ͽ���줿���Ƥ� Publisher �������롣
  #
  # @param self
  #
  # @else
  #
  # @brief destructor
  #
  # Destructor
  #
  # @endif
  def __del__(self):
    for pub in self._publishers:
      del(pub)


  ##
  # @if jp
  # @brief OutPort̾�Τμ���
  #
  # OutPort��̾�Τ�������롣
  #
  # @param self
  #
  # @return �ݡ���̾��
  #
  # @else
  #
  # @brief OutPort's name
  #
  # This operation returns OutPort's name
  #
  # @endif
  def name(self):
    return self._name


  ##
  # @if jp
  # @brief Publisher���ɲ�
  #
  # ���ꤷ��Publisher��ǡ�������������Ȥ��ƥꥹ�ȤκǸ������ɲä��롣
  # attach_back() ��Ʊ�ͤʵ�ǽ��
  #
  # @param self
  # @param id_ ���ꤵ�줿Publisher�˳�����Ƥ�ID
  # @param publisher ��Ͽ�о�Publisher���֥�������
  #
  # @else
  #
  # @brief Attach a publisher
  #
  # Attach a publisher to observe OutPort.
  #
  # @endif
  def attach(self, id_, publisher):
    self.attach_back(id_, publisher)


  ##
  # @if jp
  # @brief �ꥹ����Ƭ�ؤ�Publisher���ɲ�
  #
  # Publisher��ꥹ�Ȥ���Ƭ���ɲä��롣
  #
  # @param self
  # @param id_ ���ꤵ�줿Publisher�˳�����Ƥ�ID
  # @param publisher ��Ͽ�о�Publisher���֥�������
  #
  # @else
  #
  # @brief Attach a publisher
  #
  # Attach a publisher to the head of the Publisher list.
  #
  # @endif
  def attach_front(self, id_, publisher):
    self._publishers.insert(0, self.Publisher(id_, publisher))


  ##
  # @if jp
  # @brief �ꥹ�ȺǸ����ؤ�Publisher���ɲ�
  #
  # Publisher��ꥹ�ȤκǸ������ɲä��롣
  #
  # @param self
  # @param id_ ���ꤵ�줿Publisher�˳�����Ƥ�ID
  # @param publisher ��Ͽ�о�Publisher���֥�������
  #
  # @else
  #
  # @brief Attach a publisher
  #
  # Attach a publisher to the taile of the Publisher list.
  #
  # @endif
  def attach_back(self, id_, publisher):
    self._publishers.append(self.Publisher(id_, publisher))


  ##
  # @if jp
  # @brief Publisher�κ��
  #
  # ���ꤵ�줿 Publisher ��ǡ�������������ꥹ�Ȥ��������롣
  #
  # @param self
  # @param id_����о� Publisher ��ID
  #
  # @return ����������������ϡ�������� Publisher ���֥�������
  #         ���ꤷ�� Publisher ��¸�ߤ��ʤ����� null
  #
  # @else
  #
  # @brief Detach a publisher
  #
  # Detach a publisher to observe OutPort.
  #
  # @endif
  def detach(self, id_):
    index = -1

    for i in range(len(self._publishers)):
      if id_ == self._publishers[i].id:
        index = i
        break
    if index < 0:
      return None

    pub = self._publishers[index].publisher
    del self._publishers[index]
    return pub


  ##
  # @if jp
  # @brief ����������
  #
  # ��Ͽ����Ƥ������Ƥ� Publisher �˥ǡ������������Τ��롣
  #
  # @param self
  #
  # @else
  #
  # @brief Notify data update
  #
  # This operation notify data update to Publishers
  #
  # @endif
  def notify(self):
    for pub in self._publishers:
      pub.publisher.update()


  ##
  # @if jp
  # @brief Publisher �������������饹
  # @else
  #
  # @endif
  class Publisher:
    def __init__(self, id_, publisher_):
      self.id = id_
      self.publisher = publisher_


