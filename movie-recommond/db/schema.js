const m =  require('./db_connect');
const mongoose = m.mongoose
// /^[A-z]{3,}$/
var userSchema = mongoose.Schema({
	id:Number,
	name:String,
	password:String,
	sign_in_time:String,
	watch:[{
		movieName:String,
		movieId:Number,
	}],
	total_rate:Number,
	rates:[{
		movieId:Number,
		rate:Number
	}],
	reviews:[{
		movieName:String,
		movieId:Number,
		content:String,
		time:String
	}],
	logMes:[{
		logtime:String,
		ip:String
	}]
});

var user = mongoose.model('user',userSchema);

var  movieSchema = mongoose.Schema({
	movieId:Number,
	title:String,
	cast:[String],
	genres:[String],
	production_companies:[String],
	crew:[String],
	vote_average:Number,
	rate:[{
		username:String,
		time:String,
		rate:Number
	}],
	reviews:[{
		username:String,
		time:String,
		content:String
	}]
});

var movie = mongoose.model('movie',movieSchema);

var rateSchema = mongoose.Schema({
	username:String,
	userId:Number,
	movieId:Number,
	time:String,
	rate:Number
})
var rate = mongoose.model('rate',rateSchema);

var dateSchema = mongoose.Schema({
	date:String,
	visit_num:Number,
	register:Number,
	watch_movie:mongoose.Schema.Types.Mixed,
	review_movie:mongoose.Schema.Types.Mixed,
	rate_movie:mongoose.Schema.Types.Mixed,
	review_movie_detail:[{
		movieId:Number,
		user:String,
		content:String,
		time:String
	}],
	logs:[{
		time:String,
		log:String,
		ip:String
	}]
})

var date = mongoose.model('date',dateSchema);

module.exports = {user,movie,rate,date};