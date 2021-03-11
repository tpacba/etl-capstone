

const writeJSON = async () => {
    const MongoClient = require('mongodb').MongoClient;
    const fs = require('fs')

    const uri = "mongodb+srv://tpacba:OneYear_95@cluster0.ufwrg.mongodb.net/station_data?retryWrites=true&w=majority";
    const client = await MongoClient.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true });
      
    const db = client.db("station_data");
    var stations = await db.collection('list_stations').find({}).toArray();
    
    const jsonString = await JSON.stringify(stations)
  
    await fs.writeFile('./weather_stations.json', jsonString, err => {
      if (err) {
          console.log('Error writing file', err)
      } else {
          console.log('Successfully wrote file')
      }
    })
  
    client.close();
}

export { writeJSON };