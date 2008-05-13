#!/usr/bin/env python
# -*- coding: euc-jp -*-
	

"""
 \file Properties.py
 \brief Property list class (derived from Java Properties)
 \date $Date: $
 \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara

 Copyright (C) 2006
     Task-intelligence Research Group,
     Intelligent Systems Research Institute,
     National Institute of
         Advanced Industrial Science and Technology (AIST), Japan
     All rights reserved.
"""


import sys
import string

import OpenRTM



class Properties:
	"""
	\if jp

	\class Properties

	Properties ���饹�ϡ����ѤΥץ�ѥƥ����åȤ�ɽ����Properties �򥹥ȥ꡼��
	���ݴɤ����ꡢ���ȥ꡼�फ����ɤ����ꤹ�뤳�Ȥ��Ǥ��롣
	�ץ�ѥƥ��ꥹ�Ȥγƥ���������Ӥ�����б������ͤ�ʸ����ȤʤäƤ��롣

	�ץ�ѥƥ��ꥹ�Ȥˤϡ����Ρ֥ǥե�����͡פȤ����̤Υץ�ѥƥ��ꥹ�Ȥ����
	���Ȥ��Ǥ��롣���Υץ�ѥƥ��ꥹ�Ȥǥץ�ѥƥ����������Ĥ���ʤ��ȡ�����
	2���ܤΥץ�ѥƥ��ꥹ�Ȥ���������롣 

	�ץ�ѥƥ��μ����ˤ� getProperty���ץ�ѥƥ��Υ��åȤˤ� setProperty ��
	���ä��᥽�åɤ���Ѥ��뤳�Ȥ��侩����롣

	�ץ�ѥƥ��򥹥ȥ꡼�����¸����Ȥ����ޤ��ϥ��ȥ꡼�फ����ɤ���Ȥ��ˡ�
	ISO 8859-1 ʸ�����󥳡��ǥ��󥰤����Ѥ���롣���Υ��󥳡��ǥ��󥰤�ľ��ɽ��
	�Ǥ��ʤ�ʸ���ϡ��������Ȥ��Ǥ��ʤ���

	���Υ��饹�ϡ�Java �� Properties ���饹 (java.util.Properties) �Ȥۤ�Ʊ�ͤ�
	�᥽�åɤ���ġ��ޤ��������Ϥ����ե������ Java �� Properties ���饹��
	���Ϥ����Τȸߴ��������뤬��Unicode ��ޤ��Τϰ������Ȥ��Ǥ��ʤ���

	\else

	\class Properties

	The Properties class represents a persistent set of properties. The
	Properties can be saved to a stream or loaded from a stream. Each key and
	its corresponding value in the property list is a string. 

	A property list can contain another property list as its "defaults"; this
	second property list is searched if the property key is not found in the
	original property list. 

	Because Properties inherits from Hashtable, the put and putAll methods can
	be applied to a Properties object. Their use is strongly discouraged as they
	allow the caller to insert entries whose keys or values are not Strings. The
	setProperty method should be used instead. If the store or save method is
	called on a "compromised" Properties object that contains a non-String key
	or value, the call will fail. 

	The load and store methods load and store properties in a simple
	line-oriented format specified below. This format uses the ISO 8859-1
	character encoding. Characters that cannot be directly represented in this
	encoding can be written using Unicode escapes ; only a single 'u' character
	is allowed in an escape sequence. The native2ascii tool can be used to
	convert property files to and from other character encodings. 

	This class has almost same methods of Java's Properties class. Input and 
	Output stream of this properties are compatible each other except Unicode
	encoded property file.

	\endif
	"""

	def __init__(self, key=None, value=None, defaults_map=None, defaults_str=None, num=None, prop=None):
		"""
		\if jp

		\brief ���󥹥ȥ饯��

		(1) Properties(key = None, value = None)
		key �� value �Τߤ�Ϳ���� Property �Υ롼�ȥΡ��ɤ�������롣
		�ͤ����ƥǥե�����ͤȤ������ꤵ��롣

		(2) Properties(defaults=None)
			std::string �� std::map ��ǥե�����ͤˤ��Properties��������롣
			�ͤ����ƥǥե�����ͤȤ������ꤵ��롣

		(3) Properties(defaults=None, num = LONG_MAX)
			���ꤵ�줿�ǥե�����ͤ���Ķ��Υץ�ѥƥ��ꥹ�Ȥ�������롣
			�ͤ����ƥǥե�����ͤȤ������ꤵ��롣
			�ǥե�����ͤ� char* ������ˤ��Ϳ����졢key �� value ���ФˤʤäƤ��ꡢ
			�ꥹ�Ȥν�ü������ο���ɽ������ num ������ʸ���� key ��Ϳ������ʤ����
			�ʤ�ʤ���
			�ʲ�����򼨤���

			const char* defaults = {
				"key1", "value1",
				"key2", "value2",
				"key3", "value3",
				"key4", "value4",
				"key5", "value5",
				"" };
			Properties p(defaults);
			// �⤷����
			Properties p(defaults, 10);

		(4) Properties(prop=None)
			������Ϳ����줿 Properties �Υ������ͤ���ӥǥե�����ͤ�
			���Ƥ��Τޤޥ��ԡ�����롣

		\else
		\brief Constructor

		Creates a root node of Property with root's key and value.

		\endif
		"""
		self.default_value = ""
		self.root = None
		self.empty = ""
		self.leaf = []

		# Properties::Properties(const Properties& prop)
		if prop != None:
			self.name          = prop.name
			self.value         = prop.value
			self.default_value = prop.default_value

			keys = prop.propertyNames()
			for _key in keys:
				node = None
				node = prop.getNode(_key)
				if node != None:
					self.setDefault(_key, node.default_value)
					self.setProperty(_key, node.value)
					
			return


		# Properties::Properties(const char* key, const char* value)
		if key != None:
			self.name = key
			if value == None:
				self.value = ""
			else:
				self.value = value
			return
		

		self.name  = ""
		self.value = ""

		# Properties::Properties(std::map<std::string, std::string>& defaults)
		if defaults_map != None:
			#for i in range(len(defaults_map.items())):
			#	self.setDefault(defaults_map.keys()[i], defaults_map.values()[i])
			for key, value in defaults_map.items():
				self.setDefault(key, value)
			return


		if defaults_str != None:
			if num == None:
				_num = sys.maxint
			else:
				_num = num
			self.setDefaults(defaults_str, _num)
			return


	def assigmentOperator(self, prop):
		"""
		\if jp
		\brief �����黻��

			�����ͤ� Properties �Υ������ͤ���ӥǥե�����ͤ����ƺ�����졢
			�����ͤ� Properties �Υ������ͤ���ӥǥե�����ͤ����Ƥ��Τޤ�
			���ԡ�����롣
		\param prop(OpenRTM.Properties)
		\else
		\brief Assignment operator
		\param prop(OpenRTM.Properties)
		\endif
		"""
		self.clear()
		self.name = prop.name
		self.value = prop.value
		self.default_value = prop.default_value

		keys = prop.propertyNames()

		for key in keys:
			node = None
			node = prop.getNode(key)
			if node != None:
				self.setDefault(key, node.default_value)
				self.setProperty(key, node.value)

		return self


	def __del__(self):
		"""
		\if jp
		\brief �ǥ��ȥ饯��
		\else
		\brief Destructor
		\endif
		"""
		self.clear()
		if self.root != None:
			self.root.removeNode(self.name)
		return
    

    #============================================================
    # public functions
    #============================================================
    

	def getName(self):
		return self.name
	
	def getValue(self):
		return self.value
	
	def getDefaultValue(self):
		return self.default_value

	def getLeaf(self):
		return self.leaf
	
	def getRoot(self):
		return self.root


	def getProperty(self, key, default=None):
		"""
		\if jp

		\brief ���ꤵ�줿��������ĥץ�ѥƥ��򡢥ץ�ѥƥ��ꥹ�Ȥ���õ���� 

		���ꤵ�줿��������ĥץ�ѥƥ��򡢥ץ�ѥƥ��ꥹ�Ȥ���õ����
		���Υ������ץ�ѥƥ��ꥹ�Ȥˤʤ��ȡ��ǥե���ȤΥץ�ѥƥ��ꥹ�ȡ�
		����ˤ��Υǥե�����ͤ������֤�Ĵ�٤��롣
		���Υץ�ѥƥ������Ĥ���ʤ����ϡ��ǥե�����ͤΰ������֤���롣 

		\param key(string) �ץ�ѥƥ�����
		\param defaultValue(string) �ǥե������
		\return ���ꤵ�줿�����ͤ���Ĥ��Υץ�ѥƥ��ꥹ�Ȥ���

		\else

		\brief Searches for the property with the specified key in this property

		Searches for the property with the specified key in this property list.
		If the key is not found in this property list, the default property list,
		and its defaults, recursively, are then checked. The method returns the
		default value argument if the property is not found.

		\param key(string) the property key
		\param defaultValue(string) a default value. 
		\return the value in this property list with the specified key value.

		\endif
		"""
		if default == None:
			keys = []
			#keys = string.split(key, ".")
			self.split(key, ".", keys)

			node = None
			node = self._getNode(keys, 0, self)
			if node != None:
				if node.value != "":
					return node.value
				else:
					return node.default_value
			return self.empty

		else:
			value = self.getProperty(key)
			if value == "":
				return default
			else:
				return value


	def getDefault(self, key):
		"""
		\if jp
		\brief ���ꤵ�줿�������Ф��ƥǥե�����ͤ����ꤹ��
		\param key(string)
		\else
		\brief Set value as the default value to specified key's property
		\param key(string)
		\endif
		"""
		keys = []
		#keys = string.split(key, ".")
		self.split(key, ".", keys)
		node = None
		node = self._getNode(keys, 0, self)
		if node != None:
			return node.default_value

		return self.empty


	def setProperty(self, key, value=None):
		"""
		\if jp

		\brief Properties �� value �� key �ˤĤ�����Ͽ����

		Properties �� value �� key �ˤĤ�����Ͽ���롣
		���Ǥ� key ���Ф����ͤ���äƤ����硢����ͤ˸Ť��ͤ��֤���

		\param key(string) �ץ�ѥƥ��ꥹ�Ȥ����֤���륭��
		\param value(string) key ���б������� 
		\return �ץ�ѥƥ��ꥹ�Ȥλ��ꤵ�줿�����������͡����줬�ʤ����� null

		\else

		\brief Sets a value associated with key in the property list

		This method sets the "value" associated with "key" in the property list.
		If the property list has a value of "key", old value is returned.

		\param key(string) the key to be placed into this property list.
		\param value(string) the value corresponding to key. 
		\return the previous value of the specified key in this property list,
			or null if it did not have one.

		\endif
		"""
		if value != None:
			keys = []
			#keys = string.split(key, ".")
			self.split(key, ".", keys)
			curr = self
			for _key in keys:
				next = curr.hasKey(_key)
				if next == None:
					next = OpenRTM.Properties(key=_key)
					next.root = curr
					curr.leaf.append(next)
				curr = next
			retval = curr.value
			curr.value = value
			return retval

		else:
			self.setProperty(key, self.getProperty(key))
			prop = self.getNode(key)
			return prop.value


	def setDefault(self, key, value):
		"""
		\if jp
		\brief Properties �˥ǥե���� value �� key �ˤĤ�����Ͽ����
		\param key(string)
		\param value(string)
		\else
		\brief Sets a default value associated with key in the property list
		\param key(string)
		\param value(string)
		\endif
		"""
		keys = []
		self.split(key, ".", keys)
		#keys = string.split(key, ".")

		curr = self
		for _key in keys:
			next = curr.hasKey(_key)
			if next == None:
				next = OpenRTM.Properties(key=_key)
				next.root = curr
				curr.leaf.append(next)
			curr = next
		if value != "" and value[-1] == "\n":
			value = value[0:len(value)-1]
		curr.default_value = value
		return value


	def setDefaults(self, defaults, num = None):
		"""
		\if jp
		\brief Properties �˥ǥե�����ͤ�ޤȤ����Ͽ����
		\param defaults(string�Υꥹ��)
		\param num(long)
		\else
		\brief Sets a default value associated with key in the property list
		\param defaults(list of string)
		\param num(long)
		\endif
		"""
		if num == None:
			num = sys.maxint

		i = 0
		len_ = len(defaults)
		while 1:
			if i > num or i > (len_ - 1) or defaults[i] == "":
				break

			key = [defaults[i]]
			value = [defaults[i+1]]

			OpenRTM.eraseHeadBlank(key)
			OpenRTM.eraseTailBlank(key)

			OpenRTM.eraseHeadBlank(value)
			OpenRTM.eraseTailBlank(value)

			self.setDefault(key[0], value[0])

			i +=2

		
    
    #============================================================
	# load and save functions
    #============================================================
 
	def list(self, out):
		"""
		\if jp
		
		\brief ���ꤵ�줿���ϥ��ȥ꡼��ˡ��ץ�ѥƥ��ꥹ�Ȥ���Ϥ���

		���ꤵ�줿���ϥ��ȥ꡼��ˡ��ץ�ѥƥ��ꥹ�Ȥ���Ϥ��롣
		���Υ᥽�åɤϼ�˥ǥХå����Ѥ����롣

		\param out ���ϥ��ȥ꡼��

		\else

		\brief Prints this property list out to the specified output stream

		Prints this property list out to the specified output stream.
		This method is useful for debugging.

		\param out an output stream.

		\endif
		"""
		self._store(out, "", self)
		return


	def load(self, inStream):
		"""
		\if jp

		\brief ���ϥ��ȥ꡼�फ�饭�������Ǥ��Фˤʤä��ץ�ѥƥ��ꥹ�Ȥ��ɤ߹���

		���ϥ��ȥ꡼�फ�饭�������Ǥ��Фˤʤä��ץ�ѥƥ��ꥹ�Ȥ��ɤ߹��ࡣ
		���ȥ꡼��ϡ�ISO 8859-1 ʸ�����󥳡��ǥ��󥰤���Ѥ��Ƥ���Ȥߤʤ���롣
		�ƥץ�ѥƥ��ϡ����ϥ��ȥ꡼��˹�ñ�̤���Ͽ����Ƥ����ΤȤߤʤ��졢
		�ƹԤϹԶ��ڤ�ʸ�� (\n��\r���ޤ��� \r\n) �ǽ���롣
		���ϥ��ȥ꡼�फ���ɤ߹�����Ԥϡ����ϥ��ȥ꡼��ǥե�����ν�����
		ã����ޤǽ�������롣

		����ʸ�������ιԡ��ޤ��Ϻǽ�������ʸ���� ASCII ʸ��   �ޤ��� ! �Ǥ���
		�Ԥ�̵�뤵��롣�Ĥޤꡢ  �ޤ��� ! �ϥ����ȹԤ򼨤���

		����Ԥޤ��ϥ����ȹ԰ʳ��Τ��٤ƤιԤϡ��ơ��֥���ɲä����ץ�ѥƥ�
		�򵭽Ҥ��롣���������Ԥν���꤬ \ �ξ��ϡ����ιԤ�����з�³�ԤȤ���
		�����ޤ� (�����򻲾�)�� �����ϡ��ǽ�������ʸ�����顢�ǽ�� ASCII ʸ��
		=��:���ޤ��϶���ʸ����ľ���ޤǤΡ�����Τ��٤Ƥ�ʸ�����鹽������롣

		�����ν����򼨤�ʸ���ϡ����� \ ���դ��뤳�Ȥˤ�ꥭ���˴ޤ�뤳�Ȥ�
		�Ǥ��롣�����θ��ζ���Ϥ��٤ƥ����åפ���롣
		�����θ��κǽ�������ʸ���� = �ޤ��� : �Ǥ�����ϡ������Υ�����
		̵�뤵�졢���Τ��Ȥζ���ʸ���⤹�٤ƥ����åפ���롣
		����Τ���ʳ���ʸ���Ϥ��٤ơ���Ϣ��������ʸ����ΰ����Ȥʤ롣
		����ʸ������Ǥϡ�ASCII ���������ץ������� \t��\n��\r��\\��\"��\'��
		\ (�ߵ���ȥ��ڡ���)������� \uxxxx ��ǧ�����졢ñ�Ȥ�ʸ�����Ѵ�����롣
		�ޤ����ԤκǸ��ʸ���� \ �Ǥ�����ϡ����ιԤϸ��ߤιԤη�³�Ȥ���
		�����롣���ξ�硢\ �ȹԶ��ڤ�ʸ�����˴����졢��³�Ԥ���Ƭ�˶���
		����Ф���⤹�٤��˴����졢����ʸ����ΰ����ˤϤʤ�ʤ��� 

		���Ȥ��С����� 4 �ԤϤ��줾�쥭�� Truth �ȡ���Ϣ���������� Beauty ��ɽ����

		Truth = Beauty <BR>
		Truth:Beauty <BR>
		Truth			:Beauty <BR>

		�ޤ������� 3 �Ԥ� 1 �ĤΥץ�ѥƥ���ɽ���� 

		fruits				apple, banana, pear, \ <BR>
			cantaloupe, watermelon, \ <BR>
			kiwi, mango <BR>
		������ fruits �ǡ��������Ǥ˴�Ϣ�դ�����롣 
		"apple, banana, pear, cantaloupe, watermelon, kiwi, mango"
		�ǽ�Ū�ʷ�̤ǥ���ޤΤ��Ȥ�ɬ�����ڡ�����ɽ�������褦�ˡ�
		�� \ �����˥��ڡ��������롣�Ԥν����򼨤� \ �ȡ���³�Ԥ���Ƭ�ˤ���
		������˴����졢¾��ʸ�����ִ�����ʤ��� 
		�ޤ������� 3 ���ܤ���Ǥϡ������� cheeses �ǡ���Ϣ�������Ǥ�����ʸ����
		�Ǥ��뤳�Ȥ�ɽ���� 

		cheeses <BR>
		�����ϡ�cheeses �ǡ���Ϣ���Ǥ϶���ʸ����Ǥ��뤳�Ȥ���ꤷ�Ƥ��롣 

		\param inStream ���ϥ��ȥ꡼�� 

		\else

		\brief Loads property list consists of key:value from input stream

		Reads a property list (key and element pairs) from the input stream.
		The stream is assumed to be using the ISO 8859-1 character encoding; that
		is each byte is one Latin1 character. Characters not in Latin1, and
		certain special characters, can be represented in keys and elements using
		escape sequences similar to those used for character and string literals
		The differences from the character escape sequences used for characters
		and strings are: 
		- Octal escapes are not recognized. 
		- The character sequence \b does not represent a backspace character. 
		- The method does not treat a backslash character, \, before a non-valid
		escape character as an error; the backslash is silently dropped. For
		example, in a Java string the sequence "\z" would cause a compile time
		error. In contrast, this method silently drops the backslash. Therefore,
		this method treats the two character sequence "\b" as equivalent to the
		single character 'b'. 
		- Escapes are not necessary for single and double quotes; however, by the
		rule above, single and double quote characters preceded by a backslash
		still yield single and double quote characters, respectively. 
		An IllegalArgumentException is thrown if a malformed Unicode escape
		appears in the input. 

		This method processes input in terms of lines. A natural line of input is
		terminated either by a set of line terminator characters
		(\n or \r or \r\n) or by the end of the file. A natural line may be either
		a blank line, a comment line, or hold some part of a key-element pair.
		The logical line holding all the data for a key-element pair may be spread
		out across several adjacent natural lines by escaping the line terminator
		sequence with a backslash character, \. Note that a comment line cannot be
		extended in this manner; every natural line that is a comment must have
		its own comment indicator, as described below. If a logical line is
		continued over several natural lines, the continuation lines receive
		further processing, also described below. Lines are read from the input
		stream until end of file is reached. 

		A natural line that contains only white space characters is considered
		blank and is ignored. A comment line has an ASCII ' ' or '!' as its first
		non-white space character; comment lines are also ignored and do not
		encode key-element information. In addition to line terminators, this
		method considers the characters space (' ', '\u0020'), tab 
		('\t', '\u0009'), and form feed ('\f', '\u000C') to be white space. 

		If a logical line is spread across several natural lines, the backslash
		escaping the line terminator sequence, the line terminator sequence, and
		any white space at the start the following line have no affect on the key
		or element values. The remainder of the discussion of key and element
		parsing will assume all the characters constituting the key and element
		appear on a single natural line after line continuation characters have
		been removed. Note that it is not sufficient to only examine the character
		preceding a line terminator sequence to see if the line terminator is
		escaped; there must be an odd number of contiguous backslashes for the
		line terminator to be escaped. Since the input is processed from left to
		right, a non-zero even number of 2n contiguous backslashes before a line
		terminator (or elsewhere) encodes n backslashes after escape processing. 

		The key contains all of the characters in the line starting with the first
		non-white space character and up to, but not including, the first
		unescaped '=', ':', or white space character other than a line terminator.
		All of these key termination characters may be included in the key by
		escaping them with a preceding backslash character; for example,

		\:\=

		would be the two-character key ":=". Line terminator characters can be
		included using \r and \n escape sequences. Any white space after the key
		is skipped; if the first non-white space character after the key is '=' or
		':', then it is ignored and any white space characters after it are also
		skipped. All remaining characters on the line become part of the
		associated element string; if there are no remaining characters, the
		element is the empty string "". Once the raw character sequences
		constituting the key and element are identified, escape processing is
		performed as described above. 

		As an example, each of the following three lines specifies the key "Truth"
		and the associated element value "Beauty": 

		Truth = Beauty <BR>
		Truth:Beauty <BR>
		Truth                  :Beauty <BR>
		As another example, the following three lines specify a single property: 

		fruits                           apple, banana, pear, \ <BR>
			cantaloupe, watermelon, \ <BR>
			kiwi, mango <BR>
		The key is "fruits" and the associated element is: 
		"apple, banana, pear, cantaloupe, watermelon, kiwi, mango"Note that a
		space appears before each \ so that a space will appear after each comma
		in the final result; the \, line terminator, and leading white space on
		the continuation line are merely discarded and are not replaced by one or
		more other characters. 
		As a third example, the line: 

		cheeses <BR>
		specifies that the key is "cheeses" and the associated element is the
		empty string "".

		\param inStream the input stream.

		\endif
		"""
		pline = ""
		for readStr in inStream:
			if not readStr:
				continue
			
			tmp = [readStr]
			OpenRTM.eraseHeadBlank(tmp)
			_str = tmp[0]
			
			if _str[0] == "#" or _str[0] == "!" or _str[0] == "\n":
				continue

			if _str[-1] == "\n":
				_str = _str[0:len(_str)-1]

			if _str[len(_str)-1] == "\\" and not OpenRTM.isEscaped(_str, len(_str)-1):
				#_str = _str[0:len(_str)-1]
				tmp = [_str[0:len(_str)-1]]
				OpenRTM.eraseTailBlank(tmp)
				#pline += _str
				pline += tmp[0]
				continue
			pline += _str
			if pline == "":
				continue

			key = []
			value = []
			self.splitKeyValue(pline, key, value)
			key[0] = OpenRTM.unescape(key)
			OpenRTM.eraseHeadBlank(key)
			OpenRTM.eraseTailBlank(key)

			value[0] = OpenRTM.unescape(value)
			OpenRTM.eraseHeadBlank(value)
			OpenRTM.eraseTailBlank(value)

			self.setProperty(key[0], value[0])
			pline = ""


	def save(self, out, header):
		"""
		\if jp

		\brief �ץ�ѥƥ��ꥹ�Ȥ���ꤵ�줿���ȥ꡼�����¸����

		�侩����Ƥ��ޤ��󡣥ץ�ѥƥ��ꥹ�Ȥ���¸��ˡ�Ȥ��Ƥϡ�
		store(ostream out, string header) �᥽�åɤλ��Ѥ��侩����롣
		���Υ᥽�åɤ� Java Properties �Ȥθߴ����Τ�����������Ƥ��롣

		\param out ���ϥ��ȥ꡼��
		\param header �ץ�ѥƥ��ꥹ�Ȥε��� 

		\else

		\brief Save the properties list to the stream

		Deprecated. 

		\param out The output stream
		\param header A description of the property list

		\endif
		"""
		self.store(out, header)
		return


	def store(self, out, header):
		"""
		\if jp

		\brief �ץ�ѥƥ��ꥹ�Ȥ���ϥ��ȥ꡼�����¸����

		Properties �ơ��֥���Υץ�ѥƥ��ꥹ�� (���������ǤΥڥ�) ��load
		�᥽�åɤ�Ȥä� Properties �ơ��֥�˥��ɤ���Τ�Ŭ�ڤʥե����ޥåȤ�
		���ϥ��ȥ꡼��˽񤭹��ߤޤ��� 

		Properties �ơ��֥���Υץ�ѥƥ��ꥹ�� (���������ǤΥڥ�) ��load
		�᥽�åɤ�Ȥä� Properties �ơ��֥�˥��ɤ���Τ�Ŭ�ڤʥե����ޥåȤ�
		���ϥ��ȥ꡼��˽񤭹��ߤޤ������ȥ꡼��ϡ�ISO 8859-1 ʸ��
		���󥳡��ǥ��󥰤���Ѥ��ƽ񤭹��ޤ�ޤ��� 
		Properties �ơ��֥� (¸�ߤ�����) �Υǥե���ȥơ��֥뤫���
		�ץ�ѥƥ��ϡ����Υ᥽�åɤˤ�äƤϽ񤭹��ޤ�ޤ��� 

		header ������ null �Ǥʤ����ϡ�ASCII ʸ����  ��header ��ʸ����
		����ӹԶ��ڤ�ʸ�����ǽ�˽��ϥ��ȥ꡼��˽񤭹��ޤ�ޤ������Τ��ᡢ
		header �ϼ��̥����ȤȤ��ƻȤ����Ȥ��Ǥ��ޤ��� 

		���ˡ�ASCII ʸ����  �����ߤ����� (Date �� toString �᥽�åɤˤ�ä�
		���߻��郎���������Τ�Ʊ��)������� Writer �ˤ�ä����������Զ��ڤ�
		����ʤ륳���ȹԤ��񤭹��ޤ�ޤ��� 

		³���ơ�Properties �ơ��֥���Τ��٤ƤΥ���ȥ꤬ 1 �Ԥ��Ľ񤭽Ф���ޤ���
		�ƥ���ȥ�Υ���ʸ����ASCII ʸ���� =����Ϣ��������ʸ���󤬽񤭹��ޤ��
		��������ʸ����γ�ʸ���ϡ����������ץ������󥹤Ȥ������褹��ɬ�פ����뤫
		�ɤ�����ǧ����ޤ���ASCII ʸ���� \�����֡����ԡ�����������Ϥ��줾�� \\��
		\t��\n������� \r �Ȥ��ƽ񤭹��ޤ�ޤ���\u0020 ��꾮����ʸ�������
		\u007E ����礭��ʸ���ϡ��б����� 16 ���� xxxx ��Ȥä� \uxxxx �Ȥ��ƽ�
		���ޤ�ޤ��������߶���ʸ���Ǥ��񤭶���ʸ���Ǥ�ʤ���Զ���ʸ���ϡ�
		���� \ ���դ��ƽ񤭹��ޤ�ޤ����������ͤ�ʸ��  ��!��=������� : �ϡ�
		ɬ�����������ɤ����褦�ˡ����˥���å�����դ��ƽ񤭹��ޤ�ޤ��� 

		����ȥ꤬�񤭹��ޤ줿���Ȥǡ����ϥ��ȥ꡼�ब�ե�å��夵��ޤ���
		���ϥ��ȥ꡼��Ϥ��Υ᥽�åɤ��������������ȤⳫ�����ޤޤǤ��� 

		\else

		\brief Stores property list to the output stream

		Writes this property list (key and element pairs) in this Properties table
		to the output stream in a format suitable for loading into a Properties
		table using the load method. The stream is written using the ISO 8859-1
		character encoding. 

		Properties from the defaults table of this Properties table (if any) are
		not written out by this method. 

		If the comments argument is not null, then an ASCII   character, the
		comments string, and a line separator are first written to the output
		stream. Thus, the comments can serve as an identifying comment. 

		Next, a comment line is always written, consisting of an ASCII  
		character, the current date and time (as if produced by the toString
		method of Date for the current time), and a line separator as generated
		by the Writer. 

		Then every entry in this Properties table is written out, one per line.
		For each entry the key string is written, then an ASCII =, then the
		associated element string. Each character of the key and element strings
		is examined to see whether it should be rendered as an escape sequence.
		The ASCII characters \, tab, form feed, newline, and carriage return are
		written as \\, \t, \f \n, and \r, respectively. Characters less than
		\u0020 and characters greater than \u007E are written as \uxxxx for the
		appropriate hexadecimal value xxxx. For the key, all space characters are
		written with a preceding \ character. For the element, leading space
		characters, but not embedded or trailing space characters, are written
		with a preceding \ character. The key and element characters  , !, =, and
		: are written with a preceding backslash to ensure that they are properly
		loaded. 

		After the entries have been written, the output stream is flushed. The
		output stream remains open after this method returns. 

		\param out an output stream.
		\param header a description of the property list.

		\endif
		""" 
		out.write("#"+header+"\n")
		self._store(out, "", self)

    
	#============================================================
	# other util functions
	#============================================================
 
	def propertyNames(self):
		""" 
		\if jp

		\brief �ץ�ѥƥ��Υ����Υꥹ�Ȥ� vector ���֤�

		�ᥤ��ץ�ѥƥ��ꥹ�Ȥ�Ʊ��̾���Υ��������Ĥ���ʤ����ϡ��ǥե���Ȥ�
		�ץ�ѥƥ��ꥹ�Ȥˤ�����̤Υ�����ޤࡢ���Υץ�ѥƥ��ꥹ�Ȥˤ��뤹�٤�
		�Υ����Υꥹ�Ȥ��֤��ޤ��� 

		\return �ץ�ѥƥ��ꥹ�Ȥˤ��뤹�٤ƤΥ����Υꥹ�ȡ�
			�ǥե���ȤΥץ�ѥƥ��ꥹ�Ȥˤ��륭����ޤ�

		\else

		\brief Returns an vector of all the keys in this property

		Returns an enumeration of all the keys in this property list, including
		distinct keys in the default property list if a key of the same name has
		not already been found from the main properties list.

		\return an vector of all the keys in this property list, including the
			keys in the default property list.

		\endif
		""" 
		names = []
		for leaf in self.leaf:
			self._propertiyNames(names, leaf.name, leaf)
		return names


	def size(self):
		""" 
		\if jp
		\brief �ץ�ѥƥ��ο����������
		\else
		\brief Get number of Properties
		\endif
		""" 
		return len(self.propertyNames())


	def getNode(self, key):
		""" 
		\if jp
		\brief �Ρ��ɤ��������
		\param key(string)
		\else
		\brief Get node of Properties
		\param key(string)
		\endif
		""" 
		keys = []
		value = ""
		self.split(key, ".", keys)
		return self._getNode(keys, 0, self)

	
	def createNode(self, key):
		"""
		 \param key(string)
		"""
		p = self.getNode(key)
		if p != None:
			return False
		
		self.setProperty(key,"")
		return True


	def removeNode(self, leaf_name):
		""" 
		\if jp
		\brief �Ρ��ɤ����Ǥ���
		\param leaf_name(string)
		\else
		\brief Get node of Properties
		\param leaf_name(string)
		\endif
		""" 
		len_ = len(self.leaf)
		for i in range(len_):
			idx = (len_ - 1) - i
			if self.leaf[idx].name == leaf_name:
				prop = self.leaf[idx]
				del self.leaf[idx]
				return prop
		return None


	def hasKey(self, key):
		""" 
		\if jp
		\brief �ҥΡ��ɤ�key�����뤫�ɤ���
		\param key(string)
		\else
		\brief If key exists in the children
		\param key(string)
		\endif
		""" 
		for leaf in self.leaf:
			if leaf.name == key:
				return leaf

		return None


	def clear(self):
		""" 
		\if jp
		\brief �ҥΡ��ɤ����ƺ������
		\else
		\brief If key exists in the children
		\endif
		""" 
		len_ = len(self.leaf)
		for i in range(len_):
			if self.leaf[-1] != None:
				del self.leaf[-1]

		return


	def mergeProperties(self, prop):
		""" 
		\if jp
		\brief Property��ޡ�������
		\param prop(OpenRTM.Properties)
		\else
		\brief Merge properties
		\param prop(OpenRTM.Properties)
		\endif
		C++�� Properties& Properties::operator<<(const Properties& prop)�μ���
		""" 
		keys = prop.propertyNames()

		for i in range(prop.size()):
			self.setProperty(keys[i], prop.getProperty(keys[i]))

		return self


	def splitKeyValue(self, _str, key, value):
		"""
		 \param _str(string)
		 \param key(string)
		 \param value(string)
		"""
		i = 0
		length = len(_str)

		while i < length:
			if (_str[i] == ":" or _str[i] == "=") and not OpenRTM.isEscaped(_str, i):
				key.append(_str[0:i])
				value.append(_str[i+1:])
				return
			i += 1

		# If no ':' or '=' exist, ' ' would be delimiter.
		i = 0
		while i < length:
			if (_str[i] == " ") and not OpenRTM.isEscaped(_str, i):
				key.append(_str[0:i])
				value.append(_str[i+1:])
				return
			i += 1

		key.append(_str)
		value.append("")
		return


	def split(self, _str, delim, value):
		"""
		 \param _str(string)
		 \param delim(string)
		 \param value(string)
		"""
		if _str == "":
			return False

		begin_it = end_it = 0

		length = len(_str)

		while end_it < length:
			if _str[end_it] == delim and not OpenRTM.isEscaped(_str, end_it):
				value.append(_str[begin_it:end_it])
				begin_it = end_it + 1
			end_it += 1

		value.append(_str[begin_it:end_it])
		return True
	

	def _getNode(self, keys, index, curr):
		"""
		 \param keys(string�Υꥹ��)
		 \param index(long)
		 \param curr(OpenRTM.Properties)
		"""
		next = curr.hasKey(keys[index])

		if next == None:
			return None

		if index < (len(keys) - 1):
			index+=1
			return next._getNode(keys, index, next)
		else:
			return next

		return None


	def _propertiyNames(self, names, curr_name, curr):
		"""
		 \param names(string�Υꥹ��)
		 \param curr_name(string)
		 \param curr(OpenRTM.Properties)
		"""
		if len(curr.leaf) > 0:
			for i in range(len(curr.leaf)):
				next_name = curr_name+"."+curr.leaf[i].name
				self._propertiyNames(names, next_name, curr.leaf[i])
		else:
			names.append(curr_name)

		return
				


	def _store(self, out, curr_name, curr):
		if len(curr.leaf) > 0:
			for i in range(len(curr.leaf)):
				if curr_name == "":
					next_name = curr.leaf[i].name
				else:
					next_name = curr_name+"."+curr.leaf[i].name
				self._store(out, next_name, curr.leaf[i])
				
		else:
			val = curr.value
			if val == "":
				val = curr.default_value
			out.write(curr_name+": "+val+"\n")

		return
				

	def indent(self, index):
		"""
		 \param index(int)
		"""
		space = ""

		for i in range(index-1):
			space += " "

		return space


	def _dump(self, out, curr, index):
		if index != 0:
			#ut.write(self.indent(index)+"- "+curr.name)
			out[0]+=self.indent(index)+"- "+curr.name

		if curr.leaf == []:
			if curr.value == "":
				#out.write(": "+curr.default_value+"\n")
				out[0]+=": "+curr.default_value+"\n"
			else:
				#out.write(": "+curr.value+"\n")
				out[0]+=": "+str(curr.value)+"\n"
			return out[0]

		if index != 0:
			#out.write("\n")
			out[0]+="\n"

		for i in range(len(curr.leaf)):
			self._dump(out, curr.leaf[i], index + 1)

		return out[0]


    

	def __str__(self):
		"""
		friend std::ostream& operator<<(std::ostream& lhs, const Properties& rhs);
		������ˡ�print obj�ˤƸƤӽФ���ǽ�Ȥ��Ƥ��롣
		"""
		string=[""]
		return self._dump(string, self, 0)

	
