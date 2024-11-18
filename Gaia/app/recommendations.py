from flask import request, url_for
import matplotlib.pyplot as plt
import os
import json
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for plotting



# class Recommendations:
#     def __init__(self, survey_data):
#         self.survey_data = survey_data

#     def generate_recommendations(self):
#         recommendations = []

#         # Electricity usage recommendation
#         if self.survey_data["electricity_emissions"] > 900:
#             recommendations.append("Your electricity usage exceeds the average of 900 kWh per month. Consider reducing usage or switching to renewable energy if available.")
#             recommendations.append("Visit the [EPA Green Power Locator](https://www.epa.gov/greenpower/green-power-locator) to see if your utility company offers a renewable energy opt-in program.")
#             self.graph_electricity_usage()

#         # Energy source recommendation
#         if self.survey_data.get("energy_source") not in ["hydropower", "renewable", "nuclear"]:
#             recommendations.append("Consider switching to a renewable energy source to reduce your carbon footprint. Check out this [resource on buying clean electricity](https://www.energy.gov/energysaver/buying-clean-electricity).")

#         # Driving distance recommendation
#         if self.survey_data["car_emissions"] > 217:
#             recommendations.append("You drive more than the average 217 miles per week. Consider carpooling or using public transit.")
#             self.graph_driving_distance()

#         # Short flights recommendation
#         short_flights = self.survey_data.get("short_flights", 0)
#         if short_flights > 1:
#         # if self.survey_data.get["short_flights"] > 0:
#             recommendations.append("Try to limit short flights and consider alternative transportation like trains or buses.")
#             self.graph_flight_usage()

#         # Long flights recommendation
#         long_flights = self.survey_data.get("long_flights", 0)
#         if long_flights > 1:
#         # if self.survey_data["long_flights"] > 0:
#             recommendations.append(
#                 "Long-haul flights emit significant CO₂. For example, a flight of 4,000 km (about 2,485 miles) can produce between 600 to 1,000 kg of CO₂ per passenger. "
#                 "Consider alternatives or offsetting your carbon footprint when flying."
#             )

#         # Diet recommendation
#         self.survey_data["diet"] = request.form.get("diet", "average omnivore")
#         if self.survey_data["diet"] == "average omnivore":
#             recommendations.append(
#                 "Switching from a meat-heavy diet to a more plant-based one can reduce your carbon footprint. Beef production emits 20 times more greenhouse gases than chicken per gram of protein. "
#                 "Consider diversifying your diet or opting for more chicken and plant-based proteins."
#             )

#         # Recycling recommendation
#         self.survey_data["recycles"] = request.form.get("recycles", "no")
#         if self.survey_data.get("recycles", "no") == "no":
#             recommendations.append(
#                 "Recycling helps reduce waste and prevent plastic pollution. Globally, only about 9% of plastic waste is recycled, leaving millions of tons to pollute our land and oceans. "
#                 "Consider improving your recycling habits to help reduce plastic waste."
#             )

#         return recommendations

#     def graph_electricity_usage(self):
#         user_kwh = self.survey_data.get("electricity_emissions", 0)
#         avg_american = 900
#         avg_global = 300  # Approximate global average for context

#         # plt.figure()
#         plt.bar(['Your Usage', 'Average American', 'Global Average'], [user_kwh, avg_american, avg_global])
#         plt.title("Electricity Usage Comparison (kWh per month)")
#         plt.xlabel("Comparison")
#         plt.ylabel("kWh per month")
        
#         chart_path = os.path.join('static', 'electricity_usage.png')
#         plt.savefig(chart_path)
#         plt.close()
#         return url_for('static', filename='electricity_usage.png')

#     def graph_driving_distance(self):
#         user_miles = self.survey_data.get("car_emissions", 0)
#         avg_american = 217  # Average weekly miles for Americans

#         # plt.figure()
#         plt.bar(['Your Mileage', 'Average American'], [user_miles, avg_american])
#         plt.title("Weekly Driving Distance Comparison")
#         plt.xlabel("Comparison")
#         plt.ylabel("Miles per week")

#     def graph_flight_usage(self):
#         user_short_flights = self.survey_data.get("short_flights", 0)
#         avg_american_short = 1  # Average short flights per year

#         plt.figure()
#         plt.bar(['Your Short Flights', 'Average American'], [user_short_flights, avg_american_short])
#         plt.title("Annual Short Flights Comparison")
#         plt.xlabel("Comparison")
#         plt.ylabel("Number of Short Flights (under 3 hours)")

# Usage example for Flask view
# survey_data = session.get('survey_data')
# recommendations = Recommendations(survey_data).generate_recommendations()
# for rec in recommendations:
#     print(rec)

##################################################
# class Recommendations:
#     def __init__(self, survey_data):
#         self.survey_data = survey_data

#     def generate_recommendations(self):
#         recommendations = {
#             "electricity_usage": [],
#             "car_emissions": [],
#             "short_flights": [],
#             "energy_source": [],
#         }

#         # Electricity Usage Recommendations
#         electricity_emissions = self.survey_data.get("electricity_emissions", 0)
#         if electricity_emissions > 900:
#             recommendations["electricity_usage"].append(
#                 "Your electricity usage exceeds the average of 900 kWh per month. Consider reducing usage or switching to renewable energy if available."
#             )
#         else:
#             recommendations["electricity_usage"].append(
#                 "Your electricity usage is within the recommended range. Keep up the good work!"
#             )

