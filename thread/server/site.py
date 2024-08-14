import streamlit as st
import pandas as pd
from os import listdir

DATA = st.selectbox("Client",  listdir("data/") )
DATA_PATH = f"data/{DATA}"
@st.fragment(run_every=3)
def main():
    # preset

    N = 0
    with open(DATA_PATH, "r") as f:
        N = len(f.readline().split(","))
    head = ["time","cpumean"] + [f"cpu{i}" for i in range(N-3)] +  ["mem"]
    def get_data():
        return pd.read_csv(DATA_PATH, names =head, index_col=False) 
    data = get_data()
    data["time"] = pd.to_datetime(data["time"])
    def process_date(date):
        return date.strftime("%H:%M %Ss")

    data["tt"] = [process_date(i) for i in data["time"]]
    # showing

    st.write("""
    # Client Measure
    """
    )
    col1, col2 = st.columns(2)
    with col1:
        delta = data["cpumean"].iloc[-1] - data["cpumean"].iloc[-2]
        value = data["cpumean"].iloc[-1]
        st.metric(label="CPU", value=f"{value:.1f}%", delta=f"{delta:.1f}%")

    with col2:
        delta = data["mem"].iloc[-1] - data["mem"].iloc[-2]
        value = data["mem"].iloc[-1]
        st.metric(label="Memory", value=f"{value:.1f}%", delta=f"{delta:.1f}%")


    st.divider()
    st.write("# Memory")
    st.area_chart(data,
                 x="tt",
                 y="mem",
                 x_label="Time",
                 y_label="Memory%")

    st.divider()
    st.write("# CPU")
    st.line_chart(data,
                 x="tt",
                 y=["cpumean"]+[f"cpu{i}" for i in range(N-3)],
                 x_label="Time",
                 y_label="CPU%")
main()
