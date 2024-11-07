import matplotlib.pyplot as plt

class Recommendations:
    def __init__(self, survey_data):
        self.survey_data = survey_data

    def generate_recommendations(self):
        recommendations = []

        # Electricity usage recommendation
        if self.survey_data["electricity_emissions"] > 900:
            recommendations.append("Your electricity usage exceeds the average of 900 kWh per month. Consider reducing usage or switching to renewable energy if available.")
            recommendations.append("Visit the [EPA Green Power Locator](https://www.epa.gov/greenpower/green-power-locator) to see if your utility company offers a renewable energy opt-in program.")
            self.graph_electricity_usage()

        # Energy source recommendation
        if self.survey_data.get("energy_source") not in ["hydropower", "renewable", "nuclear"]:
            recommendations.append("Consider switching to a renewable energy source to reduce your carbon footprint. Check out this [resource on buying clean electricity](https://www.energy.gov/energysaver/buying-clean-electricity).")

        # Driving distance recommendation
        if self.survey_data["car_emissions"] > 217:
            recommendations.append("You drive more than the average 217 miles per week. Consider carpooling or using public transit.")
            self.graph_driving_distance()

        # Short flights recommendation
        if self.survey_data["short_flights"] > 1:
            recommendations.append("Try to limit short flights and consider alternative transportation like trains or buses.")
            self.graph_flight_usage()

        # Long flights recommendation
        if self.survey_data["long_flights"] > 0:
            recommendations.append(
                "Long-haul flights emit significant CO₂. For example, a flight of 4,000 km (about 2,485 miles) can produce between 600 to 1,000 kg of CO₂ per passenger. "
                "Consider alternatives or offsetting your carbon footprint when flying."
            )

        # Diet recommendation
        if self.survey_data["diet"] == "average omnivore":
            recommendations.append(
                "Switching from a meat-heavy diet to a more plant-based one can reduce your carbon footprint. Beef production emits 20 times more greenhouse gases than chicken per gram of protein. "
                "Consider diversifying your diet or opting for more chicken and plant-based proteins."
            )

        # Recycling recommendation
        if self.survey_data["recycles"] == "no":
            recommendations.append(
                "Recycling helps reduce waste and prevent plastic pollution. Globally, only about 9% of plastic waste is recycled, leaving millions of tons to pollute our land and oceans. "
                "Consider improving your recycling habits to help reduce plastic waste."
            )

        return recommendations

    def graph_electricity_usage(self):
        user_kwh = self.survey_data.get("electricity_emissions", 0)
        avg_american = 900
        avg_global = 300  # Approximate global average for context

        plt.figure()
        plt.bar(['Your Usage', 'Average American', 'Global Average'], [user_kwh, avg_american, avg_global])
        plt.title("Electricity Usage Comparison (kWh per month)")
        plt.xlabel("Comparison")
        plt.ylabel("kWh per month")
        plt.show()

    def graph_driving_distance(self):
        user_miles = self.survey_data.get("car_emissions", 0)
        avg_american = 217  # Average weekly miles for Americans

        plt.figure()
        plt.bar(['Your Mileage', 'Average American'], [user_miles, avg_american])
        plt.title("Weekly Driving Distance Comparison")
        plt.xlabel("Comparison")
        plt.ylabel("Miles per week")
        plt.show()

    def graph_flight_usage(self):
        user_short_flights = self.survey_data.get("short_flights", 0)
        avg_american_short = 1  # Average short flights per year

        plt.figure()
        plt.bar(['Your Short Flights', 'Average American'], [user_short_flights, avg_american_short])
        plt.title("Annual Short Flights Comparison")
        plt.xlabel("Comparison")
        plt.ylabel("Number of Short Flights (under 3 hours)")
        plt.show()

# Usage example for Flask view
# survey_data = session.get('survey_data')
# recommendations = Recommendations(survey_data).generate_recommendations()
# for rec in recommendations:
#     print(rec)
