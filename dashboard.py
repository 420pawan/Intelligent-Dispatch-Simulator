import streamlit as st
import pandas as pd
import plotly.express as px

from simulator.city import City
from simulator.simulation import Simulation

from algorithms.nearest_dispatch import NearestDispatch
from algorithms.priority_dispatch import PriorityDispatch
from algorithms.hungarian_dispatch import HungarianDispatch

from experiments.experiments_runner import ExperimentRunner
from experiments.recommendation import Recommendation


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Intelligent Dispatch Simulator",
    page_icon="🚚",
    layout="wide"
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🚚 Intelligent Dispatch Simulator")

st.caption(
    "Simulate, benchmark, and compare food-delivery rider "
    "dispatch strategies under different demand conditions."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("⚙️ Simulation Settings")

mode = st.sidebar.radio(
    "Mode",
    [
        "Single Simulation",
        "Compare Strategies"
    ]
)


# Strategy selector only for single simulation
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

st.sidebar.divider()

run = st.sidebar.button(
    "🚀 Run Simulation",
    use_container_width=True
)


# =========================================================
# SINGLE SIMULATION
# =========================================================

if mode == "Single Simulation":

    if run:

        city = City(
            restaurants=restaurants,
            riders=riders
        )

        simulation = Simulation(
            city,
            demand_level=demand_level
        )


        # -------------------------------------------------
        # SELECT DISPATCH STRATEGY
        # -------------------------------------------------

        if strategy == "Nearest Rider":

            simulation.dispatcher = NearestDispatch()

        elif strategy == "Priority Queue":

            simulation.dispatcher = PriorityDispatch()

        else:

            simulation.dispatcher = HungarianDispatch()


        # -------------------------------------------------
        # RUN SIMULATION
        # -------------------------------------------------

        with st.spinner("Running simulation..."):

            simulation.run(duration)

        metrics = simulation.metrics.calculate(city)
        df = simulation.history.to_dataframe()


        st.success("Simulation completed successfully! 🎉")


        # -------------------------------------------------
        # SIMULATION SUMMARY
        # -------------------------------------------------

        st.header("📊 Simulation Summary")

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
            "Avg Delivery Time",
            f"{metrics['avg_total']:.2f} min"
        )


        st.divider()


        # -------------------------------------------------
        # ORDER STATUS
        # -------------------------------------------------

        st.subheader("📦 Current Order Status")

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Waiting",
            metrics["waiting"]
        )

        c2.metric(
            "Ready",
            metrics["ready"]
        )

        c3.metric(
            "Assigned",
            metrics["assigned"]
        )

        c4.metric(
            "Picked Up",
            metrics["picked"]
        )

        c5.metric(
            "Delivered",
            metrics["delivered"]
        )


        st.divider()


        # -------------------------------------------------
        # DELIVERY METRICS
        # -------------------------------------------------

        st.subheader("⏱️ Delivery Metrics")

        c1, c2, c3, c4 = st.columns(4)

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

        c4.metric(
            "Rider Utilization",
            f"{metrics['avg_util']:.1f}%"
        )


        st.divider()


        # -------------------------------------------------
        # ORDER STATUS GRAPH
        # -------------------------------------------------

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
            title="Order Lifecycle During Simulation",
            labels={
                "time": "Simulation Time (minutes)",
                "value": "Number of Orders",
                "variable": "Order Status"
            }
        )

        fig.update_layout(
            legend_title_text="Order Status",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # -------------------------------------------------
        # RIDER AVAILABILITY
        # -------------------------------------------------

        st.subheader("🛵 Rider Availability")

        rider_df = df.set_index("time")[
            [
                "busy_riders",
                "available_riders"
            ]
        ]

        fig_riders = px.line(
            rider_df,
            x=rider_df.index,
            y=[
                "busy_riders",
                "available_riders"
            ],
            title="Rider Availability During Simulation",
            labels={
                "time": "Simulation Time (minutes)",
                "value": "Number of Riders",
                "variable": "Rider Status"
            }
        )

        fig_riders.update_layout(
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_riders,
            use_container_width=True
        )


        # -------------------------------------------------
        # SIMULATION HISTORY
        # -------------------------------------------------

        with st.expander("🔍 View Simulation History"):

            st.dataframe(
                df,
                use_container_width=True
            )


# =========================================================
# COMPARE STRATEGIES
# =========================================================

else:

    if run:

        st.header("🏆 Dispatch Strategy Comparison")

        st.info(
            f"Comparing dispatch strategies under **{demand_level} demand** "
            f"with {riders} riders and {restaurants} restaurants."
        )


        # -------------------------------------------------
        # RUN EXPERIMENTS
        # -------------------------------------------------

        with st.spinner(
            "Running benchmark experiments for all strategies..."
        ):

            runner = ExperimentRunner()

            results = runner.run(
                duration=duration,
                restaurants=restaurants,
                riders=riders,
                demand_level=demand_level
            )


        # -------------------------------------------------
        # RECOMMENDATION
        # -------------------------------------------------

        recommendation = Recommendation()

        best = recommendation.generate(results)


        st.success(
            f"🏆 Recommended Strategy: **{best['best_strategy']}**"
        )

        st.write(best["reason"])


        st.divider()


        # -------------------------------------------------
        # EXTRACT NUMERIC RESULTS
        # -------------------------------------------------

        comparison_data = []

        for result in results:

            comparison_data.append({

                "Strategy":
                    result.strategy_name,

                "Completion Rate":
                    result.metrics["completion_rate"],

                "Completion Rate Std":
                    result.metrics["completion_rate_std"],

                "Avg Total Time":
                    result.metrics["avg_total"],

                "Avg Total Time Std":
                    result.metrics["avg_total_std"],

                "Avg Pickup Delay":
                    result.metrics["avg_pickup"],

                "Avg Pickup Delay Std":
                    result.metrics["avg_pickup_std"],

                "Avg Utilization":
                    result.metrics["avg_util"],

                "Avg Utilization Std":
                    result.metrics["avg_util_std"]
            })


        comparison_df = pd.DataFrame(comparison_data)


        # -------------------------------------------------
        # TOP KPI CARDS
        # -------------------------------------------------

        best_completion = comparison_df.loc[
            comparison_df["Completion Rate"].idxmax()
        ]

        fastest_delivery = comparison_df.loc[
            comparison_df["Avg Total Time"].idxmin()
        ]

        lowest_pickup = comparison_df.loc[
            comparison_df["Avg Pickup Delay"].idxmin()
        ]

        highest_utilization = comparison_df.loc[
            comparison_df["Avg Utilization"].idxmax()
        ]


        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "🏆 Best Completion",
            best_completion["Strategy"],
            f"{best_completion['Completion Rate']:.2f}%"
        )

        c2.metric(
            "⚡ Fastest Delivery",
            fastest_delivery["Strategy"],
            f"{fastest_delivery['Avg Total Time']:.2f} min"
        )

        c3.metric(
            "📦 Lowest Pickup Delay",
            lowest_pickup["Strategy"],
            f"{lowest_pickup['Avg Pickup Delay']:.2f} min"
        )

        c4.metric(
            "🛵 Highest Utilization",
            highest_utilization["Strategy"],
            f"{highest_utilization['Avg Utilization']:.2f}%"
        )


        st.divider()


        # -------------------------------------------------
        # COMPARISON TABLE
        # -------------------------------------------------

        st.subheader("📋 Benchmark Results")

        display_df = comparison_df.copy()

        display_df["Completion Rate"] = display_df.apply(
            lambda row:
            f"{row['Completion Rate']:.2f}% ± "
            f"{row['Completion Rate Std']:.2f}%",
            axis=1
        )

        display_df["Avg Total Time"] = display_df.apply(
            lambda row:
            f"{row['Avg Total Time']:.2f} ± "
            f"{row['Avg Total Time Std']:.2f} min",
            axis=1
        )

        display_df["Avg Pickup Delay"] = display_df.apply(
            lambda row:
            f"{row['Avg Pickup Delay']:.2f} ± "
            f"{row['Avg Pickup Delay Std']:.2f} min",
            axis=1
        )

        display_df["Avg Utilization"] = display_df.apply(
            lambda row:
            f"{row['Avg Utilization']:.2f} ± "
            f"{row['Avg Utilization Std']:.2f}%",
            axis=1
        )

        display_df = display_df[
            [
                "Strategy",
                "Completion Rate",
                "Avg Total Time",
                "Avg Pickup Delay",
                "Avg Utilization"
            ]
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # =================================================
        # VISUAL COMPARISON
        # =================================================

        st.subheader("📊 Performance Comparison")


        tab1, tab2, tab3 = st.tabs(
            [
                "Completion Rate",
                "Delivery Time",
                "Rider Utilization"
            ]
        )


        # -------------------------------------------------
        # COMPLETION RATE
        # -------------------------------------------------

        with tab1:

            fig_completion = px.bar(
                comparison_df,
                x="Strategy",
                y="Completion Rate",
                error_y="Completion Rate Std",
                text="Completion Rate",
                title="Completion Rate by Dispatch Strategy",
                labels={
                    "Completion Rate": "Completion Rate (%)"
                }
            )

            fig_completion.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside"
            )

            fig_completion.update_layout(
                yaxis_title="Completion Rate (%)",
                xaxis_title="Dispatch Strategy"
            )

            st.plotly_chart(
                fig_completion,
                use_container_width=True
            )


        # -------------------------------------------------
        # DELIVERY TIME
        # -------------------------------------------------

        with tab2:

            fig_delivery = px.bar(
                comparison_df,
                x="Strategy",
                y="Avg Total Time",
                error_y="Avg Total Time Std",
                text="Avg Total Time",
                title="Average Delivery Time by Strategy",
                labels={
                    "Avg Total Time":
                    "Average Delivery Time (minutes)"
                }
            )

            fig_delivery.update_traces(
                texttemplate="%{text:.2f} min",
                textposition="outside"
            )

            fig_delivery.update_layout(
                yaxis_title="Average Delivery Time (minutes)",
                xaxis_title="Dispatch Strategy"
            )

            st.plotly_chart(
                fig_delivery,
                use_container_width=True
            )


        # -------------------------------------------------
        # RIDER UTILIZATION
        # -------------------------------------------------

        with tab3:

            fig_utilization = px.bar(
                comparison_df,
                x="Strategy",
                y="Avg Utilization",
                error_y="Avg Utilization Std",
                text="Avg Utilization",
                title="Average Rider Utilization",
                labels={
                    "Avg Utilization":
                    "Rider Utilization (%)"
                }
            )

            fig_utilization.update_traces(
                texttemplate="%{text:.2f}%",
                textposition="outside"
            )

            fig_utilization.update_layout(
                yaxis_title="Rider Utilization (%)",
                xaxis_title="Dispatch Strategy"
            )

            st.plotly_chart(
                fig_utilization,
                use_container_width=True
            )


        st.divider()


        # -------------------------------------------------
        # INTERPRETATION
        # -------------------------------------------------

        st.subheader("💡 Performance Interpretation")

        st.write(
            f"""
            Under **{demand_level} demand**, the **{best['best_strategy']}**
            strategy is recommended based on the simulator's evaluation.

            The comparison considers multiple operational indicators,
            including completion rate, delivery time, pickup delay,
            and rider utilization.

            The error bars in the charts represent the standard deviation
            across the benchmark runs, providing an indication of result
            variability.
            """
        )


        # -------------------------------------------------
        # RAW DATA
        # -------------------------------------------------

        with st.expander("🔍 View Raw Benchmark Data"):

            st.dataframe(
                comparison_df,
                use_container_width=True,
                hide_index=True
            )

    else:

        st.header("🏆 Compare Dispatch Strategies")

        st.markdown(
            """
            Configure the simulation parameters from the sidebar and
            click **Run Simulation** to benchmark all dispatch strategies.

            The comparison evaluates:

            - 📈 Completion Rate
            - ⏱️ Average Delivery Time
            - 📦 Pickup Delay
            - 🛵 Rider Utilization
            - 📊 Result Variability
            """
        )