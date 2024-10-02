import streamlit as st
import numpy as np
import pickle

# Load the trained model
file = pickle.load(open("flightfare.pkl", "rb"))

# Function to get travel time based on source and destination
def get_travel_time(source, destination):
    travel_times = {
        ('Banglore', 'New Delhi'): 150,  # example in minutes
        ('Banglore', 'Cochin'): 90,
        ('Banglore', 'Kolkata'): 120,
        ('Banglore', 'Delhi'): 150,
        ('Banglore', 'Hyderabad'): 60,
        ('Kolkata', 'New Delhi'): 120,
        ('Delhi', 'Cochin'): 180,
        # Add more routes as necessary
    }
    return travel_times.get((source, destination), 120)  # default 120 minutes if route not found

# Define prediction function
def Flight_fare(input_data):
    # Changing input data into a numpy array
    input_data_as_numpy_Array = np.array(input_data, dtype=object)
    # Reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_Array.reshape(1, -1)
    prediction = file.predict(input_data_reshaped)
    return prediction

def main():
    ## Giving a title
    st.title('FLIGHT FARE PREDICTION')
    
    # Getting input data from the user
    st.text("**Choose your Flight**")

    try:
        # Airline selection
        airline = st.selectbox("Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
                                           'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
                                           'Vistara Premium economy', 'Jet Airways Business',
                                           'Multiple carriers Premium economy', 'Trujet'])

        # Date of Journey
        Date_of_Journey = st.date_input("Date Of Journey")
        Journey_day = Date_of_Journey.day
        Journey_month = Date_of_Journey.month

        # Source and Destination
        Source = st.selectbox("Source", ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai'])
        Destination = st.selectbox("Destination", ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad'])

        # Departure Time input
        Dep_Time = st.time_input("Departure Time")
        Dep_hour = Dep_Time.hour
        Dep_min = Dep_Time.minute

        # Total Stops
        Total_Stops = st.selectbox("Total Stops", (0, 1, 2, 3, 4))

        # Define Arrival Hour
        Arrival_hour = Dep_hour  # We can keep this to Dep_hour for simplicity

        # Get travel time based on Source and Destination
        travel_time = get_travel_time(Source, Destination)

        # Mapping inputs to required features for prediction (11 features)
        input_data = [
            Total_Stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,  # Keep Arrival Hour
            travel_time // 60,  # Add travel time in hours
            travel_time % 60,   # Add travel time in minutes
        ]

        # Map categorical features as single numbers
        airline_map = {'IndiGo': 0, 'Air India': 1, 'Jet Airways': 2, 'SpiceJet': 3,
                       'Multiple carriers': 4, 'GoAir': 5, 'Vistara': 6, 'Air Asia': 7,
                       'Vistara Premium economy': 8, 'Jet Airways Business': 9,
                       'Multiple carriers Premium economy': 10, 'Trujet': 11}
        source_map = {'Banglore': 0, 'Kolkata': 1, 'Delhi': 2, 'Chennai': 3, 'Mumbai': 4}
        destination_map = {'New Delhi': 0, 'Banglore': 1, 'Cochin': 2, 'Kolkata': 3, 'Delhi': 4, 'Hyderabad': 5}

        # Append the mapped categorical variables
        input_data.append(airline_map[airline])  # Airline
        input_data.append(source_map[Source])    # Source
        input_data.append(destination_map[Destination])  # Destination

        if st.button("Predict Fare"):
            # Ensure exactly 11 features are passed in
            if len(input_data) == 11:
                prediction = Flight_fare(input_data)
                output = round(prediction[0], 2)
                st.write(f"Predicted Flight Fare: ₹{output}")
            else:
                st.write(f"Error: The model expects 11 features, but {len(input_data)} were provided.")

    except Exception as e:
        st.text(f"Error: {e}")

if __name__ == "__main__":
    main()
