import os
import pandas as pd





class OldDataTransformer():
    """
    This class is used to transform the old data to raw data format

    """

    def __init__(self) -> None:
        """
        """
        self.device_id = ["TREC_Tower", "Beach6_Buoy", "Beach2_Tower", "Beach2_Buoy"]
        #self.device_id = ["TREC_Tower"]

    
    def transform(self, device) -> None:
        """
        
        """

        df = pd.DataFrame()
        
        dfs = []
        

        for filename in os.listdir(f"../data/iChart6_data/raw/{device}"):

            if filename.endswith(".csv"):
                df = pd.read_csv(os.path.join(f"../data/iChart6_data/raw/{device}", filename), encoding='latin-1')
                
            
                new_columns = df.iloc[1] + "_" + df.iloc[2].fillna("")
                df.columns = new_columns
                df = df.drop([0,1,2])   
                df.reset_index(drop = True, inplace=True)
                df.replace("-Invalid-", pd.NA, inplace=True)
                df = df.set_index(df.columns[0]).reset_index()
                dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True)
        merged_df = merged_df.rename(columns={"Date/Time_m/d/y": "times"})
        merged_df["times"] = pd.to_datetime(merged_df["times"])
        merged_df = merged_df.sort_values(by="times")

        
        
        for parameter in merged_df.columns[1:]:
            df = merged_df[["times", parameter]]
            df = df.rename(columns={parameter: "value"})
            df["parameter"] = parameter
            df = df[["times", "parameter", "value"]]

            parameter = parameter.replace("/", "%per%")
            try:
                df.to_csv(f"../data/iChart6_data/raw/by_parameter/{device}/{parameter}.csv", index=False)
                print(f"File '{device}_{parameter}.csv' successfully saved.")
            except Exception as e:
                print(f"Error saving file '{device}_{parameter}.csv': {e}")
            

        merged_df.to_csv(f"../data/iChart6_data/processed/{device}_all_data.csv", index=False)

    
    def device_transform(self) -> None:
        for device in self.device_id:               
            self.transform(device)


    def format_pivot(self,device: str, parameter_id: str) -> None:
        """
        This function is used to format the data into pivot table format
        """
        df = pd.read_csv(f"../data/iChart6_data/raw/by_parameter/{device}/{parameter_id}", encoding='latin-1')
        df['times'] = df['times'].drop_duplicates()
        df.drop_duplicates("times", inplace=True)
        df.dropna(subset=["times"], inplace=True)

        df.reset_index(inplace=True)
          
        
        try:
            df = df.pivot(index="times", columns="parameter", values="value")
        
            column_name_parts = df.columns.str.split('_')
            unit = column_name_parts[0][1]  # Assuming the format is "parameter_unit"

            #Create a new column with the extracted unit in every cell
            df['Units'] = unit
            parameter_column = df.columns[0]
            df = df.rename(columns={parameter_column: f"{column_name_parts[0][0]}"})


            df.to_csv(f"../data/iChart6_data/raw/by_parameter/{device}_{column_name_parts[0][0]}_pivot.csv")
        except Exception as e:
            print(f"Error saving file '{device}_{parameter_id}.csv': {e}")



    def pivot_devices(self) -> None:
        for device in self.device_id:
            for filename in os.listdir(f"../data/iChart6_data/raw/by_parameter/{device}"):
                if filename.endswith(".csv"):
                    self.format_pivot(device, filename)


OldDataTransformer = OldDataTransformer()
OldDataTransformer.device_transform()
OldDataTransformer.pivot_devices()

                










