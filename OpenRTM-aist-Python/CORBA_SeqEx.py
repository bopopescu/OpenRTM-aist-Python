#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
#  @file CORBA_SeqEx.py
#  @brief CORBA utility template classes
#  @date $Date: 2007/09/12 $
#  @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
# 
#  Copyright (C) 2006
#      Task-intelligence Research Group,
#      Intelligent Systems Research Institute,
#      National Institute of
#          Advanced Industrial Science and Technology (AIST), Japan
#      All rights reserved.

import threading
import OpenRTM


class ScopedLock:
	
	def __init__(self, mutex):
		self.mutex = mutex
		self.mutex.acquire()

	def __del__(self):
		self.mutex.release()


##
# @if jp
#  CORBA sequence ���Ф��� functor ��Ŭ�Ѥ���
# 
# CORBA sequence ���Ƥ����Ǥ��Ф��ơ�Ϳ����줿 functor ��Ŭ�Ѥ��롣
# functor �� void functor(CORBA sequence ������) �η�����Ȥ�ɬ�פ����롣
# 
# @return ���Ƥ����Ǥ�������� Functor
# @param seq Functor ��Ŭ�Ѥ��� CORBA sequence
# @param functor CORBA sequence �����Ǥ�������� Functor
# 
# @else
#  Apply the functor to all CORBA sequence elements
# 
# Apply the given functor to the given CORBA sequence.
# functor should be void functor(CORBA sequence element).
# 
# @return Functor that processed all CORBA sequence elements
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# @endif

def for_each(seq, f):
	len_ = len(seq)

	for i in range(len_):
		f(seq[i])

	return f


##
# @if jp
#  CORBA sequence ���椫�� functor ��Ŭ�礹�����ǤΥ���ǥå������֤�
# 	
#  CORBA sequence ���Ƥ����Ǥ��Ф��ơ�Ϳ����줿 functor ��Ŭ�Ѥ���
#  functor �� true ���֤��褦���Υ���ǥå������֤���
#  functor �� bool functor(const CORBA sequence ������) �η�����Ȥꡢ
#  Ŭ�礹�����Ǥ��Ф��� true ���֤�ɬ�פ����롣
#  
# @return Functor ��Ŭ�礹�����ǤΥ���ǥå�����
# ���Ĥ���ʤ��Ȥ��� -1 ���֤���
# @param seq Functor ��Ŭ�Ѥ��� CORBA sequence
# @param functor CORBA sequence �������Ǥ򸫤Ĥ��� Functor
# 
# @else
# Return the index of CORBA sequence element that functor matches 
# 
# This operation applies the given functor to the given CORBA sequence,
# and returns the index of the sequence element that the functor matches.
# The functor should be bool functor(const CORBA sequence element) type,
# and it would return true, if the element matched the functor.
# 
# @return The index of the element that functor matches.
# If no element found, it would return -1.
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# @endif

def find(seq, f):
	len_ = len(seq)

	for i in range(len_):
		if f(seq[i]):
			return i
	return -1


##
# @if jp
# CORBA sequence �κǸ�����Ǥ��ɲä���
# 
# CORBA sequence �κǸ��Ϳ����줿���Ǥ��ɲä��롣
# CORBA sequence ��Ĺ���ϼ�ưŪ�˳�ĥ����롣
# 
# @param seq ���Ǥ��ɲä��� CORBA sequence
# @param elem �ɲä�������
# 
# @else
# Push the new element back to the CORBA sequence
# 
# Add the given element to the last of CORBA sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq CORBA sequence to be added a new element
# @param elem The new element to be added to the CORBA sequence
# @endif

def push_back(seq, elem):
	seq.append(elem)

##
# @if jp
# CORBA sequence �����Ǥ���������
# 
# CORBA sequence �� index �ΰ��֤����Ǥ�ä��롣
# index �� Ϳ����줿��CORBA sequence �κ���� index ����礭�����
# �Ǹ�����ǤȤ��Ʋä����롣
# CORBA sequence ��Ĺ���ϼ�ưŪ�˳�ĥ����롣
# 
# @param seq ���Ǥ��ɲä��� CORBA sequence
# @param elem �ɲä�������
# @param index ���Ǥ��ɲä������
# 
# @else
# Insert the element to the CORBA sequence
# 
# Insert a new element in the given position to the CORBA sequence.
# If the given index is greater than the length of the sequence,
# the given element is pushed back to the last of the sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq The CORBA sequence to be inserted a new element
# @param elem The new element to be inserted the sequence
# @param index The inserting position
# @endif

def insert(seq, elem, index):
	len_ = len(seq)
	if index > len:
		seq.append(elem)
		return
	seq.insert(index, elem)


