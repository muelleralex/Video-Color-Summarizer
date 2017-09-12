// functon to covert RGB values in the JSON file to a format usable for SVG
// colors (i.e. rgb(24,24,24))
function vcs_extract_color(data) {
  var R = data["R"],
      G = data["G"],
      B = data["B"];

  return "rgb(" + R + "," + G + "," + B + ")";
}

// renders pie chart from the JSON file
function vcs_render_pie(file_name) {
    // initialize width, height, and radius
    var width = 960,
        height = 500,
        radius = Math.min(width, height) / 2;

    // find vcs_div and set its width
    var vcs_div = document.getElementById("vcs_pie");
    vcs_div.style.width = width + "px";

    // create SVG
    var svg = d3.select("#vcs_pie")
                .append("svg")
                    .attr("width", width)
                    .attr("height", height);

    // append g for the pie chart
    var g = svg.append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    // read json file
    d3.json(file_name, function(error, data) {
        if (error) throw error;
        // initialize data structures for the pie chart
        var pie_data_array = [],
            k = data[0]['clusters'];
        // create cleaner array for color percentages
        for(var i=0;i<k;i++) { pie_data_array.push(data[0]['all_frame'][i]); }
        // create pie chart function based on color percentages
        var pie = d3.pie()
                    .sort(null)
                    .value(function(d) { return d.percent; });
        // create arc data
        var path = d3.arc()
                     .outerRadius(radius - 10)
                     .innerRadius(0);
        // draw the sections
        var arc = g.selectAll(".arc")
                   .data(pie(pie_data_array))
                   .enter().append("g")
                        .attr("class", "arc");
        // color the sections
        arc.append("path")
            .attr("d", path)
            .attr("fill", function(d) { return vcs_extract_color(d.data); });
    })
}

// renders the bar graph using the JSON file
function vcs_render_bars(file_name) {
    // set width of SVG, height is dependent on the JSON data
    var width = 800,
        // block_height is height of each row
        block_height = 7,
        y = 0.0;

    // create the svg
    var svg = d3.select("#vcs_bars")
                .append("svg")
                .attr("width", width);

    // set the vcs_bars div to the appropriate width
    var vcs_div = document.getElementById("vcs_bars");
    vcs_div.style.width = width + "px";

    // access the JSON file
    d3.json(file_name, function(error, data) {
        // set the svg's height
        svg.attr("height", data[0]["bars"] * block_height);

        // isolate the number of clusters used to create the data
        var k = data[0]["clusters"],
            skip_zero = false;

        // create the rows
        data.forEach(function(d) {
            // the first row is filled with metadata
            if (!skip_zero) {
                skip_zero = true;
                return;
            }

            // isolate the colors and create a new svg element
            var colors = d['colors'],
                g = svg.append("g"),
                x = 0.0;

            // create the k rectangles that make up each row
            for(var i=0; i<k; i++) {
                g.append("rect")
                    .attr("width", width*colors[i]["percent"])
                    .attr("height", block_height)
                    .attr("fill", vcs_extract_color(colors[i]))
                    .attr("transform", "translate(" + x + "," + y + ")");
                // shift for the next row
                x += width*colors[i]["percent"];
            }
            y += block_height;

        })

    })
}

// sets the background color to the most prominent color in the data
function vcs_set_background(file_name) {
  var body = document.body;

  // search for the color with the highest percentage in the all_frames data
  d3.json(file_name, function(error, data) {
    var colors = data[0]['all_frame'];
    var max_percentage = -1;
    var max_color = "rgb(255,255,255)";
    for(var i = 0;i<data[0]['clusters']; i++) {
      if (parseFloat(colors[i]['percent']) > max_percentage) {
        max_color = vcs_extract_color(colors[i]);
        max_percentage = parseFloat(colors[i]['percent']);
      }
    }
    body.style.background = max_color;
  });
}

// probably not useful to most people but I made it anyways
// it sets the inner text of a span element to show the title of the movie
function vcs_set_title(title) {
  var vcs_title = document.getElementById('vcs_title');
  vcs_title.innerHTML = title;
}

// easy way to call of of the above functions
function vcs_total(file_name, title) {
  vcs_render_bars(file_name);
  vcs_render_pie(file_name);
  vcs_set_background(file_name);
  vcs_set_title(title);
}
