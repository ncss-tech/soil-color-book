#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Charles.Ferguson
#
# Created:     12/01/2018
# Copyright:   (c) Charles.Ferguson 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def runQry(qry):


    theURL = "https://sdmdataaccess.nrcs.usda.gov"
    url = theURL + "/Tabular/SDMTabularService/post.rest"

    # Create request using JSON, return data as JSON
    request = {}
    request["format"] = "JSON"
    request["query"] = qry

    #json.dumps = serialize obj (request dictionary) to a JSON formatted str
    data = json.dumps(request)

    # Send request to SDA Tabular service using urllib2 library
    # because we are passing the "data" argument, this is a POST request, not a GET
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)

    # read query results
    qResults = response.read()

    # Convert the returned JSON string into a Python dictionary.
    qData = json.loads(qResults)

    # get rid of objects
    del qResults, response, req


    # if dictionary key "Table" is found
    if "Table" in qData:
        results = list()
        for eRes in qData['Table']:
            results.append(eRes)
    results.sort()

##    for e in results:
##        print e

    return results





import sys, os, json, urllib2, arcpy

txtDir = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\text'
resultsDir = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\results'
templateMXDPortrait = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\templatePortrait.mxd'
templateMXDLandscape = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\templateLandscape.mxd'
gSSURGODir = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18'
soilColorImageDir = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\soilcolorimage'


stDict = dict()
stDict["Alabama"] = "AL"
#stDict["Alaska"] = "AK"
#stDict["American Samoa"] = "AS"
stDict["Arizona"] =  "AZ"
stDict["Arkansas"] = "AR"
stDict["California"] = "CA"
stDict["Colorado"] = "CO"
stDict["Connecticut"] = "CT"
stDict["District of Columbia"] = "DC"
stDict["Delaware"] = "DE"
stDict["Florida"] = "FL"
stDict["Georgia"] = "GA"
#stDict["Territory of Guam"] = "GU"
#stDict["Guam"] = "GU"
stDict["Hawaii"] = "HI"
stDict["Idaho"] = "ID"
stDict["Illinois"] = "IL"
stDict["Indiana"] = "IN"
stDict["Iowa"] = "IA"
stDict["Kansas"] = "KS"
stDict["Kentucky"] = "KY"
stDict["Louisiana"] = "LA"
stDict["Maine"] = "ME"
#stDict["Northern Mariana Islands"] = "MP"
stDict["Maryland"] = "MD"
stDict["Massachusetts"] = "MA"
stDict["Michigan"] = "MI"
#stDict["Federated States of Micronesia"] ="FM"
stDict["Minnesota"] = "MN"
stDict["Mississippi"] = "MS"
stDict["Missouri"] = "MO"
stDict["Montana"] = "MT"
stDict["Nebraska"] = "NE"
stDict["Nevada"] = "NV"
stDict["New Hampshire"] = "NH"
stDict["New Jersey"] = "NJ"
stDict["New Mexico"] = "NM"
stDict["New York"] = "NY"
stDict["North Carolina"] = "NC"
stDict["North Dakota"] = "ND"
stDict["Ohio"] = "OH"
stDict["Oklahoma"] = "OK"
stDict["Oregon"] = "OR"
#stDict["Republic of Palau"] = "PW"
#stDict["Pacific Basin"] = "PB"
stDict["Pennsylvania"] = "PA"
#stDict["Puerto Rico and U.S. Virgin Islands"] = "PRUSVI"
stDict["Rhode Island"] = "RI"
stDict["South Carolina"] = "SC"
stDict["South Dakota"] = "SD"
stDict["Tennessee"] = "TN"
stDict["Texas"] = "TX"
stDict["Utah"] = "UT"
stDict["Vermont"] = "VT"
stDict["Virginia"] = "VA"
stDict["Washington"] = "WA"
stDict["West Virginia"] = "WV"
stDict["Wisconsin"] = "WI"
stDict["Wyoming"] = "WY"

#states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'FM', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MH', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'MX', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'PW', 'RI', 'SC', 'SD', 'TN', 'TX', 'US', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
#conus = ['AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
#test = ['DE', 'DC', 'TX']
test = ['DE', 'MD', 'NJ']
colorDict = {}

