# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
---
# Default values for airflow.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# Provide a name to substitute for the full names of resources
fullnameOverride: ""

# Provide a name to substitute for the name of the chart
nameOverride: ""

# Provide a Kubernetes version (used for API Version selection) to override the auto-detected version
kubeVersionOverride: ""

# User and group of airflow user
uid: 50000
gid: 0

# Airflow home directory
# Used for mount paths
airflowHome: /opt/airflow

# Default airflow repository -- overrides all the specific images below
defaultAirflowRepository: apache/airflow

# Default airflow tag to deploy
defaultAirflowTag: "2.2.1"

# Airflow version (Used to make some decisions based on Airflow Version being deployed)
airflowVersion: "2.2.1"

# Images
images:
  airflow:
    repository: ~
    tag: ~
    pullPolicy: IfNotPresent
  # To avoid images with user code, you can turn this to 'true' and
  # all the 'run-airflow-migrations' and 'wait-for-airflow-migrations' containers/jobs
  # will use the images from 'defaultAirflowRepository:defaultAirflowTag' values
  # to run and wait for DB migrations .
  useDefaultImageForMigration: false
  pod_template:
    repository: ~
    tag: ~
    pullPolicy: IfNotPresent
  flower:
    repository: ~
    tag: ~
    pullPolicy: IfNotPresent
  statsd:
    repository: apache/airflow
    tag: airflow-statsd-exporter-2021.04.28-v0.17.0
    pullPolicy: IfNotPresent
  redis:
    repository: redis
    tag: 6-buster
    pullPolicy: IfNotPresent
  pgbouncer:
    repository: apache/airflow
    tag: airflow-pgbouncer-2021.04.28-1.14.0
    pullPolicy: IfNotPresent
  pgbouncerExporter:
    repository: apache/airflow
    tag: airflow-pgbouncer-exporter-2021.09.22-0.12.0
    pullPolicy: IfNotPresent
  gitSync:
    repository: k8s.gcr.io/git-sync/git-sync
    tag: v3.3.0
    pullPolicy: IfNotPresent

# Select certain nodes for airflow pods.
nodeSelector: {}
affinity: {}
tolerations: []

# Add common labels to all objects and pods defined in this chart.
labels: {}

# Ingress configuration
ingress:
  # Enable ingress resource
  enabled: false

  # Configs for the Ingress of the web Service
  web:
    # Annotations for the web Ingress
    annotations: {}

    # The path for the web Ingress
    path: "/"

    # The pathType for the above path (used only with Kubernetes v1.19 and above)
    pathType: "ImplementationSpecific"

    # The hostname for the web Ingress (Deprecated - renamed to `ingress.web.hosts`)
    host: ""

    # The hostnames for the web Ingress
    hosts: []

    # The Ingress Class for the web Ingress (used only with Kubernetes v1.19 and above)
    ingressClassName: ""

    # configs for web Ingress TLS
    tls:
      # Enable TLS termination for the web Ingress
      enabled: false
      # the name of a pre-created Secret containing a TLS private key and certificate
      secretName: ""

    # HTTP paths to add to the web Ingress before the default path
    precedingPaths: []

    # Http paths to add to the web Ingress after the default path
    succeedingPaths: []

  # Configs for the Ingress of the flower Service
  flower:
    # Annotations for the flower Ingress
    annotations: {}

    # The path for the flower Ingress
    path: "/"

    # The pathType for the above path (used only with Kubernetes v1.19 and above)
    pathType: "ImplementationSpecific"

    # The hostname for the flower Ingress (Deprecated - renamed to `ingress.flower.hosts`)
    host: ""

    # The hostnames for the flower Ingress
    hosts: []

    # The Ingress Class for the flower Ingress (used only with Kubernetes v1.19 and above)
    ingressClassName: ""

    # configs for web Ingress TLS
    tls:
      # Enable TLS termination for the flower Ingress
      enabled: false
      # the name of a pre-created Secret containing a TLS private key and certificate
      secretName: ""

# Network policy configuration
networkPolicies:
  # Enabled network policies
  enabled: false

# Extra annotations to apply to all
# Airflow pods
airflowPodAnnotations: {}

# Extra annotations to apply to
# main Airflow configmap
airflowConfigAnnotations: {}

# `airflow_local_settings` file as a string (can be templated).
airflowLocalSettings: |-
  {{- if semverCompare ">=2.2.0" .Values.airflowVersion }}
  {{- if not (or .Values.webserverSecretKey .Values.webserverSecretKeySecretName) }}
  from airflow.www.utils import UIAlert

  DASHBOARD_UIALERTS = [
    UIAlert(
      'Usage of a dynamic webserver secret key detected. We recommend a static webserver secret key instead.'
      ' See the <a href='
      '"https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#webserver-secret-key">'
      'Helm Chart Production Guide</a> for more details.',
      category="warning",
      roles=["Admin"],
      html=True,
    )
  ]
  {{- end }}
  {{- end }}