##
# @if jp
# CORBA sequence ����Ƭ���Ǥ��������
# 
# seq[0] ��Ʊ����
# 
# @param seq ���Ǥ�������� CORBA sequence
# 
# @else
# Get the front element of the CORBA sequence
# 
# This operation returns seq[0].
# 
# @param seq The CORBA sequence to be get the element
# @endif

def front(seq):
	return seq[0]


##
# @if jp
# CORBA sequence ���������Ǥ��������
# 
# seq[seq.length() - 1] ��Ʊ����
# 
# @param seq ���Ǥ�������� CORBA sequence
# 
# @else
# 
# Get the last element of the CORBA sequence
# 
# This operation returns seq[seq.length() - 1].
# 
# @param seq The CORBA sequence to be get the element
# @endif

def back(seq):
	return seq[-1]


##
# @if jp
# CORBA sequence �λ��ꤵ�줿���֤����Ǥ�������
# 
# ���ꤵ�줿����ǥå��������Ǥ������롣
# ������줿���Ǥϵͤ��졢sequence ��Ĺ����1���롣
# 
# @param seq ���Ǥ������� CORBA sequence
# @param index ����������ǤΥ���ǥå���
# 
# @else
# 
# Erase the element of the specified index
# 
# This operation removes the element of the given index.
# The other elements are closed up around the hole.
# 
# @param seq The CORBA sequence to be get the element
# @param index The index of the element to be removed
# @endif

def erase(seq, index):
	if index > len(seq):
		return

	del seq[index]


##
# @if jp
# CORBA sequence �������Ǥ���
# 
# seq.length(0) ��Ʊ����
# 
# @else
# Erase all the elements of the CORBA sequence
# 
# same as seq.length(0).
# @endif

def clear(seq):
	del seq[0:]



""" CORBA sequence extention class """

class LockedStruct:
	
	def __init__(self):
		self.lock = threading.RLock()
		self.data = None

##
# @if jp
# @class SequenceEx
# CORBA::sequence ��ĥ���饹
# 
# ���Υ��饹�� CORBA �� sequence �����ĥ�� std::vector �Υ��󥿡��ե�������
# �󶡤��� (�㤨�� size(), max_size(), empty(), resize(), insert(),
# 	  erase(), erase_if(), push_back(), pop_back(), find()).
# CORBA �� sequence ����Ѿ����Ƥ��뤿�ᡢCORBA �� sequence ����
# ���ڥ졼�����(like operator=(), maximum(), length(), operator[])��
# ���Ѳ�ǽ�Ǥ��롣
# 
# @else
# CORBA::sequence extention class
# 
# This class extends CORBA sequence type, and provides std::vector like
# interfaces (like size(), max_size(), empty(), resize(), insert(),
# 	    erase(), erase_if(), push_back(), pop_back(), find()).
# Since this class inherits CORBA sequence class, user can also use CORBA
# sequence interfaces (like operator=(), maximum(), length(), operator[]).
# @endif

