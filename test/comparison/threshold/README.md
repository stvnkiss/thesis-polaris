# Threshold Decision Logic

## Introduction

The Threshold Decision Logic is a simple yet great way of combining two arbitrary elasticity strategies. In this short example we combine HorizontalElasticityStrategy with VerticalElasticityStrategy.

Fine-grained scaling is a key property, that is achieved by the definition of a threshold, which is used to decide between the two elasticity strategies.
On each evaluation of SLO compliance, the threshold value is compared against the deviation of the current SloCompliance and 100%.
Given the difference exceeds the threshold the primary elasticity strategy is executed, otherwise the secondary is picked to regain compliance with the SLO.


## Motivation

Whenever possible horizontal scaling is a great option to scale workloads to keep up with the requirements.
However, horizontal scaling may lead to over provisioning due to its characteristics, that the requested resources are multiplied by the number of instances.

Sudden load spikes can further outline the problem of over provisioning, as workloads cannot be adjusted in proportion to the load changes.
Over the long term a steady increase in resources is easily managed by ThresholdBasedDecisionLogic as vertical scaling allows fine-grained scaling over horizontal scaling.
When it comes to rapid scaling, this scaling strategy easily accomplishes it by utilizing horizontal scaling.

## Test Cases

| Workload      | Min | Max |
|---------------|-----|-----|
| Pod CPU mi    | 50  | 200 |
| Pod Memory Mi | 50  | 100 |
| Scale         | 1   | 10  |

### Scale up followed by scale down

Based on the following chart group it is clearly visible that threshold based scaling is capable of a more fine-grained scaling than simple horizontal scaling.
Even though the threshold strategy introduced some lag in the scaling in the test case, the workload was scaled down rapidly as the CPU usage decreased.

![plot](threshold_horizontal.png)

### Constant High CPU Usage

In this scenario the threshold based strategy shows its strengths including fine-grained scaling and the flexibility by allowing multiple strategies to be combined.
The constant CPU usage simulates a workload utilization that linearly increases over time.
This scenario benefits fine-grained scaling, as the threshold based strategy chooses vertical scaling to adjust workload resources in order to comply with the SLO. Vertical scaling is more efficient than horizontal scaling in terms of resource allocation, because horizontal scaling can only multiple its workload resource requests.
Therefore, the threshold based scaling can easily outperform the simple horizontal strategy saving not utilized resources thus costs for the service provider.
At the later stages of the test, the limit for vertical scaling is reached, therefore the threshold strategy decides to switch over to horizontal scaling. This makes the threshold scaling strategy to be more robust.

![plot](threshold_horizontal_constant.png)

### Cost Efficiency

| Workload      | Min | Max  |
|---------------|-----|------|
| Pod CPU mi    | 250 | 2000 |
| Pod Memory Mi | 50  | 100  |
| Scale         | 1   | 10   |

The cost-efficiency factor is further emphasized if a service provider deploys workloads on platforms like Google Cloud's [GKE Autopilot](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-overview).
GKE Autopilot is a fully managed platform that allows highly granular pricing based on Pods meaning that the customer does not have to pay for an entire cluster of VMs, but only for scheduled Pods on Kubernetes.
The requested resources like CPU, memory and disk are billed on a per-second basis, which benefits the key properties of threshold based scaling. That is capable of adjust resource requests in small portions, but still able to scale rapidly based on the actual conditions.
At the time of writing GKE Autopilot does not support sophisticated elasticity strategies. Polaris Cloud SLO would be a great extension to the platform to support various strategies based on the requirements of service providers.
In the following example, we show that there can be a significant difference between resource requests for the exact same load. The horizontal scaling requests 2 cores at the early stages of the test run. In contrast to that, the threshold strategy only reaches this value at the end of the test period.
This can result in vastly different costs in the long term, while the service provider can still comply with its SLOs.

![threshold_horizontal_cost.png](threshold_horizontal_cost.png)