# Enable RBAC (default on most clusters these days)
rbac:
  # Specifies whether RBAC resources should be created
  create: true
  createSCCRoleBinding: false

# Airflow executor
# Options: LocalExecutor, CeleryExecutor, KubernetesExecutor, CeleryKubernetesExecutor
executor: "CeleryExecutor"

# If this is true and using LocalExecutor/KubernetesExecutor/CeleryKubernetesExecutor, the scheduler's
# service account will have access to communicate with the api-server and launch pods.
# If this is true and using CeleryExecutor/KubernetesExecutor/CeleryKubernetesExecutor, the workers
# will be able to launch pods.
allowPodLaunching: true

# Environment variables for all airflow containers
env: []
# - name: ""
#   value: ""

# Secrets for all airflow containers
secret: []
# - envName: ""
#   secretName: ""
#   secretKey: ""

# Extra secrets that will be managed by the chart
# (You can use them with extraEnv or extraEnvFrom or some of the extraVolumes values).
# The format is "key/value" where
#    * key (can be templated) is the name of the secret that will be created
#    * value: an object with the standard 'data' or 'stringData' key (or both).
#          The value associated with those keys must be a string (can be templated)
extraSecrets: {}
# eg:
# extraSecrets:
#   '{{ .Release.Name }}-airflow-connections':
#     data: |
#       AIRFLOW_CONN_GCP: 'base64_encoded_gcp_conn_string'
#       AIRFLOW_CONN_AWS: 'base64_encoded_aws_conn_string'
#     stringData: |
#       AIRFLOW_CONN_OTHER: 'other_conn'
#   '{{ .Release.Name }}-other-secret-name-suffix':
#     data: |
#        ...

# Extra ConfigMaps that will be managed by the chart
# (You can use them with extraEnv or extraEnvFrom or some of the extraVolumes values).
# The format is "key/value" where
#    * key (can be templated) is the name of the configmap that will be created
#    * value: an object with the standard 'data' key.
#          The value associated with this keys must be a string (can be templated)
extraConfigMaps: {}
# eg:
# extraConfigMaps:
#   '{{ .Release.Name }}-airflow-variables':
#     data: |
#       AIRFLOW_VAR_HELLO_MESSAGE: "Hi!"
#       AIRFLOW_VAR_KUBERNETES_NAMESPACE: "{{ .Release.Namespace }}"

# Extra env 'items' that will be added to the definition of airflow containers
# a string is expected (can be templated).
# TODO: difference from `env`? This is a templated string. Probably should template `env` and remove this.
extraEnv: ~
# eg:
# extraEnv: |
#   - name: AIRFLOW__CORE__LOAD_EXAMPLES
#     value: 'True'

# Extra envFrom 'items' that will be added to the definition of airflow containers
# A string is expected (can be templated).
extraEnvFrom: ~
# eg:
# extraEnvFrom: |
#   - secretRef:
#       name: '{{ .Release.Name }}-airflow-connections'
#   - configMapRef:
#       name: '{{ .Release.Name }}-airflow-variables'

# Airflow database & redis config
data:
  # If secret names are provided, use those secrets
  metadataSecretName: ~
  resultBackendSecretName: ~
  brokerUrlSecretName: ~

  # Otherwise pass connection values in
  metadataConnection:
    user: postgres
    pass: postgres
    protocol: postgresql
    host: ~
    port: 5432
    db: postgres
    sslmode: disable
  # resultBackendConnection defaults to the same database as metadataConnection
  resultBackendConnection: ~
  # or, you can use a different database
  # resultBackendConnection:
  #   user: postgres
  #   pass: postgres
  #   protocol: postgresql
  #   host: ~
  #   port: 5432
  #   db: postgres
  #   sslmode: disable
  # Note: brokerUrl can only be set during install, not upgrade
  brokerUrl: ~

# Fernet key settings
# Note: fernetKey can only be set during install, not upgrade
fernetKey: ~
fernetKeySecretName: ~

# Flask secret key for Airflow Webserver: `[webserver] secret_key` in airflow.cfg
webserverSecretKey: ~
webserverSecretKeySecretName: ~

