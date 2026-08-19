# Food Order Dispatch Simulator

A discrete-time delivery dispatch simulator for evaluating and comparing rider-order assignment strategies under different demand conditions.

The simulator models restaurants, customers, riders, order preparation, rider movement, pickups, and deliveries over time. It supports multiple dispatch algorithms and provides reproducible multi-seed experiments to analyze how different strategies perform as rider capacity becomes constrained.

## Motivation

Last-mile delivery platforms need to continuously assign available riders to ready orders. A simple greedy assignment may work well when rider capacity is abundant, but under higher demand, poor assignments can increase pickup delays, delivery times, and order backlog.

This project simulates that dispatch problem and compares three strategies:

- **Nearest Rider Dispatch** - greedily assigns the nearest available rider to each ready order.
- **Priority Dispatch** - prioritizes orders based on their ready time before assigning nearby riders.
- **Hungarian Dispatch** - performs global rider-order matching using the Hungarian assignment algorithm to minimize assignment cost.

The goal is to study how dispatch strategy affects delivery performance under varying levels of system load.

---

## Features

- Discrete-time delivery simulation
- Random restaurant, customer, and rider locations
- Configurable number of restaurants and riders
- Configurable simulation duration
- Low, Normal, and Peak demand scenarios
- Rider movement from current location -> restaurant -> customer
- Order lifecycle tracking:
  - Waiting
  - Ready
  - Assigned
  - Picked Up
  - Delivered
- Rider busy/idle time tracking
- Multiple interchangeable dispatch strategies
- Multi-seed reproducible benchmarking
- Mean and standard deviation reporting
- Strategy recommendation based on simulation performance
- Interactive Streamlit dashboard
- Historical order-status and rider-availability visualization

---

## Dashboard

The Streamlit dashboard supports two modes:

### 1. Single Simulation

<img width="1853" height="841" alt="image" src="https://github.com/user-attachments/assets/4ec636a7-c3e4-46c5-b51d-a57599c17617" />

<img width="1515" height="928" alt="image" src="https://github.com/user-attachments/assets/d219b9d0-497d-4103-a7a3-666b5069bc12" />

<img width="1476" height="554" alt="image" src="https://github.com/user-attachments/assets/0e59190e-f7c7-4b76-a34e-9ed46ac36560" />

Run an individual strategy and inspect:

- simulation summary
- order status
- delivery metrics
- rider utilization
- order-status evolution over time
- rider availability over time

### 2. Compare Strategies

<img width="1845" height="574" alt="image" src="https://github.com/user-attachments/assets/ee4352bf-7100-4185-8a8c-5f2c1496b250" />


Run reproducible multi-seed experiments across all dispatch strategies and compare their aggregated performance.

The dashboard also recommends the strategy achieving the highest completion rate.

--- 

## Architecture

The project separates the simulation engine from the dispatch algorithms.

```text
DispatchSimulator/
│
├── algorithms/
│   ├── dispatch_strategy.py
│   ├── nearest_dispatch.py
│   ├── priority_dispatch.py
│   └── hungarian_dispatch.py
│
├── simulator/
│   ├── city.py
│   ├── simulation.py
│   ├── order.py
│   ├── rider.py
│   ├── restaurant.py
│   ├── customer.py
│   └── status.py
│
├── metrics/
│   ├── metrics.py
│   └── history.py
│
├── experiments/
│   ├── experiments_runner.py
│   ├── experiment_result.py
│   └── recommendation.py
│
├── utils/
│   └── distance.py
│
└── dashboard.py
```

Dispatch algorithms implement a common strategy interface, allowing the simulation engine to switch between assignment policies without changing the core simulation logic.

---

## Simulation Flow

At each simulation step:

1. New orders are generated according to the selected demand level.
2. Orders whose preparation time has elapsed transition to `READY`.
3. The selected dispatch strategy assigns available riders to ready orders.
4. Assigned riders travel toward restaurants.
5. Riders pick up their assigned orders.
6. Riders travel toward customers.
7. Orders are marked as delivered.
8. Rider and order metrics are recorded.
9. The simulation advances by one minute.

This produces a complete time history of the delivery network.

---

## Dispatch Strategies

### 1. Nearest Rider Dispatch

For each ready order, the nearest currently available rider is selected.

This provides a simple greedy baseline with low decision complexity.

### 2. Priority Dispatch

Ready orders are sorted according to their waiting/ready time before rider assignment.

This tests whether prioritizing older orders improves system-wide delivery performance compared with the basic greedy strategy.

### 3. Hungarian Dispatch

The Hungarian algorithm considers multiple available riders and ready orders simultaneously and finds a globally optimized rider-order assignment.

Unlike greedy assignment, this strategy considers the overall matching cost rather than independently selecting the closest rider for each order.

---

## Metrics

The simulator tracks operational metrics including:

- Completion Rate
- Average Preparation Time
- Average Pickup Delay
- Average Delivery Time
- Average Total Order Time
- Rider Utilization
- Available/Busy Riders
- Orders in each lifecycle state

Rider utilization is calculated from each rider's actual busy and idle minutes during the simulation.

---

## Experimental Methodology

To avoid drawing conclusions from a single random simulation, strategy comparisons are performed across multiple random seeds.

The benchmark configuration used for the primary experiments was:

```text
Simulation Duration : 200 minutes
Restaurants         : 10
Riders              : 20
Seeds               : 10
Strategies          : 3
```

For each demand level:

```text
10 seeds × 3 strategies = 30 simulations
```

Across Low, Normal, and Peak demand:

```text
30 × 3 = 90 simulations
```

For every seed, each strategy receives the same randomized environment, allowing fair comparisons between dispatch policies.

