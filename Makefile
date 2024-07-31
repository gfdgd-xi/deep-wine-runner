build:
	make package-deb -j$(nproc)

replace:
	rm Icon/Program/*
	rm Icon/*.svg
	rm Icon/doge.png
	echo "[[], []]" > IconList.json

clean:
	python3 RemovePycacheFile.py
	rm *.deb -fv
	rm *.pkg.tar* -fv

#package-rpm:

package-rpm:
	sudo rm -rf /root/rpmbuild/
	sudo rm -rf /tmp/deep-wine-runner-builder-source
	mkdir /tmp/deep-wine-runner-builder-source -pv
	cp * /tmp/deep-wine-runner-builder-source -rv
	cp rpm/spark-deepin-wine-runner.spec /tmp/spark-deepin-wine-runner.spec
	bash builddeb/ChangeDebVersion.sh
	sudo rpmbuild -bb /tmp/spark-deepin-wine-runner.spec --target noarch
	sudo bash -c 'cp /root/rpmbuild/RPMS/noarch/spark-deepin-wine-runner-*.rpm .'
	sudo rm -rf /root/rpmbuild/
	sudo rm -rf /tmp/deep-wine-runner-builder-source

package-pkg:
	#sudo debtap -u
	sudo debtap -Q spark-deepin-wine-runner.deb
	sudo debtap -Q spark-deepin-wine-runner-ace.deb

copy-files:
	#cd wine && make
	make clean -j$(nproc)
	mkdir deb/opt/apps/deepin-wine-runner/LANG -pv
	cp -rv helperset deb/opt/apps/deepin-wine-runner/
	cp -rv wine/ deb/opt/apps/deepin-wine-runner/
	cp -rv Test/ deb/opt/apps/deepin-wine-runner/
	cp -rv dxvk/ deb/opt/apps/deepin-wine-runner
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
	cp -rv InstallFont.py deb/opt/apps/deepin-wine-runner
	cp -rv CheckDLL deb/opt/apps/deepin-wine-runner
	cp -rv InstallLat.sh deb/opt/apps/deepin-wine-runner
	#cp -rv exagear.7z deb/opt/apps/deepin-wine-runner
	cp -rv dlls-arm.7z deb/opt/apps/deepin-wine-runner
	cp -rv deepin.list deb/opt/apps/deepin-wine-runner
	cp -rv sparkstore.list deb/opt/apps/deepin-wine-runner
	cp -rv arm-package.7z deb/opt/apps/deepin-wine-runner
	#cp -rv exa.7z deb/opt/apps/deepin-wine-runner
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
	cp -rv globalenv.py   deb/opt/apps/deepin-wine-runner
	if [[ ! -d novnc/utils/websockify ]]; then git submodule update --init --recursive ; fi
	if [[ ! -d novnc/utils/websockify ]]; then cd novnc/utils; git clone https://github.com/novnc/websockify ; fi
	cp -rv novnc   deb/opt/apps/deepin-wine-runner
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
	chmod -Rv 777 /tmp/spark-deepin-wine-runner-builder/opt
	chmod -Rv 777 /tmp/spark-deepin-wine-runner-builder/usr

remove-copy-files:
	sudo rm -rfv /tmp/spark-deepin-wine-runner-builder

package-deb:
	make copy-files -j$(nproc)
	dpkg-deb -Z xz -z 9 -b /tmp/spark-deepin-wine-runner-builder spark-deepin-wine-runner.deb
	make remove-copy-files -j$(nproc)
	# 构建 ace 包
	cp -rv deb-ace /tmp/spark-deepin-wine-runner-builder
	cp -rv spark-deepin-wine-runner.deb /tmp/spark-deepin-wine-runner-builder/opt/apps/spark-deepin-wine-runner-ace
	bash builddeb/ChangeDebVersion.sh
	sudo chown -R root:root /tmp/spark-deepin-wine-runner-builder
	dpkg-deb -Z xz -z 0 -b /tmp/spark-deepin-wine-runner-builder spark-deepin-wine-runner-ace.deb
	make remove-copy-files -j$(nproc)

package-termux-deb:
	make copy-files -j$(nproc)
	# 替换 DEBIAN
	sudo rm -rf /tmp/spark-deepin-wine-runner-builder/DEBIAN
	sudo rm -rf /tmp/spark-deepin-wine-runner-builder/usr/bin/*
	sudo rm -rf /tmp/spark-deepin-wine-runner-builder/usr/share/applications/*
	sudo rm -rf /tmp/spark-deepin-wine-runner-builder/opt/apps/deepin-wine-runner/entries/applications/*
	sudo mkdir -pv /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/
	sudo mv /tmp/spark-deepin-wine-runner-builder/usr/ /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/ -v
	sudo mv /tmp/spark-deepin-wine-runner-builder/opt /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/opt -v
	sudo ln -s /data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/deepin-wine-runner /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/bin/deepin-wine-runner
	sudo ln -s /data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/deepin-wine-packager.py /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/bin/deepin-wine-package-builder 
	sudo ln -s /data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/deepin-wine-packager-with-script.py /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/bin/deepin-wine-packager-with-script
	sudo ln -s /data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/deepin-wine-easy-packager.py /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/bin/deepin-wine-packager-easy-builder
	sudo cp deb-termux/DEBIAN /tmp/spark-deepin-wine-runner-builder/DEBIAN -rv
	sudo cp -rv deb-termux/usr/share/applications /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/entries/applications
	sudo cp -rv deb-termux/usr/share/applications /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/share/applications
	# 加入 termux loader
	sudo cp -rv mainwindow-termux-loader.sh /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/deepin-wine-runner
	sudo cp -rv mainwindow.py /tmp/spark-deepin-wine-runner-builder/data/data/com.termux/files/usr/opt/apps/deepin-wine-runner/mainwindow.py
	sudo bash builddeb/ChangeDebVersion.sh
	dpkg-deb -Z xz -z 9 -b /tmp/spark-deepin-wine-runner-builder spark-deepin-wine-runner-termux.deb
	make remove-copy-files -j$(nproc)
	
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
