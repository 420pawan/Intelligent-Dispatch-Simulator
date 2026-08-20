# 🚚 Intelligent Dispatch Simulator

An interactive simulation platform for evaluating and comparing food-delivery rider dispatch strategies under different demand conditions.

The simulator models restaurants, customers, riders, order preparation, rider movement, pickups, deliveries, and rider availability over time. It provides multiple dispatch strategies and an interactive Streamlit dashboard for analyzing operational performance.

## 🌐 Live Demo

**[Launch Intelligent Dispatch Simulator](https://intelligent-dispatch-simulator-dsvehae7mft3zgckzfcik2.streamlit.app/)**

---

## 📌 Project Overview

Last-mile delivery platforms continuously need to match available riders with incoming orders.

A simple nearest-rider strategy can work well when demand is low, but as rider capacity becomes constrained, inefficient assignments can increase pickup delays, delivery times, and unfinished orders.

This project simulates that environment and compares three different dispatch strategies:

* **Nearest Rider Dispatch** — assigns the closest available rider.
* **Priority Dispatch** — prioritizes orders based on their waiting/ready time.
* **Hungarian Dispatch** — performs global rider-order matching using the Hungarian optimization algorithm.

The objective is to understand how dispatch policies affect delivery performance as system demand changes.

---

## ✨ Features

* Discrete-time delivery simulation
* Configurable number of riders and restaurants
* Configurable simulation duration
* Low, Normal, and Peak demand scenarios
* Randomized restaurants, customers, riders, and orders
* Complete order lifecycle tracking
* Rider movement simulation
* Rider busy/idle tracking
* Multiple interchangeable dispatch strategies
* Multi-seed benchmarking
* Mean and standard deviation reporting
* Interactive Streamlit dashboard
* Plotly-based performance visualizations
* Algorithm comparison
* Strategy recommendation based on completion performance

---

## 🧠 Dispatch Strategies

### 1. Nearest Rider

A greedy baseline that assigns the closest currently available rider to each ready order.

**Advantages**

* Simple
* Fast
* Easy to interpret

**Limitation**

It makes decisions independently and does not consider the overall assignment of all available riders and orders.

---

### 2. Priority Dispatch

Ready orders are prioritized according to their waiting/ready time before assigning riders.

This strategy investigates whether serving older orders first can improve overall delivery performance.

---

### 3. Hungarian Dispatch

The Hungarian algorithm solves the rider-order assignment as a global matching problem.

Instead of independently selecting the closest rider for every order, it evaluates the assignment problem across multiple riders and orders simultaneously.

This can become particularly useful when rider availability is limited and demand is high.

---

## 🔄 Simulation Flow

```text
Generate Orders
      ↓
Order Preparation
      ↓
Orders Become READY
      ↓
Dispatch Strategy
      ↓
Assign Available Riders
      ↓
Rider → Restaurant
      ↓
Order Pickup
      ↓
Restaurant → Customer
      ↓
Order Delivered
      ↓
Record Metrics
      ↓
Advance Simulation
```

---

## 📊 Performance Metrics

The simulator tracks several operational metrics:

| Metric                   | Description                                           |
| ------------------------ | ----------------------------------------------------- |
| Completion Rate          | Percentage of generated orders successfully delivered |
| Average Pickup Delay     | Average waiting time before an order is picked up     |
| Average Delivery Time    | Time associated with delivery                         |
| Average Total Order Time | Total order lifecycle duration                        |
| Rider Utilization        | Percentage of simulation time riders remain busy      |
| Busy Riders              | Number of riders currently handling orders            |
| Available Riders         | Number of idle riders                                 |
| Order Status             | Distribution across order lifecycle states            |

---

## 🧪 Experimental Analysis

The simulator supports reproducible experiments using multiple random seeds.

Example benchmark configuration:

```text
Simulation Duration : 200 minutes
Restaurants         : 10
Riders              : 20
Random Seeds        : 10
Dispatch Strategies : 3
```

The same randomized environment can be evaluated using different dispatch strategies, allowing more consistent algorithm comparisons.

### Key Observation

The value of optimization changes with system load.

**Low demand**

Rider capacity is abundant, so the strategies tend to perform similarly.

**Normal demand**

Global assignment begins to provide a measurable improvement in completion rate and delivery latency.

**Peak demand**

The advantage of global rider-order optimization becomes much more significant because the system is operating close to rider capacity.

---

## 🏗️ Project Architecture

```text
Intelligent-Dispatch-Simulator/
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
├── dashboard.py
├── app.py
├── requirements.txt
└── README.md
```

The architecture separates the simulation engine from dispatch strategies, allowing different assignment algorithms to be evaluated without changing the core simulation.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Pandas**
* **NumPy**
* **Plotly**
* **SciPy**
* Object-Oriented Programming
* Algorithmic Optimization
* Simulation & Benchmarking

---

## 🚀 Run Locally

### Clone the repository

```bash
git clone https://github.com/420pawan/Intelligent-Dispatch-Simulator.git
cd Intelligent-Dispatch-Simulator
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Launch the dashboard

```bash
streamlit run dashboard.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 📈 Why This Project?

This project demonstrates practical applications of:

* Algorithm design
* Optimization
* Simulation modeling
* Object-oriented programming
* Data analysis
* Performance benchmarking
* Interactive data visualization

It also provides an example of how algorithmic decisions can affect real-world operational systems such as last-mile delivery.

---

## 🔮 Future Improvements

Potential extensions include:

* Real-world map integration
* Traffic-aware travel times
* Dynamic rider pricing
* Rider shift scheduling
* Order batching
* Reinforcement-learning-based dispatch
* Predictive demand forecasting
* Geographic heatmaps
* Real-time simulation controls
* Cost optimization alongside delivery performance

---

## 👨‍💻 Author

**Pawan Kumar Mishra**

GitHub: [@420pawan](https://github.com/420pawan)

---

## 🌐 Project Links

* **GitHub:** https://github.com/420pawan/Intelligent-Dispatch-Simulator
* **Live Demo:** https://intelligent-dispatch-simulator-dsvehae7mft3zgckzfcik2.streamlit.app/
