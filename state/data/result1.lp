<?xml version = "1.0" encoding="UTF-8" standalone="yes"?>
<CPLEXSolution version="1.2">
 <header
   problemName=""
   objectiveValue="16"
   solutionTypeValue="1"
   solutionTypeString="basic"
   solutionStatusValue="1"
   solutionStatusString="optimal"
   solutionMethodString="dual"
   primalFeasible="1"
   dualFeasible="1"
   simplexIterations="3"
   writeLevel="1"/>
 <quality
   epRHS="9.9999999999999995e-07"
   epOpt="9.9999999999999995e-07"
   maxPrimalInfeas="0"
   maxDualInfeas="0"
   maxPrimalResidual="3.3306690738754696e-16"
   maxDualResidual="0"
   maxX="1"
   maxPi="4"
   maxSlack="0.80000000000000004"
   maxRedCost="1"
   kappa="11"/>
 <linearConstraints>
  <constraint name="r0" index="0" status="LL" slack="0" dual="2"/>
  <constraint name="r1" index="1" status="LL" slack="0" dual="2"/>
  <constraint name="r2" index="2" status="LL" slack="0" dual="4"/>
  <constraint name="r3" index="3" status="BS" slack="-0.80000000000000004" dual="-0"/>
 </linearConstraints>
 <variables>
  <variable name="y0" index="0" status="BS" value="0.80000000000000004" reducedCost="0"/>
  <variable name="y1" index="1" status="BS" value="0.59999999999999998" reducedCost="0"/>
  <variable name="y2" index="2" status="BS" value="1" reducedCost="0"/>
  <variable name="y3" index="3" status="LL" value="0" reducedCost="1"/>
 </variables>
</CPLEXSolution>
