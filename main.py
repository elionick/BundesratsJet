from classAirplanes import Airplanes


# Bundesratsjets:
# Dassault = "4b7f4c"
# Cessna = "4b7fd4"

def main():
    airplanes = Airplanes(['4b7f4c', '4b7fd4', 'ADC9B6', 'AC7AA9'])
    airplanes.check_flights()

if __name__ == '__main__':
    print('Now running:')
    main()