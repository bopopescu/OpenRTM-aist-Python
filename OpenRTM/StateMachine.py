#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file StateMachine.py
 \brief State machine template class
 \date $Date: 2007/08/30$
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import threading

import OpenRTM
import RTC, RTC__POA

class ScopedLock:
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()
		

class StateHolder:
	def __init__(self):
		self.curr = None
		self.prev = None
		self.next = None



class StateMachine:
	"""
	\if jp
	\class StateMachine
	\brief ���֥ޥ��󥯥饹
	StateMachine ���饹�Ͼ��֥ޥ����¸����륯�饹�Ǥ��롣
	��: ActiveObject�Ͼ��֥ޥ������ĥ����ƥ��֥��֥������ȤǤ���Ȥ��롣
	���֤�3���� INACTIVE, ACTIVE, ERROR ���ꡢ�ƾ��֤Ǥ�Entry��Exitư���
	����������Ȥ���ȡ��ʲ��Τ褦�˼¸�����롣
	<pre>
	class ActiveObject 
	{  
	public: 
	  enum MyState { INACTIVE, ACTIVE, ERROR }; 
	  typedef States<MyState> MyStates; 

	  ActiveObject() 
		: m_sm(3) 
	  { 
		m_sm.setNOP(&ActiveObject::nullAction); 
		m_sm.setListener(this); 

		m_sm.setExitAction(NACTIVE, &ActiveObject::inactiveExit); 
		  : 
		m_sm.setPostDoAction(ERROR, &ActiveObject::errorPostDo); 
		m_sm.setTransitionAction(&ActiveObject:tratransitionnsition); 
	  }; 

	  bool nullAction(MyStates st) {}; 
	  bool inactiveExit(MyStates st) {}; 
		: 
	  bool errorPostDo(MyStates st) {}; 
	  bool transition(MyStates st) {}; 

	private: 
	  StateMachine<MyState, bool, ActiveObject> m_sm; 
	}; 
	</pre>
	���֤�������������饹�ϰʲ��ξ����������褦�˼������ʤ���Фʤ�ʤ���
	<ol>
	<li> enum �Ǿ��֤����
	<li> StateMachine �Υƥ�ץ졼�Ȱ����ϡ�<br>
		<���֤η�(MyState), ���������ؿ��������(bool), �������֥������Ȥη�>
	<li> StateMachine �Υ��󥹥ȥ饯�������Ͼ��֤ο�
	<li> �ʲ��Υ��������ؿ���(Return _function_name_(States)) �δؿ��Ȥ�������
	<ol>
		<li> ���⤷�ʤ��ؿ���ɬ���������setNOP ��Ϳ���ʤ���Фʤ�ʤ�
		<li> �ƾ������, set(Entry|PreDo|Do|PostDo|Exit)Action �ǥ�������������
		<li> �������ܻ��Υ��������� setTransitionAction() �����ꡣ
	</ol>
	<li> ���ܻ��Υ��������ϡ�Ϳ����줿���߾��֡������֡������֤򸵤ˡ�
		�桼�����������ʤ���Фʤ�ʤ���
	<li> ���֤��ѹ��� goTo() �ǡ����֤Υ����å��� isIn(state) �ǹԤ���
	<li> goTo()�ϼ����֤���Ū�˥��åȤ���ؿ��Ǥ��ꡢ���ܤβ��ݤϡ�
		�桼�������߾��֤������Ƚ�Ǥ�����å���������ʤ���Фʤ�ʤ���
	</ol>

	���Υ��饹�ϡ���Ĥξ��֤��Ф��ơ�
	<ul>
	<li> Entry action
	<li> PreDo action
	<li> Do action2
	<li> PostDo action
	<li> Exit action
	</ul>
	5�ĤΥ��������������뤳�Ȥ��Ǥ��롣
	Transition action �Ϥ�������ִ����ܤǸƤӽФ���륢�������ǡ�
	���ο����񤤤ϥ桼����������ʤ���Фʤ�ʤ���

	���Υ��饹�ϰʲ��Τ褦�ʥ����ߥ󥰤ǳƥ�������󤬼¹Ԥ���롣

	<ul>
	<li> ���֤��ѹ�����(A->B)���֤����ܤ����� <br>
	(A:Exit)->|(���ֹ���:A->B)->(B:Entry)->(B:PreDo)->(B:Do)->(B:PostDo)

	<li> ���֤��ѹ����줺��B���֤�ݻ������� (|�ϥ��ƥåפζ��ڤ��ɽ��)<br>
	(B(n-1):PostDo)->|(B(n):PreDo)->(B(n):Do)->(B(n):PostDo)->|(B(n+1):PreDo)<br>
	PreDo, Do, PostDo �������֤��¹Ԥ���롣

	<li> �������ܤ����� <br>
	(B(n-1):PostDo)->(B(n-1):Exit)->|(B(n):Entry)->(B(n):PreDo) <br>
	��ö Exit ���ƤФ줿�塢Entry ���¹Ԥ��졢�ʹߤ������Ʊ��ư��򤹤롣
	</ul>2
		\else

	\brief

	\endif

	"""

	state_array = (RTC.INACTIVE_STATE,
				   RTC.ACTIVE_STATE,
				   RTC.ERROR_STATE,
				   RTC.UNKNOWN_STATE)

	def __init__(self, num_of_state):
		"""
		\if jp
		\brief ���󥹥ȥ饯��
		\param num_of_state(int)
		\else
		\brief Constructor
		\param num_of_state(int)
		\endif
		"""
		self._num = num_of_state
		self._entry  = {}
		self._predo  = {}
		self._do     = {}
		self._postdo = {}
		self._exit   = {}

		self.setNullFunc(self._entry,  None)
		self.setNullFunc(self._do,     None)
		self.setNullFunc(self._exit,   None)
		self.setNullFunc(self._predo,  None)
		self.setNullFunc(self._postdo, None)
		self._transit = None
		self._mutex = threading.RLock()
		self._selftrans = False


	def setNOP(self, call_back):
		"""
		\if jp
		\brief NOP�ؿ�����Ͽ����
		\param call_back(function object)
		\else
		\brief Set NOP function
		\param call_back(function object)
		\endif
		"""
		self.setNullFunc(self._entry,  call_back)
		self.setNullFunc(self._do,     call_back)
		self.setNullFunc(self._exit,   call_back)
		self.setNullFunc(self._predo,  call_back)
		self.setNullFunc(self._postdo, call_back)
		self._transit = call_back


	def setListener(self, listener):
		"""
		\if jp
		\brief Listener ���֥������Ȥ���Ͽ����
		\param listener(class of function object)
		\else
		\brief Set Listener Object
		\param listener(class of function object)
		\endif
		"""
		self._listener = listener


	def setEntryAction(self, state, call_back):
		"""
		\if jp
		\brief Entry action �ؿ�����Ͽ����
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Entry action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._entry.has_key(state):
			self._entry[state] = call_back
		else:
			self._entry.setdefault(state, call_back)
		return True


	def setPreDoAction(self, state, call_back):
		"""
		\if jp
		\brief PreDo action �ؿ�����Ͽ����
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set PreDo action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._predo.has_key(state):
			self._predo[state] = call_back
		else:
			self._predo.setdefault(state, call_back)
		return True


	def setDoAction(self, state, call_back):
		"""
		\if jp
		\brief Do action �ؿ�����Ͽ����
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Do action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._do.has_key(state):
			self._do[state] = call_back
		else:
			self._do.setdefault(state, call_back)
		return True



	def setPostDoAction(self, state, call_back):
		"""
		\if jp
		\brief Post action �ؿ�����Ͽ����
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Post action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._postdo.has_key(state):
			self._postdo[state] = call_back
		else:
			self._postdo.setdefault(state, call_back)
		return True


	def setExitAction(self, state, call_back):
		"""
		\if jp
		\brief Exit action �ؿ�����Ͽ����
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\else
		\brief Set Exit action function
		\param state(RTC.LifeCycleState)
		\param call_back(function object)
		\endif
		"""
		if self._exit.has_key(state):
			self._exit[state] = call_back
		else:
			self._exit.setdefault(state, call_back)
		return True


	def setTransitionAction(self, call_back):
		"""
		\if jp
		\brief State transition action �ؿ�����Ͽ����
		\param call_back(function object)
		\else
		\brief Set state transition action function
		\param call_back(function object)
		\endif
		"""
		self._transit = call_back
		return True


	def setStartState(self, states):
		"""
		\if jp
		\brief ������֤򥻥åȤ���
		\param state(RTC.LifeCycleState)
		\else
		\brief Set Exit action function
		\param state(RTC.LifeCycleState)
		\endif
		"""
		self._states = StateHolder()
		self._states.curr = states.curr
		self._states.prev = states.prev
		self._states.next = states.next


	def getStates(self):
		"""
		\if jp
		\brief ���֤��������
		\else
		\brief Get state machine's status
		\endif
		"""
		guard = ScopedLock(self._mutex)
		return self._states


	def getState(self):
		guard = ScopedLock(self._mutex)
		return self._states.curr


	def isIn(self, state):
		"""
		\if jp
		\brief ���߾��֤��ǧ
		\param state(RTC.LifeCycleState)
		\else
		\brief Evaluate current status
		\param state(RTC.LifeCycleState)
		\endif
		"""
		guard = ScopedLock(self._mutex)
		if self._states.curr == state:
			return True
		else:
			return False


	def goTo(self, state):
		"""
		\if jp
		\brief ���֤��ѹ�
		\param state(RTC.LifeCycleState)
		\else
		\brief Change status
		\param state(RTC.LifeCycleState)
		\endif
		"""
		guard = ScopedLock(self._mutex)
		self._states.next = state
		if self._states.curr == state:
			self._selftrans  = True


	def worker(self):
		"""
		\if jp
		\brief ��ư�ؿ�
		\else
		\brief Worker function
		\endif
		"""
		states = StateHolder()
		self.sync(states)

		# If no state transition required, execute set of do-actions
		if states.curr == states.next:
			# pre-do
			if self._predo[states.curr] != None:
				self._predo[states.curr](states)
			if self.need_trans():
				return

			# do
			if self._do[states.curr] != None:
				self._do[states.curr](states)
			if self.need_trans():
				return

			# post-do
			if self._postdo[states.curr] != None:
				self._postdo[states.curr](states)
		# If state transition required, exit current state and enter next state
		else:
			if self._exit[states.curr] != None:
				self._exit[states.curr](states)
			self.sync(states)

			# If state transition still required, move to the next state
			if states.curr != states.next:
				states.curr = states.next
				if self._entry[states.curr] != None:
					self._entry[states.curr](states)
				self.update_curr(states.curr)


	def setNullFunc(self, s, nullfunc):
		"""
		 \param s(map of callback function object)
		 \param nullfunc(callback function object)
		"""
		for i in range(self._num):
			if s.has_key(StateMachine.state_array[i]):
				s[StateMachine.state_array[i]] = nullfunc
			else:
				s.setdefault(StateMachine.state_array[i], nullfunc)


	def sync(self, states):
		"""
		 \param state(OpenRTM.StateHolder<RTC.LifeCycleState>)
		"""
		guard = ScopedLock(self._mutex)
		states.prev = self._states.prev
		states.curr = self._states.curr
		states.next = self._states.next
		

	def need_trans(self):
		guard = ScopedLock(self._mutex)
		return (self._states.curr != self._states.next)


	def update_curr(self, curr):
		"""
		 \param curr(RTC.LifeCycleState)
		""" 
		guard = ScopedLock(self._mutex)
		self._states.curr = curr
