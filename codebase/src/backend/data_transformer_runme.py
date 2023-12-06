from data_transformer import DataTransformer
import pandas as pd
import os 

# # ichart
# dataTransformer = DataTransformer()
# dataTransformer.set_path("../../data/raw/ichart/pivot")
# dataTransformer.set_devices(["Beach2_Tower", "Beach2_Buoy", "Beach6_Buoy", "TREC_Tower"])
# dataTransformer.device_aggregate("ichart")
# dataTransformer.tidy_devices("ichart")
# dataTransformer.device_downsample_hour("ichart")
# dataTransformer.device_downsample_day("ichart")



#the name of all the folders in a directory


#device = os.listdir(f"../../data/raw/{project}")
class DataWrangler:
    def __init__(self) -> None:
        self.project = [ "new", "old"]

    
    def downsample(self) -> None:
        for project in self.project:
            for device in os.listdir(f"../../data/raw/{project}"):
                if device == "TREC_Tower_iSIC":
                    continue
                if device == "Beach2_Tower_iSIC":
                    continue
                for filename in os.listdir(f"../../data/raw/{project}/{device}"):
                    print(device, filename)
                    if filename.endswith(".csv"):
                        df = pd.read_csv(f"../../data/raw/{project}/{device}/{filename}")
                        df["times"] = pd.to_datetime(df["times"])
                        parameter = df.columns[1]
                        df.rename(columns={parameter: 'value'}, inplace=True)
                        df.set_index("times", inplace=True)
                        hourly_df = df.groupby(["Units"]).resample('H').agg({"value": ["mean", "std"]})
                        daily_df = df.groupby(["Units"]).resample('D').agg({"value": ["mean", "std"]})
                        hourly_df.reset_index(inplace=True)
                        daily_df.reset_index(inplace=True)
                        hourly_df.set_index("times", inplace=True)
                        daily_df.set_index("times", inplace=True)
                        hourly_df.reset_index(inplace=True)
                        daily_df.reset_index(inplace=True)
                        hourly_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in hourly_df.columns]
                        daily_df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in daily_df.columns]
                        hourly_df["parameter"] = parameter
                        daily_df["parameter"] = parameter
        
                        #save the data to a csv file
                        hourly_df.to_csv(f"../../data/processed/{project}/{device}/hourly_{filename}", index = False)
                        daily_df.to_csv(f"../../data/processed/{project}/{device}/daily_{filename}", index = False)

                self.parser(f"../../data/processed/{project}/{device}")
                    


    def parser(self, directory: str ) -> None:
        df_merged = pd.DataFrame()
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                if filename.startswith("hourly"):
                    print("location1:", filename)
                    df = pd.read_csv(f"{directory}/{filename}")
                    df_merged = pd.concat([df_merged, df], ignore_index=True)
        df_merged.to_csv(f"{directory}/tidy_hourly_all_data.csv", index = False)

        df_merged = pd.DataFrame()
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                if filename.startswith("daily"):
                    print("location2:", filename)
                    df = pd.read_csv(f"{directory}/{filename}")
                    df_merged = pd.concat([df_merged, df], ignore_index=True)
        df_merged.to_csv(f"{directory}/tidy_daily_all_data.csv", index = False)
        print("tidied the data for ", directory)











datawrangler = DataWrangler()
datawrangler.downsample()

