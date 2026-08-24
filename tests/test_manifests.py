from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
files = sorted((root / 'k8s').glob('*.yaml'))
assert len(files) == 8
objs = []
for p in files:
    objs.extend([d for d in yaml.safe_load_all(p.read_text()) if d])

by_key = {(o['kind'], o['metadata']['name']): o for o in objs}
deploy = by_key[('Deployment', 'production-app')]
container = deploy['spec']['template']['spec']['containers'][0]
assert deploy['spec']['replicas'] == 3
assert deploy['spec']['strategy']['rollingUpdate']['maxUnavailable'] == 0
assert container['securityContext']['runAsNonRoot'] is True
assert container['securityContext']['readOnlyRootFilesystem'] is True
assert container['securityContext']['allowPrivilegeEscalation'] is False
assert container['securityContext']['capabilities']['drop'] == ['ALL']
assert all(k in container for k in ('startupProbe', 'readinessProbe', 'livenessProbe'))
assert 'requests' in container['resources'] and 'limits' in container['resources']
assert deploy['spec']['template']['spec']['automountServiceAccountToken'] is False
assert by_key[('Service','production-app')]['spec']['selector'] == {'app':'production-app'}
hpa = by_key[('HorizontalPodAutoscaler','production-app')]
assert hpa['spec']['minReplicas'] == 3 and hpa['spec']['maxReplicas'] == 10
assert by_key[('PodDisruptionBudget','production-app')]['spec']['minAvailable'] == 2
assert by_key[('Namespace','production-demo')]['metadata']['labels']['pod-security.kubernetes.io/enforce'] == 'restricted'
assert set(by_key[('NetworkPolicy','production-app')]['spec']['policyTypes']) == {'Ingress','Egress'}
print('Project 28 manifest validation passed.')
