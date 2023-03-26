import pandas as pd
from spyre import server
#change path to your csv file
merged_df = pd.read_csv('D:\\uni year 2\\aks labi\\laba 1\\merged_file.csv')
class MyWebApp(server.App):
    title = "VHI Analysis"

    inputs = [
        {
            "type": "dropdown",
            "label": "Time series",
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": "time_series",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Region",
            "options": [
                {"label": "Vinnytsia", "value": 1},
                {"label": "Mykolaivska", "value": 13},
                {"label": "Volynska", "value": 2},
                {"label": "Odesa", "value": 14},
                {"label": "Dnipropetrovsk", "value": 3},
                {"label": "Poltava", "value": 15},
                {"label": "Donetska", "value": 4},
                {"label": "Rivenska", "value": 16},
                {"label": "Zhytomyrska", "value": 5},
                {"label": "Sumy", "value": 17},
                {"label": "Zakarpatska", "value": 6},
                {"label": "Ternopil", "value": 18},
                {"label": "Zaporizhia", "value": 7},
                {"label": "Kharkiv", "value": 19},
                {"label": "Ivano-Frankivsk", "value": 8},
                {"label": "Kherson", "value": 20},
                {"label": "Kyivska", "value": 9},
                {"label": "Khmelnytska", "value": 21},
                {"label": "Kirovohradska", "value": 10},
                {"label": "Cherkasska", "value": 22},
                {"label": "Luhansk", "value": 11},
                {"label": "Chernivtsi", "value": 23},
                {"label": "Lvivska", "value": 12},
                {"label": "Chernihivska", "value": 24},
                {"label": "Republic of Crimea", "value": 25}
            ],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Start week",
            "value": "1",
            "key": "start_week",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "End week",
            "value": "52",
            "key": "end_week",
            "action_id": "update_data"
        }
    ]
    
    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "get VHI info"
    }]

    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },
        {
            "type": "plot",
            "id": "plot_id",
            "control_id": "update_data",
            "tab": "Plot"
        }
    ]

    def getData(self, params):
        # Get the parameters from the user inputs
        time_series = params['time_series']
        region = params['region']
        start_week = int(params['start_week'])
        end_week = int(params['end_week'])
        
        # Load the data for the selected region from a CSV file
        data = merged_df[(merged_df['new alligned'] == int(region))][['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI','new alligned']]
        # Filter the data based on the selected time series and weeks
        if time_series == 'VCI':
            data = data[['Year', 'Week', 'VCI']]
        elif time_series == 'TCI':
            data = data[['Year', 'Week', 'TCI']]
        else:
            data = data[['Year', 'Week', 'VHI']]
        data = data[(data['Week'] >= start_week) & (data['Week'] <= end_week)]
        return data
    def getPlot(self, params):
            df = self.getData(params)
            plt_obj = df.plot(y=params['time_series'],x='Year')
            plt_obj.set_ylabel(params['time_series'])
            plt_obj.set_xlabel("Year")
            return plt_obj.get_figure()
        # # Calculate the mean and standard deviation for the selected time series
        # mean = data[time_series].mean()
        # std = data[time_series].std()
        
        # Return a dictionary with the calculated statistics and the filtered data
        # return {
        #     'mean': mean,
        #     'std': std,
        #     'data': data.to_dict('records')
        # }
app =MyWebApp()
app.launch()