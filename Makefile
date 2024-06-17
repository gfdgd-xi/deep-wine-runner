CPU_CORES=$(($(grep -c processor < /proc/cpuinfo)*2))

build:
	mkdir -p qemu-build
	ifeq ($(wildcard python3-exec/usr/local/bin/python3),)
		cd qemu-build ; ../qemu/configure --target-list=x86_64-linux-user,aarch64-linux-user,loongarch64-linux-user,i386-linux-user,arm-linux-user,aarch64-softmmu,arm-softmmu,loongarch64-softmmu,x86_64-softmmu --enable-kvm --enable-slirp --enable-system --enable-tools --enable-vhost-user --enable-slirp --enable-kvm --python=python3-exec/usr/local/bin/python3
	else
		cd qemu-build ; ../qemu/configure --target-list=x86_64-linux-user,aarch64-linux-user,loongarch64-linux-user,i386-linux-user,arm-linux-user,aarch64-softmmu,arm-softmmu,loongarch64-softmmu,x86_64-softmmu --enable-kvm --enable-slirp --enable-system --enable-tools --enable-vhost-user --enable-slirp --enable-kvm 
	endif
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
	mkdir $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/applications -p
	mkdir $(DESTDIR)/usr/share/applications -p
	mkdir $(DESTDIR)/usr/share/icons/apps -p
	mkdir $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/icons/apps -p

	cp deepin-wine-runner-qemu-system-extra.svg $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/icons/apps -r
	cp deepin-wine-runner-qemu-system-extra.svg $(DESTDIR)/usr/share/icons/apps -r
	cp deepin-wine-runner-qemu-system-extra.desktop $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/entries/applications -r
	cp deepin-wine-runner-qemu-system-extra.desktop $(DESTDIR)/usr/share/applications -r
	cp run.sh $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/ -r
	chmod +x $(DESTDIR)/opt/apps/deepin-wine-runner-qemu-system-extra/files/run.sh
