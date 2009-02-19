#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file TimeMeasure.py
# @brief Periodic time measurement class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2009
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#
#

import time
import math

import OpenRTM_aist

ULLONG_MAX = 0xffffffffffffffff

##
# @if jp
# @brief ����ñ���Ѵ������
# @else
# @endif
usec_per_sec = 1000000

##
# @if jp
# @class Time
# @brief ���ִ����ѥ��饹
# 
# ���ꤷ�������ͤ��ݻ����뤿��Υ��饹��
# 
# @since 0.4.1
# 
# @else
# 
# @endif
class Time:

    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯����
    #
    # @param self
    #
    # @else
    # @brief Constructor.
    #
    # Constructor.
    #
    # @param self
    #
    # @endif
    def __init__(self):
        global usec_per_sec
        tm = time.time()
        tm_f       = tm - int(tm)     # �������μ��Ф�
        self.sec   = int(tm - tm_f)   # �������μ��Ф�
        self.usec  = int(tm_f * usec_per_sec) # sec -> usec (micro second)
        self._timevalue = OpenRTM_aist.TimeValue(self.sec,self.usec)


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
        global usec_per_sec

        res = Time()
    
        if self.sec >= tm.sec:
            if self.usec >= tm.usec:
                res.sec  = self.sec  - tm.sec
                res.usec = self.usec - tm.usec
            else:
                res.sec  = self.sec  - tm.sec - 1
                res.usec = (self.usec + usec_per_sec) - tm.usec
        else:
            if tm.usec >= self.usec:
                res.sec  = -(tm.sec  - self.sec)
                res.usec = -(tm.usec - self.usec)
            else:
                res.sec  = -(tm.sec - self.sec - 1)
                res.usec = -(tm.usec + usec_per_sec) + self.usec
        return res

    
    def gettimeofday(self):
        global usec_per_sec
        tm = time.time()
        tm_f       = tm - int(tm)     # �������μ��Ф�
        self.sec   = int(tm - tm_f)   # �������μ��Ф�
        self.usec  = int(tm_f * usec_per_sec) # sec -> usec (micro second)
        return OpenRTM_aist.TimeValue(self.sec, self.usec)

##
# TimeMeasure object
#
# This object is used for getting statistics of code execution time. 
# Using get_stat you can get maximum, minimum, mean and standard
# deviation time for code execution.
#
class TimeMeasure:

    ##
    # @brief Time statictics object for profiling.
    # 
    # Constructor
    #
    def __init__(self, buflen=100):
        self._countMax = buflen+1
        self._record = [ OpenRTM_aist.TimeValue(0,0) for i in range(self._countMax) ]
        self._begin  = Time().gettimeofday()
        self._end  = Time().gettimeofday()
        self._count = 0
        self._recurred = False
    

    ##
    # @brief Begin time measurement for time statistics.
    #
    # Begin time measurement for time statistics
    #
    def tick(self):
        self._begin = Time().gettimeofday()
    

    ##
    # @brief Finish time measurement for time statistics.
    #
    # End of time measurement for time statistics
    #
    def tack(self):
        self._end = Time().gettimeofday()
        self._record[self._count % self._countMax] = self._end - self._begin
        self._count += 1
        if self._count > self._countMax:
            self._count = 0
            self._recurred = True
        

    def reset(self):
        self._count = 0
        self._recurred = False

    
    ##
    # Get number of time measurement buffer
    #
    # @brief Get number of time measurement buffer.
    #
    #
    def count(self):
        if self._recurred:
            return len(self._record)
        else:
            return self._count

    
    ##
    # @brief Get total statistics.
    # Get total statistics
    # max_interval, min_interval, mean_interval [ns]
    #
    def getStatistics(self, max_interval,min_interval,
                      mean_interval,stddev):
        global ULLONG_MAX
        max_interval[0] = 0
        min_interval[0] = ULLONG_MAX

        _sum = 0
        _sq_sum = 0
        _len = self.count()
        
        if _len == 0:
            return False

        for i in range(_len):
            _trecord = self._record[i].toDouble()
            _sum += _trecord
            _sq_sum += (_trecord * _trecord)

            if _trecord > max_interval[0]:
                max_interval[0] = _trecord
            
            if _trecord < min_interval[0]:
                min_interval[0] = _trecord
            
                
        mean_interval[0] = _sum / self._count
        stddev[0] = math.sqrt(_sq_sum / self._count - (mean_interval[0]*mean_interval[0]))

        return True
        
