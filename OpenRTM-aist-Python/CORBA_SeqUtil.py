#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# @file CORBA_SeqUtil.py
#  CORBA sequence utility template functions
# @date $Date: 2007/09/03 $
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#


##
# @if jp
#  
# CORBA sequence �إ�ѡ��ƥ�ץ졼�ȴؿ�
# 
# CORBA sequence ���Ф��ưʲ��Υ桼�ƥ���ƥ��ƥ�ץ졼�ȴؿ����󶡤��롣
# ���ϥ���åɥ����դǤϤʤ��Τǡ�����åɥ����դ����������ϡ�
# �оݤȤʤ륷�������ͤ�Ŭ�ڤ�mutex�����ݸ��ɬ�פ����롣
# 
# - for_each()
# - find()
# - push_back()
# - insert()
# - front()
# - back()
# - erase()
# - clear()
# 
# @else
#  
# CORBA sequence helper template functions
# 
# This group provides the following utility function to CORBA sequence.
# Since these functions are not thread-safe operations,
# if the sequence would be operated in thread-safe,
# the value should be protected by mutex properly.
# 
# - for_each()
# - find()
# - push_back()
# - insert()
# - front()
# - back()
# - erase()
# - clear()
# 
# @endif



##
# @if jp
#  
# CORBA sequence ���Ф��� functor ��Ŭ�Ѥ���
# 
# CORBA sequence ���Ƥ����Ǥ��Ф��ơ�Ϳ����줿 functor ��Ŭ�Ѥ��롣
# functor �� void functor(CORBA sequence ������) �η�����Ȥ�ɬ�פ����롣
# 
# @return ���Ƥ����Ǥ�������� Functor
# @param seq Functor ��Ŭ�Ѥ��� CORBA sequence
# @param functor CORBA sequence �����Ǥ�������� Functor
#   
# @else
# 
# Apply the functor to all CORBA sequence elements
# 
# Apply the given functor to the given CORBA sequence.
# functor should be void functor(CORBA sequence element).
# 
# @return Functor that processed all CORBA sequence elements
# @param seq CORBA sequence to be applied the functor
# @param functor A functor to process CORBA sequence elements
# 
# @endif
def for_each(seq, f):
	len_ = len(seq)
	for i in range(len_):
		f(seq[i])
	return f



##
# @if jp
# CORBA sequence ���椫�� functor ��Ŭ�礹�����ǤΥ���ǥå������֤�
# 
# CORBA sequence ���Ƥ����Ǥ��Ф��ơ�Ϳ����줿 functor ��Ŭ�Ѥ���
# functor �� true ���֤��褦���Υ���ǥå������֤���
# functor �� bool functor(const CORBA sequence ������) �η�����Ȥꡢ
# Ŭ�礹�����Ǥ��Ф��� true ���֤�ɬ�פ����롣
# 
# @return Functor ��Ŭ�礹�����ǤΥ���ǥå�����
# ���Ĥ���ʤ��Ȥ��� -1 ���֤���
# @param seq Functor ��Ŭ�Ѥ��� CORBA sequence
# @param functor CORBA sequence �������Ǥ򸫤Ĥ��� Functor
# 
# @else
# 
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
# 
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
# 
# Push the new element back to the CORBA sequence
# 
# Add the given element to the last of CORBA sequence.
# The length of the CORBA sequence will be expanded automatically.
# 
# @param seq CORBA sequence to be added a new element
# @param elem The new element to be added to the CORBA sequence
# 
# @endif
def push_back(seq, elem):
	seq.append(elem)


def push_back_list(seq1, seq2):
	for elem in seq2:
		seq1.append(elem)


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
# 
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
# 
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
# 
# Get the front element of the CORBA sequence
# 
# This operation returns seq[0].
# 
# @param seq The CORBA sequence to be get the element
# 
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
# 
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
# 
# @endif
def erase(seq, index):
	if index > len(seq):
		return

	del seq[index]


def erase_if(seq, f):
	index = find(seq, f)
	if index < 0:
		return
	del seq[index]


##
# @if jp
# CORBA sequence �������Ǥ���
# 
# seq.length(0) ��Ʊ����
# 
# @else
# 
# Erase all the elements of the CORBA sequence
# 
# same as seq.length(0).
# 
# @endif
def clear(seq):
	del seq[0:]