# In order to use kerberos you need to create secret containing the keytab file
# The secret name should follow naming convention of the application where resources are
# name {{ .Release-name }}-<POSTFIX>. In case of the keytab file, the postfix is "kerberos-keytab"
# So if your release is named "my-release" the name of the secret should be "my-release-kerberos-keytab"
#
# The Keytab content should be available in the "kerberos.keytab" key of the secret.
#
#  apiVersion: v1
#  kind: Secret
#  data:
#    kerberos.keytab: <base64_encoded keytab file content>
#  type: Opaque
#
#
#  If you have such keytab file you can do it with similar
#
#  kubectl create secret generic {{ .Release.name }}-kerberos-keytab --from-file=kerberos.keytab
#
kerberos:
  enabled: false
  ccacheMountPath: /var/kerberos-ccache
  ccacheFileName: cache
  configPath: /etc/krb5.conf
  keytabPath: /etc/airflow.keytab
  principal: airflow@FOO.COM
  reinitFrequency: 3600
  config: |
    # This is an example config showing how you can use templating and how "example" config
    # might look like. It works with the test kerberos server that we are using during integration
    # testing at Apache Airflow (see `scripts/ci/docker-compose/integration-kerberos.yml` but in
    # order to make it production-ready you must replace it with your own configuration that
    # Matches your kerberos deployment. Administrators of your Kerberos instance should
    # provide the right configuration.

    [logging]
    default = "FILE:{{ template "airflow_logs_no_quote" . }}/kerberos_libs.log"
    kdc = "FILE:{{ template "airflow_logs_no_quote" . }}/kerberos_kdc.log"
    admin_server = "FILE:{{ template "airflow_logs_no_quote" . }}/kadmind.log"

    [libdefaults]
    default_realm = FOO.COM
    ticket_lifetime = 10h
    renew_lifetime = 7d
    forwardable = true

    [realms]
    FOO.COM = {
      kdc = kdc-server.foo.com
      admin_server = admin_server.foo.com
    }

# Airflow Worker Config
workers:
  # Number of airflow celery workers in StatefulSet
  replicas: 1

  # Command to use when running Airflow workers (templated).
  command: ~
  # Args to use when running Airflow workers (templated).
  args:
    - "bash"
    - "-c"
    # The format below is necessary to get `helm lint` happy
    - |-
      exec \
      airflow {{ semverCompare ">=2.0.0" .Values.airflowVersion | ternary "celery worker" "worker" }}

  # Update Strategy when worker is deployed as a StatefulSet
  updateStrategy: ~
  # Update Strategy when worker is deployed as a Deployment
  strategy:
    rollingUpdate:
      maxSurge: "100%"
      maxUnavailable: "50%"

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to worker kubernetes service account.
    annotations: {}

  # Allow KEDA autoscaling.
  # Persistence.enabled must be set to false to use KEDA.
  keda:
    enabled: false
    namespaceLabels: {}

    # How often KEDA polls the airflow DB to report new scale requests to the HPA
    pollingInterval: 5

    # How many seconds KEDA will wait before scaling to zero.
    # Note that HPA has a separate cooldown period for scale-downs
    cooldownPeriod: 30

    # Minimum number of workers created by keda
    minReplicaCount: 0

    # Maximum number of workers created by keda
    maxReplicaCount: 10

  persistence:
    # Enable persistent volumes
    enabled: true
    # Volume size for worker StatefulSet
    size: 100Gi
    # If using a custom storageClass, pass name ref to all statefulSets here
    storageClassName:
    # Execute init container to chown log directory.
    # This is currently only needed in kind, due to usage
    # of local-path provisioner.
    fixPermissions: false

  kerberosSidecar:
    # Enable kerberos sidecar
    enabled: false
    resources: {}
    #  limits:
    #   cpu: 100m
    #   memory: 128Mi
    #  requests:
    #   cpu: 100m
    #   memory: 128Mi

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

  # Grace period for tasks to finish after SIGTERM is sent from kubernetes
  terminationGracePeriodSeconds: 600

  # This setting tells kubernetes that its ok to evict
  # when it wants to scale a node down.
  safeToEvict: true

  # Launch additional containers into worker.
  # Note: If used with KubernetesExecutor, you are responsible for signaling sidecars to exit when the main
  # container finishes so Airflow can continue the worker shutdown process!
  extraContainers: []
  # Add additional init containers into workers.
  extraInitContainers: []

  # Mount additional volumes into worker.
  extraVolumes: []
  extraVolumeMounts: []

  # Select certain nodes for airflow worker pods.
  nodeSelector: {}
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels:
                component: worker
            topologyKey: "kubernetes.io/hostname"
  tolerations: []
  # hostAliases to use in worker pods.
  # See:
  # https://kubernetes.io/docs/concepts/services-networking/add-entries-to-pod-etc-hosts-with-host-aliases/
  hostAliases: []
  # - ip: "127.0.0.2"
  #   hostnames:
  #   - "test.hostname.one"
  # - ip: "127.0.0.3"
  #   hostnames:
  #   - "test.hostname.two"

  podAnnotations: {}

  logGroomerSidecar:
    # Command to use when running the Airflow worker log groomer sidecar (templated).
    command: ~
    # Args to use when running the Airflow worker log groomer sidecar (templated).
    args: ["bash", "/clean-logs"]
    # Number of days to retain logs
    retentionDays: 15
    resources: {}
    #  limits:
    #   cpu: 100m
    #   memory: 128Mi
    #  requests:
    #   cpu: 100m
    #   memory: 128Mi

