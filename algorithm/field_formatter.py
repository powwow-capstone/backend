from outlier import find_outlier

def field_formatter(data_list):
    '''
        Format the field data into a format that the frontend can parse
        The frontend expects the following format:
        {
            id: 1,
            features : [
                {
                    name : "efficiency", value : 0, percentile : 0
                },
                ...
            ],
            categories : [
                {
                    category_name : "crop", type: "string",  value : "almonds"
                },
                {
                    category_name : "acreage", type: "real", value: 3000
                }
                ...
            ],
            centroid: [
                34.1,
                -119.5
            ],
            coordinates : {
                coordinates : [
                    { "lng": -119.575927734375, "lat": 34.4122238159181
                    },
                    { "lng": -119.607498168945, "lat": 34.4196891784669
                    },
                    ...
                ]
            } 
        }
    '''
    
    # First, calculate the percentile for all the efficiency scores
    scores = []
    for data in data_list:
        data_id = data["id"]
        efficiency = data["efficiency"]
        scores.append((data_id, efficiency))

    outliers = find_outlier(scores)
    outliers_dict = {}
    for outlier_percentile in outliers:
        outliers_dict[outlier_percentile[0]] = outlier_percentile[1]

    formatted_data = []
    for data in data_list:
        data_id = data["id"]
        centroid = data["centroid"]
        coordinates = data["coordinates"]
        categories = [{
            "name" : "Acreage", 
            "type" : "real", 
            "value" : data["acres"]
        },
        {
            "name": "Crop", 
            "type": "string", 
            "value": data["crop"]
        }]
        features = { "name" : "Efficiency", "value" : data["efficiency"], "percentile" : outliers_dict[data_id] }

        formatted_data.append(
            {
                "id" : data_id,
                "centroid" : centroid,
                "coordinates" : coordinates,
                "categories": categories,
                "features" : features
            }
        )
        
    return formatted_data


