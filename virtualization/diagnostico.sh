#!/usr/bin/env bash
set -euo pipefail
virsh list --all
virsh dominfo agro-cp
virsh vcpupin agro-cp --config
virsh dumpxml agro-cp
qemu-img info /var/lib/libvirt/images/agro-cp.qcow2
du -h /var/lib/libvirt/images/agro-cp.qcow2
# EPT check is meaningful only on a KVM host with kvm_intel loaded.
if [[ -r /sys/module/kvm_intel/parameters/ept ]]; then cat /sys/module/kvm_intel/parameters/ept; else echo 'KVM Intel/EPT unavailable on this host'; fi
