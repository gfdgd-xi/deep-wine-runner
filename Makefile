CPU_CORES=$(($(grep -c processor < /proc/cpuinfo)*2))
virtioISOUrl=https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/archive-virtio/virtio-win-0.1.248-1/virtio-win.iso
loongEFI=https://mirrors.wsyu.edu.cn/loongarch/archlinux/images/QEMU_EFI_8.2.fd

build:
	mkdir -p qemu-build
	if [ -f python3-exec/usr/local/bin/python3 ]; then cd qemu-build ; ../qemu/configure --target-list=x86_64-linux-user,aarch64-linux-user,loongarch64-linux-user,i386-linux-user,arm-linux-user,aarch64-softmmu,arm-softmmu,loongarch64-softmmu,x86_64-softmmu --enable-kvm --enable-slirp --enable-system --enable-tools --enable-vhost-user --enable-slirp --enable-kvm --python=../python3-exec/usr/local/bin/python3; fi
	if [ ! -f python3-exec/usr/local/bin/python3 ]; then cd qemu-build ; ../qemu/configure --target-list=x86_64-linux-user,aarch64-linux-user,loongarch64-linux-user,i386-linux-user,arm-linux-user,aarch64-softmmu,arm-softmmu,loongarch64-softmmu,x86_64-softmmu --enable-kvm --enable-slirp --enable-system --enable-tools --enable-vhost-user --enable-slirp --enable-kvm ; fi
	cd qemu-build ; make -j$(CPU_CORES)

build-python:
	mkdir -p python3-build
	cd python3-build ; ../python3/configure 
	cd python3-build ; make -j$(CPU_CORES)

install-to-qemu-python:
	mkdir -p python3-exec
	cd python3-build ; make install -j$(CPU_CORES) DESTDIR=../python3-exec

build-ed2k:
	git clone https://github.com/tianocore/edk2.git
	cd edk2 ; git submodule update --init

clean:
	rm -rf qemu-build

install:
	cd qemu-build ; make install DESTDIR=$(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/  -j$(CPU_CORES)
	if [ -d $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/lib ]; then mkdir $(DESTDIR)/usr/lib -p ; fi
	if [ -d $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/lib ]; then cp $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/lib/* $(DESTDIR)/usr/lib -r ; fi
	mkdir $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/applications -p
	mkdir $(DESTDIR)/usr/share/applications -p
	mkdir $(DESTDIR)/usr/share/icons/apps -p
	mkdir $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/icons/apps -p

	cp deepin-wine-runner-qemu-system-extra.svg $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/icons/apps -r
	cp deepin-wine-runner-qemu-system-extra.svg $(DESTDIR)/usr/share/icons/apps -r
	cp deepin-wine-runner-qemu-system-extra.desktop $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/applications -r
	cp deepin-wine-runner-qemu-system-extra.desktop $(DESTDIR)/usr/share/applications -r
	cp run.sh $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/ -r
	cp qemu-commands-list.sh $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/bin/qemu-commands-list -r
	chmod +x $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/usr/local/bin/qemu-commands-list
	chmod +x $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh

	# 拷贝资源文件
	mkdir $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/resources -p
	if [ -f virtio-win.iso ]; then cp virtio-win.iso $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/resources -rv -p ; fi
	if [ -f loong64-efi-ed2k.fd ]; then cp loong64-efi-ed2k.fd $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/resources -rv -p ; fi
	
download-loong64-ed2k:
	aria2c -x 16 -s 16 $(loongEFI) -c -o loong64-efi-ed2k.fd

download-virtio-iso:
	aria2c -x 16 -s 16 $(virtioISOUrl) -c -o virtio-win.iso