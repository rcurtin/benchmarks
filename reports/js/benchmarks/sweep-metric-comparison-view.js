// Define namespace: smc = sweep metric comparison.
var smc = smc = smc || {};

smc.methodName = "";
smc.paramName = "";
smc.dataset = "";
smc.libraries = [];
smc.activeLibraries = [];
smc.results = [];
smc.sweepId = -1;

// This chart type has been selected.
smc.onTypeSelect = function()
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
      .attr("onchange", "smc.methodSelect()");
  selectHolder.append("label")
      .attr("for", "param_select")
      .attr("class", "param-select-label")
      .text("Select parameters:");
  selectHolder.append("select")
      .attr("id", "param_select")
      .attr("onchange", "smc.paramSelect()");
  selectHolder.append("label")
      .attr("for", "main_dataset_select")
      .attr("class", "main-dataset-select-label")
      .text("Select dataset:");
  selectHolder.append("select")
      .attr("id", "main_dataset_select")
      .attr("onchange", "smc.datasetSelect()");
  selectHolder.append("label")
      .attr("for", "metric_select")
      .attr("class", "metric-select-label")
      .text("Select metric:");
  selectHolder.append("select")
      .attr("id", "metric_select")
      .attr("onchange", "smc.metricSelect()");

  smc.listMethods();
}

