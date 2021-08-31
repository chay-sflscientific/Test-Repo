import pyfiglet
import os
import shutil
import glob
from datetime import datetime
import sys


class Preamble:
    def __init__(self):
        self.DATE_PREFIX = "#     Last Updated: "
        self.AUTO_FINAL_LINE = "# The above is automatically generated  - DO NOT TOUCH ABOVE THIS LINE.\n"
        self.ADD_MISSING = True

    def sfl_preamble(self, file_name: str, dt=None):
        """
        args:
            file_name (str):
        :param dt (:
        :return:
        """
        auto_final_line=self.AUTO_FINAL_LINE
        date_prefix=self.DATE_PREFIX
        if dt is None:
            dt = date.today()
            dt = dt.strftime("%d/%m/%Y")

        preamble = "#" * 80
        temp = pyfiglet.figlet_format(file_name)
        comment = "#\n"
        for x in temp.split('\n'):
            comment += "#  " + x + "\n"
        preamble += comment
        preamble += "#     SFL Scientifc\n"
        preamble += date_prefix + str(dt) + "\n"
        preamble += "#\n"
        preamble += auto_final_line

        preamble += "#\n#\n"
        preamble += "#\n#\n" + "#" * 80

        return preamble


    def preamble_matches(self, text_list, preamble_list):
        """
        Checks if the the start of the text_list is the same as the preamble
        args
        """
        date_prefix=self.DATE_PREFIX
        auto_final_line=self.AUTO_FINAL_LINE
        len_preamble = len(preamble_list)
        if len_preamble > len(text_list):
            return 0

        for x, y in zip(text_list[:len_preamble], preamble_list):
            if auto_final_line == str(x)[:len(auto_final_line)]:
                break
            if date_prefix == str(x)[:len(date_prefix)]:
                continue
            if x != y:
                return 0
        return 1


    def is_diff_skip(self, file_a, file_b):
        date_prefix=self.DATE_PREFIX
        if (not os.path.isfile(file_a)) or (not os.path.isfile(file_b)):
            return True

        di = self.difference(file_a, file_b)
        if len(di) == 1 and list(di)[0][:len(date_prefix)] == date_prefix:
            print(" Date line is only difference between files. Ignoring!")
            return False
        if len(di) != 0:
            print(" File has been updated since last preamble generation with differences: \n ", di)
            return True
        return False


    def difference(self, file_a, file_b):
        with open(file_a, 'r') as file1:
            with open(file_b, 'r') as file2:
                return set(file1).difference(file2)


    def skip(self, p, white_list, black_list):
        if black_list is None:
            black_list = [".~backup~", ".~temp~", "__init__.py"]
        if white_list is None:
            white_list = [".py"]
        sk = False
        for w in white_list:
            if w not in p:
                sk = True
        for b in black_list:
            if b in p:
                sk = True
        return sk


    def main(self, path, white_list=None, black_list=None):
        print(path)
        auto_final_flag=self.AUTO_FINAL_LINE
        date_prefix=self.DATE_PREFIX
        preamble_fn=self.sfl_preamble
        for p in glob.glob(path, recursive=True):
            if self.skip(p, white_list, black_list):
                continue

            # makes a temporary file as a check for change later
            tmp = p + '.~temp~'
            shutil.copyfile(p, tmp)

            # open the file and store each line in a list
            with open(p) as file:
                text_list = list(file.readlines())

            # in case the first line defines a script split it off
            script_header = []
            if len(text_list) > 0 and text_list[0][:2] == "#!":
                script_header, text_list = text_list[:1], text_list[1:]

            # generate datetime by the files modification time
            dt_full = os.path.getmtime(p)  # date of the file
            dt = datetime.fromtimestamp(dt_full).strftime("%Y-%m-%d")

            # filename
            base = os.path.basename(p)
            file_name, file_ext = os.path.splitext(base)

            # this generates preamble
            preamble = preamble_fn(file_name, dt)
            preamble_list = list([x + '\n' for x in preamble.split('\n')])

            # ONLY EVER REPLACE COMMENTED LINES
            if self.preamble_matches(text_list, preamble_list):
                print("PREAMBLE UPDATED TO LAST MODIFY DATE:", p)
                temp = script_header
                copy_exact = False
                for t in text_list:
                    text = t
                    if "#" != t[0] or auto_final_flag == t[:len(auto_final_flag)]:
                        # if the line isn't a comment then copy exaxt
                        copy_exact = True

                    if date_prefix == t[:len(date_prefix)] and not copy_exact:
                        text = date_prefix + dt + "\n"
                    temp.append(text)
                text_list = temp
            elif self.ADD_MISSING:
                print("ADDING MISSING:", p)
                text_list = script_header + preamble_list + text_list
            else:
                print('DO NOTHING')
                text_list = script_header + text_list

            # SAVE THE FILE INPLACE ONLY IF THE FILE CHANGES
            with open(p, 'w') as file:
                file.writelines(text_list)

            # change the date of the file to the stamp
            temp = datetime.fromtimestamp(dt_full).strftime("%Y%m%d%H%M")
            cmd = "touch -mt " + str(temp) + " '" + p + "'"
            os.system(cmd)

            # if the old file and the previous backup are different by more than the date move the tmp file to backup
            bkp = p + ".~backup~"
            if self.is_diff_skip(tmp, bkp):
                shutil.copyfile(tmp, bkp)

            #SANITY CHECK THAT THE NEW FILE p & TEMP FILE tmp differ only by DATE
         #   if self.is_diff_skip(p, tmp):
         #     shutil.copyfile(tmp, p)
         #     raise Exception("REVERTING! Something was modified in the new file that wasn't the date...")

            # remove the temp file
            os.remove(tmp)

        print("ALL DONE")


if __name__ == "__main__":
    preamble = Preamble()
    preamble.main("/github/workspace")
