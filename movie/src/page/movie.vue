<template>
	<div class="mmovie">
		<div class="content" v-if="movieData">
			<div class="main" :style="{backgroundImage:'url('+backdropSrc+movieData.backdrop_path+')'}">
				<div class="box">
					<div class="showbox">
						<p><rate :name="movieData.id" :value="movieData.vote_average/2"></rate></p><!-- 
						
						<p>{{movieData.vote_average}}</p> -->
						<h1>{{movieData.title}}</h1>
						<point :radius="30" :movieId="movieData.id"></point>
						<div class="tag">
							<p><span >Genres:</span><span v-for="item in movieData.genres" class="gen">{{item.name}} </span></p>
							<p><span >Release date:</span><span>{{movieData.release_date}}</span></p>
							<p><span > Companies:</span><span v-for="item in movieData.production_companies" class="com">{{item.name}} </span></p>
						</div>
						<div class="info">
							<p><span >Overview:</span><span>{{movieData.overview}}</span></p>
						</div>

						
					</div>
				</div>
			</div>	
			<div class="link">
				<div class="item">
					<div class="box">
						FILM MESSAGE
						<span class="line"></span>
					</div>
					<div class="box">
						FILM VIDEO
						<span class="line"></span>
					</div>
					<div class="box">
						FILM IMAGE
						<span class="line"></span>
					</div>
					<div class="box">
						FILM REVIEW
						<span class="line"></span>
					</div>
				</div>
			</div>
			<div class="movieMessage">
				<h1>FILM MESSAGE</h1>
				<div class="box1">
					<div class="line">
						<div class="item">
							<p>Original title</p>
							<p>{{movieData.original_title}}</p>
						</div>
						<div class="item">
							<p>Status</p>
							<p>{{movieData.status}}</p>
						</div>
						<div class="item">
							<p>Release Date</p>
							<p>{{movieData.release_date}}</p>
						</div>
						<div class="item">
							<p>Original Language</p>
							<p>{{movieData.original_language}}</p>
						</div>
					</div>
					<div class="line">
						<div class="item">
							<p>Runtime</p>
							<p>{{movieData.runtime}} m</p>
						</div>
						<div class="item">
							<p>Budget</p>
							<p>$ {{movieData.budget}}</p>
						</div>
						<div class="item">
							<p>Revenue</p>
							<p>$ {{movieData.revenue}}</p>
						</div>
						<div class="item">
							<p>Homepage</p>
							<p><a :href="movieData.homepage" v-if="movieData.homepage">{{movieData.homepage.slice(0,30)}}...</a> <span v-else>No Homepage</span></p>
						</div>
					</div>
				</div>
				<div class="box2">
					<p>CAST</p>
					<div class="line" v-if=" movieData.credits.cast">
						<div class="item" v-for="item in movieData.credits.cast.slice(0,5)">
							<img :src="basicImgSrc+item.profile_path">
							<div class="info">
								<p>{{item.name}}</p>
								<p>{{item.character}}</p>
							</div>
							
						</div>
					</div>
				</div>
			</div>
			<div class="movieVideo">
				<h1>FILM VIDEO</h1>
				<div class="box1" v-if="movieData.videos">
					<iframe width="532.73" height="300" :src='"https://www.youtube.com/embed/" +  item.key'frameborder="0" allow="autoplay; encrypted-media" allowfullscreen  v-for="item in movieData.videos.results.slice(0,5)"></iframe>
				</div>
			</div>
			<div class="movieVideo">
				<h1>FILM IMAGE</h1>
				<div class="box2" v-if="movieData.images">
					<img :src="w300backdropSrc + item.file_path" v-for="item in movieData.images.backdrops.slice(0,5)">
					<img :src="poster_sizes + item.file_path" v-for="item in movieData.images.posters.slice(0,5)">
				</div>
			</div>
			<div class="movieReview">
				<h1>FILM REVIEW</h1>
				<div class="tmdb" v-if="movieData.reviews.total_results > 0">
					<p>TMDB reviews</p>
					<p>(total:{{movieData.reviews.total_results}})</p>
					<div class="item" v-for="item in movieData.reviews.results.slice(0,5)">
						<div class="name">
							{{item.author.slice(0,1)}}
						</div>
						<div class="content">
							<p>{{item.content}}</p>
						</div>
					</div>
				</div>
				<div class="tmdb" v-if="localReviews != null ">
					<p>Local reviews</p>
					<p>(total:{{localReviews.length}})</p>
					<div class="item" v-for="item in localReviews.slice(0,5)">
						<div class="name">
							{{item.username.slice(0,1)}}
						</div>
						<div class="content">
							<p>{{item.content}}</p>
						</div>
					</div>
				</div>
				<div class="review">
					<p>review</p>
					<textarea placeholder="input your review" v-model="content"></textarea>
					<div class="btn" @click="saveReview">
						submit
					</div>
				</div>
			</div>
		</div>
		<div v-else class="loading">
			<img src="../assets/loading.gif" alt="">
		</div>
		<foot></foot>
	</div>