#         # Car Emissions Recommendations
#         car_emissions = self.survey_data.get("car_emissions", 0)
#         if car_emissions > 217:
#             recommendations["car_emissions"].append(
#                 "You drive more than the average 217 miles per week. Consider carpooling, using public transit, or switching to an electric vehicle."
#             )
#         else:
#             recommendations["car_emissions"].append(
#                 "Your car emissions are within the recommended range. Well done!"
#             )

#         # Short Flights Recommendations
#         short_flights = self.survey_data.get("short_flights", 0)
#         if short_flights > 1:
#             recommendations["short_flights"].append(
#                 "Consider reducing short flights. Alternative transportation like trains or buses can help lower your carbon footprint."
#             )
#         else:
#             recommendations["short_flights"].append(
#                 "You are taking few or no short flights, which is excellent for reducing emissions!"
#             )

#         # Energy Source Recommendations
#         energy_source = self.survey_data.get("energy_source", "")
#         if energy_source not in ["hydropower", "renewable", "nuclear"]:
#             recommendations["energy_source"].append(
#                 "Switching to clean energy sources like renewable, hydropower, or nuclear can significantly reduce your carbon footprint."
#             )
#         else:
#             recommendations["energy_source"].append(
#                 "Your energy source is clean. Keep supporting renewable energy!"
#             )

#         return recommendations

#######################################################
class Recommendations:
    def __init__(self, responses):
        self.responses = responses

    def generate_recommendations(self):
        recommendations = []
        self.generate_visualizations()

        return recommendations


    def generate_visualizations(self):
        # Plot 1: Electricity Usage
        plt.figure(figsize=(14, 10))
        categories = ["Your Usage", "Recommended Maximum"]
        values = [self.responses.get("electricity_kwh",0), 900]
        plt.bar(categories, values, color=["blue", "green"])
        plt.title("Electricity Usage Comparison (kWh/month)", fontsize=18)
        plt.ylabel("kWh", fontsize=14)
        plt.savefig("static/electricity_usage.png")
        plt.close()

        # Plot 2: Energy Source (Binary Comparison)
        energy_sources = ["Your Energy Source", "Ideal Energy Source"]
        values = [1 if self.responses.get("energy_source", "").lower() not in ["hydropower", "renewable", "nuclear"] else 0.66, 1]
        plt.figure(figsize=(14, 10))
        plt.bar(energy_sources, values, color=["red", "green"])
        plt.title("Energy Source Comparison", fontsize=18)
        plt.ylabel("Compliance Score", fontsize=14)
        plt.savefig("static/energy_source.png")
        plt.close()

        # Plot 3: Car Emissions
        plt.figure(figsize=(14, 10))
        categories = ["Your Weekly Driving", "Recommended Maximum"]
        values = [self.responses.get("car_miles",0), 217]
        plt.bar(categories, values, color=["blue", "green"])
        plt.title("Weekly Car Emissions (Miles)", fontsize=18)
        plt.ylabel("Miles", fontsize=14)
        plt.savefig("static/car_emissions.png")
        plt.close()

        # Plot 4: Short Flights
        plt.figure(figsize=(14, 10))
        categories = ["Your Short Flights", "Recommended Maximum"]
        values = [self.responses.get("short_flights", 0), 1]
        plt.bar(categories, values, color=["blue", "green"])
        plt.title("Short Flights Taken", fontsize=18)
        plt.ylabel("Count", fontsize=14)
        plt.savefig("static/short_flights.png")
        plt.close()

        # Plot 5: Long Flights
        plt.figure(figsize=(14, 10))
        categories = ["Your Long Flights", "Recommended Maximum"]
        values = [self.responses.get("long_flights", 0), 1]
        plt.bar(categories, values, color=["blue", "green"])
        plt.title("Long Flights Taken", fontsize=18)
        plt.ylabel("Count", fontsize=14)
        plt.savefig("static/long_flights.png")
        plt.close()

        # Plot 6: Diet Emissions (Binary Comparison)
        energy_sources = ["Your Diet", "Ideal Diet"]
        values = [1 if self.responses.get("diet", "").lower() in ["meat diet", "average omnivore"] else 0.66, 1]
        plt.figure(figsize=(14, 10))
        plt.bar(energy_sources, values, color=["red", "green"])
        plt.title("Diet Emissions Comparison", fontsize=18)
        plt.ylabel("Compliance Score", fontsize=14)
        plt.savefig("static/diet_emissions.png")
        plt.close()

        # Plot 7: Waste Emissions (Binary Comparison)
        energy_sources = ["Your Waste", "Ideal Waste"]
        values = [0.2 if self.responses.get("recycles", "").lower() == "no" else 0.16, 0.2]
        plt.figure(figsize=(14, 10))
        plt.bar(energy_sources, values, color=["red", "green"])
        plt.title("Waste Emissions Comparison", fontsize=18)
        plt.ylabel("Compliance Score", fontsize=14)
        plt.savefig("static/waste_emissions.png")
        plt.close()