class SequenceEx:
	
	##
	# @if jp
	# 	
	# CorbaSequence ����Υ��ԡ����󥹥ȥ饯��
	# 
	# CorbaSequence������Υ��ԡ����󥹥ȥ饯����
	# Ϳ����줿 CorbaSequence �����Ƥ򥳥ԡ����롣
	# 
	# @param _sq CorbaSequence ���Υ��ԡ���
	# 
	# @else
	# Copy constructor from CorbaSequence
	# 
	# This constructor copies sequence contents from given CorbaSequence
	# to this object.
	# 
	# @param _sq Copy source of CorbaSequence type
	# @endif

	def __init__(self, _sq):
		len_ = len(_sq)
		self._seq = []
		for i in range(len_):
			self._seq.append(_sq[i])
		self._mutex = threading.RLock()


	##
	# @if jp
	# �ǥ��ȥ饯��
	# @else
	# Destructor
	# @endif

	def __del__(self):
		self._seq = []


	##
	# @if jp
	# 
	# ���������������
	# 
	# ���Υ��ڥ졼�����ϥ������󥹤Υ��������֤���
	# CorbaSequence::length() ��Ʊ����
	# @return �������󥹤Υ�����
	# 
	# @else
	# Get size of this sequence
	# 
	# This operation returns the size of the sequence.
	# This is same as CorbaSequence::length().
	# @return The size of the sequence.
	# @endif

	def size(self):
		return len(self._seq)


	##
	# @if jp
	# ��Ǽ��ǽ�ʺ���Υ��������������
	# 
	# ���Υ��ڥ졼�����ϥ������󥹤θ��ߤγ�Ǽ��ǽ�ʺ���Υ��������֤���
	# CorbaSequence::maximum() ��Ʊ����
	# @return �������󥹤˳�Ǽ��ǽ�ʺ���Υ�����
	# 
	# @else
	# Get current maximum size of this sequence
	# 
	# This operation returns the current maximum size of the sequence.
	# This is same as CorbaSequence::maximum().
	# @return The maximum size of the sequence.
	# @endif

	def max_size(self):
		return len(self._seq)


	##
	# @if jp
	# �������󥹤������ɤ���Ĵ�٤�
	# 
	# ���Υ��ڥ졼�����ϥ������󥹤������ɤ����� bool �ͤ��֤���
	# �������� 0 �ʤ� true�������Ǥʤ���� false ���֤���
	# @return �������󥹤������ɤ����� bool ��
	# 
	# @else
	# Test whether the sequence is empty
	# 
	# This operation returns bool value whether the sequence is empty.
	# If the size of the sequence is 0, this operation returns true,
	# and in other case this operation returns false.
	# @return The bool value whether the sequence is empty.
	# @endif

	def empty(self):
		if not self._seq:
			return False
		else:
			return True


	##
	# @if jp
	# �������󥹤�ꥵ��������
	# 
	# ���Υ��ڥ졼�����ϥ������󥹤�Ĺ�����ѹ����롣
	# ���ߤ�Ĺ������礭�ʥ�������Ϳ����줿��硢���� x �ǡ�
	# �����˥������Ȥ��줿��ʬ�������롣
	# ���ߤ�Ĺ����꾮������������Ϳ����줿��硢CorabSequence ��Ʊ�ͤ�
	# ;ʬ�ʥ������󥹤����ǤϺ������롣
	# @param new_size �������������󥹤Υ�����
	# @param item��Ĺ���ʤä�ʬ�Υ������󥹤���������
	# 
	# @else
	# Resize the length of the sequence
	# 
	# This operation resizes the length of the sequence.
	# If longer length than current sequence length is given,
	# newly allocated rooms will be assigned by element given by the argument.
	# If shorter length than current sequence length is given,
	# the excessive element of a sequence is deleted like behavior of
	# CorabSequence
	# @param new_size The new size of the sequence
	# @param item��   Sequence element to be assigned to new rooms.
	# @endif

	def resize(self, new_size, item):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		if new_size > len_:
			self._seq = []
			for i in range(len_):
				self._seq.append(item)
		elif new_size < len_:
			del self._seq[new_size:]


	##
	# @if jp
	# �������󥹤����Ǥ���������
	# 
	# ���Υ��ڥ졼�����ϥ������󥹤���������Ǥ��������롣
	# @param position ���������Ǥ�����������
	# @param item���������륷�����󥹤�����
	# 
	# @else
	# Insert a new item to the sequence
	# 
	# This operation inserts a new item to the sequence.
	# @param position The position of new inserted item.
	# @param item��   Sequence element to be inserted.
	# @endif

	def insert(self, position, item):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		if position > len_:
			raise

		self._seq.insert(position, item)


	##
	# @if jp
	# �������󥹤����Ǥ�������
	# 
	# ���Υ��ڥ졼�����ϥ������󥹤����Ǥ�������
	# @param position ������륷���������Ǥξ��
	# 
	# @else
	# Erase an item of the sequence
	# 
	# This operation erases an item from the sequence.
	# @param position The position of erased item.
	# @endif

	def erase(self, position):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		if position > (len_ - 1):
			raise

		erased = self._seq[position]
		del self._seq[position]
		return erased


	##
	# @if jp
	# �������󥹤����Ǥ�Ҹ�Τ������äƺ������
	# 
	# ���Υ��ڥ졼�����ϽҸ�Ȥ���Ϳ����줿�ؿ����֥������Ȥ�
	# ��郎���ΤȤ������Υ������󥹤����Ǥ������롣
	# @param f ������륷�����󥹤���ꤹ��Ѹ�
	# 
	# @else
	# Erase an item according to the given predicate
	# 
	# This operation erases an item according to the given predicate.
	# @param f The predicate functor to decide deletion.
	# @endif

	def erase_if(self, f):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		for i in range(len_):
			if f(self._seq[i]):
				return self.erase(i)
		raise


	##
	# @if jp
	# ���Ǥ�Ǹ������ɲä���
	# 
	# ���Υ��ڥ졼������Ϳ����줿���Ǥ򥷡����󥹤κǸ���ɲä��롣
	# @param item �ɲä��뤹�륪�֥�������
	# 
	# @else
	# Append an item to the end of the sequence.
	# 
	# This operation push back an item to the of the sequence.
	# @param item The object to be added to the end of the sequnce.
	# @endif
	def push_back(self, item):
		guard = ScopedLock(self._mutex)
		self._seq.append(item)


	def pop_back(self):
		guard = ScopedLock(self._mutex)
		del self._seq[-1]


	def find(self, f):
		guard = ScopedLock(self._mutex)
		len_ = len(self._seq)
		for i in range(len_):
			if f(self._seq[i]):
				return self._seq[i]
		raise
