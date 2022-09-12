import apt_pkg
import os
import apt_inst
import aptsources.distinfo
#print(apt_pkg.Cache.packages)
apt_pkg.init()
# 先更新
os.system("sudo apt ssupdate && sudo apt upgrade -y")
#apt_inst
version = apt_pkg.Cache()["winehq-staging"].current_ver.ver_str
#version = apt_pkg.Package()["live-filesystem"].current_ver.arch
try:
    new = version[: version.index("~")]
except:
    new = version
# 差异对比