# Airflow scheduler settings
scheduler:
  # If the scheduler stops heartbeating for 5 minutes (5*60s) kill the
  # scheduler and let Kubernetes restart it
  livenessProbe:
    initialDelaySeconds: 10
    timeoutSeconds: 10
    failureThreshold: 5
    periodSeconds: 60
  # Airflow 2.0 allows users to run multiple schedulers,
  # However this feature is only recommended for MySQL 8+ and Postgres
  replicas: 1

  # Command to use when running the Airflow scheduler (templated).
  command: ~
  # Args to use when running the Airflow scheduler (templated).
  args: ["bash", "-c", "exec airflow scheduler"]

  # Update Strategy when scheduler is deployed as a StatefulSet
  # (when using LocalExecutor and workers.persistence)
  updateStrategy: ~
  # Update Strategy when scheduler is deployed as a Deployment
  # (when not using LocalExecutor and workers.persistence)
  strategy: ~

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to scheduler kubernetes service account.
    annotations: {}

  # Scheduler pod disruption budget
  podDisruptionBudget:
    enabled: false

    # PDB configuration
    config:
      maxUnavailable: 1

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

  # This setting tells kubernetes that its ok to evict
  # when it wants to scale a node down.
  safeToEvict: true

  # Launch additional containers into scheduler.
  extraContainers: []
  # Add additional init containers into scheduler.
  extraInitContainers: []

  # Mount additional volumes into scheduler.
  extraVolumes: []
  extraVolumeMounts: []

  # Select certain nodes for airflow scheduler pods.
  nodeSelector: {}
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels:
                component: scheduler
            topologyKey: "kubernetes.io/hostname"
  tolerations: []

  podAnnotations: {}

  logGroomerSidecar:
    # Whether to deploy the Airflow scheduler log groomer sidecar.
    enabled: true
    # Command to use when running the Airflow scheduler log groomer sidecar (templated).
    command: ~
    # Args to use when running the Airflow scheduler log groomer sidecar (templated).
    args: ["bash", "/clean-logs"]
    # Number of days to retain logs
    retentionDays: 15
    resources: {}
    #  limits:
    #   cpu: 100m
    #   memory: 128Mi
    #  requests:
    #   cpu: 100m
    #   memory: 128Mi

# Airflow create user job settings
createUserJob:
  # Annotations on the create user job pod
  annotations: {}
  # jobAnnotations are annotations on the create user job
  jobAnnotations: {}

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to create user kubernetes service account.
    annotations: {}

  nodeSelector: {}
  affinity: {}
  tolerations: []

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

# Airflow database migration job settings
migrateDatabaseJob:
  # Annotations on the database migration pod
  annotations: {}
  # jobAnnotations are annotations on the database migration job
  jobAnnotations: {}

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to migrate database job kubernetes service account.
    annotations: {}

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

  # Launch additional containers into database migration job
  extraContainers: []
  nodeSelector: {}
  affinity: {}
  tolerations: []

