# LiteratureSurvey

This code uses different formats to achieve the visualized literature survey:

- **CSV** (`LitMatrix2.csv`... actually it is currently reading `LitMatrix2.tsv`, so a *tab* sepparated file) to hold the literature information, created from a spreadsheet software, for which each column will represent a classification---displayed later as one of the segments in the ring
- **Python** (`LitReview_csv2json.py`) to convert the CSV file to a JSON file that can be read by JavaScript
- **JSON** (`litRev.json`) that works as the survey data holder that is readable by JavaScript
- **JavaScript** (contained in `index.html`) which reads in the JSON-formatted data and displays it using the [D3.js](https://d3js.org/) library
- **HTML** to hold everything together

## How to prepare the data

1. Modify the ODS spreadsheet for each entry, and for each classification use a comma (',') within each cell to add multiple values
2. Add, remove or modify classifications by adding, removing or renaming columns... naturally, watch out because there's limited space in the ring to hold all the classifications... some editing of the JavaScript code in `index.html` might be necessary to keep aesthetics
3. Export to `.tsv` (tab separated), which is the current format that `LitReview_csv2json.py` translates to JSON (despite its name). **Of course, Python (above 2.7) is needed for this!**
   ```python
   data = pd.read_table('LitMatrix2.tsv',
        sep='\t',
        )
    ```

## How to publish

1. Get a webserver. Things are different if it's locally hosted, or externally, and what the external option supports and can hold.
2. Publish the `index.html` to your website directory (can be `/var/www/` if locally hosted). Also carry the file `d3.v3.min.js` with you to that folder (`index.html` points to it to read the D3 library):
   ```javascript
   <body>
    <script src="d3.v3.min.js"></script>
    <script>
   ```
3. Modify `index.html` to point to the location of `litRev.json`. In my case, I hosted it in a public folder in Dropbox, such that is it globally accessible, and more importantly, by the webserver:
   ```javascript
   var link = svg.append("g").selectAll(".link"),
   node = svg.append("g").selectAll(".node");
   var parents = [];

   d3.json("https://dl.dropboxusercontent.com/u/5045165/Literature%20Survey/litRev.json", function(error, classes) {

   // DO THE CLUSTER VISUALIZATION
   var nodes = cluster.nodes(packageHierarchy(classes)),
   links = packageImports(nodes); 
   ```