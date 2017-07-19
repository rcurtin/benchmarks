// Define namespace: sc = sweep comparison.
var sc = sc = sc || {};

sc.method_name = "";
sc.param_name = "";
sc.dataset = "";
sc.libraries = [];
sc.active_libraries = [];
sc.results = [];

// This chart type has been selected.
sc.onTypeSelect = function()
{
  // The user needs to be able to select a method, then parameters, then a
  // dataset.
  var selectHolder = d3.select(".selectholder");
  selectHolder.append("label")
      .attr("for", "method_select")
      .attr("class", "method-select-label")
      .text("Select method:");
  selectHolder.append("select")
      .attr("id", "method_select")
      .attr("onchange", "sc.methodSelect()");
  selectHolder.append("label")
      .attr("for", "param_select")
      .attr("class", "param-select-label")
      .text("Select parameters:");
  selectHolder.append("select")
      .attr("id", "param_select")
      .attr("onchange", "sc.paramSelect()");
  selectHolder.append("label")
        .attr("for", "main_dataset_select")
        .attr("class", "main-dataset-select-label")
        .text("Select dataset:");
  selectHolder.append("select")
        .attr("id", "main_dataset_select")
        .attr("onchange", "sc.datasetSelect()");

  sc.listMethods();
}

// List the available methods where there is a sweep.
sc.listMethods = function()
{
  var methods = dbExec("SELECT DISTINCT methods.name FROM methods, results "
      + "WHERE methods.id = results.method_id AND methods.sweep_id != -1 "
      + "ORDER BY name;");
  var methodSelectBox = document.getElementById("method_select");

  // Remove old things.
  clearSelectBox(methodSelectBox);

  // Add new things.
  var length = dbType === "sqlite" ? methods[0].values.length : methods.length;
  for (i = 0; i < length; i++)
  {
    var newOption = document.createElement("option");
    newOption.text = dbType === "sqlite" ? methods[0].values[i] :
        methods[i].name;
    methodSelectBox.add(newOption);
  }
  methodSelectBox.selectedIndex = -1;

  // Clear parameters box.
  clearSelectBox(document.getElementById("param_select"));
}

// Called when the user selects a method.
sc.methodSelect = function()
{
  // Extract the name of the method we selected.
  var methodSelectBox = document.getElementById("method_select");
  sc.methodName = methodSelectBox.options[methodSelectBox.selectedIndex].text; // At higher scope.

  var sqlstr = "SELECT DISTINCT methods.parameters, methods.sweep_id, " +
      "metrics.libary_id, COUNT(DISTINCT metrics.libary_id) AS count FROM " +
      "methods, metrics WHERE methods.name = '" + sc.method_name +
      "' AND methods.id = metrics.method_id AND methods.sweep_id != -1 " +
      "GROUP BY methods.parameters;";
  var params = dbExec(sqlstr);
  console.log(JSON.stringify(params));

  // Loop through results and fill the second list box.
  var paramSelectBox = document.getElementById("param_select");
  clearSelectBox(paramSelectBox);

  var newOption = document.createElement("option");
  param_select_box.add(newOption);

  if ((dbType === "sqlite" && params[0]) || (dbType === "mysql" && params))
  {
    // Put in the new options.
    var length = dbType === "sqlite" ? params[0].values.length : params.length;
    for (i = 0; i < length; i++)
    {
      var newOption = document.createElement("option");

      var parameters = dbType === "sqlite" ? params[0].values[i][0] : params[i].parameters;
      var sweepId = dbType === "sqlite" ? params[0].values[i][1] : params[i].sweep_id;
      var libraries = dbType === "sqlite" ? params[0].values[i][3] : params[i].count;

      if (parameters)
      {
        newOption.text = parameters + " (" + libraries + " libraries)";
      }
      else
      {
        newOption.text = "[no parameters] (" + libraries + " libraries)";
      }
      newOption.id = sweepId;

      paramSelectBox.add(newOption);
    }
  }

  paramSelectBox.selectedIndex = 0;
}

// Called when the user selects parameters.
// Called when a set of parameters is selected.  Now we are ready to draw the
// chart.
rc.paramSelect = function()
{
  // The user has selected a library and parameters.  Now we need to generate
  // the list of datasets.
  var methodSelectBox = document.getElementById("method_select");
  rc.method_name = methodSelectBox.options[methodSelectBox.selectedIndex].text;
  var paramSelectBox = document.getElementById("param_select");
  var paramNameFull = paramSelectBox.options[paramSelectBox.selectedIndex].text;
  var sweepId = paramSelectBox.options[paramSelectBox.selectedIndex].id;

  sc.param_name = param_name_full.split("(").slice(0, -1).join("(").replace(/^\s+|\s+$/g, ''); // At higher scope.

  var sqlstr = "SELECT DISTINCT datasets.name FROM datasets, results, methods "
      + "WHERE datasets.id = results.dataset_id AND methods.name = '"
      + sc.method_name + "' AND methods.sweep_id = " + sweepId + " AND "
      + "results.method_id = methods.id AND methods.parameters = " + sc.paramName
      + ";";
  var datasets = dbExec(sqlstr);
  console.log(JSON.stringify(params));

  // Loop through the results and fill the third list box.
  var datasetSelectBox = document.getElementById("dataset_select");
  clearSelectBox(datasetSelectBox);

  var newOption = document.createElement("option");
  datasetSelectBox.add(newOption);

  if ((dbType === "sqlite" && datasets[0]) || (dbType === "mysql" && datasets))
  {
    // Put in the datasets.
    var length = dbType === "sqlite" ? datasets[0].values.length : datasets.length;
    for (i = 0; i < length; i++)
    {
      newOption = document.createElement("option");

      var datasetName = dbType === "sqlite" ? datasets[0].values[i][0] : datasets[i].name;
      newOption.text = datasetName;
      datasetSelectBox.add(newOption);
    }
  }

  datasetSelectBox.selectedIndex = 0;
}
