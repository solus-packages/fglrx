#!/usr/bin/python

from pisi.actionsapi import get, autotools, pisitools, shelltools
import os

# Because fuck it why not, multiple versions
AmdVersion = "15.30.1025"

WDir = os.path.join(get.workDIR(), "fglrx-%s" % AmdVersion, "WorkDir")
AuxDir = os.path.join(WDir, "arch/x86_64/lib/modules/fglrx/build_mod")

# Update for the current kernel branch
kversion = "4.1.13"

def setup():
    if not os.path.exists(WDir):
        shelltools.system("./amd-driver-installer-%s-x86.x86_64.run --extract WorkDir" % AmdVersion)

def build_kernel_module():
    ''' Compile the kernel module '''
    shelltools.cd("%s/common/lib/modules/fglrx/build_mod/2.6.x" % WDir)
    FLAGS = "-DCOMPAT_ALLOC_USER_SPACE=arch_compat_alloc_user_space -DMODULE -DATI -DFGL -DPAGE_ATTR_FIX=1"
    shelltools.export("CFLAGS", "%s %s" % (get.CFLAGS(), FLAGS))
    pisitools.dosed("../kcl_ioctl.c", "COMPAT_ALLOC_USER_SPACE", "arch_compat_alloc_user_space")
    shelltools.system("make LIBIP_PREFIX=%s KVER=%s MODFLAGS=\"%s\" CFLAGS=\"%s\"" % (AuxDir, kversion, FLAGS,FLAGS))

def install_kernel_module():
    ''' Install kernel module '''
    shelltools.cd("%s/common/lib/modules/fglrx/build_mod/2.6.x" % WDir)
    kdir = "/lib64/modules/%s/kernel/drivers/video" % kversion
    pisitools.dolib_a("fglrx.ko", kdir)

def build():
    build_kernel_module()


def install():
    install_kernel_module()

    # install xorg driver
    shelltools.cd(os.path.join(WDir, "xpic_64a/usr/X11R6/lib64/modules"))
    pisitools.insinto("/usr/lib64/xorg/modules", "drivers/fglrx_drv.so")
    pisitools.insinto("/usr/lib64/xorg/modules/linux", "linux/*.so")
    pisitools.insinto("/usr/lib64/xorg/modules/extensions/fglrx", "extensions/fglrx/*.so")
    # TODO: Also push this into the glx symlinks ^
    