</template>
<script type="text/javascript">
	import foot from '@/components/foot'
	import rate from '@/components/rate'
	import point from '@/components/point'
	export default{
		components:{
			foot,rate,point
		},
		mounted(){
			if(!isNaN(this.$route.params.id))
			{
				this.axios.get('https://api.themoviedb.org/3/movie/'+this.$route.params.id+'?api_key=6e13583a127e758dac0d94b26b7068bf&append_to_response=credits,images,videos,reviews').
				then((res)=>{
					this.movieData = (res.data);
					this.checkMovieId();
					console.log(res);
				}).catch((err)=>{
					console.log(err);
				});
				this.getLoaclReviews();
			}else{
				this.$router.push({path:'/'})
			}
		},
		data(){
			return{
				movieData:null,
				backdropSrc:'https://image.tmdb.org/t/p/original',
				basicImgSrc:'https://image.tmdb.org/t/p/w185',
				w300backdropSrc:'https://image.tmdb.org/t/p/w300',
				poster_sizes:'https://image.tmdb.org/t/p/w185',
				localReviews:null,
				isSubmit:false,
				content:''
			}
		},
		methods:{
			getLoaclReviews(){
				this.axios.get('/getMovieReviews?movieId='+this.$route.params.id).
				then((res)=>{
					if(res.data.status)
						this.localReviews = res.data.reviews;
				}).catch((err)=>{
					console.log(err);
				});
			},
			checkMovieId(){
				this.axios.get('/checkMovieId?movieId='+this.$route.params.id).
				then((res)=>{
					if(res.data.status)
						this.saveMovieData();
					else
						this.userVisit();
				}).catch((err)=>{
					console.log(err);
				});
			},
			saveMovieData(){
				var gen = [],com = [],cast=[],crew = [];
				for(var i = 0; i<this.movieData.genres.length;i++)
				{
					gen.push(this.movieData.genres[i].name);
				}
				for(var i = 0; i<this.movieData.production_companies.length;i++)
				{
					com.push(this.movieData.production_companies[i].name);
				}
				for(var i = 0; i<this.movieData.credits.cast.length;i++)
				{
					cast.push(this.movieData.credits.cast[i].name);
				}
				for(var i = 0; i<this.movieData.credits.crew.length;i++)
				{
					crew.push(this.movieData.credits.crew[i].name);
				}
				this.axios.post('/saveMovie',{
					movieId:this.$route.params.id,
					title:this.movieData.title,
					cast:cast.slice(0,10),
					genres:gen,
					crew:crew.slice(0,5),
					production_companies:com,
					vote_average:this.movieData.vote_average,
				}).then((res)=>{
					this.userVisit();
				}).catch((err)=>{
					console.log(err);
				})
			},
			saveReview(){
				if(this.content == '')
					return alert('no reviews content')
				if(this.isSubmit)
					return
				this.isSubmit = true;
				this.axios.post('/saveReview',{
					movieId:this.$route.params.id,
					content:this.content
				}).then((res)=>{
					if(res.data.status)
					{
						alert('success!');
						window.location.reload();
					}else{
						alert('fail!');
						this.isSubmit = false;
					}
				}).catch((err)=>{
					console.log(err);
					this.isSubmit = false;
				})	
			},
			userVisit(){
				this.axios.get('/userVisit?movieId='+this.$route.params.id).
				then((res)=>{
					console.log(res);
				}).catch((err)=>{
					console.log(err);
				});
			}
		}
	}
