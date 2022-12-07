build:
	#cd VM-source && qmake
	#cd VM-source && make
	#cd wine && make
	cp -rv helperset deb/opt/apps/deepin-wine-runner/
	cp -rv VM-source/VirtualMachine               VM
	cp -rv VM-source/deepin-wine-runner.svg       VM
	cp -rv VM-source/api                          VM
	cp -rv VM-source/Windows7X64Auto.iso          VM
	cp -rv VM-source/Windows7X86Auto.iso          VM
	cp -rv VM-source/run.py                       VM
	cp -rv wine/                       deb/opt/apps/deepin-wine-runner/
	cp -rv Test/                       deb/opt/apps/deepin-wine-runner/
	zip -v -q -r package-script.zip package-script
	cp -rv VM                                     deb/opt/apps/deepin-wine-runner
	cp -rv Download.py                    deb/opt/apps/deepin-wine-runner/
	cp -rv AllInstall.py                          deb/opt/apps/deepin-wine-runner
	cp -rv ShellList deb/opt/apps/deepin-wine-runner
	cp -rv QemuDownload.py deb/opt/apps/deepin-wine-runner
	cp -rv QemuRun.py deb/opt/apps/deepin-wine-runner
	cp -rv kill.sh                          deb/opt/apps/deepin-wine-runner
	cp -rv InstallWineOnDeepin23Alpha.py          deb/opt/apps/deepin-wine-runner
	cp -rv wrestool          deb/opt/apps/deepin-wine-runner
	cp -rv Mount.sh          deb/opt/apps/deepin-wine-runner
	cp -rv UnMount.sh          deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-easy-packager.py     deb/opt/apps/deepin-wine-runner
	cp -rv IconList.json     deb/opt/apps/deepin-wine-runner
	cp -rv GetEXEVersion.exe deb/opt/apps/deepin-wine-runner
	echo "[]" > deb/opt/apps/deepin-wine-runner/wine/winelist.json
	rm -rfv deb/opt/apps/deepin-wine-runner/wine/winelist.json
	cp -rv req                          deb/opt/apps/deepin-wine-runner
	cp -rv BuildDesktop.py              deb/opt/apps/deepin-wine-runner
	cp -rv ChangePassword.sh              deb/opt/apps/deepin-wine-runner
	cp -rv trans                        deb/opt/apps/deepin-wine-runner
	cp -rv RegShot                          deb/opt/apps/deepin-wine-runner
	cp -rv BeCyIconGrabber.exe                    deb/opt/apps/deepin-wine-runner
	cp -rv AutoShell                              deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager-with-script.py    deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-packager.py                deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner-update-bug          deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-runner.svg                 deb/opt/apps/deepin-wine-runner
	cp -rv deepin-wine-venturi-setter.py          deb/opt/apps/deepin-wine-runner
	cp -rv InstallVisualBasicRuntime.py           deb/opt/apps/deepin-wine-runner
	cp -rv DisabledOpengl.reg                     deb/opt/apps/deepin-wine-runner
	cp -rv EnabledOpengl.reg                      deb/opt/apps/deepin-wine-runner
	cp -rv geek.exe                               deb/opt/apps/deepin-wine-runner
	cp -rv ProgramFen.py                          deb/opt/apps/deepin-wine-runner
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
	cp -rv UpdateGeek.sh                             deb/opt/apps/deepin-wine-runner
	cp -rv AppStore.py                               deb/opt/apps/deepin-wine-runner
	cp -rv InstallWineOnDeepin23.py                  deb/opt/apps/deepin-wine-runner
	cp -rv dxvk.7z                                   deb/opt/apps/deepin-wine-runner
	cp -rv InstallFont.py                            deb/opt/apps/deepin-wine-runner
	cp -rv CheckDLL                                  deb/opt/apps/deepin-wine-runner
	#cp -rv exagear.7z                               deb/opt/apps/deepin-wine-runner
	cp -rv dlls-arm.7z                               deb/opt/apps/deepin-wine-runner
	cp -rv deepin.list                               deb/opt/apps/deepin-wine-runner
	cp -rv sparkstore.list                           deb/opt/apps/deepin-wine-runner
	cp -rv arm-package.7z                         deb/opt/apps/deepin-wine-runner
	#cp -rv exa.7z                         deb/opt/apps/deepin-wine-runner
	cp -rv clean-unuse-program.py                    deb/opt/apps/deepin-wine-runner
	cp -rv InstallNewWineHQ.sh                       deb/opt/apps/deepin-wine-runner
	cp -rv cleanbottle.sh                            deb/opt/apps/deepin-wine-runner
	cp -rv StartVM.sh                                deb/opt/apps/deepin-wine-runner
	#cp -rv deepin-wine-runner-create-botton.py       deb/opt/apps/deepin-wine-runner
	cp -rv Icon                                      deb/opt/apps/deepin-wine-runner
	cp -rv ConfigLanguareRunner-help.json            deb/opt/apps/deepin-wine-runner
	cp -rv gtkGetFileNameDlg                         deb/opt/apps/deepin-wine-runner
	cp -rv LANG/*.qm                                      deb/opt/apps/deepin-wine-runner/LANG
	cp -rv InstallDll.py                                      deb/opt/apps/deepin-wine-runner/LANG
	cp -rv ConfigLanguareRunner.py                      deb/opt/apps/deepin-wine-runner
	cp -rv AutoConfig.py                      deb/opt/apps/deepin-wine-runner
	cp -rv UI                    deb/opt/apps/deepin-wine-runner/
	cp -rv InstallDll.py              deb/opt/apps/deepin-wine-runner
	cp -rv Model              deb/opt/apps/deepin-wine-runner
	cp -rv API                deb/opt/apps/deepin-wine-runner
	cp -rv key                deb/opt/apps/deepin-wine-runner
	dpkg -b deb spark-deepin-wine-runner.deb
	

install:
	make build
	sudo apt update
	#sudo dpkg -i spark-deepin-wine-runner.deb
	sudo apt reinstall ./spark-deepin-wine-runner.deb -y --allow-downgrades 

remove:
	sudo apt purge spark-deepin-wine-runner 

run:
	python3 mainwindow.py
