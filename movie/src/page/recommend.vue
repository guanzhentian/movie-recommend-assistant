<template>
	<div class="mrecommend" >
		<myheader></myheader>
		<div class="content":style="{backgroundImage:'url('+bg+')'}">
			<div class="main">
				<div class="box" v-if="movieData" v-for="item in movieData">
					<img :src="basicImgSrc + item.poster_path" alt="">
					<div class="detail">
						<h1>{{item.original_title}}</h1>
						<p><strong>Tagline </strong>: {{item.tagline}}</p>
						<p><strong>Movie Rating </strong>: {{item.vote_average}}</p>
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
		</div>
		<foot></foot>
	</div>
</template>
<script type="text/javascript">
	import myheader from '@/components/header'
	import foot from '@/components/foot'
	export default{
		components:{
			myheader,foot
		},
		data(){
			return{
				basicImgSrc:'https://image.tmdb.org/t/p/w500',
				movieData:null,
				bg:require('../assets/6.jpg'),
			}
		},
		mounted(){
			var test = [862,8844,15602,31357,11862,949,11860,45325,9091,710];
			this.movieData = [];
			for(var i = 0;i<test.length;i++)
			{
				this.axios.get('https://api.themoviedb.org/3/movie/'+test[i]+'?api_key=6e13583a127e758dac0d94b26b7068bf&append_to_response=credits').
				then((res)=>{
					this.movieData.push(res.data);
					console.log(res);
				}).catch((err)=>{
					console.log(err);
				})	
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
						h1{
							color:#805be7
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
</style>