"""
Copyright (C) 2017 MD. Ibrahim Khan

Project Name: 
Author: MD. Ibrahim Khan
Author's Email: ib.arshad777@gmail.com

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this
   list of conditions and the following disclaimer in the documentation and/or
   other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of the contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTIONS) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
from os import path as m_path
import shutil
import inspect
from ReportGenerator import Report
from ConsoleProgressBar import CPB

__author__ = "Ibrahim Khan"


class FolderDiff:
    count = 0
    src = ""
    dst = []
    delete_mode = False
    delete_count = []
    progress_action = ""
    progress_msg = ""

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def index(self):
        self.count = 0
        for root, folders, files in os.walk(self.src):
            self.count += len(folders)
            self.count += len(files)

        if self.delete_mode:
            for dst in self.dst:
                cc = 0
                for root, folders, files in os.walk(dst):
                    for __folder in folders:
                        src_path = m_path.join(root, __folder)
                        src_path = src_path[len(dst) + 1:]
                        src_path = m_path.join(self.src, src_path)
                        if not m_path.exists(src_path):
                            cc += 1
                    for __file in files:
                        org_path = m_path.join(root, __file)
                        src_path = org_path[len(dst) + 1:]
                        src_path = m_path.join(self.src, src_path)
                        if not m_path.exists(src_path):
                            cc += 1
                self.delete_count.append(cc)

    def set_delete_mode(self, boolean):
        self.delete_mode = boolean

    def set_progress_percent_action(self, action):
        self.progress_action = action

    def set_progress_msg_action(self, action):
        self.progress_msg = action

    def run_progress(self, total, var, msg=""):
        if callable(self.progress_action):
            arg_spec = inspect.getargspec(self.progress_action)
            if len(arg_spec.args) == 1:
                try:
                    self.progress_action(int((float(var) / float(total)) * 100.00))
                except ZeroDivisionError as zr:
                    self.progress_action(100)
            if len(arg_spec.args) == 2:
                try:
                    self.progress_action(int((float(var) / float(total)) * 100.00), msg)
                except ZeroDivisionError as zr:
                    self.progress_action(100, msg)

    def run_progress_msg(self, msg):
        if callable(self.progress_msg):
            arg_spec = inspect.getargspec(self.progress_msg)
            if len(arg_spec.args) == 1:
                self.progress_msg(msg)

    def apply_update(self):
        self.index()
        dst_count = 0
        dst_len = len(self.dst)
        cc = 0
        for dst in self.dst:
            dst_count += 1
            current_count = 0
            if self.delete_mode:
                for root, folders, files in os.walk(dst):
                    for __folder in folders:
                        org_path = m_path.join(root, __folder)
                        src_path = org_path[len(dst) + 1:]
                        src_path = m_path.join(self.src, src_path)
                        if not m_path.exists(src_path):
                            os.remove(org_path)
                            self.run_progress_msg(Report.report(Report.DELETE, src_path))
                            current_count += 1
                            self.run_progress((self.count + self.delete_count[cc]), current_count, "%s/%s" % (dst_count, dst_len))
                    for __file in files:
                        org_path = m_path.join(root, __file)
                        src_path = org_path[len(dst) + 1:]
                        src_path = m_path.join(self.src, src_path)
                        if not m_path.exists(src_path):
                            os.remove(org_path)
                            self.run_progress_msg(Report.report(Report.DELETE, src_path))
                            current_count += 1
                            self.run_progress((self.count + self.delete_count[cc]), current_count, "%s/%s" % (dst_count, dst_len))

            for root, folders, files in os.walk(self.src):
                for __folder in folders:
                    dst_path = m_path.join(root, __folder)
                    dst_path = dst_path[len(self.src) + 1:]
                    dst_path = m_path.join(dst, dst_path)
                    if not m_path.exists(dst_path):
                        os.mkdir(dst_path)
                        self.run_progress_msg(Report.report(Report.MAKE_DIR, dst_path))

                    current_count += 1
                    self.run_progress(self.count, current_count, "%s/%s" % (dst_count, dst_len))
                for __file in files:
                    org_path = m_path.join(root, __file)
                    dst_path = org_path[len(self.src) + 1:]
                    dst_path = m_path.join(dst, dst_path)
                    if not m_path.exists(dst_path):
                        shutil.copy2(org_path, dst_path)
                        self.run_progress_msg(Report.report(Report.COPY, dst_path))
                    else:
                        org_mod_time = int(m_path.getmtime(org_path))
                        dst_mod_time = int(m_path.getmtime(dst_path))
                        if org_mod_time > dst_mod_time:
                            shutil.copy2(org_path, dst_path)
                            self.run_progress_msg(Report.report(Report.COPY, dst_path))
                    current_count += 1
                    self.run_progress(self.count, current_count, "%s/%s" % (dst_count, dst_len))
            cc += 1
        if dst_count != dst_len:
            CPB.clear_screen()