</script>
<style type="text/css" lang="less" scoped>
	.mmovie{
		width: 100%;
		padding-top: 60px;
		.content{
			width: 100%;
			display: flex;
			flex-direction: column;
			align-items: center;
			.main{
				background-size: cover;
				background-repeat: no-repeat;
				width: 100%;
				height:auto;
				min-height: 800px;
				display: flex;
				justify-content: center;
				.box{
					width:1200px;
					padding:0 20px;
					display: flex;
					justify-content: flex-end;
					.showbox{
						overflow: hidden;
						box-sizing: border-box;
						padding:32px 35px 50px;
						width:460px;
						height:auto;
						min-height: 800px;
						background-color: rgba(0,0,0,0.7);
						display: flex;
						flex-direction: column;
						align-items: center;
						color:white;
						h1{
							font-size: 50px;
							margin: 0px;
							text-align: center;
							margin-bottom:10px;
						}
						>p:nth-child(3){
							margin-top:5px;
							font-size: 14px;
							color:rgba(255,255,255,0.8);
						}
						.tag{
							padding:20px 0px;
							border-top: 1px solid rgba(128,91,231,0.3);
							margin-top:10px;
							color:rgba(255,255,255,0.9);
							width:100%;
							>p:first-child{
								margin:0;
							}
							>p:last-child{
								margin-bottom: 0;
							}
							p{
								span:first-child{
									display: inline-block;
								}
								.gen{
									display: inline-block;
									border:1px solid rgba(255, 255, 255,0.7);
									color:rgba(255, 255, 255,0.7);
									padding:5px;
									border-radius: 5px;
									margin-left: 10px;
									margin-bottom: 10px;
								}
								.com{
									padding-left: 10px;
								}
								.com + .com::before{
									content:'|';
									margin-right:10px
								}
							}
							p:nth-child(2){
								span:nth-child(2){
									margin-left: 10px;
								}
							}
						}
						.info{
							padding-top: 20px;
							border-top: 1px solid rgba(128,91,231,0.3);
							>p{
								margin:0;
							}
							p{
								color:rgba(255,255,255,0.85);
								span:first-child{
									display: inline-block;
									width:110px;
								}
								span:last-child{
									font-size: 18px;
									line-height: 30px;
									word-break:break-all;
								}
							}
						}
					}
				}
			}
			.link{
				width: 100%;
				height:60px;
				display: flex;
				justify-content: center;
				background-color: white;
				border-bottom: 1px solid #d7d7d7;
				.item{
					width: 1200px;
					padding:0 20px;
					display: flex;
					justify-content: space-between;
					.box{
						display: flex;
						justify-content: center;
						align-items: center;
						font-weight: bold;
						font-size: 16px;
						position: relative;
						cursor: pointer;
						.line{
							position: absolute;
							bottom:0;
							display: inline-block;
							width: 0;
							height:5px;
							background-color: #805be7;
							left:50%;
							transform: translateX(-50%);
						}
						&:hover .line{
							animation: line both 0.4s;
						}
					}
				}
			}
			.movieMessage{
				width: 1200px;
				padding:30px 20px 0px;
				h1{
					font-size: 32px;
					line-height: 25px;
				}
				>h1::before{
					content:'';
					display: inline-block;
					width: 10px;
					height:25px;
					background-color: #805be7;
					margin-right: 10px;
				}
				.box1{
					box-sizing: border-box;
					padding:30px;
					.line{
						display: flex;
						.item{
							flex:0 0 25%;
							font-size: 16px;
							color:rgba(0,0,0,0.8);
							p:first-child{
								font-weight: bold;
							}
							p:last-child{
								text-indent: 2em;
							}
							p{
								a{
									text-decoration: none;
									color:rgba(0,0,0,0.8);
									&:hover{
										color:rgba(0,0,0,0.5);
									}
								}
							}
						}
					}
				}
				.box2{
					border-top:1px solid #d7d7d7;
					border-bottom: 1px solid #d7d7d7;
					box-sizing: border-box;
					padding:30px;
					>p:first-child{
						font-size: 16px;
						font-weight: bold;
					}
					.line{
						display: flex;
						justify-content: space-between;
						.item{
							flex: 0 0 185px;
							border:1px solid #d7d7d7;
							.info{
								box-sizing: border-box;
								padding:5px;
								p{
									margin:10px;
									font-size:14px;
								}
								p:first-child{
									font-weight: bold;
								}
							}
						}
					}
				}
			}
			.movieVideo{
				width: 1200px;
				padding:30px 20px;
				border-bottom: 1px solid #d7d7d7;
				>h1{
					font-size: 32px;
					line-height: 25px;
				}
				>h1::before{
					content:'';
					display: inline-block;
					width: 10px;
					height:25px;
					background-color: #805be7;
					margin-right: 10px;
				}
				.box1{
					padding:30px 0px 0px;
					display: flex;
					max-width: 1200px;
					overflow-x: scroll;
					iframe{
						flex: 0 0 532.73px;
					}
				}
				.box2{
					padding:30px 0px 0px;
					display: flex;
					max-width: 1200px;
					overflow-x: scroll;
					align-items: center;
					img{
						flex:1 0 auto;
					}
				}
			}
			.movieReview{
				width: 1200px;
				padding:30px 20px;
				h1{
					font-size: 32px;
					line-height: 25px;
				}
				>h1::before{
					content:'';
					display: inline-block;
					width: 10px;
					height:25px;
					background-color: #805be7;
					margin-right: 10px;
				}
				.tmdb,.myself{
					>p:first-child{
						font-weight: bold;
						font-size: 18px;
						margin-bottom: 2px;
					}
					>p:nth-child(2){
						margin:0px;
						font-size: 14px;
						color:rgba(0,0,0,0.7);
						text-indent: 2em;
					}
					.item{
						margin-top: 20px;
						box-sizing: border-box;
						padding:20px;
						display: flex;
						align-items: center;
						.name{
							flex: 0 0 50px;
							height:50px;
							border-radius: 50%;
							background-color: #d29001;
							text-align: center;
							line-height: 50px;
							margin-right: 30px;
							color:white;
						}
						.content{
							word-break: break-all;
						}
					}
				}
				.review{
					display: flex;
					flex-direction: column;
					>p:first-child{
						font-weight: bold;
					}
					textarea{
						align-self: center;
						resize: none;
						font-size: 20px;
						width:95%;
						height:80px;
						border:1px solid #d7d7d7;
						padding:10px;
						box-sizing: border-box;
						&:focus{
							outline: 0;
						}
					}
					>div{
						align-self: flex-end;
						width:80px;
						height:30px;
						background-color: #805be7;
						color:white;
						line-height: 30px;
						border-radius: 5px;
						text-align: center;
						cursor: pointer;
						margin-top: 20px;
						position: relative;
						right:50px;
					}
				}
			}
		}
		.loading{
			display: flex;
			align-items: center;
			justify-content: center;
		}
		@keyframes line{
			from{
				width:0px;
			}
			to{
				width:100%;
			}
		}
	}

	@media screen and (max-width: 1024px) {
		.mmovie{
			padding-top: 40px;
			.content{
				.main{
					height:auto;
					.box{
						width:100%;
						padding:0 10px;
						box-sizing: border-box;
						.showbox{
							padding:20px;
							width:auto;
							height:auto;
							h1{
								font-size: 28px;
								margin-bottom:20px;
							}
							.tag{
								padding:20px 0px;
								font-size: 14px;
							}
							.info{
								p{
									span:last-child{
										font-size: 14px;
										line-height:24px;
									}
								}
							}
						}
					}
				}
				.link{
					width: 100%;
					height:60px;
					display: flex;
					justify-content: center;
					background-color: white;
					border-bottom: 1px solid #d7d7d7;
					.item{
						width: 100%;
						padding:0 10px;
						box-sizing: border-box;
						.box{
							font-size: 12px;
						}
					}
				}
				.movieMessage{
					width: 100%;
					box-sizing: border-box;
					padding:10px 10px 0px;
					h1{
						font-size: 20px;
						line-height:20px;
					}
					>h1::before{
						height:18px;
					}
					.box1{
						box-sizing: border-box;
						padding:10px;
						.line{
							flex-wrap: wrap;
							.item{
								flex:0 0 50%;
								font-size: 14px;
							}
						}
					}
					.box2{
						box-sizing: border-box;
						padding:10px;
						width:100%;
						overflow-x: auto;
					}
				}
				.movieVideo{
					width: 100%;
					padding:10px;
					box-sizing: border-box;
					>h1{
						font-size: 20px;
						line-height: 20px;
					}
					>h1::before{
						height:18px;
					}
					.box1{
						max-width: 100%;
						overflow-x: scroll;
					}
					.box2{
						max-width: 100%;
						overflow-x: scroll;
					}
				}
				.movieReview{
					width: 100%;
					padding:10px;
					box-sizing: border-box;
					h1{
						font-size: 20px;
						line-height: 20px;
					}
					>h1::before{
						height:18px;
					}
					.tmdb,.myself{
						>p:first-child{
							font-weight: bold;
							font-size: 16px;
							margin-bottom: 2px;
						}
						.item{
							margin-top: 20px;
							box-sizing: border-box;
							padding:10px;
							display: flex;
							align-items: center;
							.name{
								margin-right: 15px;
							}
							.content{
								word-break: break-all;
								font-size: 14px;
							}
						}
					}
					.review{
						display: flex;
						flex-direction: column;
						>p:first-child{
							font-weight: bold;
						}
						textarea{
							align-self: center;
							resize: none;
							font-size: 20px;
							width:95%;
							height:80px;
							border:1px solid #d7d7d7;
							padding:10px;
							box-sizing: border-box;
							&:focus{
								outline: 0;
							}
						}
						>div{
							align-self: flex-end;
							width:80px;
							height:30px;
							background-color: #805be7;
							color:white;
							line-height: 30px;
							border-radius: 5px;
							text-align: center;
							cursor: pointer;
							margin-top: 20px;
							position: relative;
							right:50px;
						}
					}
				}
			}
			.loading{
				display: flex;
				align-items: center;
				justify-content: center;
			}
			@keyframes line{
				from{
					width:0px;
				}
				to{
					width:100%;
				}
			}
	}
	}
</style>