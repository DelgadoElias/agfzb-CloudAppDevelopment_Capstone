const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const Cloudant = require('@cloudant/cloudant');

async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: 'z7SIqB9MKWuWIi849llAYBOAgj5g7yB3oXiXgJLR-MX9' } },
            url: 'https://3aa297bd-7a6c-4bd8-b39b-ed6410efe4e8-bluemix.cloudantnosqldb.appdomain.cloud',
        });
        const db = cloudant.use('dealerships');
        console.info('¡Connection Success! CLoudant DB Connected');
        return db;
    } catch (err) {
        console.error('COnnection failure: ' + err.message + ' for cloudant db');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

app.get('/api/dealership', async (req, res) => {
    const { state, id } = req.query;

    const selector = {};
    
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id);
    }

    const queryOptions = {
        selector,
        limit: 10,
    };

    try {
        const body = await db.find(queryOptions);
        const dealerships = body.docs;
        if(dealerships.length > 0) {
            res.json(dealerships);
        } else {
            res.status(404).json({ error: 'The database is empty'})
        }
    } catch (err) {
        console.error('Something went wrong on the server:', err);
        res.status(500).json({ error: 'Something went wrong on the server' });
    }
});

app.listen(port, () => {
    console.log(`Server running at port: ${port}`);
});
