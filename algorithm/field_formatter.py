from percentile import find_percentile_helper

def field_formatter(data_list):
    '''
        Format the field data into a format that the frontend can parse
        The frontend expects the following format:
        {
            id: 1,
            group_id: 0,
            features : [
                {
                    name : "eta", value : 0, score : 0, units : "inches"
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
    # scores = []
    # for data in data_list:
    #     data_id = data["id"]
    #     efficiency = data["eta"]
    #     scores.append((data_id, efficiency))

    formatted_data = []
    for data in data_list:
        data_id = data["id"]
        group_id = data["group_id"]
        centroid = data["centroid"]
        coordinates = data["coordinates"]
        categories = [{
            "category_name" : "Acreage", 
            "type" : "real", 
            "value" : data["acres"]
        },
        {
            "category_name": "Crop",
            "type": "string", 
            "value": data["crop"]
        }]
        features = [{ "name" : "ETa", "value" : data["eta"], "score" : data["score"], "units" : "inches" }]

        formatted_data.append(
            {
                "id" : data_id,
                "groupid" : group_id,
                "centroid" : centroid,
                "coordinates" : coordinates,
                "categories": categories,
                "features" : features
            }
        )
        
    return formatted_data


