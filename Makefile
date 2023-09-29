clean:
	python3 RemovePycacheFile.py
	cd VM-source ; make clean
	rm VM-source/VirtualMachine -rfv
	rm -rfv VM-source/.qmake.stash

install:
	#cd VM-source && qmake
	#cd VM-source && make
	#cd wine && make
	make clean -j$(nproc)
	python3 RemovePycacheFile.py
	mkdir $(DESTDIR)/opt/apps/deepin-wine-runner/LANG -pv
	mkdir -pv $(DESTDIR)/usr/bin
	mkdir -pv $(DESTDIR)/usr/share/applications 
	mkdir -pv $(DESTDIR)/opt/apps/deepin-wine-runner/entries/
	cp -rv helperset $(DESTDIR)/opt/apps/deepin-wine-runner/
	#cp -rv VM-source/VirtualMachine VM
	cp -rv VM-source/deepin-wine-runner.svg VM
	cp -rv VM-source/Windows7X64Auto.iso VM
	cp -rv VM-source/Windows7X86Auto.iso VM
	cp -rv wine/ $(DESTDIR)/opt/apps/deepin-wine-runner/
	cp -rv Test/ $(DESTDIR)/opt/apps/deepin-wine-runner/
	cp -rv information.json package-script
	zip -v -q -r package-script.zip package-script
	cp -rv InstallBox86-cn.sh $(DESTDIR)/opt/apps/deepin-wine-runner/
	cp -rv VM $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv 2048 $(DESTDIR)/opt/apps/deepin-wine-runner/
	cp -rv Download.py $(DESTDIR)/opt/apps/deepin-wine-runner/
	cp -rv AllInstall.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv ShellList $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv QemuDownload.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv DefaultSetting.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv QemuRun.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv kill.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv updatekiller.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv AddWineDebMirrorForDeepin20.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallNewWineHQOrg.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallWineOnDeepin23Alpha.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv wrestool $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv Mount.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv UnMount.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv vkd3d-proton.7z $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-easy-packager.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv IconList.json $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv GetEXEVersion.exe $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv MountWithoutHome.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv RunCommandWithTerminal.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv QemuSystemInstall.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	echo "[]" > $(DESTDIR)/opt/apps/deepin-wine-runner/wine/winelist.json
	rm -rfv $(DESTDIR)/opt/apps/deepin-wine-runner/wine/winelist.json
	cp -rv req $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv pardus-chroot $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv winetricks $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv WineLib $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallFoxpro.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv BuildDesktop.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv ChangePassword.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv trans $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv RegShot $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv BeCyIconGrabber.exe $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv AutoShell $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager-with-script.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner-update-bug $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner.svg $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-venturi-setter.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallVisualBasicRuntime.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv DisabledOpengl.reg $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv EnabledOpengl.reg $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv geek.exe $(DESTDIR)/opt/apps/deepin-wine-runner
	#cp -rv uengineapi $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv getxmlimg.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv ProgramFen.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv information.json $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallMono.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallMsxml.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallNetFramework.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallOther.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallVisualCPlusPlus.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv launch.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv LICENSE $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv mainwindow.py $(DESTDIR)/opt/apps/deepin-wine-runner/deepin-wine-runner
	cp -rv package-script.zip $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv Run.bat $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv RunVM.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv "wine install" $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv 窗体透明度设置工具.exe $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv UpdateGeek.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv AppStore.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallWineOnDeepin23.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv dxvk.7z $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallFont.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv CheckDLL $(DESTDIR)/opt/apps/deepin-wine-runner
	#cp -rv exagear.7z $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv dlls-arm.7z $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv deepin.list $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv sparkstore.list $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv arm-package.7z $(DESTDIR)/opt/apps/deepin-wine-runner
	#cp -rv exa.7z $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv clean-unuse-program.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallNewWineHQ.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv cleanbottle.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv StartVM.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	#cp -rv deepin-wine-runner-create-botton.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv Icon $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv ConfigLanguareRunner-help.json $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv gtkGetFileNameDlg $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv LANG/*.qm $(DESTDIR)/opt/apps/deepin-wine-runner/LANG
	cp -rv InstallDll.py $(DESTDIR)/opt/apps/deepin-wine-runner/LANG
	cp -rv ConfigLanguareRunner.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv AutoConfig.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv UI $(DESTDIR)/opt/apps/deepin-wine-runner/
	cp -rv InstallDll.py $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv Model $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv API $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv key $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallQemuUser.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv RemoveQemuUser.sh $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallBox86.sh  $(DESTDIR)/opt/apps/deepin-wine-runner
	cp -rv InstallRuntime   $(DESTDIR)/opt/apps/deepin-wine-runner
	
	cp -rv $(DESTDIR)/opt/apps/deepin-wine-runner/entries/applications $(DESTDIR)/usr/share/applications 
	#cp -rv deb $(DESTDIR)
	python3 UpdateTime.py $(DESTDIR)/opt/apps/deepin-wine-runner/information.json
	#sudo rm -rfv $(DESTDIR)/
	#cp -rv deb /tmp/spark-deepin-wine-runner-builder
	rm -rfv package-script.zip
	
	ln -fs /opt/apps/deepin-wine-runner/deepin-wine-packager.py $(DESTDIR)/usr/bin/deepin-wine-package-builder 
	ln -fs /opt/apps/deepin-wine-runner/deepin-wine-easy-packager.py $(DESTDIR)/usr/bin/deepin-wine-packager-easy-builder
	ln -fs /opt/apps/deepin-wine-runner/deepin-wine-packager-with-script.py $(DESTDIR)/usr/bin/deepin-wine-packager-with-script
	ln -fs /opt/apps/deepin-wine-runner/deepin-wine-runner $(DESTDIR)/usr/bin/deepin-wine-runner
	ln -fs /opt/apps/deepin-wine-runner/AppStore.py $(DESTDIR)/usr/bin/deepin-wine-runner-appstore
	ln -fs /opt/apps/deepin-wine-runner/AutoShell/main.py $(DESTDIR)/usr/bin/deepin-wine-runner-auto-install-bash
	ln -fs /opt/apps/deepin-wine-runner/ConfigLanguareRunner.py $(DESTDIR)/usr/bin/deepin-wine-runner-auto-install-config-old
	ln -fs /opt/apps/deepin-wine-runner/AutoConfig.py $(DESTDIR)/usr/bin/deepin-wine-runner-auto-install-gui
	ln -fs /opt/apps/deepin-wine-runner/launch.sh $(DESTDIR)/usr/bin/deepin-wine-runner-dtk-launch
	ln -fs /opt/apps/deepin-wine-runner/deepin-wine-runner-update-bug $(DESTDIR)/usr/bin/deepin-wine-runner-update-bug
	ln -fs /opt/apps/deepin-wine-runner/InstallFont.py $(DESTDIR)/usr/bin/deepin-wine-runner-wine-font-installer
	ln -fs /opt/apps/deepin-wine-runner/InstallNewWineHQ.sh $(DESTDIR)/usr/bin/deepin-wine-runner-winehq-install
	ln -fs '/opt/apps/deepin-wine-runner/wine install' $(DESTDIR)/usr/bin/deepin-wine-runner-wine-install
	ln -fs '/opt/apps/deepin-wine-runner/wine install' $(DESTDIR)/usr/bin/deepin-wine-runner-wine-installer
	ln -fs /opt/apps/deepin-wine-runner/InstallWineOnDeepin23.py $(DESTDIR)/usr/bin/deepin-wine-runner-wine-install-deepin23
	ln -fs /opt/apps/deepin-wine-runner/InstallMono.py $(DESTDIR)/usr/bin/deepin-wine-runner-wine-monogecko-installer
	ln -fs /opt/apps/deepin-wine-runner/InstallNetFramework.py $(DESTDIR)/usr/bin/deepin-wine-runner-wine-netframework-installer
	ln -fs /opt/apps/deepin-wine-runner/InstallVisualCPlusPlus.py $(DESTDIR)/usr/bin/deepin-wine-runner-wine-vscppruntime-installer
	ln -fs /opt/apps/deepin-wine-runner/deepin-wine-venturi-setter.py $(DESTDIR)/usr/bin/deepin-wine-venturi-setter

build:
	echo Done!

run:
	python3 mainwindow.py