for t in test:
    for st, stAbbr in stDict.iteritems():
        if stAbbr == t:
            state = st

            overlapQry = """SELECT legend.areasymbol FROM (legend INNER JOIN laoverlap ON legend.lkey = laoverlap.lkey)
            INNER JOIN sastatusmap ON legend.areasymbol = sastatusmap.areasymbol
            WHERE laoverlap.areatypename = 'State or Territory' AND laoverlap.areaname LIKE '""" + state + """' AND
            legend.areatypename = 'Non-MLRA Soil Survey Area'"""

            aSyms = list()

            oResults = runQry(overlapQry)

            for o in oResults:
                aSyms.append(o[0])

            aSymsQry = ",".join(map("'{0}'".format, aSyms))

            #print aSymsQry

            domCokeyQry = """SELECT muname,
            mapunit.mukey,cokey,

            CASE WHEN compname LIKE '%variant%' THEN UPPER (REPLACE (compname, 'variant', ''))
            	 WHEN compname LIKE '%family%' THEN UPPER (REPLACE (compname, 'family', ''))
            	 WHEN compname LIKE '%taxadjunct%' THEN UPPER (REPLACE (compname, 'taxadjunct', '')) ELSE UPPER (compname) END AS compname, comppct_r

            FROM (legend INNER JOIN (mapunit INNER JOIN component ON mapunit.mukey = component.mukey AND majcompflag = 'yes') ON legend.lkey = mapunit.lkey AND legend.areasymbol IN (""" + aSymsQry + """)
            AND component.cokey =
            (SELECT TOP 1 c1.cokey FROM component AS c1
            INNER JOIN mapunit AS c ON c1.mukey=c.mukey AND c.mukey=mapunit.mukey ORDER BY c1.comppct_r DESC, CASE WHEN LEFT (muname,2)= LEFT (compname,2) THEN 1 ELSE 2 END ASC, c1.cokey))
            ORDER BY muname ASC, compname ASC, cokey"""

            domCokeyRes = runQry(domCokeyQry)

            stQryDict = dict()

            #n=0


            for e in domCokeyRes:

                #[mukey] = [series]
                stQryDict[e[1]] = e[3]

                #n+=1

            txtList = os.listdir(txtDir)
            for t in txtList:
                suffix = t[-9:-4]
                clrF = resultsDir + os.sep + stAbbr + "_" + suffix + ".clr"
                with open(clrF, 'w') as f:
                    colorDict[clrF] = clrF
                    with open(txtDir + os.sep + t, 'r') as z:

                        depthDict = dict()

                        z.readline()
                        lines = z.readlines()
                        for line in lines:
                            clearline = (line.replace('"', "")[:-1])
                            lineList = clearline.split(",")
                            # [series] = ['r','g','b']
                            depthDict[lineList[0]] = lineList[1:]

                        #for every mukey, get the series
                        for mkey in stQryDict:
                            mkeyResult = stQryDict.get(mkey)

                            #use the series to get rgb at for that depth
                            rgb = depthDict.get(mkeyResult)
                            if rgb:
                                r=rgb[0]
                                g=rgb[1]
                                b=rgb[2]
                            else:
                                r='255'
                                g='0'
                                b='127'

                            l = mkey + " " +  r + " " + g + " " +  b + "\n"
                            f.write(l)
                    z.close()
                f.close()

del clrF

arcpy.env.workspace = gSSURGODir
arcpy.env.overwriteOutput = True
depthList = ['_005cm.clr', '_010cm.clr', '_015cm.clr', '_025cm.clr', '_050cm.clr', '_075cm.clr', '_100cm.clr', '_125cm.clr', '_brigh.clr']
for state in test:
    for ws in arcpy.ListWorkspaces(test, "FileGDB"):
        if os.path.basename(ws)[-11:-9] == state:
            print arcpy.env.workspace
            gdbRaster = ws + os.sep + 'MapunitRaster_10m'
            raster = gSSURGODir + os.sep + state + "_color"
            arcpy.arcpy.management.CopyRaster(gdbRaster, raster)
            for d in depthList:
                print d
                clrMap = resultsDir + os.sep + state + d
                arcpy.management.AddColormap(raster, None, clrMap)
                desc = arcpy.Describe(raster)
                h = desc.height
                w = desc.width

                if h > w :
                    savePath = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\mxd' + os.sep + state + 'soilcolor.mxd'
                    mxd = arcpy.mapping.MapDocument(templateMXDPortrait)
                    mxd.saveACopy(savePath)

                    mxd = arcpy.mapping.MapDocument(savePath)
                    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
                    df.spatialReference = arcpy.SpatialReference(4326)
                    arcpy.management.MakeRasterLayer(raster, "raster")
                    addLayer = arcpy.mapping.Layer("raster")
                    print  state + ' madeLayer ' + d[:-4]
                    arcpy.mapping.AddLayer(df, addLayer)
                    print 'added that layer ' +  state + ' madeLayer ' + d[:-4]
                    arcpy.mapping.ExportToPNG(mxd, soilColorImageDir + os.sep + state + d[:-4] + '.png', df)
                    mxd.save()
                    arcpy.management.Delete("raster")

                    del mxd

                else:
                    savePath = r'D:\Chad\GIS\PROJECT_18\SOILCOLOR18\mxd' + os.sep + state + 'soilcolor.mxd'
                    mxd = arcpy.mapping.MapDocument(templateMXDLandscape)
                    mxd.saveACopy(savePath)

                    mxd = arcpy.mapping.MapDocument(savePath)
                    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
                    df.spatialReference = arcpy.SpatialReference(4326)
                    arcpy.management.MakeRasterLayer(raster, "raster")
                    addLayer = arcpy.mapping.Layer("raster")
                    print  state + ' madeLayer ' + d[:-4]
                    arcpy.mapping.AddLayer(df, addLayer)
                    print 'added that layer ' +  state + ' madeLayer ' + d[:-4]
                    arcpy.mapping.ExportToPNG(mxd, soilColorImageDir + os.sep + state + d[:-4] + '.png', df)
                    mxd.save()
                    arcpy.management.Delete("raster")

                    del mxd















