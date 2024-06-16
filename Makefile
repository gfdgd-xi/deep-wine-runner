build:
	mkdir qemu-build
	cd qemu-build ; ../qemu/configure --target-list=aarch64-softmmu,arm-softmmu,loongarch64-softmmu,x86_64-softmmu --enable-kvm --enable-slirp
	cd qemu-build ; make build -j$(JOBS)

install:
	cd qemu-build ; make install DESTDIR=$(DESTDIR)