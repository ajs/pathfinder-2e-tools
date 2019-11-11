function randItem(arr) {
  return arr[Math.floor(Math.random()*arr.length)];
}

function costOf(creature, partyLevel, costs) {
  return costs[(creature[2]-partyLevel)+4];
}

function inBudget(partyLevel, costs, budget) {
  /* This is in its own function to get the closure right */
  return function (row) {
    return costOf(row, partyLevel, costs) <= budget;
  }
}

function inLevelRange(creature, partyLevel) {
  var creatureLevel = parseInt(creature[2], 10);
  partyLevel = parseInt(partyLevel, 10);
  var minLevel = partyLevel - 4;
  var maxLevel = partyLevel + 2;
  return creatureLevel >= minLevel && creatureLevel <= maxLevel;
}

function addResult(spreadsheetId, creature, where) {
  var valueRange = Sheets.newValueRange();
  valueRange.values = [[creature]];
  Sheets.Spreadsheets.Values.update(valueRange, spreadsheetId, where, {
    valueInputOption: "RAW"
  });
}

function clearResult(spreadsheetId, where) {
  for (var i = 0; i < 10; i++) {
    addResult(spreadsheetId, "", where + (i+2));
  }
}

function creatureType(creature, type) {
  return creature[4] == type;
}

function creatureAligned(creature, alignment) {
  return creature[3] == alignment || creature[3] == "Neutral";
}

function generateEncounter() {
  var threatBudget = {
    "Trivial": 40,
    "Low": 60,
    "Moderate": 80,
    "Severe": 120,
    "Extreme": 160
  };
  var costs = [10, 15, 20, 30, 40, 60, 80];
  var minCost = costs[0];

  var spreadsheetId = "1zAAqlW4gnh_zfjyzgE17CCdL8HV07KSv0xxA2qqg8d8";
  var creaturesRange = "Sheet1!E:J"; /* The table of creatures */
  var inputsColumn = "Sheet2!B";
  var outputColumn = "Sheet2!D";

  var creaturesResult = Sheets.Spreadsheets.Values.get(spreadsheetId, creaturesRange);
  var partyLevel = Sheets.Spreadsheets.Values.get(spreadsheetId, inputsColumn+"1").values[0][0];
  var threatLevel = Sheets.Spreadsheets.Values.get(spreadsheetId, inputsColumn+"2").values[0][0];

  clearResult(spreadsheetId, outputColumn);
  
  var creatures = creaturesResult.values.slice(1); /* Remove header */
  creatures = creatures.filter(function (row) { return inLevelRange(row, partyLevel); });
  var budget = threatBudget[threatLevel];
  var creatureIndex = 0;
  var resultType = null;
  var resultAlign = null;

  while (budget > minCost) {
    var creature;
    creatures = creatures.filter(inBudget(partyLevel, costs, budget));
    if (creatures.length == 0) {
      break;
    }
    creature = randItem(creatures)
    if (!resultType) {
      resultType = creature[4];
      resultAlign = creature[3];
      /* Was using only like-creatures, but results were too thin */
      /*creatures = creatures.filter(function (row) {return creatureType(row, resultType) && creatureAligned(row, resultAlign);});*/
      creatures = creatures.filter(function (row) {return creatureAligned(row, resultAlign);});
    }
    addResult(spreadsheetId, creature[0] + " lvl " + creature[2] + " " + resultAlign + " " + resultType, outputColumn + (creatureIndex + 2));
    creatureIndex += 1;
    budget -= costOf(creature, partyLevel, costs);
  }
  if (creatureIndex == 0) {
    addResult(spreadsheetId, "NO RESULT", outputColumn + "2");
  }
}
