CPU_CORES=$(($(grep -c processor < /proc/cpuinfo)*2))

build:
	mkdir -p qemu-build
	cd qemu-build ; ../qemu/configure --target-list=aarch64-softmmu,arm-softmmu,loongarch64-softmmu,x86_64-softmmu --enable-kvm --enable-slirp
	cd qemu-build ; make -j$(CPU_CORES)

clean:
	rm -rf qemu-build

install:
	mkdir qemu-install -p
	cd qemu-build ; make install DESTDIR=../qemu-install/opt/apps/deepin-wine-runner/VM/qemu-extra  -j$(CPU_CORES)
	rm -rf qemu-install/usr
	cp qemu-install/* $(DESTDIR) -r