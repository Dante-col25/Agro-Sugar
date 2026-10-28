#!/usr/bin/env bash
set -euo pipefail
vm_name=${1:-agro-cp}
disk_path=${2:-/var/lib/libvirt/images/${vm_name}.qcow2}

echo '=== Host ==='
uname -a
nproc
free -h
df -h /
lscpu
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
if command -v virt-host-validate >/dev/null 2>&1; then
  virt-host-validate qemu || true
else
  echo 'virt-host-validate is not installed'
fi

echo '=== Virtualization flags ==='
grep -m 1 -oE '\b(vmx|svm|ept)\b' /proc/cpuinfo | sort -u || true
if [[ -r /sys/module/kvm_intel/parameters/ept ]]; then
  printf 'Intel EPT enabled: '
  cat /sys/module/kvm_intel/parameters/ept
elif [[ -r /sys/module/kvm_amd/parameters/npt ]]; then
  printf 'AMD NPT enabled: '
  cat /sys/module/kvm_amd/parameters/npt
else
  echo 'KVM EPT/NPT module unavailable on this host'
fi

echo '=== libvirt ==='
virsh list --all
if virsh dominfo "$vm_name" >/dev/null 2>&1; then
  virsh dominfo "$vm_name"
  virsh vcpupin "$vm_name" --config || true
  virsh dumpxml "$vm_name"
else
  echo "VM not found in libvirt: $vm_name"
fi

echo '=== qcow2 ==='
if [[ -f "$disk_path" ]]; then
  qemu-img info "$disk_path"
  du -h "$disk_path"
else
  echo "Disk file not found: $disk_path"
fi