# Airflow webserver settings
webserver:
  allowPodLogReading: true
  livenessProbe:
    initialDelaySeconds: 15
    timeoutSeconds: 30
    failureThreshold: 20
    periodSeconds: 5

  readinessProbe:
    initialDelaySeconds: 15
    timeoutSeconds: 30
    failureThreshold: 20
    periodSeconds: 5

  # Number of webservers
  replicas: 1

  # Command to use when running the Airflow webserver (templated).
  command: ~
  # Args to use when running the Airflow webserver (templated).
  args: ["bash", "-c", "exec airflow webserver"]

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to webserver kubernetes service account.
    annotations: {}

  # Allow overriding Update Strategy for Webserver
  strategy: ~

  # Additional network policies as needed (Deprecated - renamed to `webserver.networkPolicy.ingress.from`)
  extraNetworkPolicies: []
  networkPolicy:
    ingress:
      # Peers for webserver NetworkPolicy ingress
      from: []
      # Ports for webserver NetworkPolicy ingress (if `from` is set)
      ports:
        - port: airflow-ui

  resources: {}
  #   limits:
  #     cpu: 100m
  #     memory: 128Mi
  #   requests:
  #     cpu: 100m
  #     memory: 128Mi

  # Create initial user.
  defaultUser:
    enabled: true
    role: Admin
    username: admin
    email: admin@example.com
    firstName: admin
    lastName: user
    password: admin

  # Launch additional containers into webserver.
  extraContainers: []
  # Add additional init containers into webserver.
  extraInitContainers: []

  # Mount additional volumes into webserver.
  extraVolumes: []
  extraVolumeMounts: []

  # This string (can be templated) will be mounted into the Airflow Webserver as a custom
  # webserver_config.py. You can bake a webserver_config.py in to your image instead.
  webserverConfig: ~
  # webserverConfig: |
  #   from airflow import configuration as conf

  #   # The SQLAlchemy connection string.
  #   SQLALCHEMY_DATABASE_URI = conf.get('core', 'SQL_ALCHEMY_CONN')

  #   # Flask-WTF flag for CSRF
  #   CSRF_ENABLED = True

  service:
    type: ClusterIP
    ## service annotations
    annotations: {}
    ports:
      - name: airflow-ui
        port: "{{ .Values.ports.airflowUI }}"
    # To change the port used to access the webserver:
    # ports:
    #   - name: airflow-ui
    #     port: 80
    #     targetPort: airflow-ui
    # To only expose a sidecar, not the webserver directly:
    # ports:
    #   - name: only_sidecar
    #     port: 80
    #     targetPort: 8888
    loadBalancerIP: ~
    ## Limit load balancer source ips to list of CIDRs
    # loadBalancerSourceRanges:
    #   - "10.123.0.0/16"
    loadBalancerSourceRanges: []

  # Select certain nodes for airflow webserver pods.
  nodeSelector: {}
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels:
                component: webserver
            topologyKey: "kubernetes.io/hostname"
  tolerations: []

  podAnnotations: {}

# Airflow Triggerer Config
triggerer:
  enabled: true
  # Number of airflow triggerers in the deployment
  replicas: 1

  # Command to use when running Airflow triggerers (templated).
  command: ~
  # Args to use when running Airflow triggerer (templated).
  args: ["bash", "-c", "exec airflow triggerer"]

  # Update Strategy for triggerers
  strategy:
    rollingUpdate:
      maxSurge: "100%"
      maxUnavailable: "50%"

  # If the triggerer stops heartbeating for 5 minutes (5*60s) kill the
  # triggerer and let Kubernetes restart it
  livenessProbe:
    initialDelaySeconds: 10
    timeoutSeconds: 10
    failureThreshold: 5
    periodSeconds: 60

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to triggerer kubernetes service account.
    annotations: {}

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

  # Grace period for triggerer to finish after SIGTERM is sent from kubernetes
  terminationGracePeriodSeconds: 60

  # This setting tells kubernetes that its ok to evict
  # when it wants to scale a node down.
  safeToEvict: true

  # Launch additional containers into triggerer.
  extraContainers: []
  # Add additional init containers into triggerers.
  extraInitContainers: []

  # Mount additional volumes into triggerer.
  extraVolumes: []
  extraVolumeMounts: []

  # Select certain nodes for airflow triggerer pods.
  nodeSelector: {}
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels:
                component: triggerer
            topologyKey: "kubernetes.io/hostname"
  tolerations: []

  podAnnotations: {}

# Flower settings
flower:
  # Enable flower.
  # If True, and using CeleryExecutor/CeleryKubernetesExecutor, will deploy flower app.
  enabled: true

  # Command to use when running flower (templated).
  command: ~
  # Args to use when running flower (templated).
  args:
    - "bash"
    - "-c"
    # The format below is necessary to get `helm lint` happy
    - |-
      exec \
      airflow {{ semverCompare ">=2.0.0" .Values.airflowVersion | ternary "celery flower" "flower" }}

  # Additional network policies as needed (Deprecated - renamed to `flower.networkPolicy.ingress.from`)
  extraNetworkPolicies: []
  networkPolicy:
    ingress:
      # Peers for flower NetworkPolicy ingress
      from: []
      # Ports for flower NetworkPolicy ingress (if ingressPeers is set)
      ports:
        - port: flower-ui

  resources: {}
  #   limits:
  #     cpu: 100m
  #     memory: 128Mi
  #   requests:
  #     cpu: 100m
  #     memory: 128Mi

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to worker kubernetes service account.
    annotations: {}

  # A secret containing the connection
  secretName: ~

  # Else, if username and password are set, create secret from username and password
  username: ~
  password: ~

  service:
    type: ClusterIP
    ## service annotations
    annotations: {}
    ports:
      - name: flower-ui
        port: "{{ .Values.ports.flowerUI }}"
    # To change the port used to access flower:
    # ports:
    #   - name: flower-ui
    #     port: 8080
    #     targetPort: flower-ui
    loadBalancerIP: ~
    ## Limit load balancer source ips to list of CIDRs
    # loadBalancerSourceRanges:
    #   - "10.123.0.0/16"
    loadBalancerSourceRanges: []

  # Launch additional containers into the flower pods.
  extraContainers: []
  # Mount additional volumes into the flower pods.
  extraVolumes: []

  # Select certain nodes for airflow flower pods.
  nodeSelector: {}
  affinity: {}
  tolerations: []

  podAnnotations: {}