// List the available methods where there is a sweep.
smc.listMethods = function()
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
smc.methodSelect = function()
{
  // Extract the name of the method we selected.
  var methodSelectBox = document.getElementById("method_select");
  smc.methodName = methodSelectBox.options[methodSelectBox.selectedIndex].text; // At higher scope.

  var sqlstr = "SELECT DISTINCT methods.parameters, methods.sweep_id, " +
      "metrics.libary_id, COUNT(DISTINCT metrics.libary_id) AS count FROM " +
      "methods, metrics WHERE methods.name = '" + smc.methodName +
      "' AND methods.id = metrics.method_id AND methods.sweep_id != -1 " +
      "GROUP BY methods.parameters;";
  var params = dbExec(sqlstr);
  console.log(JSON.stringify(params));

  // Loop through results and fill the second list box.
  var paramSelectBox = document.getElementById("param_select");
  clearSelectBox(paramSelectBox);

  var newOption = document.createElement("option");
  paramSelectBox.add(newOption);

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
smc.paramSelect = function()
{
  // The user has selected a library and parameters.  Now we need to generate
  // the list of datasets.
  var methodSelectBox = document.getElementById("method_select");
  smc.methodName = methodSelectBox.options[methodSelectBox.selectedIndex].text;
  var paramSelectBox = document.getElementById("param_select");
  var paramNameFull = paramSelectBox.options[paramSelectBox.selectedIndex].text;
  var sweepId = paramSelectBox.options[paramSelectBox.selectedIndex].id;

  smc.paramName = paramNameFull.split("(").slice(0, -1).join("(").replace(/^\s+|\s+$/g, ''); // At higher scope.

  var sqlstr = "SELECT DISTINCT datasets.name FROM datasets, results, methods "
      + "WHERE datasets.id = results.dataset_id AND methods.name = '"
      + smc.methodName + "' AND methods.sweep_id = " + sweepId + " AND "
      + "results.method_id = methods.id AND methods.parameters = '" + smc.paramName
      + "';";
  var datasets = dbExec(sqlstr);
  console.log(JSON.stringify(datasets));

  // Loop through the results and fill the third list box.
  var datasetSelectBox = document.getElementById("main_dataset_select");
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

smc.datasetSelect = function()
{
  // The user selected a dataset, so now we can plot.
  var methodSelectBox = document.getElementById("method_select");
  smc.methodName = methodSelectBox.options[methodSelectBox.selectedIndex].text;
  var paramSelectBox = document.getElementById("param_select");
  var paramNameFull = paramSelectBox.options[paramSelectBox.selectedIndex].text;
  smc.sweepId = paramSelectBox.options[paramSelectBox.selectedIndex].id;
  var datasetSelectBox = document.getElementById("main_dataset_select");
  var datasetName =
      datasetSelectBox.options[datasetSelectBox.selectedIndex].text;

  smc.paramName = paramNameFull.split("(").slice(0, -1).join("(").replace(/^\s+|\s+$/g, '');

  // What metrics do we have available?
  // TODO: from here
}

smc.metricSelect = function()

  var sqlstr = "SELECT DISTINCT * FROM "
      + "(SELECT results.time as time, results.var as var, "
      + "        results.sweep_elem_id as sweep_elem_id, libraries.name as lib,"
      + "        max(results.build_id) as bid, datasets.instances as di, "
      + "        datasets.attributes as da, datasets.size as ds"
      + " FROM results, datasets, methods, libraries"
      + " WHERE results.dataset_id = datasets.id"
      + "   AND results.method_id = methods.id"
      + "   AND methods.name = '" + smc.methodName + "'"
      + "   AND methods.parameters = '" + smc.paramName + "'"
      + "   AND libraries.id = results.libary_id"
      + "   AND datasets.name = '" + datasetName + "'"
      + " GROUP BY lib, sweep_elem_id)"
      + "tmp GROUP BY sweep_elem_id, lib;";

  smc.results = dbExec(sqlstr);
  smc.results = dbType === "sqlite" ? sc.results[0].values : sc.results;

  // Obtain unique list of libraries.
  smc.libraries = sc.results.map(
      function(d) {
          return dbType === "sqlite" ? d[3] : d.lib;
      }).reduce(
      function(p, c) {
          if (p.indexOf(c) < 0) p.push(c); return p;
      }, []);

  // By default, all libraries are active.
  smc.activeLibraries = {};
  for (i = 0; i < smc.libraries.length; ++i)
  {
    smc.activeLibraries[sc.libraries[i]] = true;
  }

  clearChart();
  buildChart();
}

smc.clearChart = function()
{
  d3.select("svg").remove();
}

smc.buildChart = function()
{
  smc.results = sc.results.map(
      function(d)
      {
        var runtime = dbType === "sqlite" ? d[0] : d.time;
        if (runtime == -2)
        {
          if (dbType === "sqlite")
            d[0] = "failure";
          else
            d.time = "failure";
        }
        else if (runtime == -1)
        {
          if (dbType === "sqlite")
            d[0] = ">9000";
          else
            d.time = "failure";
        }

        return d;
      });

    // Get the parameter name we are sweeping.
  var params = JSON.parse(smc.paramName);
  var name = "";
  for (var i in params)
  {
    if (params[i].search(/sweep\(/) !== -1)
    {
      name = i;
      break;
    }
  }

  // Get lists of active libraries.
  var activeLibraryList = smc.libraries.map(function(d) { return d; }).reduce(
      function(p, c)
      {
        if (smc.activeLibraries[c] == true) 
          p.push(c);
        return p;
      }, []);

  var maxRuntime = d3.max(smc.results,
      function(d)
      {
        if (smc.activeLibraries[dbType === "sqlite" ? d[3] : d.lib] == false)
          return 0;
        else
          return mapRuntime(dbType === "sqlite" ? d[0] : d.time, 0);
      });
  // Increase so we have 16 spare pixels at the top.
  maxRuntime *= ((height + 16) / height);

  var runtimeScale = d3.scale.linear()
      .domain([0, maxRuntime])
      .range([height, 0]);

  // We need to find out how big the sweep is.
  var sweepSql = "SELECT type, begin, step, end FROM sweeps where id = " + smc.sweepId;
  var sweepResults = dbExec(sweepSql);
  sweepResults = dbType === "sqlite" ? sweepResults[0].values : sweepResults.results;

  var func = (dbType === "sqlite" ? sweepResults[0][0] : sweepResults[0].type) === "int" ? parseInt : parseFloat;
  var start = func(dbType === "sqlite" ? sweepResults[0][1] : sweepResults[0].start);
  var step = func(dbType === "sqlite" ? sweepResults[0][2] : sweepResults[0].step);
  var end = func(dbType === "sqlite" ? sweepResults[0][3] : sweepResults[0].end);

  var sweepScale = d3.scale.linear()
      .domain([start, end])
      .range([0, width]);

  var xAxis = d3.svg.axis().scale(sweepScale).orient("bottom");
  var yAxis = d3.svg.axis().scale(runtimeScale).orient("left").tickFormat(d3.format(".2f"));

  // Create svg object.
  var svg = d3.select(".svgholder").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Add x axis.
  svg.append("g").attr("id", "xaxis")
      .attr("class", "x axis")
      .attr("transform", "translate(0, " + height + ")")
      .call(xAxis)
      .append("text")
      .style("text-anchor", "end")
      .attr("dx", 500)
      .attr("dy", "3em")
      .text("Value of parameter '" + name + "'");

  // Add y axis.
  svg.append("g").attr("id", "yaxis")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Runtime (s)");

  // Create tooltips.
  var tip = d3.tip()
      .attr("class", "d3-tip")
      .offset([-10, 0])
      .html(function(d) {
          var runtime = d[0];
          if (d[0] != ">9000" && d[0] != "failure") {
            runtime = d[0].toFixed(2);
          }
          return "<strong>" + d[3] + "; " + name + ": " + (start + step * d[2]) + ":</strong> <span style='color:yellow'>" + runtime + "s</span>"; });
  svg.call(tip);

  // Add all of the data points.
  var lineFunc = d3.svg.line()
      .x(function(d) { return sweepScale(dbType === "sqlite" ? start + step * d[2] : start + step * d.sweep_elem_id); })
      .y(function(d) { return runtimeScale(mapRuntime(
          dbType === "sqlite" ? d[0] : d.time, maxRuntime)); })
      .interpolate("linear");

  var lineResults = []
  for (var l in smc.libraries)
  {
    if (smc.activeLibraries[sc.libraries[l]] == true)
    {
      lineResults.push(smc.results.map(function(d) { return d; }).reduce(function(p, c) { if(c[3] == sc.libraries[l]) { p.push(c); } return p; }, []));
    }
    else
    {
      lineResults.push([]);
    }
  }

  for (i = 0; i < lineResults.length; ++i)
  {
    console.log(JSON.stringify(lineResults[i]));
    if (lineFunc(lineResults[i]) != null)
    {
      svg.append('svg:path')
          .attr('d', lineFunc(lineResults[i]))
          .attr('stroke', color(smc.libraries[i]))
          .attr('stroke-width', 2)
          .attr('fill', 'none');
    }
  }

  for (i = 0; i < lineResults.length; i++)
  {
    if (lineFunc(lineResults[i]) == null)
      continue;

    // Colored circle enclosed in white circle enclosed in background color
    // circle; looks kind of nice.
    svg.selectAll("dot").data(lineResults[i]).enter().append("circle")
        .attr("r", 6)
        .attr("cx", function(d) { return sweepScale(dbType === "sqlite" ? start + step * d[2] : start + step * d.sweep_elem_id); })
        .attr("cy", function(d) { return runtimeScale(mapRuntime(dbType === "sqlite" ? d[0] : d.time, maxRuntime)); })
        .attr('fill', '#222222')
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
    svg.selectAll("dot").data(lineResults[i]).enter().append("circle")
        .attr("r", 4)
        .attr("cx", function(d) { return sweepScale(dbType === "sqlite" ? start + step * d[2] : start + step * d.sweep_elem_id); })
        .attr("cy", function(d) { return runtimeScale(mapRuntime(dbType === "sqlite" ? d[0] : d.time, maxRuntime)); })
        .attr('fill', '#ffffff')
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
    svg.selectAll("dot").data(lineResults[i]).enter().append("circle")
        .attr("r", 3)
        .attr("cx", function(d) { return sweepScale(dbType === "sqlite" ? start + step * d[2] : start + step * d.sweep_elem_id); })
        .attr("cy", function(d) { return runtimeScale(mapRuntime(dbType === "sqlite" ? d[0] : d.time, maxRuntime)); })
        .attr('fill', function(d) { return color(d[4]) })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
  }

  // Create the library selector.
  var librarySelectTitle = d3.select(".legendholder").append("div")
    .attr("class", "library-select-title");
  librarySelectTitle.append("div")
    .attr("class", "library-select-title-text")
    .text("Libraries:");
  librarySelectTitle.append("div")
    .attr("class", "library-select-title-open-paren")
    .text("(");
  librarySelectTitle.append("div")
    .attr("class", "library-select-title-enable-all")
    .text("enable all")
    .on('click', function() { smc.enableAllLibraries(); });
  librarySelectTitle.append("div")
    .attr("class", "library-select-title-bar")
    .text("|");
  librarySelectTitle.append("div")
    .attr("class", "library-select-title-disable-all")
    .text("disable all")
    .on('click', function() { smc.disableAllLibraries(); });
  librarySelectTitle.append("div")
    .attr("class", "library-select-title-close-paren")
    .text(")");

  var libraryDivs = d3.select(".legendholder").selectAll("input")
    .data(smc.libraries)
    .enter()
    .append("div")
    .attr("class", "library-select-div")
    .attr("id", function(d) { return d + '-library-checkbox-div'; });

  libraryDivs.append("label")
    .attr('for', function(d) { return d + '-library-checkbox'; })
    .style('background', color)
    .attr('class', 'library-select-color');

  libraryDivs.append("input")
    .property("checked", function(d) { return smc.activeLibraries[d]; })
    .attr("type", "checkbox")
    .attr("id", function(d) { return d + '-library-checkbox'; })
    .attr('class', 'library-select-box')
    .attr("onClick", function(d, i) { return "smc.toggleLibrary(\"" + d + "\");"; });

  libraryDivs.append("label")
    .attr('for', function(d) { return d + '-library-checkbox'; })
    .attr('class', 'library-select-label')
    .text(function(d) { return d; });
}

// Toggle a library to on or off.
smc.toggleLibrary = function(library)
{
  smc.activeLibraries[library] = !hc.activeLibraries[library];

  clearChart();
  buildChart();
}

// Set all libraries on.
smc.enableAllLibraries = function()
{
  for (v in smc.activeLibraries) { hc.activeLibraries[v] = true; }

  clearChart();
  buildChart();
}

// Set all libraries off.
smc.disableAllLibraries = function()
{
  for (v in hc.activeLibraries) { hc.activeLibraries[v] = false; }

  clearChart();
  buildChart();
}
