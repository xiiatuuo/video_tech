#!python
import sys
import os
import hashlib

class CopyDetector(object):

    def get_file_md5(self, filename):
        if not os.path.isfile(filename):
            return False
        myhash = hashlib.md5()
        f = file(filename,'rb')
        while True:
            b = f.read(8096)
            if not b :
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

    def md5_check(self, video_path_a, video_path_b):
        indentity_a = self.get_file_md5(video_path_a)
        indentity_b = self.get_file_md5(video_path_b)
        if indentity_a == indentity_b:
            return True
        else:
            return False


if __name__ == "__main__":
    cd = CopyDetector()
    print cd.md5_check(sys.argv[1], sys.argv[2])
