#!/usr/bin/env bash
set -euo pipefail

# Submits or removes the sample NDVI batch Job in a preconfigured cloud
# Kubernetes context. It does not provision cloud nodes or transfer imagery.
: "${CLOUD_CONTEXT:?Set CLOUD_CONTEXT to the preconfigured cloud Kubernetes context}"
: "${NDVI_WORKER_IMAGE:?Set NDVI_WORKER_IMAGE to an image available to the cloud cluster}"

CLOUD_NAMESPACE=${CLOUD_NAMESPACE:-agrosugar}
PENDING_NDVI_PODS=${PENDING_NDVI_PODS:-0}
PENDING_DURATION_MINUTES=${PENDING_DURATION_MINUTES:-0}
QUEUE_AGE_MINUTES=${QUEUE_AGE_MINUTES:-0}
QUEUE_EMPTY_MINUTES=${QUEUE_EMPTY_MINUTES:-0}
NDVI_VALUES_JSON=${NDVI_VALUES_JSON:-'[0.32, 0.48, 0.61]'}

if [[ ! "$NDVI_WORKER_IMAGE" =~ ^[A-Za-z0-9.-]+/[A-Za-z0-9._:/-]+$ ]]; then
  echo 'NDVI_WORKER_IMAGE must be a registry/image:tag reference.' >&2
  exit 2
fi
if [[ ! "$CLOUD_NAMESPACE" =~ ^[a-z0-9]([-a-z0-9]*[a-z0-9])?$ ]]; then
  echo 'CLOUD_NAMESPACE must be a lowercase Kubernetes namespace name.' >&2
  exit 2
fi
if ! python3 -c 'import json, math, sys; values=json.loads(sys.argv[1]); assert isinstance(values, list) and values and all(isinstance(v, (int, float)) and math.isfinite(v) and -1 <= v <= 1 for v in values)' "$NDVI_VALUES_JSON"; then
  echo 'NDVI_VALUES_JSON must be a non-empty JSON array of finite numbers from -1 to 1.' >&2
  exit 2
fi

for name in PENDING_NDVI_PODS PENDING_DURATION_MINUTES QUEUE_AGE_MINUTES QUEUE_EMPTY_MINUTES; do
  value=${!name}
  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    echo "$name must be a non-negative integer (received: $value)" >&2
    exit 2
  fi
done

if ! kubectl config get-contexts -o name | grep -Fxq -- "$CLOUD_CONTEXT"; then
  echo "Unknown Kubernetes context: $CLOUD_CONTEXT" >&2
  exit 2
fi
kubectl --context "$CLOUD_CONTEXT" get nodes >/dev/null

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
manifest="$script_dir/../k8s-nube/ndvi-cloudburst-job.yaml"
export NDVI_NAMESPACE="$CLOUD_NAMESPACE" NDVI_VALUES_JSON NDVI_WORKER_IMAGE

if (( (PENDING_NDVI_PODS > 3 && PENDING_DURATION_MINUTES >= 10) || QUEUE_AGE_MINUTES > 30 )); then
  echo "Burst condition met; submitting the sample NDVI Job to $CLOUD_CONTEXT/$CLOUD_NAMESPACE."
  kubectl --context "$CLOUD_CONTEXT" create namespace "$CLOUD_NAMESPACE" --dry-run=client -o yaml \
    | kubectl --context "$CLOUD_CONTEXT" apply -f -
  envsubst '${NDVI_NAMESPACE} ${NDVI_VALUES_JSON} ${NDVI_WORKER_IMAGE}' < "$manifest" \
    | kubectl --context "$CLOUD_CONTEXT" apply -f -
elif (( QUEUE_EMPTY_MINUTES >= 30 )); then
  echo "Queue has been empty for at least 30 minutes; removing the managed sample Job and its input ConfigMap."
  envsubst '${NDVI_NAMESPACE} ${NDVI_VALUES_JSON} ${NDVI_WORKER_IMAGE}' < "$manifest" \
    | kubectl --context "$CLOUD_CONTEXT" delete -f - --ignore-not-found=true
else
  echo 'No burst or cleanup threshold reached; no cloud resources changed.'
fi