# Statsd settings
statsd:
  enabled: true

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to worker kubernetes service account.
    annotations: {}

  # Additional network policies as needed
  extraNetworkPolicies: []
  resources: {}
  #   limits:
  #     cpu: 100m
  #     memory: 128Mi
  #   requests:
  #     cpu: 100m
  #     memory: 128Mi

  service:
    extraAnnotations: {}

  # Select certain nodes for statsd pods.
  nodeSelector: {}
  affinity: {}
  tolerations: []

  # Additional mappings for statsd exporter.
  extraMappings: []

  uid: 65534

# PgBouncer settings
pgbouncer:
  # Enable PgBouncer
  enabled: false
  # Command to use for PgBouncer(templated).
  command: ["pgbouncer", "-u", "nobody", "/etc/pgbouncer/pgbouncer.ini"]
  # Args to use for PgBouncer(templated).
  args: ~

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to worker kubernetes service account.
    annotations: {}

  # Additional network policies as needed
  extraNetworkPolicies: []

  # Pool sizes
  metadataPoolSize: 10
  resultBackendPoolSize: 5

  # Maximum clients that can connect to PgBouncer (higher = more file descriptors)
  maxClientConn: 100

  # supply the name of existing secret with pgbouncer.ini and users.txt defined
  # you can load them to a k8s secret like the one below
  #  apiVersion: v1
  #  kind: Secret
  #  metadata:
  #    name: pgbouncer-config-secret
  #  data:
  #     pgbouncer.ini: <base64_encoded pgbouncer.ini file content>
  #     users.txt: <base64_encoded users.txt file content>
  #  type: Opaque
  #
  #  configSecretName: pgbouncer-config-secret
  #
  configSecretName: ~

  # PgBouncer pod disruption budget
  podDisruptionBudget:
    enabled: false

    # PDB configuration
    config:
      maxUnavailable: 1

  # Limit the resources to PgBouncer.
  # When you specify the resource request the k8s scheduler uses this information to decide which node to
  # place the Pod on. When you specify a resource limit for a Container, the kubelet enforces those limits so
  # that the running container is not allowed to use more of that resource than the limit you set.
  # See: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
  # Example:
  #
  # resource:
  #   limits:
  #     cpu: 100m
  #     memory: 128Mi
  #   requests:
  #     cpu: 100m
  #     memory: 128Mi
  resources: {}

  service:
    extraAnnotations: {}

  # https://www.pgbouncer.org/config.html
  verbose: 0
  logDisconnections: 0
  logConnections: 0

  sslmode: "prefer"
  ciphers: "normal"

  ssl:
    ca: ~
    cert: ~
    key: ~

  # Add extra PgBouncer ini configuration in the databases section:
  # https://www.pgbouncer.org/config.html#section-databases
  extraIniMetadata: ~
  extraIniResultBackend: ~
  # Add extra general PgBouncer ini configuration: https://www.pgbouncer.org/config.html
  extraIni: ~

  # Select certain nodes for PgBouncer pods.
  nodeSelector: {}
  affinity: {}
  tolerations: []

  uid: 65534

  metricsExporterSidecar:
    resources: {}
    #  limits:
    #   cpu: 100m
    #   memory: 128Mi
    #  requests:
    #   cpu: 100m
    #   memory: 128Mi

# Configuration for the redis provisioned by the chart
redis:
  enabled: true
  terminationGracePeriodSeconds: 600

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to worker kubernetes service account.
    annotations: {}

  persistence:
    # Enable persistent volumes
    enabled: true
    # Volume size for worker StatefulSet
    size: 1Gi
    # If using a custom storageClass, pass name ref to all statefulSets here
    storageClassName:

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

  # If set use as redis secret. Make sure to also set data.brokerUrlSecretName value.
  passwordSecretName: ~

  # Else, if password is set, create secret with it,
  # Otherwise a new password will be generated on install
  # Note: password can only be set during install, not upgrade.
  password: ~

  # This setting tells kubernetes that its ok to evict
  # when it wants to scale a node down.
  safeToEvict: true

  # Select certain nodes for redis pods.
  nodeSelector: {}
  affinity: {}
  tolerations: []

