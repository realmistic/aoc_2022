# https://topaz.github.io/paste/#XQAAAQCZDAAAAAAAAAAzHIoib6poHLpewxtGE3pTrRdzrponKxDhfDpmqFiuiXW67dc6QvDAbHxd/MkcXN5KnngpeDbxpiWabnGbQVwWZYiPtkfNbXnSdQgzM8TIuYQeClbpOxRvw21gc5m9eegLXCOknsgLg1NPLLcG85E/Fldc2wQpm0Pw4is4d1CjT+1gJDnwwJn6M9U78oRlFfpVG6ZYG+yiYIpmWxNQa9tqCWhdfeJCJBiC45IID2gFjJkGAclC18rLPlKMOQg0rOI0EI0p/7b54V8xbgX6b8wcyenwxWMi+jbGZPn2DTdbHEEYA1cs4AfBm7JHhGSFpvNSSio6iX2GTzjeIO7CU/P2Wn2PLQZl8YmtTey6Pi69XPbjsy5u8w4YAVQeOM30DAMLLChvS7rjjS0qEfOYV7ckbdxfDhAjB3pOGdLfQmCV8EHlWNQ34rjoON7uiI5HFCNm6guqrgZJFT2Ma2577iSYGTLiB+2DvdQtVv13PnQJwubGnCIFognAZ3g4piF0QuNEDz85j82XjTnQuPo8R1oUfJtOX/FfMQkvUkbrFloQnkOqezIsqmTpX0GpqNvhjseRj5W/T25iRx7DdzmeuEMHNZbAaNmnLveSQ9VnPiU2bV+3FE7LUcW7DlEfzLFZUCERdDBP9DKtzaDbSZGoI44GWjvbjLlUCmNjdAiJJbd59uprykAP/R64k3AWLC9oYcsVDnl+1JFx4V4KHJsBj56+dudHX8Tu5pGSF85ZfnkIJQWrXo/N3Qsf+jKPbp3Z8SAniJ3aMVWS0YS9RvjOdB6HSEImeliBp/Mk3IEO95I5x6CdxokR/7hHtddzRceRDc5F/Yp7nq7V0VrqzHhBFY7cXSSW3rDD23UxcKgHljrZ7cX7AAkooQwcVB78QDiEL9oYoYoDi/r0dEg5gkTQdidVTA+2RnavduN/hS7se6vM0VRQoXRtlerC6prPyHc4rxngTNyk4+OJFKbkxTphdrDxb3IpUlibXRxT1hT/IOAJSOvNMp374q+pptqUpT6s+DfaV8kaMSXf2xvW63iEduKHl5B+YVHztjawzzN357Z8subdw80jrWPPCIUO7atXfyjyY8yCGwtvpcvSLuXF0XirPOcZLyMncmdRLknLOgwPHOncfI//GagfctCjHZi1/ndsxg==


# from functools import cache
from functools import lru_cache
import os

BluePrintList = []
with open("../inputs/inputs_day19.txt", "r") as data:
    for t in data:
        Line = t.strip().split()
        BlueNum, OreRO, ClayRO, ObsnRO, ObsnRC, GeodeROr, GeogeROb = int(Line[1][:-1]), int(Line[6]), int(
            Line[12]), int(Line[18]), int(Line[21]), int(Line[27]), int(Line[30])
        NewTuple = (BlueNum, OreRO, ClayRO, (ObsnRO, ObsnRC), (GeodeROr, GeogeROb))
        BluePrintList.append(NewTuple)


@lru_cache(maxsize=14000000)
def ParseMinute(Minute, Ore, Clay, Obsn, OreRo, ClayRo, ObsnRo, OreCost, ClayCost, ObsnCost, GeodeRoCost):
    ObsnRoCostOre, ObsnRoCostClay = ObsnCost
    GeodeRoCostOre, GeodeRoCostObsn = GeodeRoCost
    OreCosts = [OreCost, ClayCost, ObsnRoCostOre, GeodeRoCostOre]
    MaxOreCost = max(OreCosts)

    if Minute == 1:
        return 0

    GeodeScoreList = []
    CollectedOre = Ore + OreRo
    CollectedClay = Clay + ClayRo
    CollectedObns = Obsn + ObsnRo

    # Added efficiency, can't build more robots than you can consume in resources
    if Ore >= OreCost and OreRo < MaxOreCost:
        BuildOre = ParseMinute(Minute - 1, CollectedOre - OreCost, CollectedClay, CollectedObns, OreRo + 1, ClayRo,
                               ObsnRo, OreCost, ClayCost, ObsnCost, GeodeRoCost)
        GeodeScoreList.append(BuildOre)
    if Ore >= ClayCost and ClayRo < ObsnRoCostClay:
        BuildClay = ParseMinute(Minute - 1, CollectedOre - ClayCost, CollectedClay, CollectedObns, OreRo, ClayRo + 1,
                                ObsnRo, OreCost, ClayCost, ObsnCost, GeodeRoCost)
        GeodeScoreList.append(BuildClay)
    if Ore >= ObsnRoCostOre and Clay >= ObsnRoCostClay and ObsnRo < GeodeRoCostObsn:
        BuildObsn = ParseMinute(Minute - 1, CollectedOre - ObsnRoCostOre, CollectedClay - ObsnRoCostClay, CollectedObns,
                                OreRo, ClayRo, ObsnRo + 1, OreCost, ClayCost, ObsnCost, GeodeRoCost)
        GeodeScoreList.append(BuildObsn)
    if Ore >= GeodeRoCostOre and Obsn >= GeodeRoCostObsn:
        BuildGeode = ParseMinute(Minute - 1, CollectedOre - GeodeRoCostOre, CollectedClay,
                                 CollectedObns - GeodeRoCostObsn, OreRo, ClayRo, ObsnRo, OreCost, ClayCost, ObsnCost,
                                 GeodeRoCost)
        BuildGeode += (Minute - 1)
        return BuildGeode

    BuildNothing = ParseMinute(Minute - 1, CollectedOre, CollectedClay, CollectedObns, OreRo, ClayRo, ObsnRo, OreCost,
                               ClayCost, ObsnCost, GeodeRoCost)
    GeodeScoreList.append(BuildNothing)

    FinalScore = max(GeodeScoreList)
    return FinalScore


QualityTotal = 0
for b in BluePrintList:
    ParseMinute.cache_clear()
    BlueNum, OreCost, ClayCost, ObsnCost, GeodeCost = b
    MaxGeodes = ParseMinute(24, 0, 0, 0, 1, 0, 0, OreCost, ClayCost, ObsnCost, GeodeCost)
    print(MaxGeodes, BlueNum)
    print(ParseMinute.cache_info())
    BlueQuality = MaxGeodes * BlueNum
    QualityTotal += BlueQuality
ParseMinute.cache_clear()
Part1Answer = QualityTotal

del BluePrintList[3:]
Part2Answer = 1
for b in BluePrintList:
    ParseMinute.cache_clear()
    BlueNum, OreCost, ClayCost, ObsnCost, GeodeCost = b
    MaxGeodes = ParseMinute(32, 0, 0, 0, 1, 0, 0, OreCost, ClayCost, ObsnCost, GeodeCost)
    print(MaxGeodes, BlueNum)
    print(ParseMinute.cache_info())
    Part2Answer *= MaxGeodes

print(f"{Part1Answer}")
print(f"{Part2Answer}")
