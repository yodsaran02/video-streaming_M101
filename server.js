const express = require('express');
const fs = require('fs');

const app = express();


app.get('/video/:subject/:name', (req, res) => {
    const range = req.headers.range;
    const videoPath = 'Video/'+ req.params.subject +'/'+ req.params.name + '.mp4';
    const videoSize = fs.statSync(videoPath).size;
    
    res.sendfile(videoPath, { root:__dirname });
});

app.listen('3000');
