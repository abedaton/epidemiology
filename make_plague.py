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
           "Montserrat", "Maldives", "Saint Barthelemy", "Saint Martin", "Holy See (Vatican City)"]

to_merge = ['Brunei Darussalam', 'Djibouti', 'Papua New Guinea', 'Andorra', 'Haiti', 'Qatar', 'Lebanon', 'El Salvador', 'Gambia']

done = ['Taiwan', 'Sri Lanka', 'Trinidad and Tobago', 'Puerto Rico', 'Western Sahara', 'Timor-Leste', 'Oman', 'Burma', 'Luxembourg', 'United Arab Emirates', 'Belize', 'Bhutan', 'Swaziland', 'Hong Kong', 'Liechtenstein', 'Monaco', 'Kuwait', 'San Marino', 'Burundi', 'Palestine', 'Macau', "Israel", "Lesotho", 'Dominican Republic', 'Rwanda']

keep_alone = ["Australia", "Greenland", "New Zealand", "Iceland", "Philippines", "Madagascar", "Antarctica", "Japan"]
want = ["Cuba", "Belgium", "Portugal", "Serbia", "United Kingdom", "Slovenia", "Montenegro", "Ireland", "Canada", "Denmark"]

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



def main():
    old = gp.read_file("shapes/myShape.shp")
    new, alone = filter_country(old)

    print("Tanzania" in new["name"].to_string())





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
