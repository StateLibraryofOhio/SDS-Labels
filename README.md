# SDS-Labels

SDS-Labels is a static web-based application for generating shipping labels to be used by the Statewide Delivery System, a service managed and coordinated by the State Library of Ohio. More information about the service can be found on the [State Library's website](https://library.ohio.gov/services-for-libraries/statewide-delivery/).

## Tools Used

SDS Labels uses the following libraries:
* [Bootstrap 5.0 alpha](https://v5.getbootstrap.com)
* [TaffyDB](https://github.com/typicaljoe/taffydb)

## Notes on Usage
TaffyDB consumes a JSON file, `output.json`, of the shipping label data and creates a JavaScript-like database of the entries:

```javascript
// Initialise TaffyDB from JSON file
function initDB() {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            data = JSON.parse(this.responseText);
            db = TAFFY(data);
            db.sort("name"); // Alphabetize
            loadOptions();
        }
    };
    xmlhttp.open("GET", "output.json", true);
    xmlhttp.send();
}
```
If the JSON structure is malformed, the entries will __not__ populate the dropdown menus. If the dropdown menus are empty, verify the structure of the JSON data, and correct it. A single label object will look like the following:

```json
  {
    "id": 9999,
    "libid": 900,
    "name": "A Single Library",
    "address": "123 Very Nice Rd.",
    "city": "Columbus",
    "state": "OH",
    "zip": 43201,
    "seo": "XXX",
    "hub": "ZZZ",
    "route": 9999,
    "latitude": "39.98153098",
    "longitude": "-82.99600477",
    "is_primary": true
  }
```

The `output.json` content may occasionally need to be updated to add entries as new libraries enter the program.  When adding a new library, append their new entry to the end of the `output.json` file and increment the previous entry's `id` value by "1" to get the value for your new entry.  It is not necessary for new entries to be sorted alphabetically in the output.json file; the libraries will be displayed alphabetically in the web form.  The critical thing to remember is that the `id` value must be unique.

When adding a branch location for an existing library in the list, you can duplicate the "libid" value for the branch, but the "is_primary" value must be set to "false" for the new branch.  Only 1 entry per libid can be flagged as "true" in the "is_primary" field.
