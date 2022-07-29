build:
	cd VM-source && qmake
	cd VM-source && make
	cp -rv VM-source/VirtualMachine               VM
	cp -rv VM-source/deepin-wine-runner.svg       VM
	cp -rv VM-source/api                          VM
	cp -rv VM-source/Windows7X64Auto.iso          VM
	cp -rv VM-source/Windows7X86Auto.iso          VM
	cp -rv VM-source/run.py                       VM
	zip -v -q -r package-script.zip package-script
	cp -rv VM                                     deb/opt/apps/deepin-wine-runner
	cp -rv AllInstall.py                          deb/opt/apps/deepin-wine-runner
	cp -rv BeCyIconGrabber.exe                    deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager-with-script.py    deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager.py                deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner-update-bug          deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner.svg                 deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-venturi-setter.py          deb/opt/apps/deepin-wine-runner
	cp -rv DisabledOpengl.reg                     deb/opt/apps/deepin-wine-runner
	cp -rv EnabledOpengl.reg                      deb/opt/apps/deepin-wine-runner
	cp -rv geek.exe                               deb/opt/apps/deepin-wine-runner
	cp -rv information.json                       deb/opt/apps/deepin-wine-runner
	cp -rv InstallMono.py                         deb/opt/apps/deepin-wine-runner
	cp -rv InstallMsxml.py                        deb/opt/apps/deepin-wine-runner
	cp -rv InstallNetFramework.py                 deb/opt/apps/deepin-wine-runner
	cp -rv InstallOther.py                        deb/opt/apps/deepin-wine-runner
	cp -rv InstallVisualCPlusPlus.py              deb/opt/apps/deepin-wine-runner
	cp -rv launch.sh                              deb/opt/apps/deepin-wine-runner
	cp -rv LICENSE                                deb/opt/apps/deepin-wine-runner
	cp -rv mainwindow.py                          deb/opt/apps/deepin-wine-runner/deepin-wine-runner
	cp -rv package-script.zip                     deb/opt/apps/deepin-wine-runner
	cp -rv Run.bat                                deb/opt/apps/deepin-wine-runner
	cp -rv RunVM.sh                               deb/opt/apps/deepin-wine-runner
	cp -rv "wine install"                         deb/opt/apps/deepin-wine-runner
	cp -rv 窗体透明度设置工具.exe                    deb/opt/apps/deepin-wine-runner
	cp -rv dlls                                   deb/opt/apps/deepin-wine-runner
	cp -rv UpdateGeek.sh                          deb/opt/apps/deepin-wine-runner
	dpkg -b deb spark-deepin-wine-runner.deb

install:
	make build
	sudo apt update
	sudo dpkg -i spark-deepin-wine-runner.deb
	sudo apt install -f 

remove:
	sudo apt purge spark-deepin-wine-runner 

depend:
	sudo apt update
	sudo apt install python3 python3-pil python3-pil.imagetk\
	 python3-pyquery deepin-terminal aria2 curl unrar unzip\
	  python3-requests fakeroot bash python3-pyqt5

run:
	python3 mainwindow.py