const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/movie_recommend');
const db = mongoose.connection;

db.on('open',(date)=>{
	// console.log(date);
	console.log("db connect success");
});

db.on('error',(err)=>{
	console.error(err);
	console.error("db connection error");
});

const userlinks = db.collection('userlinks');
userlinks.findOne({},(err,data)=>{
	if (err) console.log(err)
	console.log(data)
})
