#!/usr/bin/env python

from subprocess import Popen

class Git:

    def clone(repo_url, folder_path):
        from subprocess import Popen
        process = Popen(["git", "clone", repo_url, str(folder_path)])
        process.wait()
