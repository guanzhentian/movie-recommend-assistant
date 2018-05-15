<template>
	<div class="mrecommend" >
		<div class="content":style="{backgroundImage:'url('+bg+')'}">
			<div class="main" v-if="movieData &&  movieData.length && movieData.length>0" >
				<div class="box"v-for="item in movieData" @click="getDetail(item.id)">
					<img :src="basicImgSrc + item.poster_path" alt="">
					<div class="detail">
						<h1>{{item.original_title}}</h1>
						<p>
							<span><strong>Movie Rating :</strong></span>
							<rate :value="item.vote_average/2" :name="item.id"></rate>
						</p>
						<p><strong>Tagline </strong>: {{item.tagline}}</p>
						<!-- <p><strong>Movie Rating </strong>: {{item.vote_average/2}}</p> -->
						
						<p><strong>Overview </strong>: {{item.overview}}</p>
						<p class="genres">
							<strong>Genres </strong>:
							<span v-for="item2 in item.genres">{{item2.name}}</span>
						</p>
						<p class="cast"><strong>Cast </strong>:
							<span v-for="item3 in item.credits.cast.slice(0,5)">{{item3.name}}</span>
						</p>
					</div>
				</div>
			</div>
			<div v-else class="loading">
				<img src="../assets/loading.gif" alt="">
			</div>
		</div>
		<foot></foot>
	</div>
</template>
<script type="text/javascript">
	import foot from '@/components/foot'
	import rate from '@/components/rate'
	export default{
		components:{
			foot,rate
		},
		data(){
			return{
				basicImgSrc:'https://image.tmdb.org/t/p/w500',
				movieData:[],
				bg:require('../assets/6.jpg'),
				list:[],
				itemList:[],
				// testData:{status: true, mes: "488,1578,238,278,240,"}
			}
		},
		mounted(){
			this.axios.get('/getRecommend').then((res)=>{
				if(res.data.status)
				{
					var list = res.data.mes.split(',');
					list.pop();
					this.list = list;
					this.getMovie();
				}else{
					console('fail'+res.data.msg);
				}
				this.axios.get('/getItemRecommend').then((res)=>{
					if(res.data.status)
					{
						var list = res.data.mes.split(',');
						list.pop();
						this.itemList = list;
						this.getItemMove();
					}else{
						alert('fail '+res.data.msg);
						this.$router.push({path:'/'});
					}
				}).catch((err)=>{
					console.log(err);
					this.$router.push({path:'/'});
				})
			}).catch((err)=>{
				console.log(err);
				this.$router.push({path:'/'});
			})
			
			// test
			// var list = this.testData.mes.split(',');
			// list.pop();
			// this.list = list;
			// this.getMovie();
		},
		methods:{
			getDetail(id){
				this.$router.push({path:'/movie/'+id})
			},
			getMovie(){
				this.movieData = [];
				for(var i = 0;i<this.list.length;i++)
				{
					this.axios.get('https://api.themoviedb.org/3/movie/'+this.list[i]+'?api_key=6e13583a127e758dac0d94b26b7068bf&append_to_response=credits').
					then((res)=>{
						this.movieData.push(res.data);
						console.log(res);
					}).catch((err)=>{
						console.log(err);
					})	
				}
			},
			getItemMove(){
				for(var i = 0;i<this.itemList.length;i++)
				{
					this.axios.get('https://api.themoviedb.org/3/movie/'+this.itemList[i]+'?api_key=6e13583a127e758dac0d94b26b7068bf&append_to_response=credits').
					then((res)=>{
						this.movieData.push(res.data);
						console.log(res);
					}).catch((err)=>{
						console.log(err);
					})	
				}
			}
		}
	}
</script>
<style type="text/css" lang='less' scoped>
	.mrecommend{
		padding-top: 60px;
		width: 100%;
		.content{
			background-position: cover;
			background-position: center;
			background-repeat: repeat;
			width: 100%;
			display: flex;
			justify-content: center;
			.main{
				width:1000px;
				padding:0 20px;
				.loading{
					display: flex;
					align-items: center;
					justify-content: center;
				}
				.box{
					position: relative;
					cursor: pointer;
					margin:50px 0px;
					background-color: white;
					border-radius: 5px;
					display: flex;
					height:750px;
					transition: all .2s;
					img{
						flex:0 0 50%;
					}
					.detail{
						flex: 1 1 auto;
						padding:30px;
						color:#081c24;
						overflow: hidden;
						h1{
							color:#805be7
						}
						p:nth-child(2){
							display: flex;
							align-items: center;
							span{
								margin-right:20px;
							}
						}
						p.genres{
							span + span{
								&::before{
									content:' / '
								}
								
							}
						}
						p.cast{
							span{
								display: block;
								margin:10px;
								position: relative;
								left: 50px;
							}
						}
					}
					&:hover{
						 transform: translateX(20px);
						// box-shadow:0 0 10px 50px rgba(255, 255,255, 0.2)
					}
				}
			}
		}
	}

	@media screen and (max-width: 1024px) {
		.mrecommend{
			padding-top:40px;
			.content{
				.main{
					width:100%;
					padding:0 10px;
					box-sizing: border-box;
					.box{
						height:auto;
						flex-direction: column;
						img{
							height:auto;
							width: 100%;
						}
						.detail{
							padding:20px;
							box-sizing: border-box;
							h1{
								font-size: 20px;
							}
							p{
								font-size: 14px;
							}
						}
						&:hover{
							 transform: translateX(0px);
							// box-shadow:0 0 10px 50px rgba(255, 255,255, 0.2)
						}
					}
				}
			}
		}
	}
</style>