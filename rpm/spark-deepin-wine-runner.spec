Summary: text package.
Name: spark-deepin-wine-runner
Version: 3.6.1
Release: 200
License: GPLv3+
AutoReqProv: no

Requires: python3

%define __os_install_post %{nil}
%description
wine runner

%prep
%build
git clone https://gitlink.org.cn/gfdgd_xi/deep-wine-runner --depth=1 | true
cd deep-wine-runner
git pull
make package-deb -j4
%install
cd deep-wine-runner
sudo dpkg -x spark-deepin-wine-runner.deb ~/rpmbuild/BUILDROOT/*
sudo chmod 777 -Rv ~/rpmbuild/BUILDROOT/*/opt
sudo chmod 755 -Rv ~/rpmbuild/BUILDROOT/*/usr

#%dir %attr(0755, root, root) "/usr"

%files
/usr/
/opt/

