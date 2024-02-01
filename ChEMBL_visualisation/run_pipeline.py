import data_acquisition
import data_processing
import visualisation

def run_pipeline():
    print("Fetching data from ChEMBL...")
    data_acquisition.main()

    print("Processing data...")
    data_processing.main()

    print("Generating visualizations...")
    visualisation.main()

if __name__ == "__main__":
    run_pipeline()
