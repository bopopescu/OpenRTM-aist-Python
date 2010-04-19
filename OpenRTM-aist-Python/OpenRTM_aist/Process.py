#!/usr/bin/env python
# -*- coding: euc-jp -*-


##
# \file Process.py
# \brief Process handling functions
# \author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2010
#     Noriaki Ando
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import os,sys
import subprocess
import signal

##
# @if jp
# @brief �ץ�����ư����
# @else
# @brief Launching a process
# @endif
#
# int launch_shell(std::string command)
def launch_shell(command):
  try:
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
  except:
    pass

  args = command.split(" ")
  subproc_args = { 'stdin':     None,
                   'stdout':    None,
                   'stderr':    None,
                   'cwd':       None,
                   'close_fds': False }
  try:
    p = subprocess.Popen(args, **subproc_args)
  except OSError:
    # fork failed
    print sys.exc_info()[0]
    return -1
  return 0