Results are reported as:

```text
Mean ± Standard Deviation
```

---

## Experimental Results

### Low Demand

| Strategy | Completion Rate | Avg Total Time | Avg Pickup Delay | Avg Utilization |
|---|---:|---:|---:|---:|
| Nearest | **86.82 ± 2.94%** | 26.39 ± 2.05 min | 3.58 ± 0.95 min | 32.17 ± 3.33% |
| Priority | **86.82 ± 2.94%** | 26.39 ± 2.05 min | 3.58 ± 0.95 min | 32.17 ± 3.33% |
| Hungarian | 86.73 ± 2.81% | **26.36 ± 2.05 min** | **3.56 ± 0.94 min** | 32.11 ± 3.35% |

Under low demand, rider utilization is only around 32%, leaving substantial spare capacity. All three strategies therefore perform almost identically.

---

### Normal Demand

| Strategy | Completion Rate | Avg Total Time | Avg Pickup Delay | Avg Utilization |
|---|---:|---:|---:|---:|
| Nearest | 75.44 ± 5.31% | 37.22 ± 5.96 min | 7.22 ± 0.98 min | 86.79 ± 2.32% |
| Priority | 75.49 ± 5.18% | 37.45 ± 6.11 min | 7.23 ± 0.81 min | 86.78 ± 2.28% |
| **Hungarian** | **83.46 ± 2.80%** | **30.69 ± 3.66 min** | **5.29 ± 0.42 min** | 85.21 ± 2.88% |

Under normal demand, Hungarian matching improves completion rate while reducing both pickup delay and total order time.

Compared with Nearest Dispatch, Hungarian Dispatch achieved:

- **+8.02 percentage points** higher completion rate
- **17.5% lower** average total order time
- **26.7% lower** average pickup delay

---

### Peak Demand

| Strategy | Completion Rate | Avg Total Time | Avg Pickup Delay | Avg Utilization |
|---|---:|---:|---:|---:|
| Nearest | 31.28 ± 2.48% | 77.98 ± 4.34 min | 7.64 ± 0.89 min | 92.25 ± 0.54% |
| Priority | 31.30 ± 2.49% | 78.02 ± 4.84 min | 7.61 ± 0.82 min | 92.25 ± 0.54% |
| **Hungarian** | **44.09 ± 3.48%** | **58.73 ± 4.60 min** | **2.74 ± 0.54 min** | 92.25 ± 0.54% |

The difference becomes significantly larger under peak demand.

Compared with Nearest Dispatch, Hungarian Dispatch achieved:

- **+12.81 percentage points** higher completion rate
- approximately **41% relative improvement** in completion rate
- **24.7% lower** average total order time
- **64.1% lower** average pickup delay

All three strategies operate at approximately **92% rider utilization**, suggesting that Hungarian Dispatch improves performance through better allocation of existing rider capacity rather than increased resource usage.

---
## Statistical Interpretation

The reported standard deviations capture variation in performance across the 10 random seeds and help distinguish consistent improvements from differences that may simply result from simulation randomness.

Under **Low demand**, Nearest and Hungarian Dispatch achieve completion rates of **86.82 ± 2.94%** and **86.73 ± 2.81%**, respectively. The difference is only **0.09 percentage points**, which is negligible relative to the observed run-to-run variability. This indicates that the strategies are effectively indistinguishable under low system load.

Under **Normal demand**, Hungarian Dispatch improves mean completion rate from **75.44% to 83.46%**, a gain of **8.02 percentage points**. This gap is large relative to the observed standard deviations (**5.31% for Nearest and 2.80% for Hungarian**) and is accompanied by substantial reductions in both total delivery time and pickup delay. The improvement therefore appears robust across the tested random scenarios rather than being driven by a single favorable simulation.

Under **Peak demand**, the separation becomes even stronger. Hungarian Dispatch achieves **44.09 ± 3.48%** completion compared with **31.28 ± 2.48%** for Nearest Dispatch, a difference of **12.81 percentage points**. At the same time, pickup delay falls from **7.64 ± 0.89 min** to **2.74 ± 0.54 min** while rider utilization remains effectively identical at approximately **92.25%**.

These results suggest that the performance advantage of global rider-order matching becomes increasingly consistent and operationally significant as rider capacity becomes constrained.

--- 

## Key Findings

The experiments demonstrate that the value of sophisticated dispatch optimization depends strongly on system load.

**Low demand:**  
All strategies perform similarly because rider capacity is abundant.

**Normal demand:**  
Global rider-order optimization begins to provide meaningful improvements in completion rate and delivery latency.

**Peak demand:**  
Hungarian matching significantly outperforms greedy assignment while using essentially the same rider capacity.

A key observation is:

> **Global assignment optimization provides little benefit when rider capacity is abundant, but becomes increasingly valuable as resource contention increases.**

The experiments also show that Priority Dispatch performs very similarly to Nearest Dispatch across all three demand regimes. In this simulation, changing order priority alone provides little benefit compared with improving the rider-order matching itself.

---

## Tech Stack

- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- **SciPy** — Hungarian assignment optimization

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/Garuna-A/DispatchSimulator.git
cd DispatchSimulator
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run dashboard.py
```

---

## Conclusion

This project demonstrates how dispatch strategy affects the performance of a simulated last-mile delivery network.

The experiments show that simple greedy dispatch is sufficient when rider capacity is abundant, while globally optimized assignment becomes increasingly valuable as the network approaches saturation.

Across reproducible multi-seed experiments, Hungarian matching improved completion rate and reduced delivery delays under Normal and Peak demand without requiring additional rider capacity.
