import streamlit as st
import plotly.express as px

from simulator.city import City
from simulator.simulation import Simulation

from algorithms.nearest_dispatch import NearestDispatch
from algorithms.priority_dispatch import PriorityDispatch
from algorithms.hungarian_dispatch import HungarianDispatch

from experiments.experiments_runner import ExperimentRunner
from experiments.recommendation import Recommendation

st.set_page_config(
    page_title="Food Order Dispatch Simulator",
    page_icon="🚚",
    layout="wide"
)

st.title("Food Order Dispatch Simulator")

st.sidebar.header("Simulation Settings")

mode = st.sidebar.radio(
    "Mode",
    [
        "Single Simulation",
        "Compare Strategies"
    ]
)

if mode == "Single Simulation":

    strategy = st.sidebar.selectbox(
        "Dispatch Strategy",
        [
            "Nearest Rider",
            "Priority Queue",
            "Hungarian"
        ]
    )

duration = st.sidebar.slider(
    "Simulation Duration (minutes)",
    30,
    300,
    100,
    10
)

restaurants = st.sidebar.slider(
    "Restaurants",
    5,
    30,
    10
)

riders = st.sidebar.slider(
    "Riders",
    5,
    40,
    20
)

demand_level = st.sidebar.selectbox(
    "Demand Level",
    [
        "Low",
        "Normal",
        "Peak"
    ],
    index=1
)

run = st.sidebar.button("Run Simulation")

if run:

    if mode == "Single Simulation":

        city = City(
            restaurants=restaurants,
            riders=riders
        )

        simulation = Simulation(city,demand_level=demand_level)

        if strategy == "Nearest Rider":
            simulation.dispatcher = NearestDispatch()

        elif strategy == "Priority Queue":
            simulation.dispatcher = PriorityDispatch()

        else:
            simulation.dispatcher = HungarianDispatch()

        simulation.run(duration)

        metrics = simulation.metrics.calculate(city)
        df = simulation.history.to_dataframe()

        st.success("Simulation Complete!")

        st.header("Simulation Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Delivered Orders",
            metrics["delivered"]
        )

        c2.metric(
            "Completion Rate",
            f"{metrics['completion_rate']:.1f}%"
        )

        c3.metric(
            "Busy Riders",
            metrics["busy"]
        )

        c4.metric(
            "Average Delivery Time",
            f"{metrics['avg_total']:.2f} min"
        )

        st.divider()

        st.subheader("Current Order Status")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("Waiting", metrics["waiting"])
        c2.metric("Ready", metrics["ready"])
        c3.metric("Assigned", metrics["assigned"])
        c4.metric("Picked Up", metrics["picked"])
        c5.metric("Delivered", metrics["delivered"])

        st.divider()

        st.subheader("Delivery Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Preparation Time",
            f"{metrics['avg_prep']:.2f} min"
        )

        c2.metric(
            "Pickup Delay",
            f"{metrics['avg_pickup']:.2f} min"
        )

        c3.metric(
            "Total Delivery Time",
            f"{metrics['avg_total']:.2f} min"
        )

        st.metric(
            "Average Rider Utilization",
            f"{metrics['avg_util']:.1f}%"
        )

        st.subheader("📈 Order Status Over Time")

        fig = px.line(
        df,
        x="time",
        y=[
            "waiting",
            "ready",
            "assigned",
            "picked",
            "delivered"
        ],
        title="Order Status Over Time"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("🛵 Rider Availability")

        st.line_chart(
            df.set_index("time")[
                [
                    "busy_riders",
                    "available_riders"
                ]
            ]
        )

        with st.expander("Simulation History"):
            st.dataframe(df)

    else:

        runner = ExperimentRunner()

        results = runner.run(
            duration=duration,
            restaurants=restaurants,
            riders=riders,
            demand_level=demand_level
        )

        recommendation = Recommendation()

        best = recommendation.generate(results)

        rows = []

        for result in results:

            rows.append({

                "Strategy": result.strategy_name,

                "Completion Rate":
                    f"{result.metrics['completion_rate']:.2f} ± "
                    f"{result.metrics['completion_rate_std']:.2f}%",

                "Avg Total Time":
                    f"{result.metrics['avg_total']:.2f} ± "
                    f"{result.metrics['avg_total_std']:.2f} min",

                "Avg Pickup Delay":
                    f"{result.metrics['avg_pickup']:.2f} ± "
                    f"{result.metrics['avg_pickup_std']:.2f} min",

                "Avg Utilization":
                    f"{result.metrics['avg_util']:.2f} ± "
                    f"{result.metrics['avg_util_std']:.2f}%"
            })

        st.header("Strategy Comparison")

        st.table(rows)

        st.divider()

        st.subheader("Recommendation")

        st.success(
            f"Recommended Strategy : {best['best_strategy']}"
        )

        st.write(best["reason"])

