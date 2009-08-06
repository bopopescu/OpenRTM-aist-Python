#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExecutionContext.py
# @brief ExecutionContext class
# @date $Date: 2007-01-21 13:43:18 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#

import OpenRTM_aist
import RTC, RTC__POA

##
# @if jp
#
# @class ExecutionContextBase
# @brief ExecutionContext base class
#
# ExecutionContext �� RTC �Υӥ��ͥ����å��򤽤��¹Ԥ��륹��å�����
# ����ʬΥ���뤳�Ȥ��ǽ�ˤ��롣 ����ƥ����Ȥ�����Ū�ʥ���å������������
# �¹Ի��� RTC ���Ф����󶡤���롣����ƥ����Ȥϼ�Υ��ڥ졼���������
# ���켫�Ȥ���ӥ���ƥ����Ȥ˽�°���� RTC �����ľ��֤��䤤��碌�����ѹ�
# �����ꤹ�뤳�Ȥ��Ǥ��롣
# ���������ط���ʬΥ�ϰʲ�����Ĥ���ͳ�˵����פǤ���
# <ul>
# <li> ¿���Υ���ݡ��ͥ�Ȥϰ�ĤΥΡ��ɤ⤷���ϥץ������̩�ܤ˶�Ĵ
#      �����ǽ��������ޤ��� ���줾��Υ���ݡ��ͥ�ȼ��Ȥ�����å�����
#      ����ľ�硢����åɤ��켫�Ȥο��䥹��å���ߤ�Ʊ�������뤿��ˡ�
#      �ߥɥ륦�����ϥꥢ�륿���ॢ�ץꥱ�������ˤ����롢�ꥢ�륿��������
#      ������Ū���׵�����������Ȥ��Ǥ��ʤ���ǽ��������ޤ���
# <li> ��ĤΥ��ץꥱ�������ϰۤʤ�����Ǽ¹Ԥ����ʣ������Ω������������
#      �¹Ԥ��뤫�⤷��ޤ��󡣤��Ȥ��С����󥵤Υ���ץ�󥰤��ᤤ������
#      �Ԥ��ʤ��顢�桼�����󥿡��ե������ι������٤������ǹԤ����⤷��
#      �ޤ���
# </ul>
#
# <b> �����ʡ����åפȥ���ƥ����Ȥؤν�° </b><br>
# �� ExecutionContext �ϰ�Ĥ� RTC �˽�°���Ƥ��ꡢ���� RTC ����ӡ�
# ���� RTC ����ޤ��� RTC �μ¹Ԥ�ľ��Ū�ޤ�����ľ��Ū�˹Ԥ��� 
# ��İʾ�� ExecutionContext ����� RTC �� autonomous RTC �ȸƤФ�롣
# autonomous RTC ����Ӥ����˴ޤޤ�뤽�Υ��֥��åȤ� RTC (����ϥ��ץꥱ��
# �����ȯ�Ԥˤ���������롣) �� ExecutionKind �˽��äơ��ߥɥ륦����
# �ˤ��¹Ԥ���롣ExecutionKind �Ϥ��줾��� RTC �Υ��ڥ졼�����ϡ�����
# �ɤ����ä����֤Ǽ¹Ԥ��뤫���ꤹ�롣������ RTC �Ϥ��Υ���ƥ����Ȥ�
# �ֽ�°�פ����ɽ������롣���Ѳ�ǽ�� ExecutionKind �ϰʲ��ǽҤ٤롣
# ����Ū�ˤϡ�RTC�� ExecutionContext �δط���¿��¿�Ǥ��뤫�⤷��ʤ���
# ���Ȥ��С�ʣ���� RTC ��Ʊ��� ExecutionContext �ˤ��¹Ԥ��줿�ꡢ
# ��Ĥ� RTC ��ʣ���� ExecutionContext ����¹Ԥ��줿�ꤹ�뤫�⤷��ʤ���
# ʣ����RTC��Ʊ��Υ���ƥ����Ȥ���¹Ԥ������ˤϡ�ExecutionContext ��
# �������Ȥ��뤤�ϥ��ȥåפ������ꤹ�뤳�Ȥˤ�ꡢ��������ƤΥ���ݡ��ͥ��
# �Υ饤�ե���������֤����ܤ������ǽ�������롣
#
# <b> Logical and Physical Threads </b><br>
# ExecutionContext ������Ū����å������ɽ�����Ƥ����ΤΡ�
# �����ɤ���äƶ���Ū�ʥ���åɤ˥ޥåԥ󥰤��뤫�Ȥ��ä�����ϡ�
# ���ץꥱ�������ǥץ����ȴĶ��˰Ѥͤ��Ƥ��롣
# �����˺ݤ��Ƥϴ�Ϣ�դ�����ExecutionContext�ȶ���Ū�ʥ���åɤ���а�
# �ǥޥåԥ󥰤����ꡢ��ĤΥ���åɤ�ʣ���� ExecutionContext �˴�Ϣ�դ�
# ��줿�ꤹ���ǽ�������롣
# RTC ��ʣ���� ExecutionContext �ˤ��¹Ԥ������Υ��󥫥�󥷡�����
# �ϼ�����¸�Ǥ��롣
#
# @else
#
# @class ExecutionContextBase
# @brief ExecutionContext base class
#
# An ExecutionContext allows the business logic of an RTC to be decoupled
# from the thread of control in which it is executed. The context represents
# a logical thread of control and is provided to RTCs at runtime as an
# argument to various operations, allowing them to query and modify their
# own state, and that of other RTCs executing within the same context, in
# the lifecycle.
# This separation of concerns is important for two primary reasons:
# <ul>
# <li> Large number of components may collaborate tightly within a single
#      node or process. If each component were to run within its own thread
#      of control, the infrastructure may not be able to satisfy the
#      timeliness and determinism requirements of real-time applications due
#      to the large number of threads and the required synchronization
#      between them.
# <li> A single application may carry out a number of independent tasks that
#      require different execution rates. For example, it may need to sample
#      a sensor periodically at a very high rate and update a user
#      interface at a much lower rate.
# </ul>
#
# <b> Ownership and Participation </b><br>
# Each execution context is owned by a single RTC and may be used to execute
# that RTC and the RTCs contained within it, directly or indirectly. An RTC
# that owns one or more execution contexts is known as an autonomous RTC.
# An autonomous RTC and some subset of the RTCs within it (to be defined by
# the application developer) shall be executed by the infrastructure
# according to the context's execution kind, which defines when each RTC's
# operations will be invoked when and in which order. These RTCs are said
# to participate in the context. The available execution kinds are described
# below.
# The relationship between RTCs and execution contexts may be many-to-many
# in the general case: multiple RTCs may be invoked from the same execution
# context, and a single RTC may be invoked from multiple contexts.
# In the case where multiple RTCs are invoked from the same context,
# starting or stopping the context shall result in the corresponding
# lifecycle transitions for all of those components.
#
# <b> Logical and Physical Threads </b><br>
# Although an execution context represents a logical thread of control,
# the choice of how it maps to a physical thread shall be left to the
# application��s deployment environment. Implementations may elect to
# associate contexts with threads with a one-to-one mapping, to serve
# multiple contexts from a single thread, or by any other means. In the
# case where a given RTC may be invoked from multiple contexts, concurrency
# management is implementation-dependent.
#
# @endif
#
class ExecutionContextBase(RTC__POA.ExecutionContextService):
    
    #
    # @if jp
    # @brief ���󥹥ȥ饯��
    # @else
    # @brief Constructor
    # @endif
    #
    def __init__(self,owner):
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("exec_cxt")
        self._running = False
        self._profile = RTC.ExecutionContextProfile(RTC.OTHER,0.0,owner,[])



    ##
    # @if jp
    # @brief �ǥ��ȥ饯��
    # @else
    # @brief Destructor
    # @endif
    #
    def __del__(self):
        pass


    #============================================================
    # ExecutionContext interfaces
    #============================================================
    ##
    # @if jp
    # @brief ExecutionContext ���¹��椫�ɤ����Υƥ���
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼�����Ϥ��� ExecutionContext �μ¹Ծ��֤��֤���
    #
    # <h3> Semantics </h3>
    # ���Υ���ƥ����Ȥ� Running ���֤Ǥ���С����ƤΥ����ƥ��֤� RTC ��
    # ���å���ݡ��ͥ�Ȥϥ���ƥ����Ȥ� ExecutionKind �˽��äƼ¹Ԥ���롣
    #
    # @return �¹Ծ��֤Ǥ���� true ���֤���
    #
    # @else
    #
    # @brief Test for ExecutionContext running state
    #
    # <h3>Description</h3>
    # This operation shall return true if the context is in the Running state.
    #
    # <h3> Semantics </h3>
    # While the context is Running, all Active RTCs participating in the
    # context shall be executed according to the context's execution kind.
    #
    # @return If the ExecutionContext is running, it returns true.
    #
    # @endif
    #
    # virtual CORBA::Boolean is_running();
    def is_running(self):
        self._rtcout.RTC_TRACE("is_running()")
        return self._running


    ##
    # @if jp
    #
    # @brief ExecutionContext �򥹥����Ȥ�����
    #
    # <h3> Description </h3>
    #  ExecutionContext �� Running ���֤����ܤ����뤿��Υ��ڥ졼�����
    # �������ܤ�ȯ��������硢ComponentAction::on_startup ���¹Ԥ���롣
    # (OMG RTC Specification section 2.2.2.5.2 �򻲾�)
    #
    # <h3> Semantics </h3>
    # ExecutionContext ���Ф��� start ����� stop �Ϸ����֤��¹Ԥ���롣
    #
    # <h3> Constraints </h3>
    # @return ���Υ��ڥ졼������ ExecutionContext �� Stopped ���֤ˤʤ��Ȥ�
    #         �¹Ԥ����ȡ�PRECONDITION_NOT_MET ���֤���롣
    #
    # @else
    #
    # @brief Start the ExecutionContext
    #
    # <h3> Description </h3>
    # Request that the context enter the Running state. Once the state
    # transition occurs, the ComponentAction::on_startup operation
    # (see OMG RTC Specification section 2.2.2.5.2) will be invoked.
    #
    # <h3> Semantics </h3>
    # An execution context may be started and stopped multiple times.
    #
    # <h3> Constraints </h3>
    # @return This operation shall fail with PRECONDITION_NOT_MET if the
    #         context is not in the Stopped state.
    #
    # @endif
    #
    # virtual ReturnCode_t start();
    def start(self):
        self._rtcout.RTC_TRACE("start()")
        return RTC.RTC_OK


    ##
    # @if jp
    #
    # @brief ExecutionContext �򥹥ȥåפ�����
    #  
    # <h3> Description </h3>
    #  ExecutionContext �� Stopped ���֤����ܤ����뤿��Υ��ڥ졼�����
    # �������ܤ�ȯ��������硢ComponentAction::on_shutdown ���¹Ԥ���롣
    # (OMG RTC Specification section 2.2.2.5.4 �򻲾�)
    #
    # <h3> Semantics </h3>
    # ExecutionContext ���Ф��� start ����� stop �Ϸ����֤��¹Ԥ���롣
    #
    # <h3> Constraints </h3>
    # @return ���Υ��ڥ졼������ ExecutionContext �� Stopped ���֤ˤʤ��Ȥ�
    #         �¹Ԥ����ȡ�PRECONDITION_NOT_MET ���֤���롣
    #
    # @else
    # @brief Stop the ExecutionContext
    #
    # <h3> Description </h3>
    # Request that the context enter the Stopped state. Once the transition
    # occurs, the ComponentAction::on_shutdown operation
    # (see OMG RTC Specification section 2.2.2.5.4) will be invoked.
    #
    # <h3> Semantics </h3>
    # An execution context may be started and stopped multiple times.
    #
    # <h3> Constraints </h3>
    # @return This operation shall fail with PRECONDITION_NOT_MET if the
    #         context is not in the Stopped state.
    #
    # @endif
    #
    # virtual ReturnCode_t stop();
    def stop(self):
        self._rtcout.RTC_TRACE("stop()")
        return RTC.RTC_OK


    ##
    # @if jp
    #
    # @brief �¹Լ���(Hz)���������
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼�����Ϥ��Υ���ƥ����Ȥ˻��ä��Ƥ��륢���ƥ��֤�RTC
    # �μ¹Ԥ���������Hz���֤���
    #
    # <h3> Semantics </h3>
    # �����ˤ����Ƥ� PERIODIC �ʳ��� ExecutionKind ����Ĥ����μ���Ū
    # �⤷���ϵ�������Ū�ʽ�����������뤳�Ȥ������ޤ������ξ��ˤϡ�
    # ���Υ��ڥ졼�����η�̤ϼ�������˽����ޤ���
    # �⤷������ExecutionContext������Ū������Ԥ�ʤ�����ƥ����ȤǤ����硢
    # ���Υ��ڥ졼�����ϼ��Ԥ��ޤ���
    #
    # <h3> Constraints </h3>
    # @return ����ExecutionContext �� ExecutionKind �� PERIODIC�Ǥ���С�
    #         0����礭���ͤ��֤���
    #
    # @else
    #
    # @brief Get executionrate(Hz)
    #
    # <h3> Description </h3>
    # This operation shall return the rate (in hertz) at which its Active
    # participating RTCs are being invoked.
    #
    # <h3> Semantics </h3>
    # An implementation is permitted to perform some periodic or
    # quasi-periodic processing within an execution context with an
    # ExecutionKind other than PERIODIC. In such a case, the result of this
    # operation is implementation-defined.
    # If no periodic processing of any kind is taking place within the
    # context, this operation shall fail as described in section 2.2.1 above.
    #
    # <h3> Constraints </h3>
    # @return If the context has an ExecutionKind of PERIODIC, this operation
    #         shall return a rate greater than zero.
    #
    # @endif
    #
    # virtual CORBA::Double get_rate();
    def get_rate(self):
        self._rtcout.RTC_TRACE("get_rate()")
        return self._profile.rate


    ##
    # @if jp
    #
    # @brief �¹Լ���(Hz)��Ϳ���� 
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼�����Ϥ��Υ���ƥ����Ȥ����ĥ����ƥ��֤�RTC��¹Ԥ���
    # ������Ϳ���롣
    #
    # <h3> Semantics </h3>
    # ���� ExecutionContext �� ExecutionKind �� PERIODIC �Ǥ����硢
    # �¹Լ������ѹ���ȼ�������� ExecutionContext �˻��ä��� RTC �Ȥ���
    # ��Ͽ����Ƥ��� DataFlowComponentAction ��������� RTC �Υ��ڥ졼�����
    # on_rate_changed ��¹Ԥ��롣
    # �����ˤ����Ƥ� PERIODIC �ʳ��� ExecutionKind ����Ĥ����μ���Ū
    # �⤷���ϵ�������Ū�ʽ�����������뤳�Ȥ������ޤ����ä��Ƥ��μ�����
    # �����Ƽ����� get_rate �ˤ������Ǥ�����ˤϡ��⤷Ϳ����줿������
    # ͭ���ʼ����Ǥ���С����Υ��ڥ졼�����ϼ��������ꤹ���ΤȤ��ޤ���
    # �⤷������ExecutionContext������Ū������Ԥ�ʤ�����ƥ����ȤǤ����硢
    # ���Υ��ڥ졼������ ReturnCode_t::UNSUPPORTED ���֤��Ƽ��Ԥ��ޤ���
    #
    # <h3> Constraints </h3>
    # @return Ϳ�����������0����礭���ʤ���Фʤ餺�������Ǥʤ����
    #         ���Υ��ڥ졼������ ReturnCode_t::BAD_PARAMETER ���֤���
    #
    # @else
    #
    # @brief Set rate (Hz)
    #
    # <h3> Description </h3>
    # This operation shall set the rate (in hertz) at which this context's
    # Active participating RTCs are being called.
    #
    # <h3> Semantics </h3>
    # If the execution kind of the context is PERIODIC, a rate change shall
    # result in the invocation of on_rate_changed on any RTCs realizing
    # DataFlowComponentAction that are registered with any RTCs participating
    # in the context.
    # An implementation is permitted to perform some periodic or
    # quasi-periodic processing within an execution context with an
    # ExecutionKind other than PERIODIC. If such is the case, and the
    # implementation reports a rate from get_rate, this operation shall set
    # that rate successfully provided that the given rate is valid. If no
    # periodic processing of any kind is taking place within the context,
    # this operation shall fail with ReturnCode_t::UNSUPPORTED.
    #
    # <h3> Constraints </h3>
    # @return The given rate must be greater than zero. Otherwise, this
    #         operation shall fail with ReturnCode_t::BAD_PARAMETER.
    #
    # @endif
    #
    # virtual ReturnCode_t set_rate(CORBA::Double rate);
    def set_rate(self, rate):
        self._rtcout.RTC_TRACE("set_rate()")
        if rate > 0.0:
            self._profile.rate = rate
            return RTC.RTC_OK

        return RTC.BAD_PARAMETER
        


    ##
    # @if jp
    #
    # @brief ����ݡ��ͥ�Ȥ򥢥��ƥ��ֲ�����
    #
    # <h3> Description </h3>
    # Ϳ������ RTC �Ϥ��Υ���ƥ����Ȥˤ����� Inactive �Ǥ��ꡢ���ä�
    # ExecutionContext �� ExecutionKind �˽��äƼ¹Ԥ���Ƥ��ʤ���
    # ���Υ��ڥ졼�����ˤ�äƤ��� RTC �Ϥ��� ExecutionContext �ˤ�ä�
    # �¹Ԥ���� Active ���֤����ܤ��롣
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> ExecutionContext �Ϥ��켫�Ȥ˻��ä��Ƥ��륳��ݡ��ͥ�Ȥ��� Active
    #      ���Ǥ��ʤ��Τǡ��⤷Ϳ����줿RTC�����Υ���ƥ����Ȥ˻��ä��Ƥ���
    #      ����С����Υ��ڥ졼������ BAD_PARAMETER ���֤��Ƽ��Ԥ��롣
    # <li> Error ���֤ˤ��� RTC �� reset ���ʤ���� Active ���Ǥ��ʤ���
    #      �⤷Ϳ����줿 RTC �� Error ���֤ˤ����硢���Υ��ڥ졼������
    #      PRECONDITION_NOT_MET ���֤��Ƽ��Ԥ��롣
    # </ul>
    # @return OK, BAD_PARAMETER �⤷���� PRECONDITION_NOT_MET ���֤���
    #
    # @else
    #
    # @brief Activate a component
    # 
    # <h3> Description </h3>
    # The given participant RTC is Inactive and is therefore not being invoked
    # according to the execution context's execution kind. This operation
    # shall cause the RTC to transition to the Active state such that it may
    # subsequently be invoked in this execution context.
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> An execution context can only activate its participant components.
    #      If the given RTC is not participating in the execution context,
    #      this operation shall fail with BAD_PARAMETER.
    # <li> An RTC that is in the Error state cannot be activated until after
    #      it has been reset. If the given RTC is in the Error state, this
    #      operation shall fail with PRECONDITION_NOT_MET.
    # </ul>
    # @return This operation returns OK, BAD_PARAMETER or PRECONDITION_NOT_MET
    #
    # @endif
    #
    # virtual ReturnCode_t activate_component(LightweightRTObject_ptr comp);
    def activate_component(self, comp):
        self._rtcout.RTC_TRACE("activate_component()")
        return RTC.RTC_OK


    ##
    # @if jp
    #
    # @brief ����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
    #
    # <h3> Description </h3>
    # Ϳ������ RTC �Ϥ��Υ���ƥ����Ȥ���� Active ���֤Ǥ��롣
    # ���Υ��ڥ졼�����ˤ�äƤ��� RTC �� Inactive ���֤����ܤ��롣
    # Inactive ���֤Ǥ� Active �������ޤ� RTC �ϼ¹Ԥ���ʤ���
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> ExecutionContext �ϼ��Ȥ˽�°���륳��ݡ��ͥ�ȤΤ��󥢥��ƥ��ֲ�
    #      �Ǥ��롣�⤷��Ϳ����줿 RTC ������ ExecutionContext �˽�°���Ƥ�
    #      �ʤ���� BAD_PARAMETER ���֤��Ƽ��Ԥ��롣
    # </ul>
    # @return OK, BAD_PARAMETER ���֤���
    #
    # @else
    #
    # @brief Deactivate a component
    #
    # <h3> Description </h3>
    # The given RTC is Active in the execution context. Cause it to transition
    # to the Inactive state such that it will not be subsequently invoked from
    # the context unless and until it is activated again.
    #  
    # <h3> Constraints </h3>
    # <ul>
    # <li> An execution context can only deactivate its participant
    #      components. If the given RTC is not participating in the execution
    #      context, this operation shall fail with BAD_PARAMETER.
    # </ul>
    # @return This operation returns OK or BAD_PARAMETER.
    #
    # @endif
    #
    # virtual ReturnCode_t deactivate_component(LightweightRTObject_ptr comp);
    def deactivate_component(self, comp):
        self._rtcout.RTC_TRACE("deactivate_component()")
        return RTC.RTC_OK

    ##
    # @if jp
    #
    # @brief ����ݡ��ͥ�Ȥ�ꥻ�åȤ���
    #
    # <h3> Description </h3>
    # Ϳ������ RTC �Ϥ��Υ���ƥ����Ȥ���� Error �ޤ��� Active ���֤Ǥ��롣
    # ���Υ��ڥ졼�����ˤ�äƤ��� RTC �� Inactive ���֤����ܤ��롣
    # Inactive ���֤Ǥ� Active �������ޤ� RTC �ϼ¹Ԥ���ʤ���
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> ExecutionContext �ϼ��Ȥ˽�°���륳��ݡ��ͥ�ȤΤ��󥢥��ƥ��ֲ�
    #      �Ǥ��롣�⤷��Ϳ����줿 RTC ������ ExecutionContext �˽�°���Ƥ�
    #      �ʤ���� BAD_PARAMETER ���֤��Ƽ��Ԥ��롣
    # </ul>
    # @return OK, BAD_PARAMETER ���֤���
    #
    # @else
    #
    # @brief Deactivate a component
    #
    # <h3> Description </h3>
    # The given RTC is Error or Active in the execution context. Cause it to
    # transition to the Inactive state such that it will not be subsequently
    # invoked from the context unless and until it is activated again.
    #  
    # <h3> Constraints </h3>
    # <ul>
    # <li> An execution context can only deactivate its participant
    #      components. If the given RTC is not participating in the execution
    #      context, this operation shall fail with BAD_PARAMETER.
    # </ul>
    # @return This operation returns OK or BAD_PARAMETER.
    #
    # @endif
    #
    # virtual ReturnCode_t reset_component(LightweightRTObject_ptr comp);
    def reset_component(self, comp):
        self._rtcout.RTC_TRACE("reset_component()")
        return RTC.RTC_OK


    ##
    # @if jp
    #
    # @brief ����ݡ��ͥ�Ȥξ��֤��������
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼������Ϳ����줿 RTC �� LifeCycleState ���֤���
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> RTC �� Alive���֤Ǥʤ���Фʤ�ʤ���
    # <li> Ϳ������ RTC �� ExecutionContext �˽�°���Ƥ��ʤ���Фʤ�ʤ���
    # </ul>
    # @return LifeCycleState::INACTIVE, ACTIVE, ERROR ���֤���
    #
    # @else
    #
    # @brief Get component's state
    #
    # <h3> Description </h3>
    # This operation shall report the LifeCycleState of the given participant
    # RTC.
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> The given RTC must be Alive.
    # <li> The given RTC must be a participant in the target ExecutionContext.
    # <li> The LifeCycleState returned by this operation shall be one of
    #      LifeCycleState::INACTIVE, ACTIVE, or ERROR.
    # </ul>
    # @return The LifeCycleState returned by this operation shall be one of
    #         LifeCycleState::INACTIVE, ACTIVE, or ERROR.
    # @endif
    #
    # virtual LifeCycleState get_component_state(LightweightRTObject_ptr comp);
    def get_component_state(self, comp):
        self._rtcout.RTC_TRACE("get_component_state()")
        return RTC.INACTIVE_STATE


    ##
    # @if jp
    #
    # @brief ExecutionKind ���������
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼������ ExecutionContext �� ExecutionKind ���֤���
    #
    # <h3> ExecutionKind </h3>
    # ExecutionKind ���Ҥ� ExecutionContext ��°���� Execution ��
    # ���ޥ�ƥ����� (OMG RTC Specification section 2.3 �򻲾�) ��������롣
    # <table>
    # <tr><td> PERIODIC </td>
    #     <td> ���Υ����פ� ExecutionContext ��°���� RTC ��
    #          periodic sampled data ���ޥ�ƥ������˽��äƼ¹�
    #          ����롣(OMG RTC Specification section 2.3.1 �򻲾�)</td>
    # </tr>
    # <tr><td> EVENT_DRIVEN </td>
    #     <td> ���Υ����פ� ExecutionContext ��°���� RTC ��
    #          stimulus response ���ޥ�ƥ������˽��äƼ¹Ԥ���롣
    #          (OMG RTC Specification section 2.3.2 �򻲾�) </td>
    # </tr>
    # <tr><td> OTHER </td>
    #     <td> ���Υ����פ� ExecutionContext ��°���� RTC ��
    #          ���μ¹ԥ��ޥ�ƥ������ϼ����Ԥ�Ǥ�դ˼����Ǥ���
    #          ���;�ϤȤ����������Ƥ��ʤ���</td>
    # </tr>
    # </table>
    #
    # @else
    #
    # @brief Get the ExecutionKind
    #
    # <h3> Description </h3>
    # This operation shall report the execution kind of the execution context.
    #
    # <h3> ExecutionKind </h3>
    # The ExecutionKind enumeration defines the execution semantics
    # (see OMG RTC Specification section 2.3) of the RTCs that participate
    # in an execution context.
    # <table>
    # <tr><td> PERIODIC </td>
    #     <td> The participant RTCs are executing according to
    #          periodic sampled data semantics
    #          (see OMG RTC Specification section 2.3.1). </td>
    # </tr>
    # <tr><td> EVENT_DRIVEN </td>
    #     <td>  The participant RTCs are executing according to
    #           stimulus response semantics
    #           (see OMG RTC Specification section 2.3.2).</td>
    # </tr>
    # <tr><td> OTHER </td>
    #     <td> The participant RTCs are executing according to some
    #          semantics not defined by this specification.</td>
    # </tr>
    # </table>
    # @endif
    #
    # virtual ExecutionKind get_kind();
    def get_kind(self):
        self._rtcout.RTC_TRACE("get_kind()")
        return self._profile.kind


    ##
    # @if jp
    #
    # @brief ����ݡ��ͥ�Ȥ��ɲä���
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼������Ϳ����줿RTC�򤳤�ExecutionContext�˽�°�����롣
    #
    # <h3> Semantics </h3>
    # �������ɲä��줿��RTC �ϤϤ���ϡ�Inactive ���֤ˤ��롣
    # ExecutionKind �� PERIODIC �ʤ�а��� index �Ϥ��� RTC ���¹Ԥ����
    # ���֤ˤ����륽���Ȥ��줿���֤���ꤹ�롣
    # ����ʳ��Ǥϡ�������¸�Ǥ���̵�뤵��뤫�⤷��ʤ���
    #
    # <h3> Constraints </h3>
    # <ul>
    # <li> ExecutionKind �� PERIODIC �ξ��, RTC �� data flow participant
    #      (OMG RTC Specification section 2.3.1.2 �򻲾�) �Ǥʤ���Фʤ�ʤ���
    #      ����ʳ��ϡ����Υ��ڥ졼������ PRECONDITION_NOT_MET
    #      ���֤����Ԥ��롣.
    # </ul>
    # @return OK or PRECONDITION_NOT_ME ���֤����
    #
    # @else
    #
    # @brief Add a component
    #
    # The operation causes the given RTC to begin participating in the
    # execution context.
    #
    # The newly added RTC will begin in the Inactive state.
    # If the ExecutionKind is PERIODIC, the index represents the sorted order
    # in which the RTC is to be executed. Otherwise, the meaning of the index
    # is implementation-defined and may be ignored.
    # <p>
    # <h3> Constraints </h3>
    # <ul>
    # <li> If the ExecutionKind is PERIODIC, the RTC must be a data flow
    #      participant (see OMG RTC Specification section 2.3.1.2).
    #      Otherwise, this operation will fail with PRECONDITION_NOT_MET.
    # </ul>
    # @return OK or PRECONDITION_NOT_ME would be returned.
    # </p>
    # @endif
    #
    # virtual ReturnCode_t add_component(LightweightRTObject_ptr comp);
    def add_component(self, comp):
        self._rtcout.RTC_TRACE("add_component()")
        if CORBA.is_nil(comp):
            self._profile.participants.append(comp._narrow(RTC.RTObject))
            return RTC.RTC_OK

        return RTC.BAD_PARAMETER

    ##
    # @if jp
    #
    # @brief ����ݡ��ͥ�Ȥ򥳥�ݡ��ͥ�ȥꥹ�Ȥ���������
    # 
    # <h3> Description </h3>
    # ���Υ��ڥ졼�����Ͻ�°���Ƥ��� RTC ���°�������ä��롣
    # <b> Constraints </b>
    # <ul>
    # <li> �⤷Ϳ����줿 RTC �����Υ���ƥ����Ȥ˻��ä��Ƥ��ʤ����ˤϡ�
    #      ���Υ��ڥ졼������ BAD_PARAMETER ���֤���
    # <li> RTC �򤳤� ExecutionContext �ν�°����Ϥ������ˤϡ�
    #      RTC ���󥢥��ƥ��ֲ����ʤ���Фʤ�ʤ���
    #      Ϳ����줿 RTC �� ExecutionContext �˽�°���Ƥ����ΤΡ�
    #      Active ���֤ˤ�����ˤϡ�PRECONDITION_NOT_MET ���֤���
    # </ul>
    #
    # @else
    #
    # @brief Remove the component from component list
    #
    # <h3> Description </h3>
    # This operation causes a participant RTC to stop participating in the
    # execution context.
    # 
    # <h3> Constraints </h3>
    # <ul>
    # <li> If the given RTC is not currently participating in the execution
    #      context, this operation shall fail with BAD_PARAMETER.
    # <li> An RTC must be deactivated before it can be removed from an
    #      execution context. If the given RTC is participating in the
    #      execution context but is still in the Active state, this operation
    #      shall fail with PRECONDITION_NOT_MET.
    # </ul>
    # @endif
    #			     
    # virtual ReturnCode_t remove_component(LightweightRTObject_ptr comp);
    def remove_component(self, comp):
        self._rtcout.RTC_TRACE("remove_component()")
        index = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.participants,
                                                self.find_objref(comp._narrow(RTC.RTObject)))

        if index < 0:
            return RTC.BAD_PARAMETER

        del self._profile.participants[index]
        return RTC.RTC_OK


    #============================================================
    # ExecutionContextAdmin interfaces
    #============================================================
    ##
    # @if jp
    #
    # @brief ExecutionContextProfile ���������
    #
    # <h3> Description </h3>
    # ���Υ��ڥ졼������ ExecutionContext �� Profile ���������
    #
    # @else
    #
    # @brief Get the ExecutionContextProfile
    #
    # <h3> Description </h3>
    # This operation provides a profile descriptor for the execution context.
    #
    # @endif
    #
    # virtual ExecutionContextProfile* get_profile();
    def get_profile(self):
        self._rtcout.RTC_TRACE("get_profile()")
        return self._profile


    class find_objref:
        def __init__(self, ref):
            self._ref = ref

        def __call__(self, ref):
            return ref._is_equivalent(self._ref)
