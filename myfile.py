import streamlit as st 
import pandas as pd

LIST_OF_CITIES = ["Zurich", "Bern", "Basel", "Geneva", "Lausanne", "Lugano", "Lucerne", "St. Gallen"]

st.set_page_config(layout="wide")

st.title("Tram Heating Costs Savings Calculator")

# Take inputs : - Length, width, height (in m)
# Average operation from [time] to [time] (in hours, minutes)
# Average tram count in operation
# Average instantaneous passenger number per tram
# Average fresh air supply via ventilation (in m³/h)
# Average fresh air supply from door openings (in m³/h)
# Average convection coefficient (in kW/(m²K) )
# Button "Load VBZ values for Cobra tram" (or something)* """

# Defaults will be set to VBZ Cobra tram values

#region Specifications

"""## Specifications:"""

if "reset" not in st.session_state:
    st.session_state.reset = False

with st.container():

    default_values = {
    "Length (m)": 30,
    "Width (m)": 2.2,
    "Height (m)": 2.5,
    "Average hours of Operation per tram:": 10,
    "Tram count": 10,
    "Average passenger count": 100,
    "Average fresh air supply via ventilation (m³/h)": 1000,
    "Average fresh air supply from door openings (m³/h)": 100,
    "Average convection coefficient (kW/(m²K))": 10,
    }
    
    length = st.number_input("Length (m)", key="length")
    width = st.number_input("Width (m)", key="width")
    height = st.number_input("Height (m)", key="height")
    operation = st.number_input("Average hours of Operation per tram: ", key="operation")
    tram_count = st.number_input("Tram count", key="tram_count")
    passenger_count = st.number_input("Average Passenger Count", key="passenger_count")
    ventilation = st.number_input("Average fresh air supply via ventilation (m³/h)", key="ventilation")
    door_openings = st.number_input("Average fresh air supply from door openings (m³/h)", key="door_openings")
    convection = st.number_input("Average convection coefficient (kW/(m²K))", key="convection")

def deafults ():
    st.session_state["length"] = default_values["Length (m)"]
    st.session_state["width"] = default_values["Width (m)"]
    st.session_state["height"] = default_values["Height (m)"]
    st.session_state["operation"] = default_values["Average hours of Operation per tram:"]
    st.session_state["tram_count"] = default_values["Tram count"]
    st.session_state["passenger_count"] = default_values["Average passenger count"]
    st.session_state["ventilation"] = default_values["Average fresh air supply via ventilation (m³/h)"]
    st.session_state["door_openings"] = default_values["Average fresh air supply from door openings (m³/h)"]
    st.session_state["convection"] = default_values["Average convection coefficient (kW/(m²K))"]

def reset():
    st.session_state['length'] = 0
    st.session_state['width'] = 0
    st.session_state['height'] = 0
    st.session_state['operation'] = 0
    st.session_state['tram_count'] = 0
    st.session_state['passenger_count'] = 0
    st.session_state['ventilation'] = 0
    st.session_state['door_openings'] = 0
    st.session_state['convection'] = 0

col1,col2,col3,col4 = st.columns(4)

col1.button("Reset Values", on_click=reset, key="reset_specs")
col2.button("Cobra Tram Defaults", on_click=deafults, key="cobra_defaults")

#endregion

# region operating condition

st.markdown("## Operating Conditions:")

# Get operating conditions

location = st.selectbox('Select City', LIST_OF_CITIES)
begin_day = st.number_input("Day of starting operation", min_value=1, value=1, key="begin_day")
end_day = st.number_input("Day of ending operation", min_value=1, value=1, key="end_day")
begin_hour = st.number_input("Hour of starting operation", min_value=0, value=0, key="begin_hour")
end_hour = st.number_input("Hour of ending operation", min_value=0, value=0, key="end_hour")

#endregion

#region: Heater Inputs

st.markdown(" ## Heating:")

user_inputs = []

def heater_options(i):

    st.write(f"Heater {i + 1}")

    # Dropdown to select type of heater
    heater_type = st.selectbox(f"Select Heater Type {i+1}", ["Heat Pump", "Resistance"], key = f"heatertype{i+1}")

    # Maximum thermal power (input field)
    max_thermal_power = st.number_input("Maximum Thermal Power (kW):", min_value=0.1, value=1.0, format="%.1f", key = "maxthermalpower" + str(i + 1))

    if heater_type == "Heat Pump":
        # Input field for average COP
        cop = st.number_input("Average COP:", min_value=1.0, value=3.0, format="%.2f", key = i + 1)
    else:
        cop = "Not Applicable"

    user_inputs.append({
        "Heater Type": heater_type,
        "Maximum Thermal Power (kW)": max_thermal_power,
        "Average COP": cop,
    })


if 'heaters' not in st.session_state:
    st.session_state['heaters'] = 0

def add_heater_option():
    st.session_state['heaters'] += 1

def reset_heaters():
    st.session_state['heaters'] = 0

if 'heaters' in st.session_state:
    for i in range(st.session_state['heaters']):
        heater_options(i)

st.button("Add Heater", on_click=add_heater_option, key="add_heater")

# Create a button to reset the input section
reset_button = st.button("Remove Heaters", on_click=reset_heaters, key="reset_heaters")

# Print the user inputs
df = pd.DataFrame(user_inputs)
# if dataframe is not empty
if not df.empty:
    df.set_index("Heater Type", inplace=True)
    st.dataframe(df)
else:
    st.write("No heaters added yet.")

#endregion

#region: Temperature Inputs

st.markdown(" ## Temperature Settings:")

temp_inputs = []

if 'temp_inputs' not in st.session_state:
    st.session_state['temp_inputs'] = 0

def temp_options(i):
    
        st.write(f"Set point temperature {i + 1}")
    
        # Maximum thermal power (input field)
        temp_value = st.number_input("Set Point Temperature (°C):", min_value=5.0, max_value=30.0, format="%.1f", key = "temp_value" + str(i + 1))
    
        temp_inputs.append({
            "Set Point Temperature (°C)": temp_value,
        })

def add_temp_option():
    st.session_state['temp_inputs'] += 1


def reset_temp():
    st.session_state['temp_inputs'] = 0

if 'temp_inputs' in st.session_state:
    for i in range(st.session_state['temp_inputs']):
        temp_options(i)

st.button("Add Temperature Setting", on_click=add_temp_option, key="add_temp")
st.button("Reset Temperature Settings", on_click=reset_temp, key="reset_temp")

#endregion

#region Electricity Costs

st.markdown("## Input Costs:")

# Get cost of electricity
cost_electricity = st.number_input("Cost of electricity (CHF/kWh):", min_value=0.01, value=0.2, format="%.2f", key = "cost_electricity")

#endregion

# Button which executes Python function to calculate and display results

def calculate_results(user_inputs, temp_inputs, cost_electricity):
    return "Results"

if st.button("Calculate", key="calculate"):
    results = calculate_results(user_inputs, temp_inputs, cost_electricity)
    st.write(results)
