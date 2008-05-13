#!/usr/bin/env python 
# -*- coding: euc-jp -*-

##
# @file PublisherBase.py
# @brief Publisher base class
# @date $Date: 2007/09/05$
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
# @class PublisherBase
#
# @brief Publisher ���쥯�饹
# 
# �ǡ������Х����ߥ󥰤�����������Ф��ư����Publisher* �δ��쥯�饹��
# �Ƽ� Publisher �Ϥ��Υ��饹��Ѿ����ƾܺ٤�������롣
#
# @since 0.4.0
#
# @else
#
# @class PublisherBase
#
# @brief Base class of Publisher.
#
# A base class of Publisher*.
# Variation of Publisher* which implements details of Publisher
# inherits this PublisherBase class.
#
# @endif
class PublisherBase:
  """
  """



  ##
  # @if jp
  #
  # @brief ���Х����ߥ󥰤����Τ��롣(���֥��饹������)
  #
  # ���Ф��Ԥĥ��֥������Ȥˡ����Х����ߥ󥰤����Τ��뤿��δؿ���<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self
  # 
  # @else
  #
  # @endif
  def update(self):
    pass


  ##
  # @if jp
  #
  # @brief Publisher ���˴����롣(���֥��饹������)
  #
  # ���� Publisher ���˴����롣
  # ���� Publisher �����פˤʤä����� PublisherFactory ����ƤӽФ���롣<BR>
  # �����֥��饹�Ǥμ���������
  # 
  # @param self
  #
  # @else
  #
  # @endif
  def release(self):
    pass