# Auth secret for a private registry
# This is used if pulling airflow images from a private registry
registry:
  secretName: ~

  # Example:
  # connection:
  #   user: ~
  #   pass: ~
  #   host: ~
  #   email: ~
  connection: {}

# Elasticsearch logging configuration
elasticsearch:
  # Enable elasticsearch task logging
  enabled: false
  # A secret containing the connection
  secretName: ~
  # Or an object representing the connection
  # Example:
  # connection:
  #   user: ~
  #   pass: ~
  #   host: ~
  #   port: ~
  connection: {}

# All ports used by chart
ports:
  flowerUI: 5555
  airflowUI: 8080
  workerLogs: 8793
  redisDB: 6379
  statsdIngest: 9125
  statsdScrape: 9102
  pgbouncer: 6543
  pgbouncerScrape: 9127

# Define any ResourceQuotas for namespace
quotas: {}

# Define default/max/min values for pods and containers in namespace
limits: []

# This runs as a CronJob to cleanup old pods.
cleanup:
  enabled: false
  # Run every 15 minutes
  schedule: "*/15 * * * *"
  # Command to use when running the cleanup cronjob (templated).
  command: ~
  # Args to use when running the cleanup cronjob (templated).
  args: ["bash", "-c", "exec airflow kubernetes cleanup-pods --namespace={{ .Release.Namespace }}"]


  # Select certain nodes for airflow cleanup pods.
  nodeSelector: {}
  affinity: {}
  tolerations: []

  resources: {}
  #  limits:
  #   cpu: 100m
  #   memory: 128Mi
  #  requests:
  #   cpu: 100m
  #   memory: 128Mi

  # Create ServiceAccount
  serviceAccount:
    # Specifies whether a ServiceAccount should be created
    create: true
    # The name of the ServiceAccount to use.
    # If not set and create is true, a name is generated using the release name
    name: ~

    # Annotations to add to cleanup cronjob kubernetes service account.
    annotations: {}

# Configuration for postgresql subchart
# Not recommended for production
postgresql:
  enabled: true
  postgresqlPassword: postgres
  postgresqlUsername: postgres

# Config settings to go into the mounted airflow.cfg
#
# Please note that these values are passed through the `tpl` function, so are
# all subject to being rendered as go templates. If you need to include a
# literal `{{` in a value, it must be expressed like this:
#
#    a: '{{ "{{ not a template }}" }}'
#
# Do not set config containing secrets via plain text values, use Env Var or k8s secret object
# yamllint disable rule:line-length
config:
  core:
    dags_folder: '{{ include "airflow_dags" . }}'
    # This is ignored when used with the official Docker image
    load_examples: 'False'
    executor: '{{ .Values.executor }}'
    # For Airflow 1.10, backward compatibility; moved to [logging] in 2.0
    colored_console_log: 'False'
    remote_logging: '{{- ternary "True" "False" .Values.elasticsearch.enabled }}'
  # Authentication backend used for the experimental API
  api:
    auth_backend: airflow.api.auth.backend.deny_all
  logging:
    remote_logging: '{{- ternary "True" "False" .Values.elasticsearch.enabled }}'
    colored_console_log: 'False'
  metrics:
    statsd_on: '{{ ternary "True" "False" .Values.statsd.enabled }}'
    statsd_port: 9125
    statsd_prefix: airflow
    statsd_host: '{{ printf "%s-statsd" .Release.Name }}'
  webserver:
    enable_proxy_fix: 'True'
    # For Airflow 1.10
    rbac: 'True'
  celery:
    worker_concurrency: 16
  scheduler:
    # statsd params included for Airflow 1.10 backward compatibility; moved to [metrics] in 2.0
    statsd_on: '{{ ternary "True" "False" .Values.statsd.enabled }}'
    statsd_port: 9125
    statsd_prefix: airflow
    statsd_host: '{{ printf "%s-statsd" .Release.Name }}'
    # `run_duration` included for Airflow 1.10 backward compatibility; removed in 2.0.
    run_duration: 41460
  elasticsearch:
    json_format: 'True'
    log_id_template: "{dag_id}_{task_id}_{execution_date}_{try_number}"
  elasticsearch_configs:
    max_retries: 3
    timeout: 30
    retry_timeout: 'True'
  kerberos:
    keytab: '{{ .Values.kerberos.keytabPath }}'
    reinit_frequency: '{{ .Values.kerberos.reinitFrequency }}'
    principal: '{{ .Values.kerberos.principal }}'
    ccache: '{{ .Values.kerberos.ccacheMountPath }}/{{ .Values.kerberos.ccacheFileName }}'
  celery_kubernetes_executor:
    kubernetes_queue: 'kubernetes'
  kubernetes:
    namespace: '{{ .Release.Namespace }}'
    airflow_configmap: '{{ include "airflow_config" . }}'
    airflow_local_settings_configmap: '{{ include "airflow_config" . }}'
    pod_template_file: '{{ include "airflow_pod_template_file" . }}/pod_template_file.yaml'
    worker_container_repository: '{{ .Values.images.airflow.repository | default .Values.defaultAirflowRepository }}'
    worker_container_tag: '{{ .Values.images.airflow.tag | default .Values.defaultAirflowTag }}'
    multi_namespace_mode: '{{ if .Values.multiNamespaceMode }}True{{ else }}False{{ end }}'
