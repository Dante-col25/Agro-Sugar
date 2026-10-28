#!/usr/bin/env bash
set -euo pipefail

container_name=${1:?Usage: check-container-namespaces.sh CONTAINER_NAME}
container_pid=$(docker inspect --format '{{.State.Pid}}' "$container_name")
if [[ -z "$container_pid" || "$container_pid" == 0 ]]; then
  echo "Container is not running: $container_name" >&2
  exit 1
fi

printf 'Container: %s (host PID %s)\n' "$container_name" "$container_pid"
for ns in pid net mnt; do
  host_ns=$(readlink "/proc/1/ns/$ns")
  container_ns=$(readlink "/proc/$container_pid/ns/$ns")
  if [[ "$host_ns" == "$container_ns" ]]; then
    state='SHARED'
  else
    state='ISOLATED'
  fi
  printf '%-4s host=%-24s container=%-24s %s\n' "$ns" "$host_ns" "$container_ns" "$state"
done

echo 'Container resource configuration:'
docker inspect --format 'NanoCpus={{.HostConfig.NanoCpus}} Memory={{.HostConfig.Memory}} PidsLimit={{.HostConfig.PidsLimit}}' "$container_name"
