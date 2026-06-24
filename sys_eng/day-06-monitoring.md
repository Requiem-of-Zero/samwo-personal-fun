# Day 06 - Monitoring and Observability

## Objective

Learn how modern infrastructure teams monitor systems, applications, and services in production environments.

The goal is not simply collecting metrics, but understanding how to answer critical operational questions:

```text
Is the server healthy?
Is the application healthy?
Is the database healthy?
Can users access the service?
When should an alert be triggered?
```

---

# Monitoring Architecture

The monitoring stack deployed during this exercise:

```text
Ubuntu Server
│
├── Node Exporter
│      ↓
│  Host Metrics
│
├── Blackbox Exporter
│      ↓
│  Service Availability Checks
│
├── Prometheus
│      ↓
│  Metrics Storage
│
└── Grafana
       ↓
   Dashboards & Visualization
```

---

# Node Exporter

## Purpose

Node Exporter exposes Linux operating system metrics to Prometheus.

Examples:

```text
CPU Usage
Memory Usage
Disk Usage
Filesystem Statistics
Network Traffic
Load Average
```

Node Exporter answers:

```text
"How healthy is the server?"
```

### Verification

Metrics endpoint:

```bash
curl localhost:9100/metrics
```

Example metrics:

```text
node_cpu_seconds_total
node_memory_MemAvailable_bytes
node_filesystem_avail_bytes
node_load1
```

---

# Prometheus

## Purpose

Prometheus is a time-series database that collects and stores metrics.

Prometheus does not wait for metrics to be pushed.

Instead, it periodically scrapes configured targets.

Example:

```text
Prometheus
      ↓
Node Exporter
      ↓
Collect Metrics
```

### Prometheus Concepts

Every metric consists of:

```text
Metric Name
Labels
Timestamp
Value
```

Example:

```text
Metric:
probe_success

Label:
instance=http://pos-nginx

Timestamp:
1782268007

Value:
1
```

---

# Metrics Collection

Prometheus scrapes:

```text
node-exporter
prometheus
blackbox-exporter
```

Verification:

```bash
curl localhost:9090/api/v1/targets
```

Expected:

```text
health = up
```

for all targets.

---

# Grafana

## Purpose

Grafana provides visualization and dashboards for metrics stored in Prometheus.

Without Grafana:

```text
CPU = 15%
RAM = 30%
```

With Grafana:

```text
Graphs
Dashboards
Historical Trends
```

### Data Source

Grafana connected to:

```text
http://prometheus:9090
```

inside Docker networking.

---

# Dashboards

Imported Dashboard:

```text
ID: 1860
Node Exporter Full
```

Dashboard provides:

```text
CPU Usage
Memory Usage
Disk Usage
Filesystem Usage
Load Average
Network Traffic
```

This completed the monitoring pipeline:

```text
Ubuntu
   ↓
Node Exporter
   ↓
Prometheus
   ↓
Grafana Dashboard
```

---

# Uptime Monitoring

## Why Node Exporter Is Not Enough

Node Exporter only answers:

```text
Is the server healthy?
```

It does not answer:

```text
Can users reach the application?
```

Example:

```text
Ubuntu Server   UP
Node Exporter   UP
NGINX           DOWN
```

Node Exporter would still appear healthy.

---

# Blackbox Exporter

Blackbox Exporter performs endpoint testing.

It answers:

```text
Can I reach this service?
```

Architecture:

```text
Prometheus
      ↓
Blackbox Exporter
      ↓
http://pos-nginx
```

---

# Probe Success

Metric:

```text
probe_success
```

Values:

```text
1 = Success
0 = Failure
```

Example:

```text
NGINX Running
probe_success = 1
```

```text
NGINX Stopped
probe_success = 0
```

---

# Uptime Verification

Service stopped:

```bash
docker stop pos-nginx
```

Verification:

```bash
curl -s \
"http://localhost:9090/api/v1/query?query=probe_success"
```

Result:

```text
probe_success = 0
```

Service restored:

```bash
docker start pos-nginx
```

Result:

```text
probe_success = 1
```

This confirmed uptime monitoring was functioning correctly.

---

# Alerting Concepts

Monitoring tells engineers:

```text
Something is wrong.
```

Alerting tells engineers:

```text
Go fix it.
```

---

# Alert Structure

Every alert follows:

```text
Metric
   ↓
Threshold
   ↓
Duration
   ↓
Alert
```

Example:

```text
probe_success
```

Threshold:

```text
== 0
```

Duration:

```text
1 minute
```

Alert:

```text
Website Down
```

---

# Why Duration Matters

Bad Alert:

```text
probe_success == 0
```

Problem:

```text
Temporary network hiccup
↓
False Alert
```

Better:

```text
probe_success == 0
FOR 1m
```

This avoids alert fatigue.

---

# Understanding Load Average

Metric:

```text
node_load1
```

Represents:

```text
1-minute Linux Load Average
```

Observed value:

```text
0.77
```

Meaning:

```text
Healthy system load
```

Important lesson:

Before creating an alert:

```text
Understand the metric
Understand normal behavior
Then choose thresholds
```

---

# Filesystem Monitoring

Metrics:

```text
node_filesystem_avail_bytes
node_filesystem_size_bytes
```

Observed values:

```text
Available:
225,994,727,424

Total:
322,291,367,936
```

---

# Percentage-Based Alerting

Avoid:

```text
Alert if free space < fixed byte value
```

Reason:

```text
Different systems have different disk sizes
```

Preferred:

```text
Alert if free space < 20%
```

Prometheus Query:

```promql
(node_filesystem_avail_bytes /
 node_filesystem_size_bytes) * 100
```

Advantages:

```text
Scales across servers
Cloud VMs
Physical Machines
Containers
```

---

# Key Lessons Learned

Monitoring layers are different:

```text
Node Exporter
↓
Server Health

Blackbox Exporter
↓
Application Reachability

Prometheus
↓
Metric Storage

Grafana
↓
Visualization
```

A healthy server does not guarantee a healthy application.

Example:

```text
Ubuntu Server   UP
CPU             Normal
RAM             Normal
NGINX           DOWN
```

Only uptime monitoring detects this scenario.

---

# Completed Objectives

- [x] Grafana
- [x] Prometheus
- [x] Metrics Collection
- [x] Dashboards
- [x] Uptime Monitoring
- [x] Alerting Concepts

---

# Outcome

Built and validated a complete monitoring stack capable of:

- Collecting Linux host metrics
- Storing metrics in Prometheus
- Visualizing infrastructure health in Grafana
- Monitoring service uptime
- Understanding alert design and thresholds
- Distinguishing infrastructure failures from application failures

This monitoring stack resembles the foundation commonly used by Systems Engineering, Infrastructure Engineering, Platform Engineering, DevOps, and Site Reliability Engineering teams in production environments.