# yamllint enable rule:line-length

# Whether the KubernetesExecutor can launch workers and pods in multiple namespaces
# If true, it creates ClusterRole/ClusterRolebinding (with access to entire cluster)
multiNamespaceMode: false

# `podTemplate` is a templated string containing the contents of `pod_template_file.yaml` used for
# KubernetesExecutor workers. The default `podTemplate` will use normal `workers` configuration parameters
# (e.g. `workers.resources`). As such, you normally won't need to override this directly, however,
# you can still provide a completely custom `pod_template_file.yaml` if desired.
# If not set, a default one is created using `files/pod-template-file.kubernetes-helm-yaml`.
podTemplate: ~
# The following example is NOT functional, but meant to be illustrative of how you can provide a custom
# `pod_template_file`. You're better off starting with the default in
# `files/pod-template-file.kubernetes-helm-yaml` and modifying from there.
# We will set `priorityClassName` in this example:
# podTemplate: |
#   apiVersion: v1
#   kind: Pod
#   metadata:
#     name: dummy-name
#     labels:
#       tier: airflow
#       component: worker
#       release: {{ .Release.Name }}
#   spec:
#     priorityClassName: high-priority
#     containers:
#       - name: base
#         ...

# Git sync
dags:
  persistence:
    # Enable persistent volume for storing dags
    enabled: false
    # Volume size for dags
    size: 1Gi
    # If using a custom storageClass, pass name here
    storageClassName:
    # access mode of the persistent volume
    accessMode: ReadOnlyMany
    ## the name of an existing PVC to use
    existingClaim: centos-pv-claim
  gitSync:
    enabled: true

    # git repo clone url
    # ssh examples ssh://git@github.com/apache/airflow.git
    # git@github.com:apache/airflow.git
    # https example: https://github.com/apache/airflow.git
    repo: https://github.com/jfsharron/week13.git
    branch: main
    rev: HEAD
    subPath: ""
    #sshKeySecret: airflow-ssh-git-secret
    depth: 1
    # the number of consecutive failures allowed before aborting
    maxFailures: 0
    # subpath within the repo where dags are located
    # should be "" if dags are at repo root
    subPath: ""
    # if your repo needs a user name password
    # you can load them to a k8s secret like the one below
    #   ---
    #   apiVersion: v1
    #   kind: Secret
    #   metadata:
    #     name: git-credentials
    #   data:
    #     GIT_SYNC_USERNAME: <base64_encoded_git_username>
    #     GIT_SYNC_PASSWORD: <base64_encoded_git_password>
    # and specify the name of the secret below
    #
    # credentialsSecret: git-credentials
    #
    #
    # If you are using an ssh clone url, you can load
    # the ssh private key to a k8s secret like the one below
    #   ---
    #   apiVersion: v1
    #   kind: Secret
    #   metadata:
    #     name: airflow-ssh-secret
    #   data:
    #     # key needs to be gitSshKey
    #     gitSshKey: <base64_encoded_data>
    # and specify the name of the secret below
    # sshKeySecret: airflow-ssh-secret
    #
    # If you are using an ssh private key, you can additionally
    # specify the content of your known_hosts file, example:
    #
    # knownHosts: |
    #    <host1>,<ip1> <key1>
    #    <host2>,<ip2> <key2>
    # interval between git sync attempts in seconds
    wait: 60
    containerName: git-sync
    uid: 65533
    extraVolumeMounts: []
    env: []
    resources: {}
    #  limits:
    #   cpu: 100m
    #   memory: 128Mi
    #  requests:
    #   cpu: 100m
    #   memory: 128Mi

logs:
  persistence:
    # Enable persistent volume for storing logs
    enabled: false
    # Volume size for logs
    size: 100Gi
    # If using a custom storageClass, pass name here
    storageClassName:
    ## the name of an existing PVC to use
    existingClaim:





