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

import sys
import os

__author__ = "Ibrahim Khan"


class ParameterManager:

    SRC = "src"
    DST = "dst"
    COUNT = "count"
    DELETE = "delete"
    DO_EXPORT = "do_export"
    ASK_EXPORT = "ask_export"
    IS_INVALID = "is_invalid"
    EXPORT_PATH = "export_path"

    config = {SRC: ".", DST: [], COUNT: 0, DELETE: False, DO_EXPORT: True, ASK_EXPORT: True, IS_INVALID: True,
              EXPORT_PATH: ".\\export_list.log"}

    def __init__(self):
        self.parse_argv()

    def parse_argv(self):
        for i in sys.argv[1:]:
            parts = i.split("=")
            self.config[self.COUNT] += 1
            if len(parts) == 2:
                if parts[0] == "src":
                    self.config[self.SRC] = parts[1]
                if parts[0] == "dst":
                    self.config[self.DST].append(parts[1])
                if parts[0] == "delete":
                    if parts[1] == "y":
                        self.config[self.DELETE] = True
                    else:
                        self.config[self.DELETE] = False
                if parts[0] == "export":
                    if parts[1] == "ask":
                        self.config[self.ASK_EXPORT] = True
                    elif parts[1] == "y":
                        self.config[self.DO_EXPORT] = True
                    elif parts[1] == "n":
                        self.config[self.DO_EXPORT] = False

                if parts[0] == "exportfile":
                    self.config[self.EXPORT_PATH] = parts[1]

    def is_valid_config(self):
        if not os.path.exists(self.config[self.SRC]):
            return False
        for i in self.config[self.DST]:
            if not os.path.exists(i):
                return False
        if len(self.config[self.DST]) > 0:
            self.config[self.IS_INVALID] = False

        if self.config[self.COUNT] > 0 and not self.config[self.IS_INVALID]:
            return True
        else:
            return False

    def export_to_path(self, message_list):
        export_file = open(self.config[self.EXPORT_PATH], "a+")
        try:
            for line in message_list[1:]:
                export_file.write("%s\n" % line)
        except Exception as ex:
            print("Could not export log to file, cause : %s" % ex.message)
        finally:
            export_file.close()
            print("\nExport complete")

    def print_help(self):
        print("\nSynchronize from single source folder to multiple destination folders.")
        print("Will copy updated or new files and folders to the destination and"
              "\ndelete that doesn't exist in the source folder"
              "\n**Both source and destination folder must exist before running this")
        print("\nPLEASE USE WITH CAUTION, YOU HAVE BEEN WARNED\n")
        print("Command : %s parameters:values ..." % os.path.basename(sys.argv[0]))
        print("Parameters :")
        print("\n\tsrc=\"Source Folder\"\t\tDefault : Not Set")
        print("\t\t-->\tYou can use only one source folder")
        print("\n\tdst=\"Destination Folder 1\"\t\tDefault : Not Set")
        print("\tdst=\"Destination Folder 2\"")
        print("\t\t-->\tYou can use one destination folder or multiple folders")
        print("\n\tdelete=y\t\tDefault : delete=n")
        print("\t\t-->\tDelete file in the destination that does not exist in\n\t\t-->\tthe source folder")
        print("\n\tdelete=n\t\tDefault : delete=n")
        print("\t\t-->\tDon't delete file in the destination folder")
        print("\n\texport=ask\t\tDefault : export=ask")
        print("\t\t-->\tAsk for confirmation to export change list to file\n\t\t-->\tat the end of the process")
        print("\n\texport=y\t\tDefault : export=ask")
        print("\t\t-->\tExport change list automatically to the file")
        print("\n\texport=n\t\tDefault : export=ask")
        print("\t\t-->\tDon't export change list")
        print("\n\texportfile=\"Export File\"\t\tDefault : %s" % self.config[self.EXPORT_PATH])
        print("\t\t-->\tSet file name for the export change list")
