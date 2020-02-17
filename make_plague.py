import geopandas as gp
from shapely.geometry import Polygon, MultiPolygon
import matplotlib.pyplot as plt
import time

columns = ["name", "ISO2", "ISO3", "area", "pop", "neighbors", "geometry"]

no_want = ["South Georgia South Sandwich Islands", "Jersey", "Guernsey", "Svalbard", "Turks and Caicos Islands", "Saint Helena",
           "Saint Pierre and Miquelon", "Barbados", "Bahrain", "American Samoa", "Marshall Islands", "Palau", "Pitcairn Islands",
           "Netherlands Antilles", "Guadeloupe", "Samoa", "Solomon Islands", "Bahamas", "Bermuda", "Antigua and Barbuda",
           "Cayman Islands", "Comoros", "Cape Verde", " Saint Vincent and the Grenadines", "British Virgin Islands",
           "United States Virgin Islands", "Wallis and Futuna Islands", "Cook Islands", "Cyprus", "Dominica",
           "Fiji", "Falkland Islands (Malvinas)", "Micronesia, Federated States of", " Saint Vincent and the Grenadines",
           "French Polynesia", "Grenada", "Aruba", "Singapore", "Mayotte", "Jamaica", "Mauritius", "Gibraltar",
           "Sao Tome and Principe", "Guam", "Kiribati", "Martinique", "Saint Vincent and the Grenadines",
           "Tuvalu", "Tonga", "Tokelau", "Saint Lucia", "Seychelles", "Saint Kitts and Nevis", "Reunion", "Nauru",
           "Vanuatu", "United States Minor Outlying Islands", "Christmas Island", "British Indian Ocean Territory",
           "British Indian Ocean Territory", "French Southern and Antarctic Lands", "Heard Island and McDonald Islands",
           "Bouvet Island", "Cocos (Keeling) Islands", "Norfolk Island", "Isle of Man", "Isle of Man", "Anguilla",
           "Niue", "Malta", "Åland Islands", "Faroe Islands", "Northern Mariana Islands", "New Caledonia",
           "Montserrat", "Maldives", "Saint Barthelemy", "Saint Martin", "Holy See (Vatican City)", 'Brunei Darussalam',
           "Djibouti", 'Andorra', "Qatar", 'Lebanon', "Gambia", "Taiwan", "Sri Lanka", "Trinidad and Tobago", "Timor-Leste", "Liechtenstein",
           "Monaco", "San Marino", "Palestine", "Macau"]

to_merge = []

done = []

keep_alone = ["Australia", "Greenland", "New Zealand", "Iceland", "Philippines", "Madagascar", "Antarctica", "Japan"]
want = ["Cuba", "Belgium", "Portugal", "Serbia", "United Kingdom", "Slovenia", "Montenegro", "Ireland", "Canada", "Denmark", 'Papua New Guinea',
        "Haiti", "El Salvador", "Puerto Rico", "Western Sahara", "Oman", "Burma", "Luxembourg", "United Arab Emirates", "Belize", "Bhutan",
        "Swaziland", "Hong Kong", "Kuwait", "Burundi", "Israel", "Lesotho", "Dominican Republic", "Rwanda"]

def filter_country(old):
    new = gp.GeoDataFrame(columns=columns)
    alone = gp.GeoDataFrame(columns=columns)
    for index, row in old.iterrows():
        if (row["NAME"] not in no_want and row["NAME"] not in to_merge and row["NAME"] not in keep_alone and row["NAME"] not in done):
            if row["NEIGHBORS"] is not None and len(row["NEIGHBORS"].split(", ")) > 1 and row["AREA"] >= 2500 or row["NAME"] in want:
                new = new.append({"name": row["NAME"], "ISO2": row["ISO2"], "ISO3": row["ISO3"], "area": row["AREA"],
                        "pop": row["POP2005"], "neighbors": row["NEIGHBORS"], "geometry": row["geometry"]}, ignore_index=True)
            else:
                alone = alone.append({"name": row["NAME"], "ISO2": row["ISO2"], "ISO3": row["ISO3"], "area": row["AREA"],
                        "pop": row["POP2005"], "neighbors": row["NEIGHBORS"], "geometry": row["geometry"]}, ignore_index=True)

    return new, alone


def mergeCountry(old: gp.geodataframe.GeoDataFrame, new: gp.geodataframe.GeoDataFrame, mini: str, big: str) -> gp.GeoDataFrame:
    bigName = big
    mini = old.loc[old["NAME"] == mini]["geometry"].tolist()[0]
    big = old.loc[old["NAME"] == big]["geometry"].tolist()[0]

    try:
        final = MultiPolygon([*list(mini), *list(big)])
    except:
        try:
            final = MultiPolygon([mini, *list(big)])
        except:
            try:
                final = MultiPolygon([*list(mini), big])
            except:
                try:
                    final = MultiPolygon([mini, big])
                except:
                    print("wtf???")

    #new.loc[new["name"] == "China", "geometry"] = final
    new = new.drop(new.loc[new["name"] == bigName].index.tolist()[0])

    new = new.append({"name": old.loc[old["NAME"] == bigName]["NAME"].tolist()[0],
                      "ISO2": old.loc[old["NAME"] == bigName]["ISO2"].tolist()[0],
                      "ISO3": old.loc[old["NAME"] == bigName]["ISO3"].tolist()[0],
                      "area": old.loc[old["NAME"] == bigName]["AREA"].tolist()[0],
                      "pop": old.loc[old["NAME"] == bigName]["POP2005"].tolist()[0],
                      "neighbors": old.loc[old["NAME"] == bigName]["NEIGHBORS"].tolist()[0],
                      "geometry": final}, ignore_index=True)


    return new


def plotCountryName(new: gp.geodataframe.GeoDataFrame, country: str) -> None:
    country = new.loc[new["name"] == country]["geometry"].tolist()[0]
    try:
        country = list(country)
        for i in list(country):
            plt.plot(*i.exterior.xy)
        plt.show()
    except:
        plt.plot(*country.exterior.xy)
        plt.show()


def plotEntireCountry(geo: MultiPolygon) -> None:
    country = list(geo)
    for i in list(country):
        plt.plot(*i.exterior.xy)
    plt.show()

def updateNeighbors(df: gp.geodataframe.GeoDataFrame) -> gp.geodataframe.GeoDataFrame:
    for index, country in df.iterrows():   
        neighbors = df[~df.geometry.disjoint(country.geometry)]["name"].tolist()
        neighbors = [ name for name in neighbors if country["name"] != name ]
        df.at[index, "neighbors"] = ", ".join(neighbors)
    return df


def main():
    old = gp.read_file("shapes/myShape.shp")
    new, alone = filter_country(old)
    new["neighbors"] = None
    
    print(new)
    new = updateNeighbors(new)
    print(new)
    new.to_file("shapes/useShape.shp")
    return

    for mini in to_merge:
        try:
            big = input(mini + " : merge with which country? ")
            plotCountryName(new, big)
            new = mergeCountry(old, new, mini, big)
            plotCountryName(new, big)
            new.to_file("shapes/plagueShapes")
            done.append(mini)
            to_merge.remove(mini)
        except Exception as e:
            print(e)
            print(done)
            print(to_merge)
        print(done)
        print(to_merge)







main()
