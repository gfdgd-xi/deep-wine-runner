build:
	make package -j$(nproc)

clean:
	python3 RemovePycacheFile.py
	rm *.deb -fv
	cd VM-source ; make clean
	rm VM-source/VirtualMachine -rfv
	rm -rfv VM-source/.qmake.stash

package:
	#cd VM-source && qmake
	#cd VM-source && make
	#cd wine && make
	make clean -j$(nproc)
	mkdir deb/opt/apps/deepin-wine-runner/LANG -pv
	cp -rv helperset deb/opt/apps/deepin-wine-runner/
	#cp -rv VM-source/VirtualMachine VM
	
	cp -rv VM-source/deepin-wine-runner.svg VM
	cp -rv VM-source/Windows7X64Auto.iso VM
	cp -rv VM-source/Windows7X86Auto.iso VM
	cp -rv VM-source/test.qcow2 VM
	cp -rv VM-source/*.fd VM
	cp -rv wine/ deb/opt/apps/deepin-wine-runner/
	cp -rv Test/ deb/opt/apps/deepin-wine-runner/
	cp -rv information.json package-script
	zip -v -q -r package-script.zip package-script
	cp -rv InstallBox86-cn.sh deb/opt/apps/deepin-wine-runner/
	cp -rv VM deb/opt/apps/deepin-wine-runner
	cp -rv 2048 deb/opt/apps/deepin-wine-runner/
	cp -rv Download.py deb/opt/apps/deepin-wine-runner/
	cp -rv AllInstall.py deb/opt/apps/deepin-wine-runner
	cp -rv ShellList deb/opt/apps/deepin-wine-runner
	cp -rv QemuDownload.py deb/opt/apps/deepin-wine-runner
	cp -rv DefaultSetting.py deb/opt/apps/deepin-wine-runner
	cp -rv QemuRun.py deb/opt/apps/deepin-wine-runner
	cp -rv kill.sh deb/opt/apps/deepin-wine-runner
	cp -rv updatekiller.py deb/opt/apps/deepin-wine-runner
	cp -rv AddWineDebMirrorForDeepin20.sh deb/opt/apps/deepin-wine-runner
	cp -rv InstallNewWineHQOrg.sh deb/opt/apps/deepin-wine-runner
	cp -rv InstallWineOnDeepin23Alpha.py deb/opt/apps/deepin-wine-runner
	cp -rv wrestool deb/opt/apps/deepin-wine-runner
	cp -rv Mount.sh deb/opt/apps/deepin-wine-runner
	cp -rv UnMount.sh deb/opt/apps/deepin-wine-runner
	cp -rv vkd3d-proton.7z deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-easy-packager.py deb/opt/apps/deepin-wine-runner
	cp -rv IconList.json deb/opt/apps/deepin-wine-runner
	cp -rv GetEXEVersion.exe deb/opt/apps/deepin-wine-runner
	cp -rv MountWithoutHome.sh deb/opt/apps/deepin-wine-runner
	cp -rv RunCommandWithTerminal.py deb/opt/apps/deepin-wine-runner
	cp -rv QemuSystemInstall.sh deb/opt/apps/deepin-wine-runner
	echo "[]" > deb/opt/apps/deepin-wine-runner/wine/winelist.json
	rm -rfv deb/opt/apps/deepin-wine-runner/wine/winelist.json
	cp -rv req deb/opt/apps/deepin-wine-runner
	cp -rv pardus-chroot deb/opt/apps/deepin-wine-runner
	cp -rv winetricks deb/opt/apps/deepin-wine-runner
	cp -rv WineLib deb/opt/apps/deepin-wine-runner
	cp -rv InstallFoxpro.py deb/opt/apps/deepin-wine-runner
	cp -rv BuildDesktop.py deb/opt/apps/deepin-wine-runner
	cp -rv ChangePassword.sh deb/opt/apps/deepin-wine-runner
	cp -rv trans deb/opt/apps/deepin-wine-runner
	cp -rv RegShot deb/opt/apps/deepin-wine-runner
	cp -rv BeCyIconGrabber.exe deb/opt/apps/deepin-wine-runner
	cp -rv AutoShell deb/opt/apps/deepin-wine-runner
	cp -rv Resources deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager-with-script.py deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager.py deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner-update-bug deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner.svg deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-venturi-setter.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallVisualBasicRuntime.py deb/opt/apps/deepin-wine-runner
	cp -rv DisabledOpengl.reg deb/opt/apps/deepin-wine-runner
	cp -rv EnabledOpengl.reg deb/opt/apps/deepin-wine-runner
	cp -rv geek.exe deb/opt/apps/deepin-wine-runner
	#cp -rv uengineapi deb/opt/apps/deepin-wine-runner
	cp -rv getxmlimg.py deb/opt/apps/deepin-wine-runner
	cp -rv ProgramFen.py deb/opt/apps/deepin-wine-runner
	cp -rv information.json deb/opt/apps/deepin-wine-runner
	cp -rv InstallMono.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallMsxml.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallNetFramework.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallOther.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallVisualCPlusPlus.py deb/opt/apps/deepin-wine-runner
	cp -rv launch.sh deb/opt/apps/deepin-wine-runner
	cp -rv LICENSE deb/opt/apps/deepin-wine-runner
	cp -rv mainwindow.py deb/opt/apps/deepin-wine-runner/deepin-wine-runner
	cp -rv package-script.zip deb/opt/apps/deepin-wine-runner
	cp -rv Run.bat deb/opt/apps/deepin-wine-runner
	cp -rv RunVM.sh deb/opt/apps/deepin-wine-runner
	cp -rv "wine install" deb/opt/apps/deepin-wine-runner
	cp -rv 窗体透明度设置工具.exe deb/opt/apps/deepin-wine-runner
	cp -rv UpdateGeek.sh deb/opt/apps/deepin-wine-runner
	cp -rv AppStore.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallWineOnDeepin23.py deb/opt/apps/deepin-wine-runner
	cp -rv dxvk.7z deb/opt/apps/deepin-wine-runner
	cp -rv InstallFont.py deb/opt/apps/deepin-wine-runner
	cp -rv CheckDLL deb/opt/apps/deepin-wine-runner
	#cp -rv exagear.7z deb/opt/apps/deepin-wine-runner
	cp -rv dlls-arm.7z deb/opt/apps/deepin-wine-runner
	cp -rv deepin.list deb/opt/apps/deepin-wine-runner
	cp -rv sparkstore.list deb/opt/apps/deepin-wine-runner
	cp -rv arm-package.7z deb/opt/apps/deepin-wine-runner
	#cp -rv exa.7z deb/opt/apps/deepin-wine-runner
	cp -rv clean-unuse-program.py deb/opt/apps/deepin-wine-runner
	cp -rv InstallNewWineHQ.sh deb/opt/apps/deepin-wine-runner
	cp -rv cleanbottle.sh deb/opt/apps/deepin-wine-runner
	cp -rv StartVM.sh deb/opt/apps/deepin-wine-runner
	#cp -rv deepin-wine-runner-create-botton.py deb/opt/apps/deepin-wine-runner
	cp -rv Icon deb/opt/apps/deepin-wine-runner
	cp -rv ConfigLanguareRunner-help.json deb/opt/apps/deepin-wine-runner
	cp -rv gtkGetFileNameDlg deb/opt/apps/deepin-wine-runner
	cp -rv LANG/*.qm deb/opt/apps/deepin-wine-runner/LANG
	cp -rv InstallDll.py deb/opt/apps/deepin-wine-runner/LANG
	cp -rv ConfigLanguareRunner.py deb/opt/apps/deepin-wine-runner
	cp -rv AutoConfig.py deb/opt/apps/deepin-wine-runner
	cp -rv UI deb/opt/apps/deepin-wine-runner/
	cp -rv InstallDll.py deb/opt/apps/deepin-wine-runner
	cp -rv Model deb/opt/apps/deepin-wine-runner
	cp -rv API deb/opt/apps/deepin-wine-runner
	cp -rv key deb/opt/apps/deepin-wine-runner
	cp -rv InstallQemuUser.sh deb/opt/apps/deepin-wine-runner
	cp -rv RemoveQemuUser.sh deb/opt/apps/deepin-wine-runner
	cp -rv InstallBox86.sh  deb/opt/apps/deepin-wine-runner
	cp -rv InstallRuntime   deb/opt/apps/deepin-wine-runner
	mkdir -pv deb/opt/apps/deepin-wine-runner/entries/
	cp -rv deb/usr/share/applications deb/opt/apps/deepin-wine-runner/entries/applications
	python3 UpdateTime.py
	python3 RemovePycacheFile.py
	sudo rm -rfv /tmp/spark-deepin-wine-runner-builder/
	cp -rv deb /tmp/spark-deepin-wine-runner-builder
	rm -rfv deb/opt/apps/deepin-wine-runner/*
	rm -rfv package-script.zip
	mkdir -pv /tmp/spark-deepin-wine-runner-builder/usr/bin
	ln -s /opt/apps/deepin-wine-runner/deepin-wine-packager.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-package-builder 
	ln -s /opt/apps/deepin-wine-runner/deepin-wine-easy-packager.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-packager-easy-builder
	ln -s /opt/apps/deepin-wine-runner/deepin-wine-packager-with-script.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-packager-with-script
	ln -s /opt/apps/deepin-wine-runner/deepin-wine-runner /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner
	ln -s /opt/apps/deepin-wine-runner/AppStore.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-appstore
	ln -s /opt/apps/deepin-wine-runner/AutoShell/main.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-auto-install-bash
	ln -s /opt/apps/deepin-wine-runner/ConfigLanguareRunner.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-auto-install-config-old
	ln -s /opt/apps/deepin-wine-runner/AutoConfig.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-auto-install-gui
	ln -s /opt/apps/deepin-wine-runner/launch.sh /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-dtk-launch
	ln -s /opt/apps/deepin-wine-runner/deepin-wine-runner-update-bug /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-update-bug
	ln -s /opt/apps/deepin-wine-runner/InstallFont.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-font-installer
	ln -s /opt/apps/deepin-wine-runner/InstallNewWineHQ.sh /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-winehq-install
	ln -s '/opt/apps/deepin-wine-runner/wine install' /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-install
	ln -s '/opt/apps/deepin-wine-runner/wine install' /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-installer
	ln -s /opt/apps/deepin-wine-runner/InstallWineOnDeepin23.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-install-deepin23
	ln -s /opt/apps/deepin-wine-runner/InstallMono.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-monogecko-installer
	ln -s /opt/apps/deepin-wine-runner/InstallNetFramework.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-netframework-installer
	ln -s /opt/apps/deepin-wine-runner/InstallVisualCPlusPlus.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-runner-wine-vscppruntime-installer
	ln -s /opt/apps/deepin-wine-runner/deepin-wine-venturi-setter.py /tmp/spark-deepin-wine-runner-builder/usr/bin/deepin-wine-venturi-setter
	bash builddeb/ChangeDebVersion.sh
	sudo chown -R root:root /tmp/spark-deepin-wine-runner-builder
	
	dpkg-deb -Z xz -z 9 -b /tmp/spark-deepin-wine-runner-builder spark-deepin-wine-runner.deb
	sudo rm -rfv /tmp/spark-deepin-wine-runner-builder
	# 构建 ace 包
	cp -rv deb-ace /tmp/spark-deepin-wine-runner-builder
	cp -rv spark-deepin-wine-runner.deb /tmp/spark-deepin-wine-runner-builder/opt/apps/spark-deepin-wine-runner-ace
	bash builddeb/ChangeDebVersion.sh
	sudo chown -R root:root /tmp/spark-deepin-wine-runner-builder
	dpkg-deb -Z xz -z 9 -b /tmp/spark-deepin-wine-runner-builder spark-deepin-wine-runner-ace.deb
	sudo rm -rfv /tmp/spark-deepin-wine-runner-builder
	
install:
	make build -j$(nproc)
	sudo apt update ; true
	#sudo dpkg -i spark-deepin-wine-runner.deb
	sudo apt reinstall ./spark-deepin-wine-runner.deb -y --allow-downgrades 
	rm spark-deepin-wine-runner.deb -vf

remove:
	sudo apt purge spark-deepin-wine-runner  -y

run:
	python3 mainwindow.py
