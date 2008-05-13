#!/usr/bin/env python
# -*- coding: euc-jp -*-

"""
 \file StringUtil.py
 \brief String operation utility
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2003-2005
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import string


def isEscaped(_str, pos):
	"""
	\if jp
	\brief ʸ���󤬥��������פ���Ƥ��뤫Ƚ�Ǥ���

	���ꤷ��ʸ�������������פ���Ƥ����true������Ƥ��ʤ����false���֤���

	\param str ���������פ���Ƥ��뤫�ɤ���Ƚ�Ǥ���ʸ����ޤ�ʸ����
	\param pos ���������פ���Ƥ��뤫�ɤ���Ƚ�Ǥ���ʸ���ΰ���
	\return ���ꤷ��ʸ�������������פ���Ƥ���� true, ����ʳ��� false

	\else
	\brief Whether the character is escaped or not

	This operation returns true if the specified character is escaped, and
	if the specified character is not escaped, it returns false

	\param str The string thath includes the character to be investigated.
	\param pos The position of the character to be investigated.
	\return true: the character is escaped, false: the character is not escaped.

	\endif
	"""
	pos -= 1

	i = 0
	while pos >= 0 and _str[pos] == "\\":
		i += 1
		pos -= 1

	return i % 2 == 1
  


class escape_functor:
	"""
	\if jp
	\brief ʸ����򥨥������פ��뤿���Fanctor
	\else
	\brief A fanctor to escape string
	\endif
	"""
	def __init__(self):
		self._str = ""

	def __call__(self,c):
		if   c == '\t':
			self._str += "\\t"
		elif c == '\n':
			self._str += "\\n"
		elif c == '\f':
			self._str += "\\f"
		elif c == '\r':
			self._str += "\\r"
		else:
			self._str += c


class unescape_functor:
	"""
	\if jp
	\brief ʸ����򥢥󥨥������פ����Fanctor
	\else
	\brief The functor to unescape string
	\endif
	"""
	def __init__(self):
		self.count = 0
		self._str = ""

	def __call__(self,c):
		if c == "\\":
			self.count += 1
			if not (self.count % 2):
				self._str += c
		else:
			if self.count > 0 and (self.count % 2):
				self.count = 0
				if c == 't':
					self._str+='\t'
				elif c == 'n':
					self._str+='\n'
				elif c == 'f':
					self._str+='\f'
				elif c == 'r':
					self._str+='\r'
				elif c == '\"':
					self._str+='\"'
				elif c == '\'':
					self._str+='\''
				else:
					self._str+=c
			else:
				self.count = 0
				self._str+=c


class Toupper:
	"""
	\if jp
	\brief ��ʸ�����Ѵ����� Fanctor
	\else
	\brief A functor to convert to capital letter
	\endif
	"""
	def __init__(self):
		self._str = ""
	
	def __call__(self,c):
		self._str = upper(c)


class unique_strvec:
	def __init__(self):
		self._str = []

	def __call__(self,s):
		if self._str.count(s) == 0:
			return self._str.append(s)


def for_each(_str, instance):
	for i in _str:
		instance(i)

	return instance


def escape(_str):
	"""
	\if jp
	\brief ʸ����򥨥������פ���

	����ʸ���򥨥������ץ������󥹤��Ѵ����롣<br>
	HT -> "\t" <br>
	LF -> "\n" <br>
	CR -> "\r" <br>
	FF -> "\f" <br>
	���󥰥륯�����ȡ����֥륯�����ȤˤĤ��ƤϤȤ��˽����Ϥ��ʤ���

	\else

	\brief Escape string

	The following characters are converted. <br>
	HT -> "\t" <br>
	LF -> "\n" <br>
	CR -> "\r" <br>
	FF -> "\f" <br>
	Single quote and dobule quote are not processed.

	\endif
	"""
	return for_each(_str, escape_functor())._str


def unescape(_str):
	"""
	\if jp
	\brief ʸ����Υ��������פ��᤹
	
	���Υ��������ץ������󥹤�ʸ�����Ѵ����롣<br>
	"\t" -> HT <br>
	"\n" -> LF <br>
	"\r" -> CR <br>
	"\f" -> FF <br>
	"\"" -> "  <br>
	"\'" -> '  <br>
	
	\else
	
	\brief Unescape string
	
	The following characters are converted. <br>
	"\t" -> HT <br>
	"\n" -> LF <br>
	"\r" -> CR <br>
	"\f" -> FF <br>
	"\'" -> '  <br>
	"\"" -> "  <br>
	\endif
	"""
	return for_each(_str, unescape_functor())._str


def eraseHeadBlank(_str):
	"""
	\if jp
	\brief ʸ�������Ƭ�ζ���ʸ����������
	\else
	\brief Erase the head blank characters of string
	\endif
	"""
	if _str[0] == "":
		return

	while _str[0][0] == " " or _str[0][0] == '\t':
		_str[0] = _str[0][1:]


def eraseTailBlank(_str):
	"""
	\if jp
	\brief ʸ����������ζ���ʸ����������
	\else
	\brief Erase the tail blank characters of string
	\endif
	"""
	if _str[0] == "":
		return

	while (_str[0][-1] == " " or _str[0][-1] == '\t') and not isEscaped(_str[0], len(_str[0]) - 1):
		_str[0] = _str[0][:-1]


def replaceString(str, _from, _to):
	"""
	\if jp
	\brief ʸ������֤�������
	\else
	\brief Replace string
	\endif
	"""
	str[0] = str[0].replace(_from, _to)


def split(input, delimiter):
	"""
	\if jp
	\brief ʸ�����ʬ��ʸ����ʬ�䤹��
	\else
	\brief Split string by delimiter
	\endif
	"""
	if not input:
		return []

	del_result = input.split(delimiter)

	len_ = len(del_result)

	result = []
	for i in range(len_):
		if del_result[i] == "" or del_result[i] == " ":
			continue
			
		str_ = [del_result[i]]
		eraseHeadBlank(str_)
		eraseTailBlank(str_)
		result.append(str_[0])
		
	return result


def toBool(_str, yes, no, default_value=None):
	"""
	\if jp
	\brief Ϳ����줿ʸ�����bool�ͤ��Ѵ�����
	\else
	\brief Convert given string to bool value
	\endif
	"""
	if default_value == None:
		default_value = True

	_str = _str.upper()
	yes  = yes.upper()
	no   = no.upper()

	if _str.find(yes) != -1:
		return True
	elif (_str.find(no)) != -1:
		return False
	else:
		return default_value


def isAbsolutePath(str):
	"""
	\if jp
	\brief Ϳ����줿ʸ�������Хѥ����ɤ�����Ƚ�Ǥ���
	\else
	\brief Investigate whether the given string is absolute path or not
	\endif
	"""
	if str[0] == "/":
		return True
	if str[0].isalpha() and str[1] == ":" and str[2] == "\\":
		return True
	if str[0] == "\\" and str[1] == "\\":
		return True

	return False


def isURL(str):
	"""
	\if jp
	\brief Ϳ����줿ʸ����URL���ɤ�����Ƚ�Ǥ���
	\else
	\brief Investigate whether the given string is URL or not
	\endif
	"""
	pos = 0
	if str == "":
		return False

	pos = str.find(":")
	if pos != 0 and pos != -1 and str[pos+1] == "/" and str[pos+2] == "/":
		return True

	return False


def otos(n):
	"""
	\if jp
	\brief Ϳ����줿���֥������Ȥ�std::string���Ѵ�
	\else
	\brief Convert the given object to st::string.
	\endif
	"""
	if type(n) == int or type(n) == str or type(n) == long or type(n) == float:
		return str(n)


def _stringToList(_type, _str):
	list_ = split(_str,",")
	len_ = len(list_)

	if len(_type[0]) < len(list_):
		sub = len(list_) - len(_type[0])
		for i in range(sub):
			_type[0].append(_type[0][0])
	elif len(_type[0]) > len(list_):
		sub = len(_type[0]) - len(list_)
		for i in range(sub):
			del _type[0][-1]

	for i in range(len_):
		str_ = [list_[i]]
		eraseHeadBlank(str_)
		eraseTailBlank(str_)
		list_[i] = str_[0]

	for i in range(len(list_)):
		if type(_type[0][i]) == int:
			_type[0][i] = int(list_[i])
		elif type(_type[0][i]) == long:
			_type[0][i] = long(list_[i])
		elif type(_type[0][i]) == float:
			_type[0][i] = float(list_[i])
		elif type(_type[0][i]) == str:
			_type[0][i] = str(list_[i])
		else:
			return False

	return True


def stringTo(_type, _str):
	if type(_type[0]) == int:
		_type[0] = int(_str)
		return True
	elif type(_type[0]) == long:
		_type[0] = long(_str)
		return True
	elif type(_type[0]) == float:
		_type[0] = float(_str)
		return True
	elif type(_type[0]) == list:
		return _stringToList(_type, _str)
	elif type(_type[0]) == str:
		_type[0] = str(_str)
		return True
	
	return False


def unique_sv(sv):
	return for_each(sv, unique_strvec())._str
	

def flatten(sv):
	if len(sv) == 0:
		return ""

	_str = ""
	for i in range(len(sv) -1):
		_str += sv[i] + ", "

	return _str + sv[-1] 
		

def toArgv(args):
	return args
