const express = require('express');
const request = require('request');
const cors = require('cors');
const app = express();

// Link to your API Url here
const apiUrl = '<insert your url here>';


app.use(cors());
app.use(express.json());
const port = 2017;

app.post('/', function(req, res) {
    let options = {
        url: apiUrl,
        method: 'POST',
        json: req.body
    }
    res.contentType('application/json');
    request(options, function(error, response, body) {
        if (!error && response.statusCode == 200) {
            res.json(body);
        } else {
            let failure = {
                "statusCode" : response.statusCode,
                "message" : error
            }
            res.json(failure);
        }
    });
});

app.listen(port, () => console.log(`App listening on port ${port}!`));