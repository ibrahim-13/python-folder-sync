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

from backend.FolderDiffUtil import FolderDiff
from backend.ParamManager import ParameterManager as PMan
from backend import ConsoleProgressBar as consolePB


class FolderSyncApp:

    def __init__(self):
        pass

    @staticmethod
    def app_loader():
        pb = consolePB.CPB()
        p_manager = PMan()
        message = [""]

        if p_manager.is_valid_config():
            pass
        else:
            p_manager.print_help()
            exit(-1)

        f_diff = FolderDiff(p_manager.config[PMan.SRC], p_manager.config[PMan.DST])
        count = f_diff.count

        f_diff.set_delete_mode(p_manager.config[PMan.DELETE])

        def p_msg(msg):
            message.append(msg)

        def p_act(var, msg):
            pb.update(100, var, msg=msg, length=50)

        print("=== Synchronizing folders ===")
        print("Source :\n\t\t%s" % p_manager.config[PMan.SRC])
        print("Destination :")
        for i in p_manager.config[PMan.DST]:
            print("\t\t%s" % i)

        f_diff.set_progress_msg_action(p_msg)
        f_diff.set_progress_percent_action(p_act)
        f_diff.apply_update()

        if p_manager.config[PMan.DO_EXPORT]:
            if p_manager.config[PMan.ASK_EXPORT]:
                while True:
                    choose = raw_input("\nExport list to %s? y/n : " % p_manager.config[PMan.EXPORT_PATH])
                    if choose == "y" or choose == "y":
                        p_manager.export_to_path(message)
                        break
                    elif choose == "n" or choose == "N":
                        break
                    else:
                        print("Wrong input !")
